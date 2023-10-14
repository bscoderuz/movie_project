from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .models import Category, Genre, Movie, MovieShorts, Actor, Rating, RatingStar, Reviews


class MovieAdminForm(forms.ModelForm):
    description_en = forms.CharField(label="Description ru", widget=CKEditorUploadingWidget())
    description_ru = forms.CharField(label="Description en", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Category"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Reviews on the film page"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShortsInline(admin.TabularInline):
    model = MovieShorts
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200", height="150"')

    get_image.short_description = "Images"


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Film"""
    list_display = ('id', "title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [ReviewInline, MovieShortsInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = MovieAdminForm
    actions = ["publish", "unpublish"]
    readonly_fields = ("get_image",)

    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", "get_image")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100px", height="100"')

    get_image.short_description = "Poster"

    def unpublish(self, request, queryset):
        """Remove from publication"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 post has been updated"
        else:
            message_bit = f"{row_update} records have been updated"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Publish"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 post has been updated"
        else:
            message_bit = f"{row_update} records have been updated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Remove from publication"
    unpublish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Review"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Genre"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Actor"""
    list_display = ('id', "name", "age", 'get_image')
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200", height="150"')

    get_image.short_description = "Images"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating"""
    list_display = ("ip", "star", 'movie')


@admin.register(MovieShorts)
class MovieShotsAdmin(TranslationAdmin):
    """Hells from the movie"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="200", height="150"')

    get_image.short_description = "Images"


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
