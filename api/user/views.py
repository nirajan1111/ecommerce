from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.forms.models import model_to_dict
import re
import random
# Create your views here.


def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))


@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a Post request with valid parameters'})
# validation part
    username = request.POST['email']
    password = request.POST['password']

    if not re.match(r'^([\w.\-]+)?\w+@[\w\-]+(\.\w+){1,}$', username):
        return JsonResponse({'error ': 'Enter  valid Email'})
    if len(password) < 3:
        return JsonResponse({'error': 'password needs to be more longer'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict = model_to_dict(user)
            usr_dict.pop('password')
            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error': 'Previous session exists'})
            token = generate_session_token()
            user.session_token = token
            user.set_password(password)
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': usr_dict})
        else:
            return JsonResponse({'error': 'Invalid password'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error': ' Invalid Email'})


def signout(request, id):
    logout(request)

    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'

        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid user id'})

    return JsonResponse({'success': 'Logout success'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
