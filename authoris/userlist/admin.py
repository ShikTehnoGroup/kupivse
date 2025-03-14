from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Users

class UserAdmin(BaseUserAdmin):
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'is_active', 'is_admin')
    
    # Фильтры в правой панели
    list_filter = ('is_active', 'is_admin')
    
    # Поля, которые будут отображаться в форме редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    
    # Поля, которые будут отображаться в форме создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    
    # Поля, по которым можно осуществлять поиск
    search_fields = ('email',)
    
    # Поле, по которому будет осуществляться сортировка
    ordering = ('email',)

    # Удаляем поля groups и user_permissions
    filter_horizontal = ()

# Регистрация модели Users в админ-панели
admin.site.register(Users, UserAdmin)
