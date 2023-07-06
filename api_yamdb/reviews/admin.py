from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'slug',
                    'name',
                    )
    search_fields = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'slug',
                    'name',
                    )
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'year',
                    'category_name',
                    'display_genres',
                    'description',
                    )
    search_fields = ('name', 'year', )
    empty_value_display = '-пусто-'
    list_editable = ('name', 'year')

    def display_genres(self, obj):
        genre_list = obj.genre.all().values_list('name', flat=True)
        return ", ".join(genre_list)

    def category_name(self, obj):
        return obj.category.name


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    search_fields = ('title', 'author', 'text')
    list_filter = ('pub_date', 'score', 'author')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
