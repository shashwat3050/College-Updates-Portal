from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Announcement, Category
from .forms import AnnouncementForm, StaffRegistrationForm

def home(request):
    pinned = Announcement.objects.filter(is_pinned=True).order_by('-created_at')
    latest = Announcement.objects.filter(is_pinned=False).order_by('-created_at')
    categories = Category.objects.all()

    return render(request, 'updates/home.html', {
        'pinned': pinned,
        'latest': latest,
        'categories': categories
    })


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'updates/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def add_announcement(request):
    if not request.user.is_staff:
        return redirect('/')

    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'updates/add_announcement.html', {'form': form})


@login_required
def manage_announcements(request):
    if not request.user.is_staff:
        return redirect('/')

    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'updates/manage_announcements.html', {'announcements': announcements})


@login_required
def delete_announcement(request, announcement_id):
    if not request.user.is_staff:
        return redirect('/')

    Announcement.objects.get(id=announcement_id).delete()
    return redirect('/manage/')


@user_passes_test(lambda u: u.is_superuser)
def register_staff(request):
    form = StaffRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')

    staff = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'updates/register_staff.html', {
        'form': form,
        'staff': staff
    })


@user_passes_test(lambda u: u.is_superuser)
def deactivate_staff(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('/register-staff/')


@user_passes_test(lambda u: u.is_superuser)
def delete_staff(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/register-staff/')


@login_required
def staff_list(request):
    # Only staff and head can see the list
    if not request.user.is_staff:
        return redirect('/')

    staff_users = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'updates/staff_list.html', {
        'staff_users': staff_users
    })


@user_passes_test(lambda u: u.is_superuser)
def reactivate_staff(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('/staff/')