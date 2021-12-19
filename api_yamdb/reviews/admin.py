from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(GenreTitle)
