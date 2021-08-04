from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from messenger.models import GroupChat, Members, Message
from django.utils.safestring import mark_safe
from messenger.forms import group_form, join_group_form
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET"])
@login_required
def main(request):
    user = request.user
    return render(request , 'messenger/messenger.html' , {'chats':user.members.all()})

@require_http_methods(["GET"])
@login_required
def group_chat(request , slug):
    user = request.user
    try:
        chat = GroupChat.objects.get(slug=slug)
        chat_messages = Message.objects.filter(chat=chat)
        access = Members.objects.get(chat_id = chat.id , user_id = user.id)
    except:
        return render(request , 'error_404.html')
    return render(request , 'messenger/messenger.html' , {'chats':user.members.all() ,"group_chat":chat,"livechat":chat_messages,"chat_slug": mark_safe(json.dumps(chat.slug))})

class create_group (LoginRequiredMixin,CreateView):
    model = GroupChat
    template_name = "messenger/create_group.html"
    form_class = group_form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('messenger:messenger_main_page' )

@require_http_methods(["GET","POST"])
@login_required
def join_group(request):
    form = join_group_form(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name']
            user = request.user 
            try:
                chat = GroupChat.objects.get(name = name)
            except GroupChat.DoesNotExist:
                return render(request , 'error_404.html')
            if Members.objects.filter(chat_id = chat.id , user_id = user.id).count()==0:
                Members.objects.create(chat_id = chat.id , user_id = user.id)
                new_message = Message.objects.create(chat_id = chat.id , author_id = user.id , warning = True)
                new_message.body = new_message.join()
                new_message.save()
                chat_room_id = f"chat_{chat.slug}"
                channel_layer = get_channel_layer()            
                async_to_sync(channel_layer.group_send)(
                    chat_room_id,{
                    'type':'chat_message_warning' , 
                    'message': json.dumps({'type':"join", 'text':new_message.join() ,'time':new_message.date_format()}),
                    }
                )
                return render(request , 'messenger/messenger.html' , {'chats':user.members.all()})
            else:
                form.add_error(None, "you are already joined to this group !")
    context={"form":form}
    return render(request , 'messenger/join_group.html' , context)

@require_http_methods(["GET","POST"])
@login_required
def leave_chat(request , slug):
    try :
        chat = GroupChat.objects.get(slug = slug)
    except GroupChat.DoesNotExist:
        return render(request , 'error_404.html')    
    user = request.user
    chat_room_id = f"chat_{slug}"
    channel_layer = get_channel_layer()
    if chat.creator_id == user.id:
        chat.delete()
        async_to_sync(channel_layer.group_send)(
            chat_room_id,{
            'type':'chat_message_warning' , 
            'message': json.dumps({'type':"delete", 'text':f"Chat deleted :(" }),
            }
        )
    elif(chat.members.filter(user=user).count()==1):
        new_message = Message.objects.create(chat_id = chat.id , author_id = user.id ,warning = True)
        new_message.body = f"User {request.user.username} leave chat :("
        new_message.save()
        Members.objects.get(chat_id = chat.id , user_id = user.id).delete()
        async_to_sync(channel_layer.group_send)(
            chat_room_id,{
            'type':'chat_message_warning' , 
            'message': json.dumps({'type':"leave", 'text':f"User {request.user.username} leave chat :(",'time':new_message.date_format() }),
            }
        )
    else:
        return render(request , 'error_404.html')
    return render(request , "messenger/messenger.html",{'chats':user.members.all()})

@require_http_methods(["GET"])
@login_required
def chat_detail(request , slug):
    try:
        chat = GroupChat.objects.get(slug = slug)
        members = Members.objects.filter(chat=chat)
        return render(request , 'messenger/chat_detail.html' , {'members':members , 'chat':chat})
    except GroupChat.DoesNotExist:
        return render(request , 'error_404.html')   

@require_http_methods(["GET"])
@login_required
def chat_member_kick(request , slug , id):
    try:
        user = User.objects.get(id=id)
        chat = GroupChat.objects.get(slug = slug)
        chat_room_id = f"chat_{slug}"
        channel_layer = get_channel_layer()
    except GroupChat.DoesNotExist:
        return render(request , 'error_404.html')    
    if chat.creator_id == user.id:
        chat.delete()
        async_to_sync(channel_layer.group_send)(
            chat_room_id,{
            'type':'chat_message_warning' , 
            'message': json.dumps({'type':"delete", 'text':f"Chat deleted :(" }),
            }
        )
    elif(chat.members.filter(user=user).count()==1):
        new_message = Message.objects.create(chat_id = chat.id , author_id = user.id ,warning = True)
        new_message.body = new_message.kick()
        new_message.save()
        Members.objects.filter(chat_id = chat.id , user_id = user.id).delete()
        async_to_sync(channel_layer.group_send)(
            chat_room_id,{
            'type':'chat_message_warning' , 
            'message': json.dumps({'type':"leave", 'text':new_message.body,'time':str(new_message.date_create) }),
            }
        )
    else:
        return render(request , 'error_404.html')
    return render(request , "messenger/messenger.html",{'chats':request.user.members.all()})

