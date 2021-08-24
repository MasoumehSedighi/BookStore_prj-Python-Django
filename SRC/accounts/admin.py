from django.contrib import admin

# Register your models here.
from .models import Customer, Addresses, Management, User, Staff


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
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


admin.site.register(Addresses)