from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Review)
admin.site.register(Titles)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Comment)
admin.site.register(GenreTitles)