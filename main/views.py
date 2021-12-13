from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views import View
import json
from main.models import ChatRoom, Message, User


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class CreateRoomView(View):
    def get(self, request, name):
        user = User.objects.create(name=name)
        user.save()

        room = ChatRoom.objects.create()
        room.participants.add(user)
        room.save()

        return redirect(reverse('chatroom', kwargs={'code': room.code}) + f"?user={user.name}")


class JoinRoomView(View):
    def get(self, request, name):
        roomcode = request.GET.get('code')
        user = User.objects.create(name=name)
        user.save()

        try:
            room = ChatRoom.objects.get(code=roomcode)
            room.participants.add(user)
            room.save()
            return JsonResponse({'success': True})

        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'INVALID_CODE'})


class RoomView(View):
    def get(self, request, code):
        user = request.GET.get('user')
        try:
            room = ChatRoom.objects.get(code=code)
            if room.participants.count() == 0:
                room.delete()
                return render(request, 'error_page.html', context={"error": "This room does not exist!"})
            
            user_obj = User.objects.get(name=user)

            if not room.participants.filter(id=user_obj.id).exists():
                return render(request, 'error_page.html', context={"error": "This user is not a participant of the specified room!"})

        except ChatRoom.DoesNotExist:
            return render(request, 'error_page.html', context={"error": "This room does not exist!"})

        except User.DoesNotExist:
            return render(request, 'error_page.html', context={"error": "This user is not a participant of the specified room!"})

        return render(request, 'chatroom.html', context={'room': room, 'user': user})


class SendMessage(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['user']
        roomcode = data['room']
        msg_content = data['message']

        room = ChatRoom.objects.get(code=roomcode)

        message = Message.objects.create(author=User.objects.get(name=name), room=room, content=msg_content)
        message.save()

        messages = list(Message.objects.filter(room=room).order_by('date_posted').values('content', 'date_posted', 'author__name'))

        return JsonResponse({'success': True, 'messages': messages})


class GetRoomMessages(View):
    def get(self, request):
        roomcode = request.GET.get('room')
        room = ChatRoom.objects.get(code=roomcode)
        messages = list(Message.objects.filter(room=room).order_by('date_posted').values('content', 'date_posted', 'author__name'))

        return JsonResponse({'success': True, 'messages': messages})


class ChatCleanupView(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['user']

        user = User.objects.get(name=name)

        rooms = user.get_rooms()
        user.delete()

        for room in rooms:
            print(room.participants.count())
            if room.participants.count() == 0:
                room.delete()


        return JsonResponse({"success": True})
