from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Customer, Addresses, Management, User, Staff, UserProfile


class AddressesInline(admin.TabularInline):
    model = Addresses
    raw_id_fields = ('user',)
    search_fields = ('user',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    inlines = (AddressesInline,)
    search_fields = ('first_name',)
    ordering = ('email',)
    fieldsets = (
        ('information', {'fields': ('email', 'first_name', 'last_name', 'phone', 'password')}),
        ('permissions', {'fields': ('is_active','groups', 'user_permissions',)}),
    )

    class Meta:
        model = User

    def get_queryset(self, request):
        return User.objects.filter(is_staff=False)


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email']
    search_fields = ('first_name',)
    ordering = ('email',)
    fieldsets = (
        ('information',{'fields': ('email', 'first_name', 'last_name', 'phone', 'password')}),
        ('permissions', {'fields': ('is_staff','is_superuser','groups', 'user_permissions',)}),
    )

    class Meta:
        model = User

    def get_queryset(self, request):
        return User.objects.filter(is_superuser=True)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email']
    search_fields = ('first_name',)
    ordering = ('email',)
    fieldsets = (
        ('information', {'fields': ('email', 'first_name', 'last_name', 'phone', 'password')}),
        ('permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )

    class Meta:
        model = User

    def get_queryset(self, request):
        return User.objects.filter(is_staff=True)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)

#
# @admin.register(UserDefaultAddress)
# class UserDefaultAddressAdmin(admin.ModelAdmin):
#     list_display = ('user',)
#     search_fields = ('user',)