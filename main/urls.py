from django.urls import path

from main.views import CreateRoomView, GetRoomMessages, HomeView, JoinRoomView, RoomView, SendMessage, ChatCleanupView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('join-room/<str:name>', JoinRoomView.as_view(), name='join-room'),
    path('create-room/<str:name>', CreateRoomView.as_view(), name='create-room'),
    path('chat/<str:code>', RoomView.as_view(), name='chatroom'),
    path('send-message', SendMessage.as_view(), name='send-message'),
    path('get-all-messages', GetRoomMessages.as_view(), name='get-all-messages'),
    path('chat-cleanup', ChatCleanupView.as_view(), name="chat-cleanup"),
]