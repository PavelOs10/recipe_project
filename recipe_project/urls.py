from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('users/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('users/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('users/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('users/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('users/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('users/register/', include('recipes_app.urls_users')),
    path('', include('recipes_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)