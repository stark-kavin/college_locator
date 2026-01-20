from django.contrib import admin
from .models import Country, State, District, Degree, College

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'created_at')
    list_filter = ('state__country', 'state')
    search_fields = ('name', 'state__name')

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_years', 'created_at')
    search_fields = ('name',)

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'college_type', 'district', 'created_at')
    list_filter = ('college_type', 'district__state', 'degrees')
    search_fields = ('name', 'district__name', 'district__state__name')
    autocomplete_fields = ['district'] # Useful if many districts
    filter_horizontal = ('degrees',) # Better UI for ManyToMany
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'college_type', 'image')
        }),
        ('Location Details', {
            'fields': ('district', 'address_line', 'pincode', 'latitude', 'longitude')
        }),
        ('Contact', {
            'fields': ('website', 'email', 'phone_number')
        }),
        ('Academics', {
            'fields': ('degrees',)
        }),
    )

    class Media:
        css = {
            'all': ('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',)
        }
        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'site_admin/js/admin_map_picker.js',
        )
