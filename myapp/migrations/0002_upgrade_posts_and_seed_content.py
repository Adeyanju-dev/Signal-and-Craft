from django.db import migrations, models
import django.utils.timezone


SAMPLE_POSTS = [
    {
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
]


def populate_post_metadata(apps, schema_editor):
    Post = apps.get_model("myapp", "Post")

    for post in Post.objects.all():
        if not post.subtitle:
            post.subtitle = "A practical note from a growing Django publishing project."
        if not post.excerpt:
            plain_text = " ".join(post.content.split())
            post.excerpt = (plain_text[:217] + "...") if len(plain_text) > 220 else plain_text
        if not post.category:
            post.category = "engineering"
        post.save(update_fields=["subtitle", "excerpt", "category", "updated_at"])

    for sample in SAMPLE_POSTS:
        Post.objects.get_or_create(
            title=sample["title"],
            defaults=sample,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.CharField(
                choices=[
                    ("engineering", "Engineering"),
                    ("design", "Design"),
                    ("process", "Process"),
                    ("career", "Career"),
                    ("tutorial", "Tutorial"),
                ],
                default="engineering",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="excerpt",
            field=models.CharField(blank=True, max_length=260),
        ),
        migrations.AddField(
            model_name="post",
            name="featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="post",
            name="subtitle",
            field=models.CharField(blank=True, max_length=220),
        ),
        migrations.AddField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RunPython(populate_post_metadata, migrations.RunPython.noop),
    ]
