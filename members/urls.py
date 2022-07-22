from django.urls import path
from . views import UserRegisterView, UserEditView, PasswordsChangeView, EditParameterView, SetParameterView
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('register/', UserRegisterView.as_view(), name = 'register'),
	path('edit_profile/', UserEditView.as_view(), name = 'edit_profile'),
	#path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
	path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
	path('<int:pk>/edit_params/', EditParameterView.as_view(), name='edit_params'),
	path('set_params/', SetParameterView.as_view(), name='set_params'),
]