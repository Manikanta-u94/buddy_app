from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class UserSignupSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'contact']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        contact = validated_data.pop('contact')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, contact=contact)
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Incorrect username or password.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


# 1. Platform Serializer
class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']

# 2. Page Serializer with nested Platform data
class PageSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(read_only=True)
    platform_id = serializers.PrimaryKeyRelatedField(queryset=Platform.objects.all(), source='platform', write_only=True)

    class Meta:
        model = Page
        fields = ['id', 'name', 'post_no', 'platform', 'platform_id']

# 3. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# 4. Image Serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

# 5. Place Serializer with nested Page, Category and Images
class PlaceSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), source='page', write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = [
            'id', 'page', 'page_id', 'category', 'category_id', 'name', 'location', 'link',
            'views', 'likes', 'comments_count', 'google_rating', 'google_reviews',
            'sub_type', 'family_friendly', 'convenience', 'price_per_person', 'newly_opened',
            'local_rating', 'pet_friendly', 'best_time_to_visit', 'company_ranking',
            'highlights', 'top_picks', 'top_rated_comments', 'recent_comments', 'images'
        ]

# 6. Place Comment Serializer
class PlaceCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    place = serializers.StringRelatedField(read_only=True)
    place_id = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all(), source='place', write_only=True)

    class Meta:
        model = PlaceComment
        fields = ['id', 'user', 'user_id', 'place', 'place_id', 'comment', 'created_at']
        read_only_fields = ['created_at']


