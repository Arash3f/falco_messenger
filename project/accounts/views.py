from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout , login ,authenticate
from django.views.generic import UpdateView , CreateView
from accounts.forms import login_form, register_form ,information_form


def login_view(request):
    form = login_form(request.POST or None)

    if request.user.is_authenticated:
        return render(request , 'error_404.html')

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request , user)
                return render(request , "main_page.html" )
            form.add_error(None, "incorect data")
            context={"form":form}
            return render(request , "accounts/login.html" , context)
    else:
        context={"form":form}
        return render(request , "accounts/login.html" , context)

@login_required
def logout_view(request):
    logout(request)
    return render(request  , "main_page.html" )

class register (CreateView):
    model = User
    template_name = "accounts/register.html"
    form_class = register_form
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse('accounts:login' )

class user_information(LoginRequiredMixin,UpdateView):
    template_name = "accounts/user_information.html"
    model = User
    form_class = information_form

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']
        if request.user.pk == pk:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request , 'error_404.html')

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse('accounts:information' , kwargs={'pk': pk})

