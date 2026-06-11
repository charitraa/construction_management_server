"""Assign all pre-existing domain rows to the original account.

Before per-user isolation every record was global. This backfills `owner` on
the legacy rows so they belong to the account that created them.
"""
from django.db import migrations

OWNER_EMAIL = "aakash.adhikari@construction.com"

# (app_label, model_name) for every model that gained an `owner` field.
OWNED_MODELS = [
    ("project", "Project"),
    ("employee", "Employee"),
    ("expense", "Expense"),
    ("advance", "Advance"),
    ("revenue", "Revenue"),
    ("attendance", "Attendance"),
]


def assign_owner(apps, schema_editor):
    User = apps.get_model("user", "User")
    owner = User.objects.filter(email=OWNER_EMAIL).first()
    if owner is None:
        # Fall back to the first superuser if the named account is absent.
        owner = User.objects.filter(is_superuser=True).order_by("date_joined").first()
    if owner is None:
        return
    for app_label, model_name in OWNED_MODELS:
        Model = apps.get_model(app_label, model_name)
        Model.objects.filter(owner__isnull=True).update(owner=owner)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0003_alter_project_options_alter_project_managers_and_more"),
        ("employee", "0006_alter_employee_options_alter_employee_managers_and_more"),
        ("expense", "0004_alter_expense_options_alter_expense_managers_and_more"),
        ("advance", "0004_alter_advance_options_alter_advance_managers_and_more"),
        ("revenue", "0003_alter_revenue_options_alter_revenue_managers_and_more"),
        ("attendance", "0005_alter_attendance_options_alter_attendance_managers_and_more"),
    ]

    operations = [
        migrations.RunPython(assign_owner, noop),
    ]
