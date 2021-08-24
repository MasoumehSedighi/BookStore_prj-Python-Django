from django.contrib import admin

# Register your models here.
from .forms import AddressForm
from .models import Customer, Addresses, Management, User, Staff, UserProfile


class AddressesInline(admin.TabularInline):
    model = Addresses
    raw_id_fields = ('user',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = (AddressesInline,)

    class Meta:
        model = User
        fields = '__all__'

    def get_queryset(self, request):
        return User.objects.filter(is_staff=False)


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email')

    def get_queryset(self, request):
        return User.objects.filter(is_staff=True)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email')

    def get_queryset(self, request):
        return User.objects.filter(is_admin=True)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'image')


