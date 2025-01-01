from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'full_name',
        'username',
        'rol_academico',
        'email',
        'is_active',
    ]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    full_name.short_description = 'Nombre Completo'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Campos predeterminados
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','formacion', 'rol_academico')}),  # Información personalizada
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'email',
                'formacion',
                'rol_academico'
                       ),
        }),
    )



admin.site.register(CustomUser, CustomUserAdmin)
