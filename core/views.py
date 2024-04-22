import string, random
from django.shortcuts import render, redirect
from django.urls import reverse
from core.forms import UserSignUpForm, EditUserProfile
from core.models import UserProfile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers, status


symbols = string.ascii_letters +string.digits + string.punctuation
symbols = list(symbols)

def generate_invite_code():
    random_code = ""
    for i in range(6):
        random_code += random.choice(symbols)
    return random_code
    

# Create your views here.
def home(request):
    if request.method == "GET":
        form = UserSignUpForm()
        return render(request, "home.html", {"form": form})
    elif request.method == "POST":
        form = UserSignUpForm(request.POST)
        phone_number = request.POST.get("phone_number")
        if form.is_valid():
            # data = form.cleaned_data
            # check if the user exists
            # phone_number = data.get("phone_number")
            print("creating new object")
            invite_code = generate_invite_code()
            UserProfile.objects.create(phone_number=phone_number, own_invite_code=invite_code)
            return redirect("profile", phone_number)
        else:
            print("user exists????")
            user_data = UserProfile.objects.get(phone_number=phone_number)
            return redirect("profile", phone_number)
            
        # return render(request, "home.html", {"form": form})
    
def get_user_profile(request, phone_number):
    if request.method == "GET":
        # if the user has entered an invite code, output it in the field
        user_info =  UserProfile.objects.get(phone_number=phone_number)
        friends_invite_code = user_info.friends_invite_code
        edit_profile = EditUserProfile({"friends_invite_code":friends_invite_code})
        return render(request, "user_profile.html", {"form": edit_profile})
    elif request.method == "POST":
        edit_profile = EditUserProfile(request.POST)
        if edit_profile.is_valid():
            data = edit_profile.cleaned_data
            friends_invite_code = data.get("friends_invite_code")
            # checking if the code is valid
            code_exists = None
            try:
                if UserProfile.objects.get(own_invite_code=friends_invite_code):
                    code_exists = True
            except Exception:
                code_exists = False
                
            if code_exists:
                current_user = UserProfile.objects.get(phone_number = phone_number)
                if current_user.friends_invite_code == "":
                    current_user.friends_invite_code = friends_invite_code
                    current_user.save()
                else:
                    print("there's a code already")
                print(current_user)
        else:
            print("invalid form")
        return render(request, "user_profile.html", {"form": edit_profile})


class OneUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    friend_numbers  =  serializers.ListField()
    class Meta:
        model = UserProfile
        fields = ["phone_number", "friend_numbers"]
    
@api_view(['GET'])
def api_user_profile(request, phone_number):
    print("api getttt")
    user_data = UserProfile.objects.get(phone_number=phone_number)
    raw_all_users_phones = UserProfile.objects.filter(friends_invite_code=user_data.own_invite_code)
    all_users_phones = []
    for user in raw_all_users_phones:
        all_users_phones.append(user.phone_number)
    serializer = OneUserSerializer({"phone_number":phone_number, "friend_numbers":all_users_phones})
    return Response(serializer.data, status=status.HTTP_200_OK)