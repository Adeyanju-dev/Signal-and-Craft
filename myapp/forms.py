from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "subtitle", "category", "featured", "excerpt", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-emerald-400 dark:focus:ring-emerald-900/40",
                    "placeholder": "A clear, specific headline",
                }
            ),
            "subtitle": forms.TextInput(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-emerald-400 dark:focus:ring-emerald-900/40",
                    "placeholder": "One sentence that tells readers why this post matters",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-emerald-400 dark:focus:ring-emerald-900/40",
                }
            ),
            "featured": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 h-4 w-4 rounded border-slate-300 text-emerald-600 focus:ring-emerald-500 dark:border-slate-600 dark:bg-slate-900",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-emerald-400 dark:focus:ring-emerald-900/40",
                    "rows": 3,
                    "placeholder": "A short summary for the homepage cards. Leave blank to auto-generate one.",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-4 focus:ring-emerald-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:focus:border-emerald-400 dark:focus:ring-emerald-900/40",
                    "rows": 16,
                    "placeholder": "Write the full article here.",
                }
            ),
        }
