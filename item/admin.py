from django.contrib import admin
from django.utils.html import format_html
from .models import Item, ItemImage
import os

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_first_image','category', 'creator','owner', 'starting_price', 'display_provenance_image')
    def display_provenance_image(self, obj):
        if obj.provenance:
            return format_html('<img src="{}" width="100" height="100" />', obj.provenance.url)
        return "No Image"
    def get_first_image(self, obj):
        item_image = obj.itemimage_set.first()
        if item_image and item_image.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(item_image.image.url))
        return "No Image"
    get_first_image.short_description = "Image"
    display_provenance_image.short_description = 'Provenance Image'

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'display_item_image')

    def display_item_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    display_item_image.short_description = 'Item Image'