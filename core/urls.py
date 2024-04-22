from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from core.views import home, api_user_profile, get_user_profile
from .models import UserProfile
from rest_framework import routers, serializers, viewsets

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone_number", "own_invite_code", "friends_invite_code"]

                
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    


router = routers.DefaultRouter()
router.register(r'profiles', UserViewSet)
# router.register(r'profile/<int:pk>', get_user_profile)

urlpatterns = [
    path("", home),
    path("profile/<str:phone_number>", get_user_profile, name="profile"),
    path("api/", include(router.urls)),
    path("api/profile/<str:phone_number>/", api_user_profile)
]

# urlpatterns = format_suffix_patterns(urlpatterns)