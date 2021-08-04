from django.urls import path
from messenger import views

app_name= 'messenger'

urlpatterns = [
    path('', views.main , name = "messenger_main_page"),
    path('<slug:slug>/', views.group_chat , name = "group_chat"),
    path('group/create/', views.create_group.as_view() , name = "create_group"),
    path('group/join/', views.join_group , name = "join_group"),
    path('group/leave/<str:slug>', views.leave_chat , name = "leave_chat"),
    path('<slug:slug>/detail/', views.chat_detail , name = "chat_detail"),
    path('chat/member/kick/<slug:slug>/<int:id>', views.chat_member_kick , name = "chat_member_kick"),
]