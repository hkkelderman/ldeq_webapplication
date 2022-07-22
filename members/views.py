from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, ParameterForm
from website.models import Parameter

class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home') #add message

	def get_object(self):
		return self.request.user

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('edit_profile') #add message

class EditParameterView(generic.UpdateView):
	model = Parameter
	template_name = 'registration/edit_params.html'
	fields = ['organization', 'ais']
	success_url = reverse_lazy('home') #add message

class SetParameterView(generic.CreateView):
	model = Parameter
	form_class = ParameterForm
	template_name = 'registration/set_params.html'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)