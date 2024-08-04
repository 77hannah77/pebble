from django.contrib.auth import get_user_model
from rest_framework import serializers
from quote.serializers import QuoteSerializer, QuoteForProfileSerializer
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'nickname','profile_image'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # #profile_image = validated_data.get('profile_image', '/static/default_images/default_profile_image.jpg')
        if 'profile_image' not in validated_data or not validated_data['profile_image']:
            validated_data['profile_image'] = 'profile_images/default_profile_image.jpg'
        # profile_image = validated_data.get('profile_image')
        # if not profile_image:
        #     profile_image = 'default_images/default_profile_image.jpg'


        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            # profile_image=validated_data.get('profile_image', '/static/default_images/default_profile_image.jpg')
           
        )
        profile_image = validated_data.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
            user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class SimpleUserSerializer(serializers.ModelSerializer):
    registered_quotes = QuoteForProfileSerializer(many=True, read_only=True)  # 팔로잉 한 유저가 등록한 명언들을 프로파일 뷰에서 간단하게 보여주기 위해 만듦
    class Meta:
        model = User
        fields = ['id', 'nickname','registered_quotes']

class ProfileSerializer(serializers.ModelSerializer):
    like_quotes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    registered_quotes = QuoteForProfileSerializer(many=True, read_only=True) # Quote에 foreign key 로 들어간 user id 역참조
    # followings =serializers.PrimaryKeyRelatedField(many=True, read_only=True) #팔로잉 한 유저 id 만 저장
    followings = SimpleUserSerializer(many=True, read_only=True) # 팔로잉 한 유저 간단한 정보를 담아서 보냄
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #팔로워 한 유저 id 만 저장

    class Meta:
        model = User
        fields = ['nickname', 'like_quotes', 'email','profile_image','registered_quotes','followings', 'followers', 'following_count','follower_count']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password_confirm = serializers.CharField(write_only=True, required=False)
    profile_image = serializers.ImageField(required=False)  # 프로필 이미지 필드 추가
    class Meta:
        model = User
        fields = ['nickname', 'email', 'current_password', 'new_password', 'new_password_confirm','profile_image']

    def validate(self, data):
        user = self.instance
        if not user.check_password(data.get('current_password')):
            raise serializers.ValidationError("Current password is incorrect.")
        if 'new_password' in data or 'new_password_confirm' in data:
            if data.get('new_password') != data.get('new_password_confirm'):
                raise serializers.ValidationError("The new passwords do not match.")
        return data

    def update(self, instance, validated_data):
        validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('new_password_confirm', None)
        instance = super().update(instance, validated_data)
        if new_password:
            instance.set_password(new_password)
            instance.save()
        return instance