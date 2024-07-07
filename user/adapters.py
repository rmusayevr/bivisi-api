from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        if 'google' in request.path:
            user.sign_up_method = 'google'
        elif 'facebook' in request.path:
            user.sign_up_method = 'facebook'
        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if 'google' in request.path:
            user.sign_up_method = 'google'
            user.status = 'Active'
            user.is_active = True
        elif 'facebook' in request.path:
            user.sign_up_method = 'facebook'
            user.status = 'Active'
            user.is_active = True
