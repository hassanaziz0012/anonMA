from django.contrib import admin
from main.models import ChatRoom, Message, User

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(User)