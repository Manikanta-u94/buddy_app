from django.contrib import admin
from .models import Profile, Platform, Page, Category, Place, Image, PlaceComment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact')


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'platform', 'post_no')
    list_filter = ('platform',)
    search_fields = ('name', 'platform__name', 'post_no')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'page', 'location', 'google_rating', 'family_friendly', 'pet_friendly', 'newly_opened')
    list_filter = ('category', 'family_friendly', 'pet_friendly', 'newly_opened', 'page__platform')
    search_fields = ('name', 'location', 'highlights', 'top_picks', 'sub_type')
    inlines = [ImageInline]

@admin.register(PlaceComment)
class PlaceCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'place', 'created_at')
    list_filter = ('place', 'user')
    search_fields = ('comment', 'user__username', 'place__name')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'image')
    list_filter = ('place',)
    search_fields = ('place__name',)


