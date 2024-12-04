from django.contrib import admin

from .models import Housing, RoomType, Offering, Review, Statistics


class HousingAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "address"]
    ordering = ["id"]

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "friendly_name", "bedroom_count", "bathroom_count"]
    ordering = ["id"]
    save_as = True

class OfferingAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


class StatisticsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Housing, HousingAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Offering, OfferingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Statistics, StatisticsAdmin)
