from django.db import models
from django.utils import timezone
import secrets


def generate_code():
    return secrets.token_hex(12).upper()

# Create your models here.
class ChatRoom(models.Model):
    code = models.CharField(max_length=200, default=generate_code)
    participants = models.ManyToManyField("User")

    def __str__(self) -> str:
        return f'{self.code}'

    def __repr__(self) -> str:
        return f'<ChatRoom: {self.code}>'


class User(models.Model):
    name = models.CharField(max_length=150)

    def get_rooms(self):
        return ChatRoom.objects.filter(participants=self)

    def __str__(self) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'<User: {self.name}>'


class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'{self.author}: {self.content}'

    def __repr__(self) -> str:
        return f'<Message: {self.author}: {self.content}>'