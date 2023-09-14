from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from . import settings


def index(request):
    return render(request, 'index.html')

def set_language(request):
    lang = request.GET.get('l', 'en')
    request.session[settings.LANGUAGE_SESSION_KEY] = lang
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response

class UserLogin(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = _("You're logged in")

class UserLogout(LogoutView):
    next_page = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("You're logged out"))
        return redirect(self.next_page)
