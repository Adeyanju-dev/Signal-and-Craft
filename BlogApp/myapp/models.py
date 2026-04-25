import math
import textwrap

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify

class Post(models.Model):
    class Category(models.TextChoices):
        ENGINEERING = "engineering", "Engineering"
        DESIGN = "design", "Design"
        PROCESS = "process", "Process"
        CAREER = "career", "Career"
        TUTORIAL = "tutorial", "Tutorial"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    subtitle = models.CharField(max_length=220, blank=True)
    excerpt = models.CharField(max_length=260, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.ENGINEERING,
    )
    featured = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])

    @property
    def reading_time_minutes(self):
        word_count = len(strip_tags(self.content).split())
        return max(1, math.ceil(word_count / 180))

    @property
    def author_name(self):
        if not self.author:
            return "Editorial Desk"
        return self.author.get_full_name() or self.author.get_username()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            candidate = base_slug
            counter = 2
            while Post.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate
        if not self.excerpt:
            plain_text = " ".join(strip_tags(self.content).split())
            self.excerpt = textwrap.shorten(plain_text, width=220, placeholder="...")
        if self.featured:
            Post.objects.exclude(pk=self.pk).filter(featured=True).update(featured=False)
        super().save(*args, **kwargs)
