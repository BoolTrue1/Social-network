from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import User, UserProfile, Message
from users.forms import UserCreationForm, UserProfileForm, UserForm, MessageForm
from django.contrib import messages



def profile(request):
    return render(request, 'profile.html')


def friends(request):
    return render(request, 'friends.html')


def people(request):
    all_people = User.objects.all()
    return render(request, 'people.html', {'data': all_people})


@login_required
def edit_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', username=user.username)
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    friends = user_profile.friends.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', username=user.username)
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_user': user,
        'friends': friends,
    })

@login_required
def add_friend(request, username):
    user_to_add = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if user_to_add != request.user:
        user_profile.friends.add(user_to_add.userprofile)
        messages.success(request, f'Вы добавили {user_to_add.username} в друзья!')
    else:
        messages.warning(request, 'Вы не можете добавить себя в друзья.')

    return redirect('profile', username=username)

@login_required
def send_message(request, username):
    recipient = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            messages.success(request, 'Сообщение отправлено!')
            return redirect('profile', username=username)
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'recipient': recipient})

@login_required
def view_messages(request):
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def dialogs_view(request):
    return render(request, 'dialogs.html')

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('profile', username=request.user.username)

    users = User.objects.all()
    return render(request, 'admin_panel.html', {'users': users})

@login_required
def edit_user(request, user_id):
    if not request.user.is_staff:
        return redirect('profile', username=request.user.username)

    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'User profile was successfully updated!')
            return redirect('admin_panel')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_user': user
    })

@login_required
def block_user(request, user_id):
    if not request.user.is_staff:
        return redirect('profile', username=request.user.username)

    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f'User {user.username} has been blocked.')
    return redirect('admin_panel')


@login_required
def unblock_user(request, user_id):
    if not request.user.is_staff:
        return redirect('profile', username=request.user.username)

    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f'User {user.username} has been unblocked.')
    return redirect('admin_panel')


class Register(View):
    
    template_name = 'registration/register.html'
    
    def get(self, request):
        context = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)