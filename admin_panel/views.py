from django.shortcuts import render
def admin_panel(request):
    return render(request, 'admin_panel/admin.html')
# Create your views here.
