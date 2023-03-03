from django.http import JsonResponse

# Create your views here.


def home(request):
    return JsonResponse({'info':'Dyango React course', 'name':'Nirajan'})