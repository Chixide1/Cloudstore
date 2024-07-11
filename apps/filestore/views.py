from django.shortcuts import render

# Create your views here.

def dashboard(request):
    test = [num for num in range(1, 101)]
    return render(request, 'dashboard.html', {"test": test})