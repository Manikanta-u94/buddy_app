from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


# 1. Platform: (Instagram, Google, YouTube, etc.)
class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 2. Page: A business/social media page, linked to Platform
class Page(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='pages')
    name = models.CharField(max_length=100)
    post_no = models.CharField(max_length=50, blank=True, null=True)  # if post_no is not always present

    def __str__(self):
        return f"{self.name} ({self.platform.name})"

# 3. Category: Type of place (Restaurant, Café, etc.)
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 4. Place: Central table
class Place(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    google_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    google_reviews = models.PositiveIntegerField(null=True, blank=True)
    sub_type = models.CharField(max_length=100, blank=True)  # e.g. Indian, Chinese, etc.
    family_friendly = models.BooleanField(default=False)
    convenience = models.CharField(max_length=100, blank=True)
    price_per_person = models.CharField(max_length=50, blank=True)
    newly_opened = models.BooleanField(default=False)
    local_rating = models.CharField(max_length=20, blank=True)  # e.g. 4.5/5
    pet_friendly = models.BooleanField(default=False)
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    company_ranking = models.CharField(max_length=50, blank=True)
    highlights = models.TextField(blank=True)
    top_picks = models.TextField(blank=True)  # comma-separated
    top_rated_comments = models.TextField(blank=True)  # can use JSON or text
    recent_comments = models.TextField(blank=True)  # can use JSON or text

    def __str__(self):
        return self.name

# 5. Image: Multiple per Place
class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='place_images/')

    def __str__(self):
        return f"Image for {self.place.name}"

# 6. User Comment: Logged in users can comment on a Place
class PlaceComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='user_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.place.name}"


