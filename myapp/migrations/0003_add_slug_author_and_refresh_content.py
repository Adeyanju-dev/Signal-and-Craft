from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify


REFRESHED_POSTS = [
    {
        "match_titles": ["Designing a Django Project That Feels Like a Product"],
        "title": "Designing Calm Interfaces for Content-Heavy Products",
        "subtitle": "Clear hierarchy and disciplined spacing do more for trust than most feature lists.",
        "excerpt": "Calm interfaces help readers orient themselves quickly. The strongest layouts reduce friction, shape attention, and make complex content feel easier to navigate.",
        "category": "design",
        "featured": True,
        "content": (
            "When a product carries a lot of information, the interface has two jobs. It needs to hold the content, "
            "and it needs to prevent that content from feeling heavy.\n\n"
            "Good hierarchy is the first lever. Strong headings, disciplined spacing, and a reliable rhythm between "
            "sections let people predict where to look next. That lowers cognitive effort before anyone consciously "
            "notices the design.\n\n"
            "The second lever is restraint. Not every panel needs the same emphasis, and not every interaction deserves "
            "a visual flourish. A quieter surface often makes important actions stand out more clearly.\n\n"
            "The result is not minimalism for its own sake. It is clarity that holds up when the archive grows, the "
            "screen gets busy, and readers want answers quickly."
        ),
    },
    {
        "match_titles": ["From CRUD to Craft: Small UX Changes That Build Trust"],
        "title": "Shipping Small Features Without Leaving Rough Edges",
        "subtitle": "The finishing work is usually operational: naming, defaults, sequencing, and cleanup.",
        "excerpt": "Most product friction lives in the details around a feature, not inside the main interaction itself. Small improvements compound when defaults, messages, and layout all pull in the same direction.",
        "category": "process",
        "featured": False,
        "content": (
            "Teams often think of polish as a visual exercise, but the rough edges users notice first are usually "
            "operational. A weak default, a vague button label, or an awkward redirect can make a small feature feel less trustworthy.\n\n"
            "This is why finishing work deserves its own pass. Naming needs to be specific, empty states need to be calm, "
            "and the order of actions should match the way people naturally move through a task.\n\n"
            "The strongest improvement passes also remove leftovers. Duplicate controls, dead views, and stale copy all "
            "create drag, even when the main path technically works.\n\n"
            "Shipping well is rarely about adding more. It is about tightening the sequence until the work feels settled."
        ),
    },
    {
        "match_titles": ["What I Learned Shipping My First Django Blog"],
        "title": "Operational Details That Make Small Products Feel Reliable",
        "subtitle": "Settings, permissions, and publishing rules quietly shape whether an app feels trustworthy.",
        "excerpt": "Reliability is often established in the background. Access control, sane defaults, and clear editorial rules make a small application feel steady long before scale enters the picture.",
        "category": "engineering",
        "featured": False,
        "content": (
            "A small product does not need massive infrastructure to feel reliable, but it does need discipline. "
            "The settings file should be ready for different environments, the editing workflow should be protected, "
            "and the data model should express the rules the interface relies on.\n\n"
            "Publishing systems are a good example. If one article should lead the home page, that rule belongs in the "
            "application logic rather than in team memory. If content changes should be traceable, updated timestamps "
            "and author lines should already exist.\n\n"
            "Reliability also shows up in failure paths. Sign-in needs to be straightforward, delete actions need a pause, "
            "and redirects should always land in a sensible place.\n\n"
            "None of this is flashy. That is precisely the point. Good operational work makes the product feel composed."
        ),
    },
    {
        "match_titles": ["Structuring a Portfolio Project Recruiters Can Scan Quickly"],
        "title": "Writing Interface Copy That Helps People Move Faster",
        "subtitle": "Strong product language shortens decision time and makes workflows easier to trust.",
        "excerpt": "Interface copy works best when it reduces hesitation. Clear labels, steady voice, and direct guidance help people keep moving without second-guessing the product.",
        "category": "career",
        "featured": False,
        "content": (
            "Copy is often treated as the final step, but it shapes how quickly people can understand a screen. "
            "A button label, section title, or confirmation message can either keep the task moving or introduce unnecessary doubt.\n\n"
            "Useful interface language does not over-explain. It tells people where they are, what happens next, and "
            "what the system expects from them. The best wording feels obvious in retrospect.\n\n"
            "Consistency matters here as much as elegance. If one part of the product says article, another says post, "
            "and a third says entry, the user has to do translation work that the interface should have handled.\n\n"
            "Clear language is one of the cheapest ways to make a product feel more mature. It helps every other decision land."
        ),
    },
    {
        "match_titles": ["BlogApp"],
        "title": "Why Clear Structure Makes a Small Blog Feel Bigger",
        "subtitle": "A compact publishing system can still feel substantial when the content model and layout carry real intent.",
        "excerpt": "Readers experience structure before they experience scale. A good archive, a lead story, and steady metadata make a small body of writing feel coherent from the first visit.",
        "category": "tutorial",
        "featured": False,
        "content": (
            "Small publishing systems benefit from structure long before they benefit from volume. "
            "A lead story, a readable archive, and stable metadata give the journal a shape that readers can learn quickly.\n\n"
            "This matters because structure creates confidence. When the latest writing is easy to scan and every article "
            "follows the same editorial pattern, the archive feels purposeful rather than accidental.\n\n"
            "Good structure also helps the author. Clear fields for title, excerpt, category, and body make it easier to "
            "maintain a standard over time.\n\n"
            "A small publication does not need to feel temporary. It simply needs enough discipline that each new piece fits naturally into the whole."
        ),
    },
]


def build_unique_slug(Post, title, pk):
    base_slug = slugify(title) or "post"
    candidate = base_slug
    counter = 2
    while Post.objects.exclude(pk=pk).filter(slug=candidate).exists():
        candidate = f"{base_slug}-{counter}"
        counter += 1
    return candidate


def refresh_content(apps, schema_editor):
    Post = apps.get_model("myapp", "Post")

    for payload in REFRESHED_POSTS:
        post = None
        for title in payload["match_titles"]:
            post = Post.objects.filter(title=title).first()
            if post:
                break

        if post:
            post.title = payload["title"]
            post.subtitle = payload["subtitle"]
            post.excerpt = payload["excerpt"]
            post.category = payload["category"]
            post.featured = payload["featured"]
            post.content = payload["content"]
            post.slug = build_unique_slug(Post, payload["title"], post.pk)
            post.save()
        else:
            Post.objects.create(
                title=payload["title"],
                slug=build_unique_slug(Post, payload["title"], None),
                subtitle=payload["subtitle"],
                excerpt=payload["excerpt"],
                category=payload["category"],
                featured=payload["featured"],
                content=payload["content"],
            )

    for post in Post.objects.filter(slug__isnull=True):
        post.slug = build_unique_slug(Post, post.title, post.pk)
        post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("myapp", "0002_upgrade_posts_and_seed_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, max_length=240, null=True),
        ),
        migrations.RunPython(refresh_content, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=models.SlugField(blank=True, max_length=240, unique=True),
        ),
    ]
