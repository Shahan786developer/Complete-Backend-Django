from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfileView.as_view(), name='register_page'),
    path('pin/', views.LoginAPIView.as_view(), name='pin_page'),
    # path('homepage/', views.homepage, name='homepage'),
    # path('waiting_page/', views.waiting_page, name='waiting_page'),
]
