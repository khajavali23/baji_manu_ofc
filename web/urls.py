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
    path(
    'add-content-section/',
    views.add_content_section,
    name='add_content_section'
),

path(
    'edit-content-section/<int:id>/',
    views.edit_content_section,
    name='edit_content_section'
),

path(
    'delete-content-section/<int:id>/',
    views.delete_content_section,
    name='delete_content_section'
),
path(
    "submenu-content/<int:submenu_id>/",
    views.submenu_content,
    name="submenu_content"
),
path(
        "document/<int:id>/",
        views.view_submenu_document,
        name="view_submenu_document"
    ),
    path(
        "navbar-document/<int:id>/",
        views.view_navbar_document,
        name="view_navbar_document"
    ),
     # Navbar Content
    path(
        'navbar-content/<int:navbar_id>/',
        views.navbar_content,
        name='navbar_content',
    ),
   path(
    "submenu-document/<int:document_id>/",
    views.view_submenu_document,
    name="view_submenu_document"
),

path(
    "navbar-document/<int:document_id>/",
    views.view_navbar_document,
    name="view_navbar_document"
),
path(
    "delete-banner-button/<int:button_id>/",
    views.delete_banner_button,
    name="delete_banner_button"
),
path(
    "delete-submenu-document/<int:document_id>/",
    views.delete_submenu_document,
    name="delete_submenu_document"
),
]

# MEDIA FILES (must be separate)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)