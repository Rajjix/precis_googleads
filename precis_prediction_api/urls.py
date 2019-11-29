"""
Url Configuration.
"""

from django.contrib import admin
from django.urls import path
from predict_me.views import call_me_oracle

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', call_me_oracle, name="the_oracle")
]
