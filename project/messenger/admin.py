from django.contrib import admin
from messenger import models
# Register your models here.

@admin.register(models.GroupChat)
class GroupChat(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display  = ['__str__' , 'creator' , 'date_create']

@admin.register(models.Members)
class Members(admin.ModelAdmin):
    list_display  = ['chat' , '__str__' , 'date_join']

@admin.register(models.Message)
class Message(admin.ModelAdmin):
    list_display  = ['chat' , 'chat' , 'date_create']