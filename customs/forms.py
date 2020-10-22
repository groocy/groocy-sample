from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=100, help_text='First Name')
	last_name = forms.CharField(max_length=100, help_text='Last Name')
	email = forms.EmailField(max_length=150, help_text='Email')
	mobile = forms.CharField(max_length=10, help_text='Mobile Number')

	def clean_email(self):
		# Get the email
		email = self.cleaned_data.get('email')

		# Check to see if any users already exist with this email as a username.
		try:
			match = User.objects.get(email=email)
		except User.DoesNotExist:
			# Unable to find a user, this is fine
			return email

		# A user was found with this as a username, raise an error.
		raise forms.ValidationError('This email address is already in use.')

	def clean_mobile(self):
		# Get the mobile number 
		mobile = self.cleaned_data.get('mobile')

		# Check to see if any users already exist with this email as a username.
		try:
			match = Profile.objects.get(mobile=mobile)
		except Profile.DoesNotExist:
			# Unable to find a user, this is fine
			return mobile

		# A user was found with this as a username, raise an error.
		raise forms.ValidationError('This mobile number is already in use.')
	
	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email', 'mobile', 'password1', 'password2', )


class OtpForm(forms.Form):
	otp = forms.CharField(max_length=6, help_text='OTP')




