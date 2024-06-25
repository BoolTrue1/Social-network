from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from users.models import User, UserProfile, Message, Post, Album, Photo, Community
from users.forms import UserCreationForm, UserProfileForm, UserForm, MessageForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta



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
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    friends = user_profile.friends.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Post.objects.create(user=request.user, content=content)
            return redirect('profile', username=username)
        
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
    if request.user.is_blocked or (request.user.mute_until and request.user.mute_until > timezone.now()):
        messages.error(request, 'Вы не можете отправлять сообщения в данный момент.')
        return redirect('profile', username=username)
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


@staff_member_required
def admin_block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = True
    user.save()
    messages.success(request, f'Пользователь {user.username} заблокирован.')
    return redirect('admin:user_changelist')

@staff_member_required
def admin_unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = False
    user.save()
    messages.success(request, f'Пользователь {user.username} разблокирован.')
    return redirect('admin:user_changelist')

@staff_member_required
def admin_mute_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_muted = True
    user.mute_until = timezone.now() + timedelta(days=1)
    user.save()
    messages.success(request, f'Пользователь {user.username} временно отключен.')
    return redirect('admin:user_changelist')

@staff_member_required
def admin_unmute_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_muted = False
    user.mute_until = None
    user.save()
    messages.success(request, f'Пользователь {user.username} снова может отправлять сообщения.')
    return redirect('admin:user_changelist')

@staff_member_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f'Пользователь {user.username} удален.')
    return redirect('admin:user_changelist')


@login_required
def album_view(request, username):
    user = get_object_or_404(User, username=username)
    albums = Album.objects.filter(user=user)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Album.objects.create(user=request.user, title=title)
            return redirect('album', username=username)

    return render(request, 'album.html', {
        'profile_user': user,
        'albums': albums,
    })

@login_required
def photo_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    photos = album.photos.all()

    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')
        if image:
            Photo.objects.create(album=album, image=image, caption=caption)
            return redirect('photo', album_id=album.id)

    return render(request, 'photo.html', {
        'album': album,
        'photos': photos,
    })


@login_required
def community_view(request):
    communities = Community.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Community.objects.create(name=name, description=description, creator=request.user)
            return redirect('community')

    return render(request, 'community.html', {
        'communities': communities,
    })

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.add(request.user)
    return redirect('community_detail', community_id=community.id)

@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.remove(request.user)
    return redirect('community_detail', community_id=community.id)

@login_required
def community_detail_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    members = community.members.all()
    return render(request, 'community_detail.html', {
        'community': community,
        'members': members,
    })




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
