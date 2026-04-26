from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('add-navbar/', views.add_navbar, name='add_navbar'),
    path('edit-navbar/<int:id>/', views.edit_navbar, name='edit_navbar'),
    path('delete-navbar/<int:id>/', views.delete_navbar, name='delete_navbar'),

    path('add-banner/', views.add_banner, name='add_banner'),
    path('edit-banner/<int:id>/', views.edit_banner, name='edit_banner'),
    path('delete-banner/<int:id>/', views.delete_banner, name='delete_banner'),

    path('add-submenu/<int:nav_id>/', views.add_submenu, name='add_submenu'),
    path('edit-submenu/<int:id>/', views.edit_submenu, name='edit_submenu'),
    path('delete-submenu/<int:id>/', views.delete_submenu, name='delete_submenu'),
]

# MEDIA FILES (must be separate)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)