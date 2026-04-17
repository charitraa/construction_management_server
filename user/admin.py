from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import User, Role, Page


# =====================================================
# ROLE ADMIN
# =====================================================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id","name",)
    search_fields = ("name",)
    ordering = ("name",)


# =====================================================
# PAGE ADMIN
# =====================================================

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id","name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# =====================================================
# USER CREATION FORM (ADMIN SIDE)
# =====================================================

class UserCreationAdminForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "full_name", "role", "pages")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


# =====================================================
# USER ADMIN
# =====================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_form = UserCreationAdminForm
    model = User

    # -------------------------
    # LIST VIEW
    # -------------------------
    list_display = (
        "email",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = ("email", "full_name")
    ordering = ("email",)

    filter_horizontal = ("pages", "groups", "user_permissions")

    readonly_fields = ("date_joined", "last_login")

    # -------------------------
    # DETAIL VIEW
    # -------------------------
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("full_name",)}),
        (
            _("Role & Page Access"),
            {
                "fields": (
                    "role",
                    "pages",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    # -------------------------
    # ADD USER VIEW
    # -------------------------
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "role",
                    "pages",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    # -------------------------
    # OPTIMIZATION
    # -------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("role").prefetch_related("pages")