from rest_framework.permissions import BasePermission


class HasPageAccess(BasePermission):
    """Custom permission class that checks if the user has access to the page based on their role and assigned pages."""
    def has_permission(self, request, view):

        user = request.user

        if user.is_superuser:
            return True

        if user.role.name == "admin":
            return True

        page_slug = getattr(view, "page_slug", None)

        if not page_slug:
            return True

        if not user.pages.filter(slug=page_slug).exists():
            return False

        if user.role.name == "viewer":
            return request.method == "GET"

        if user.role.name == "editor":
            return request.method in ["GET", "POST", "PUT", "PATCH"]

        return False