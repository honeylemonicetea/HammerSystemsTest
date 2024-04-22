from django import forms
from core.models import UserProfile
class UserSignUpForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, label="Номер телефона")
    class Meta:
        model = UserProfile
        fields = ["phone_number"]


class EditUserProfile(forms.ModelForm):
    friends_invite_code = forms.CharField(max_length=6, label="Инвайт-код")
    class Meta:
        model = UserProfile
        fields = ["friends_invite_code"]