from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from participants.models import Participant

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.user_type == 'admin':
                return JsonResponse({"status": "success", "role": "admin"})
            else:
                return JsonResponse({"status": "success", "role": "participant"})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({"status": "failure", "errors": "credential_error"})
    else:
        form = AuthenticationForm()
        return render(request, 'utilities/login.html', {'form': form})

def user_dashboard(request):
    return render(request, 'utilities/home.html')

def user_register(request):
    if request.method == "POST":
        fields = ["firstname", "lastname", "email", "username", "password", "phone", "address"]
        form_data = {field: request.POST.get(field) for field in fields}
        participant = Participant.objects.create_user(first_name=form_data["firstname"], last_name=form_data["lastname"], email=form_data["email"], username=form_data["username"], password=form_data["password"], phone=form_data["phone"], address=form_data["address"], user_type='participant')
        return JsonResponse({"status":"success"})
    return render(request, 'utilities/register.html')