from django.shortcuts import render  # Add this import statement

def home(request):
    return render(request, 'home.html')