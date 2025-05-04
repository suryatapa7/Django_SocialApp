from django.contrib.auth.models import User
from django.views.generic import DetailView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from feed.models import Post
from followers.models import Follower
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect
from .forms import UserForm, ProfileForm, CustomPasswordChangeForm
from django.contrib import messages




# Create your views here.
class ProfileDetailView(DetailView):
    http_method_names = ['get']
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        # Count all Follower entries where this profile is being followed
        context['total_followers'] = Follower.objects.filter(following=user).count()

        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(
                following=user, 
                followed_by= self.request.user
            ).exists()
        return context
    
class FollowView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing Data")
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("User does not exist")
        if data['action'] == 'follow':
            #follow
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user, 
                following=other_user
            )
        else:
            #unfollow
            try:
                follower = Follower.objects.get(
                    followed_by=request.user, 
                    following=other_user
                )
            except Follower.DoesNotExist:
                follower = None
            if follower:
                follower.delete()
        
        # After creating or deleting the Follower:
        new_count = Follower.objects.filter(following=other_user).count()
        return JsonResponse({
            'success': True,
            'wording':"Unfollow" if data['action'] == 'follow' else "Follow",
            'total_followers': new_count,
        })

class EditProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        context['profile_form'] = ProfileForm(instance=self.request.user.profile)
        context['password_form'] = CustomPasswordChangeForm(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('profiles:edit_profile', username=request.user.username)

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been changed successfully.")
                return redirect('profiles:edit_profile', username=request.user.username)

        return self.render_to_response({
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
        })