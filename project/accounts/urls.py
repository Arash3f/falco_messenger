from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path('login/' , views.login_view , name="login"),
    path('logout/' , views.logout_view , name="logout"),
    path('register/' , views.register.as_view() , name="register"),
    path('user/information/<int:pk>/' , views.user_information.as_view() , name="information"),
]

