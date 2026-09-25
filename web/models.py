from django.db import models


class Navbar(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SubMenu(models.Model):
    navbar = models.ForeignKey(
        Navbar,
        on_delete=models.CASCADE,
        related_name="submenus"
    )

    name = models.CharField(max_length=100)

    file = models.FileField(
        upload_to="submenu_files/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="banners/")
    description = models.TextField()

    def __str__(self):
        return self.title


class WebsiteSection(models.Model):
    heading = models.CharField(max_length=200)
    paragraph = models.TextField()
    image = models.ImageField(upload_to="website_sections/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading