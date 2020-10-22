from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
import requests
from .forms import SignUpForm, OtpForm
from oscar.core.loading import get_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

API_KEY = ""


def activation_sent_view(request, uidb64):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if request.method == 'POST':
		form = OtpForm(request.POST)
		if form.is_valid():
			otp = form.cleaned_data.get('otp')
			if otp:
				user.is_active = True
				user.save()
				return redirect('/accounts/profile/')
			else:
				# if OTP is wrong then we have to redirect it on the same page with the msg " wrong OTP Please Enter a Valid OTP"
				request.session['wrong_otp'] = True
				return redirect(request.META['HTTP_REFERER'])
	else:
		form = OtpForm()
	return render(request, 'oscar/customer/activation_sent.html', {'form': form})


def signup_view(request):
	if request.method  == 'POST':
		form = SignUpForm(request.POST)
		print(form)
		if form.is_valid():
			request.session['wrong_otp'] = False
			user = form.save()
			user.refresh_from_db()
			user.profile.mobile = form.cleaned_data.get('mobile')
			user.is_active = False
			user.save()
			uid = urlsafe_base64_encode(force_bytes(user.pk))
			return redirect('/account/verificaation/'+ uid)

	else:
		form = SignUpForm()
	return render(request, 'oscar/customer/registration.html', {'form': form})


def catagories_product(request):
	Product = get_model('catalogue', 'Product')
	fruit = Product.objects.filter(product_class=4)[:6]
	vegetable = Product.objects.filter(product_class=5)[:6]
	groocy = Product.objects.filter(product_class=6)[:6]
	return render(request, 'oscar/catalogue/browse.html', {'fruit': fruit, 'vegetable': vegetable, 'groocy': groocy})

@csrf_exempt
def check_pincode(request):
	pin_list = ['452001', '452002', '452003']
	input_pin = request.GET.get('pincode')
	if input_pin in pin_list:
		pinvalid = True
	else:
		pinvalid = False
	return JsonResponse({"valid":pinvalid}, status = 200)