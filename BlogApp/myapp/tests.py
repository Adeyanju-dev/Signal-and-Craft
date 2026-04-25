from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post

User = get_user_model()


class PostModelTests(TestCase):
    def test_excerpt_is_generated_when_left_blank(self):
        post = Post.objects.create(
            title="Generated excerpt",
            content=" ".join(["Django"] * 80),
        )

        self.assertTrue(post.excerpt)
        self.assertGreaterEqual(post.reading_time_minutes, 1)

    def test_featured_post_replaces_previous_featured_post(self):
        first = Post.objects.create(
            title="First featured",
            content="First content",
            featured=True,
        )
        second = Post.objects.create(
            title="Second featured",
            content="Second content",
            featured=True,
        )

        first.refresh_from_db()
        second.refresh_from_db()

        self.assertFalse(first.featured)
        self.assertTrue(second.featured)
        self.assertTrue(second.slug)


class PostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="editor",
            password="strong-pass-123",
        )

    def test_home_uses_featured_post_when_available(self):
        older = Post.objects.create(
            title="Older post",
            category=Post.Category.PROCESS,
            excerpt="Older post summary",
            content="Older post content",
            created_at=timezone.now() - timedelta(days=2),
        )
        featured = Post.objects.create(
            title="Featured post",
            category=Post.Category.ENGINEERING,
            excerpt="Featured summary",
            content="Featured content",
            featured=True,
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["featured_post"], featured)
        self.assertIn(older, response.context["article_posts"])

    def test_create_post_requires_login(self):
        response = self.client.get(reverse("post-create"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('post-create')}")

    def test_create_post_redirects_to_detail_page(self):
        self.client.login(username="editor", password="strong-pass-123")
        response = self.client.post(
            reverse("post-create"),
            {
                "title": "Shipped with confidence",
                "subtitle": "Making a small app feel complete",
                "category": Post.Category.DESIGN,
                "featured": "on",
                "excerpt": "",
                "content": "A longer article body that should create the new post.",
            },
        )

        post = Post.objects.get(title="Shipped with confidence")
        self.assertRedirects(response, post.get_absolute_url())
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.slug)
