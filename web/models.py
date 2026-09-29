
from django.db import models


# =========================================================
# NAVBAR
# =========================================================

class Navbar(models.Model):

    name = models.CharField(
        max_length=100
    )

    url = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.name


# =========================================================
# NAVBAR CONTENT
# Main Navbar click → this content
# =========================================================

class NavbarContent(models.Model):

    navbar = models.OneToOneField(
        Navbar,
        on_delete=models.CASCADE,
        related_name="content"
    )

    heading = models.CharField(
        max_length=200
    )

    paragraph = models.TextField()

    image = models.ImageField(
        upload_to="navbar_content/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.heading


# =========================================================
# NAVBAR DOCUMENT
# One NavbarContent → Multiple Documents
# =========================================================

class NavbarDocument(models.Model):

    navbar_content = models.ForeignKey(
        NavbarContent,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_name = models.CharField(
        max_length=200
    )

    document = models.FileField(
        upload_to="navbar_documents/"
    )

    def __str__(self):
        return self.document_name


# =========================================================
# SUBMENU
# =========================================================

class SubMenu(models.Model):

    navbar = models.ForeignKey(
        Navbar,
        on_delete=models.CASCADE,
        related_name="submenus"
    )

    name = models.CharField(
        max_length=100
    )

    file = models.FileField(
        upload_to="submenu_files/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# =========================================================
# SUBMENU CONTENT
# SubMenu click → this content
# =========================================================

class SubMenuContent(models.Model):

    submenu = models.OneToOneField(
        SubMenu,
        on_delete=models.CASCADE,
        related_name="content"
    )

    heading = models.CharField(
        max_length=200
    )

    paragraph = models.TextField()

    image = models.ImageField(
        upload_to="submenu_content/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.heading


# =========================================================
# SUBMENU DOCUMENT
# One SubMenuContent → Multiple Documents
# =========================================================

class SubMenuDocument(models.Model):

    submenu_content = models.ForeignKey(
        SubMenuContent,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_name = models.CharField(
        max_length=200
    )

    document = models.FileField(
        upload_to="submenu_documents/"
    )

    def __str__(self):
        return self.document_name


# =========================================================
# BANNER
# =========================================================

class Banner(models.Model):

    title = models.CharField(
        max_length=200
    )

    image = models.ImageField(
        upload_to="banners/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    button_email = models.EmailField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class BannerButton(models.Model):

    BUTTON_TYPES = [
        ("page", "Page"),
        ("url", "External URL"),
        ("document", "Document"),
        ("email", "Email"),
    ]

    banner = models.ForeignKey(
        Banner,
        on_delete=models.CASCADE,
        related_name="buttons"
    )

    text = models.CharField(
        max_length=100
    )

    button_type = models.CharField(
        max_length=20,
        choices=BUTTON_TYPES,
        default="page"
    )

    url = models.URLField(
        blank=True,
        null=True
    )

    page_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    document = models.FileField(
        upload_to="banner_documents/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.text
# =========================================================
# WEBSITE SECTION
# =========================================================

class WebsiteSection(models.Model):

    heading = models.CharField(
        max_length=200
    )

    paragraph = models.TextField()

    image = models.ImageField(
        upload_to="website_sections/"
    )

    link = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.heading

