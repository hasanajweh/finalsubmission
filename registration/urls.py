from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import course_popularity_report
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('search/', views.course_search, name='course_search'),
    path('home/', views.home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/register/', views.register_course, name='register_course'),  
    path('course/<int:course_id>/schedule/', views.course_schedule, name='course_schedule'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('schedule/', views.view_schedule, name='view_schedule'),
    path('reports/course_popularity/', course_popularity_report, name='course_popularity_report'),
]
