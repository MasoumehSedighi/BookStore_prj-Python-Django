from django.contrib import admin

# Register your models here.
from .models import Book, Category, DiscountCash, DiscountPercent


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)  #فیلدهایی که در پنل ادمین درخصوص مدل مورد نظر میخواهیم نشان دهد
    prepopulated_fields = {'slug': ('title',)}  #فیلد slug را در پنل ادمین براساس  فیلد title  در نظر میگبرد


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'stock', 'categories')
    list_display_links = ['title']
    prepopulated_fields = {'slug': ('title',)}


    def categories(self, obj):
        return [cat.title for cat in obj.category.all()]


@admin.register(DiscountCash)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('amount', 'valid_from', 'valid_to','active')
    list_filter = ('active', 'valid_from', 'valid_to')



@admin.register(DiscountPercent)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('percentage', 'valid_from', 'valid_to','active')
    list_filter = ('active', 'valid_from', 'valid_to')
