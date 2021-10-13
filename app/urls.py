from django.urls import path

from app.views import pdf1, pdf2

urlpatterns = [
    path('pdf1/', pdf1, name='pdf1'),
    path('pdf2/', pdf2, name='pdf2'),
]
