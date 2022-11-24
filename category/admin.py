
from django.contrib import admin
from .models import Age, Brand, Category, Charector 

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug': ('sub_category_name',)}
    list_display         = ('sub_category_name','slug')

class AgeAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug': ('age_name',)}
    list_display         = ('age_name','slug')

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug': ('brand_name',)}
    list_display         = ('brand_name','slug')

class CharectorAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug': ('charector_name',)}
    list_display         = ('charector_name','slug')

admin.site.register(Category, CategoryAdmin)
# admin.site.register(Sub_Category,SubCategoryAdmin)
admin.site.register(Age,AgeAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Charector,CharectorAdmin)
