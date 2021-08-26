from django.contrib import admin

# Register your models here.
from .forms import AddressForm
from .models import Customer, Addresses, Management, User, Staff, UserProfile


class AddressesInline(admin.TabularInline):
    model = Addresses
    raw_id_fields = ('user',)
    search_fields = ('user',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = (AddressesInline,)
    search_fields = ('first_name',)

    class Meta:
        model = User
        fields = '__all__'

    def get_queryset(self, request):
        return User.objects.filter(is_staff=False)


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):

    class Meta:
        model = User
        fields = '__all__'

    def get_queryset(self, request):
        return User.objects.filter(is_superuser=True)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'is_staff', 'is_admin')
    search_fields = ('first_name',)

    def get_queryset(self, request):
        return User.objects.filter(is_staff=True)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'image')
    search_fields = ('full_name',)


