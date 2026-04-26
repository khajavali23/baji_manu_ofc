from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Navbar, Banner, SubMenu

# HOME
def home(request):
    navbars = Navbar.objects.all()
    banner = Banner.objects.first()
    return render(request, 'index.html', {
        'navbars': navbars,
        'banner': banner
    })

# LOGIN
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


# DASHBOARD
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'navbars': Navbar.objects.all(),
        'banners': Banner.objects.all()
    })


# NAVBAR CRUD
@login_required
def add_navbar(request):
    if request.method == "POST":
        Navbar.objects.create(
            name=request.POST['name'],
            url=request.POST['url']
        )
        return redirect('/dashboard/')
    return render(request, 'add_navbar.html')


@login_required
def edit_navbar(request, id):
    nav = Navbar.objects.get(id=id)
    if request.method == "POST":
        nav.name = request.POST['name']
        nav.url = request.POST['url']
        nav.save()
        return redirect('/dashboard/')
    return render(request, 'edit_navbar.html', {'nav': nav})


@login_required
def delete_navbar(request, id):
    Navbar.objects.get(id=id).delete()
    return redirect('/dashboard/')


# BANNER CRUD
@login_required
def add_banner(request):
    if request.method == "POST":
        Banner.objects.create(
            title=request.POST['title'],
            image=request.FILES['image'],
            description=request.POST['description']
        )
        return redirect('/dashboard/')
    return render(request, 'add_banner.html')


@login_required
def edit_banner(request, id):
    banner = Banner.objects.get(id=id)
    if request.method == "POST":
        banner.title = request.POST['title']
        if request.FILES.get('image'):
            banner.image = request.FILES['image']
        banner.description = request.POST['description']
        banner.save()
        return redirect('/dashboard/')
    return render(request, 'edit_banner.html', {'banner': banner})


@login_required
def delete_banner(request, id):
    Banner.objects.get(id=id).delete()
    return redirect('/dashboard/')

from django.shortcuts import get_object_or_404

def delete_submenu(request, id):
    submenu = get_object_or_404(SubMenu, id=id)
    submenu.delete()
    return redirect('dashboard')

def add_submenu(request, nav_id):
    navbar = get_object_or_404(Navbar, id=nav_id)

    if request.method == 'POST':
        print("POST:", request.POST)
        print("FILES:", request.FILES)   # 🔥 ADD THIS

        name = request.POST.get('name')
        file = request.FILES.get('file')

        SubMenu.objects.create(
            navbar=navbar,
            name=name,
            file=file
        )
        return redirect('dashboard')

    return render(request, 'add_submenu.html', {'navbar': navbar})

def edit_submenu(request, id):
    submenu = get_object_or_404(SubMenu, id=id)

    if request.method == 'POST':
        submenu.name = request.POST.get('name')

        # ✅ HANDLE FILE UPDATE
        if request.FILES.get('file'):
            submenu.file = request.FILES.get('file')

        submenu.save()
        return redirect('dashboard')

    return render(request, 'edit_submenu.html', {'submenu': submenu})


def delete_submenu(request, id):
    submenu = get_object_or_404(SubMenu, id=id)
    submenu.delete()
    return redirect('dashboard')