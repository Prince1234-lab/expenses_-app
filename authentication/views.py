from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .utils import token_generator
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator



from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.


class UsernameValidationView(View):
    def post(self, request,*args, **kwargs ):
        data = json.loads(request.body)
        username = data.get("username")

        if not str(username).isalnum():
            return JsonResponse({ 'username_error': 'username should contain alphnumaric charaters'}, status= 400)

        if User.objects.filter(username =username).exists():
            return JsonResponse({ 'username_error': 'Sorry username in user, Choose another one'}, status= 419)
        
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request,*args, **kwargs ):
        data = json.loads(request.body)
        email = data.get("email")

        if not validate_email(email):
            return JsonResponse({ 'email_error': 'Email is invalid'}, status= 400)

        if User.objects.filter(email = email).exists():
            return JsonResponse({ 'email_error': 'Sorry email is taking'}, status= 419)
        
        return JsonResponse({'email_valid': True})


   
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        context= {
            'fieldValues' : request.POST
        }

            # validate username
        if not User.objects.filter(username = username).exists():
            # validate email
            if not User.objects.filter(email = email).exists():
                 if len(password) < 6:
                     messages.warning(request, 'Password is short. it should be at least 8 charaters')
                     return render(request, 'authentication:register', context)
                 
                 user = User.objects.create_user(username = username, email =email)
                 user.set_password(password)
                 user.is_active = False
                 user.save()

                 uid64 = urlsafe_base64_encode(force_bytes(user.pk)) 
                 domain = get_current_site(request).domain
                 link = reverse('authentication:activate', kwargs={'uid64': uid64, 'token': token_generator.make_token(user)})


                 # Email subject and body
                 activate_url = 'http://'+domain+link
                 email_body = " Hi " +user.username + " Please use the link below to verify you account\n" +activate_url 
                 email_subject = "Activate you account"

                 # Send the email (no need to call send() on the result)
                 email = send_mail(
                 email_subject,
                email_body,
                "noreply@expenses.com",
                [email],

                fail_silently= False
               
                  )
                
                 messages.success(request, 'Account has been successful created')
                 return render(request, 'authentication/register.html',)
                   

        return render(request, 'authentication/register.html')

    



class VerificationView(View):
    def get(self, request, uid64, token):

          id = force_str(urlsafe_base64_decode(uid64))

          try:
              id = force_str(urlsafe_base64_decode(uid64))
              user = User.objects.get(pk=id)

              if not token_generator.check_token(user, token):
                  return redirect('login'+'?message='+'User already activated')

              if user.is_active:
                  return redirect('authentication:login')
              user.is_active = True
              user.save()
              
              messages.success(request, 'Account activate successfully')
              return redirect('authentication:login')

          except Exception as ex:
              pass



          return redirect('authentication:login')
        




class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username = username, password=password)

            if user:
              if user.is_active:
                  auth.login(request, user)
                  messages.success(request, 'Welcome, '+user.username+' you are logged in')
                  return redirect('expenses')
                        
              messages.warning(request,'Account is not activated, please check your email')
              return render(request, 'authentication/login.html')
            
            messages.warning(request,'Invalid   Credentials, try again')
            return render(request, 'authentication/login.html')
        
        messages.warning(request,'Please fill all fields')
        return render(request, 'authentication/login.html')

                  
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request, 'You have been logout')
        return redirect('authentication:login')



