from django.contrib import admin


from .models import Review, Title, GenreTitle, Genre, Category, Comment


admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(GenreTitle)
