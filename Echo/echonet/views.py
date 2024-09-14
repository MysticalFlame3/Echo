from django.shortcuts import render
from .models import Echo
from .forms import EchoForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
#  Create your views here.
from django.core.files.storage import default_storage


def index(request):
  return render(request, 'index.html')


def echo_list(request):
  echoes = Echo.objects.all().order_by('-created_at')
  return render(request, 'echo_list.html', {'echoes': echoes})

@login_required
def echo_create(request):
  if request.method == "POST":
    form = EchoForm(request.POST, request.FILES)
    if form.is_valid():
      echo = form.save(commit=False)
      echo.user = request.user
      echo.save()
      return redirect('echo_list')
    if echo.photo:
        file_path = default_storage.path(echo.photo.name)
        print(f"File saved at: {file_path}")
                # Optionally, print file information
        print(f"File name: {echo.photo.name}")
        print(f"File size: {echo.photo.size} bytes")
            
        return redirect('echo_list')
    else:
        print(form.errors)
    

    
    
  else:
    form = EchoForm()
  return render(request, 'echo_form.html', {'form': form})

@login_required
def echo_edit(request, echo_id):
  echo = get_object_or_404(Echo, pk=echo_id, user = request.user)
  if request.method == 'POST':
    form = EchoForm(request.POST, request.FILES, instance=echo)
    if form.is_valid():
      echo = form.save(commit=False)
      echo.user = request.user
      echo.save()
      return redirect('echo_list')
  else:
    form = EchoForm(instance=echo)
  return render(request, 'echo_form.html', {'form': form})

@login_required
def echo_delete(request, echo_id):
  echo = get_object_or_404(Echo, pk=echo_id, user = request.user)
  if request.method == 'POST':
    echo.delete()
    return redirect('echo_list')
  return render(request, 'echo_confirm_delete.html', {'echo': echo})
  

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password1'])
      user.save()
      login(request, user)
      return redirect('echo_list')
  else:
    form = UserRegistrationForm()

  return render(request, 'registration/register.html', {'form': form})