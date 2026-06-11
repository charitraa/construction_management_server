"""
Per-user (tenant) data isolation.

Every domain model that should be private to a single account uses
``OwnerManager`` as its default manager. The manager filters every query by the
"current owner" — the authenticated user of the request being handled — which is
stored in a thread-local set by ``LoginRequiredPermission`` and cleared after the
request by ``CurrentOwnerMiddleware``.

The design fails CLOSED for tenants: inside an authenticated request the current
owner is always set, so a query can never accidentally return another account's
rows. When no owner is set (Django admin via session auth, the shell, management
commands, data migrations) queries are unscoped so a superuser/operator can see
everything.
"""

import threading

from django.db import models

_state = threading.local()


def set_current_owner(user):
    """Record the authenticated user for the duration of the current request."""
    _state.owner = user


def get_current_owner():
    """Return the current request's owner, or ``None`` outside a tenant request."""
    return getattr(_state, "owner", None)


def clear_current_owner():
    """Drop the current owner. Always call this at the end of a request."""
    if hasattr(_state, "owner"):
        del _state.owner


def _active_owner():
    """Return the current owner only if it is a real, authenticated user."""
    owner = get_current_owner()
    if owner is not None and getattr(owner, "is_authenticated", False):
        return owner
    return None


class OwnerQuerySet(models.QuerySet):
    """QuerySet whose default rows are scoped to the current owner."""

    def for_owner(self, owner):
        return self.filter(owner=owner)


class OwnerManager(models.Manager.from_queryset(OwnerQuerySet)):
    """Default manager that auto-scopes reads to the current owner.

    When a tenant request is in flight, ``get_queryset`` only returns rows owned
    by that user. Outside a request (admin, shell, migrations) it returns
    everything so operators retain full visibility.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        owner = _active_owner()
        if owner is not None:
            return qs.filter(owner=owner)
        return qs


class OwnedModel(models.Model):
    """Abstract base for tenant-scoped models.

    Adds the ``owner`` foreign key, swaps in :class:`OwnerManager`, and auto-fills
    ``owner`` from the current request on first save so callers never have to pass
    it explicitly.
    """

    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)ss",
        db_index=True,
    )

    objects = OwnerManager()
    # Unscoped manager for admin/ops code that must see every account's rows.
    all_objects = models.Manager()

    class Meta:
        abstract = True
        # Keep related-object fetching / refresh_from_db unscoped; only explicit
        # `.objects` queries are tenant-filtered.
        base_manager_name = "all_objects"

    def save(self, *args, **kwargs):
        if self.owner_id is None:
            owner = _active_owner()
            if owner is not None:
                self.owner = owner
        super().save(*args, **kwargs)
