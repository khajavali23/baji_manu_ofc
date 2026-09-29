
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from .models import Navbar, Banner, SubMenu, WebsiteSection, SubMenuContent,SubMenuDocument
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import (
    Navbar,
    SubMenu,
    Banner,
    WebsiteSection,
    SubMenuContent,
    NavbarContent,
    NavbarDocument,
    SubMenuDocument,
    BannerButton,
)


# =========================================================
# HOME
# =========================================================

def home(request):

    # =========================================================
    # NAVBAR
    # =========================================================

    navbars = Navbar.objects.all()

    # =========================================================
    # BANNER
    # =========================================================

    banner = Banner.objects.first()

    if banner:
        banner.buttons_list = banner.buttons.filter(
            is_active=True
        ).order_by("order")

    # =========================================================
    # WEBSITE SECTIONS
    # =========================================================

    sections = WebsiteSection.objects.all().order_by('-id')

    # =========================================================
    # SUBMENUS
    # =========================================================

    submenus = SubMenu.objects.all()

    # =========================================================
    # SUBMENU CONTENTS
    # =========================================================

    submenu_contents = []

    for submenu in submenus:

        content = SubMenuContent.objects.filter(
            submenu=submenu
        ).first()

        documents = []

        if content:

            for doc in content.documents.all():

                documents.append({
                    "id": doc.id,
                    "name": doc.document_name,
                    "url": doc.document.url if doc.document else "",
                })

        submenu_contents.append({

            "id": submenu.id,

            "name": submenu.name,

            "heading": (
                content.heading
                if content
                else ""
            ),

            "paragraph": (
                content.paragraph
                if content
                else ""
            ),

            "image": (
                content.image.url
                if content and content.image
                else ""
            ),

            "documents": documents,
        })

    # =========================================================
    # NAVBAR CONTENTS
    # =========================================================

    navbar_contents = []

    for navbar in navbars:

        content = NavbarContent.objects.filter(
            navbar=navbar
        ).first()

        documents = []

        if content:

            for doc in content.documents.all():

                documents.append({
                    "id": doc.id,
                    "name": doc.document_name,
                    "url": doc.document.url if doc.document else "",
                })

        navbar_contents.append({

            "id": navbar.id,

            "name": navbar.name,

            "heading": (
                content.heading
                if content
                else ""
            ),

            "paragraph": (
                content.paragraph
                if content
                else ""
            ),

            "image": (
                content.image.url
                if content and content.image
                else ""
            ),

            "documents": documents,
        })

    # =========================================================
    # RENDER
    # =========================================================

    return render(
        request,
        "index.html",
        {
            "navbars": navbars,
            "banner": banner,
            "sections": sections,
            "submenus": submenus,
            "submenu_contents": submenu_contents,
            "navbar_contents": navbar_contents,
        }
    )
# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect('/login/')


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    return render(request, 'dashboard.html', {

        'navbars': Navbar.objects.all(),

        'banners': Banner.objects.all(),

        'submenus': SubMenu.objects.all(),

        'sections': WebsiteSection.objects.all(),

        'navbar_contents': NavbarContent.objects.all(),

    })


# =========================================================
# NAVBAR CRUD
# =========================================================

@login_required
def add_navbar(request):

    if request.method == "POST":

        Navbar.objects.create(
            name=request.POST['name'],
            url=request.POST['url']
        )

        return redirect('/dashboard/')

    return render(request, 'add_navbar.html')


@login_required
def edit_navbar(request, id):

    nav = get_object_or_404(
        Navbar,
        id=id
    )

    if request.method == "POST":

        nav.name = request.POST['name']
        nav.url = request.POST['url']

        nav.save()

        return redirect('/dashboard/')

    return render(request, 'edit_navbar.html', {
        'nav': nav
    })


@login_required
def delete_navbar(request, id):

    nav = get_object_or_404(
        Navbar,
        id=id
    )

    nav.delete()

    return redirect('/dashboard/')


# =========================================================
# BANNER CRUD
# =========================================================

@login_required
def add_banner(request):

    if request.method == "POST":

        banner = Banner.objects.create(
            title=request.POST['title'],
            image=request.FILES['image'],
            description=request.POST['description'],
            button_text=request.POST.get('button_text'),
            button_email=request.POST.get('button_email')
        )


        # =========================================
        # CREATE BANNER BUTTONS
        # =========================================

        button_texts = request.POST.getlist(
            'button_texts[]'
        )

        button_types = request.POST.getlist(
            'button_types[]'
        )

        button_values = request.POST.getlist(
            'button_values[]'
        )


        for index, text in enumerate(button_texts):

            text = text.strip()

            if not text:
                continue


            button_type = (
                button_types[index]
                if index < len(button_types)
                else "url"
            )


            value = (
                button_values[index].strip()
                if index < len(button_values)
                else ""
            )


            BannerButton.objects.create(

                banner=banner,

                text=text,

                button_type=button_type,

                url=value
                if button_type == "url"
                else "",

                page_url=value
                if button_type == "page"
                else "",

                email=value
                if button_type == "email"
                else "",

                order=index,

                is_active=True
            )


        return redirect('/dashboard/')


    return render(
        request,
        'add_banner.html'
    )

@login_required
def edit_banner(request, id):

    banner = get_object_or_404(
        Banner,
        id=id
    )

    if request.method == "POST":

        # =========================================
        # UPDATE EXISTING BANNER
        # =========================================

        banner.title = request.POST.get(
            'title',
            banner.title
        )

        if request.FILES.get('image'):
            banner.image = request.FILES['image']

        banner.description = request.POST.get(
            'description',
            banner.description
        )

        # =========================================
        # EXISTING BANNER CTA
        # =========================================

        banner.button_text = request.POST.get(
            'button_text'
        )

        banner.button_email = request.POST.get(
            'button_email'
        )

        banner.save()


        # =========================================
        # BANNER BUTTONS
        # =========================================

        button_ids = request.POST.getlist(
            'button_ids[]'
        )

        button_texts = request.POST.getlist(
            'button_texts[]'
        )

        button_types = request.POST.getlist(
            'button_types[]'
        )

        button_values = request.POST.getlist(
            'button_values[]'
        )


        # -----------------------------------------
        # UPDATE / CREATE BUTTONS
        # -----------------------------------------

        for index, text in enumerate(button_texts):

            text = text.strip()

            if not text:
                continue


            button_type = (
                button_types[index]
                if index < len(button_types)
                else "url"
            )


            value = (
                button_values[index].strip()
                if index < len(button_values)
                else ""
            )


            button_id = (
                button_ids[index]
                if index < len(button_ids)
                else ""
            )


            # -------------------------------------
            # EXISTING BUTTON
            # -------------------------------------

            if button_id:

                button = get_object_or_404(
                    BannerButton,
                    id=button_id,
                    banner=banner
                )

            # -------------------------------------
            # NEW BUTTON
            # -------------------------------------

            else:

                button = BannerButton(
                    banner=banner
                )


            # -------------------------------------
            # COMMON DATA
            # -------------------------------------

            button.text = text
            button.button_type = button_type


            # Clear old destinations

            button.url = None
            button.page_url = None
            button.email = None
            button.document = None


            # -------------------------------------
            # DESTINATION
            # -------------------------------------

            if button_type == "url":

                button.url = value


            elif button_type == "page":

                button.page_url = value


            elif button_type == "email":

                button.email = value


            elif button_type == "document":

                # Document handling can be added
                # here when needed.

                pass


            button.save()


        return redirect('/dashboard/')


    return render(
        request,
        'edit_banner.html',
        {
            'banner': banner
        }
    )

@login_required
def delete_banner(request, id):

    banner = get_object_or_404(
        Banner,
        id=id
    )

    banner.delete()

    return redirect('/dashboard/')


# =========================================================
# SUBMENU CRUD
# =========================================================

@login_required
def add_submenu(request, nav_id):

    navbar = get_object_or_404(
        Navbar,
        id=nav_id
    )

    if request.method == "POST":

        name = request.POST.get('name')
        file = request.FILES.get('file')

        SubMenu.objects.create(
            navbar=navbar,
            name=name,
            file=file
        )

        return redirect('dashboard')

    return render(request, 'add_submenu.html', {
        'navbar': navbar
    })


@login_required
def edit_submenu(request, id):

    submenu = get_object_or_404(
        SubMenu,
        id=id
    )

    if request.method == "POST":

        submenu.name = request.POST.get('name')

        if request.FILES.get('file'):
            submenu.file = request.FILES.get('file')

        submenu.save()

        return redirect('dashboard')

    return render(request, 'edit_submenu.html', {
        'submenu': submenu
    })


@login_required
def delete_submenu(request, id):

    submenu = get_object_or_404(
        SubMenu,
        id=id
    )

    submenu.delete()

    return redirect('dashboard')


# =========================================================
# WEBSITE SECTION CRUD
# =========================================================

@login_required
def add_content_section(request):

    if request.method == "POST":

        WebsiteSection.objects.create(
            heading=request.POST.get('heading'),
            paragraph=request.POST.get('paragraph'),
            image=request.FILES.get('image'),
            link=request.POST.get('link')
        )

        return redirect('dashboard')

    return render(
        request,
        'add_content_section.html'
    )


@login_required
def edit_content_section(request, id):

    section = get_object_or_404(
        WebsiteSection,
        id=id
    )

    if request.method == "POST":

        section.heading = request.POST.get('heading')

        section.paragraph = request.POST.get('paragraph')

        section.link = request.POST.get('link')

        if request.FILES.get('image'):
            section.image = request.FILES.get('image')

        section.save()

        return redirect('dashboard')

    return render(
        request,
        'edit_content_section.html',
        {
            'section': section
        }
    ) 


@login_required
def delete_content_section(request, id):

    section = get_object_or_404(
        WebsiteSection,
        id=id
    )

    section.delete()

    return redirect('dashboard')


@login_required
def submenu_content(request, submenu_id):

    submenu = get_object_or_404(
        SubMenu,
        id=submenu_id
    )

    try:
        content = submenu.content
    except SubMenuContent.DoesNotExist:
        content = None

    if request.method == "POST":

        # =========================================
        # BASIC CONTENT
        # =========================================

        heading = request.POST.get(
            "heading",
            ""
        ).strip()

        paragraph = request.POST.get(
            "paragraph",
            ""
        ).strip()

        image = request.FILES.get("image")


        # =========================================
        # CREATE / UPDATE CONTENT
        # =========================================

        if content:

            content.heading = heading
            content.paragraph = paragraph

            if image:
                content.image = image

            content.save()

        else:

            content = SubMenuContent.objects.create(
                submenu=submenu,
                heading=heading,
                paragraph=paragraph,
                image=image
            )


        # =========================================
        # GET ALL DOCUMENT NAMES
        # =========================================

        document_names = request.POST.getlist(
            "document_names"
        )

        # =========================================
        # GET ALL DOCUMENT FILES
        # =========================================

        documents = request.FILES.getlist(
            "documents"
        )


        # =========================================
        # SAVE EVERY DOCUMENT
        # =========================================

        for index, document in enumerate(documents):

            if index >= len(document_names):
                break

            name = document_names[index].strip()

            if name and document:

                SubMenuDocument.objects.create(
                    submenu_content=content,
                    document_name=name,
                    document=document
                )


        return redirect("dashboard")


    return render(
        request,
        "submenu_content.html",
        {
            "submenu": submenu,
            "content": content,
        }
    )
def view_submenu_document(request, id):

    content = get_object_or_404(
        SubMenuContent,
        submenu_id=id
    )

    if not content.document:
        return HttpResponse("Document not found.", status=404)

    response = FileResponse(
        content.document.open("rb"),
        content_type="application/pdf"
    )

    response["Content-Disposition"] = "inline"

    return response


def view_navbar_document(request, id):

    content = NavbarContent.objects.filter(
        navbar_id=id
    ).first()

    if not content or not content.document:
        return HttpResponse("Document not found.", status=404)

    return FileResponse(
        content.document.open("rb"),
        content_type="application/pdf"
    )


@login_required
def navbar_content(request, navbar_id):

    navbar = get_object_or_404(
        Navbar,
        id=navbar_id
    )

    try:
        content = navbar.content
    except NavbarContent.DoesNotExist:
        content = None


    if request.method == "POST":

        heading = request.POST.get("heading", "").strip()
        paragraph = request.POST.get("paragraph", "").strip()

        image = request.FILES.get("image")


        # =========================================
        # CREATE / UPDATE NAVBAR CONTENT
        # =========================================

        if content:

            content.heading = heading
            content.paragraph = paragraph

            if image:
                content.image = image

            content.save()

        else:

            content = NavbarContent.objects.create(
                navbar=navbar,
                heading=heading,
                paragraph=paragraph,
                image=image
            )


        # =========================================
        # DELETE EXISTING DOCUMENTS
        # =========================================

        delete_documents = request.POST.getlist(
            "delete_documents"
        )

        if delete_documents:

            NavbarDocument.objects.filter(
                id__in=delete_documents,
                navbar_content=content
            ).delete()


        # =========================================
        # ADD NEW DOCUMENTS
        # =========================================

        document_names = request.POST.getlist(
            "document_names"
        )

        documents = request.FILES.getlist(
            "documents"
        )


        for name, document in zip(
            document_names,
            documents
        ):

            name = name.strip()

            if name and document:

                NavbarDocument.objects.create(
                    navbar_content=content,
                    document_name=name,
                    document=document
                )


        return redirect(
            "dashboard"
        )


    return render(
        request,
        "navbar_content.html",
        {
            "navbar": navbar,
            "content": content,
        }
    )

import mimetypes

from django.http import FileResponse
from django.shortcuts import get_object_or_404


@login_required
def view_submenu_document(request, document_id):

    document = get_object_or_404(
        SubMenuDocument,
        id=document_id
    )

    file_path = document.document.path

    content_type, _ = mimetypes.guess_type(file_path)

    if content_type is None:
        content_type = "application/octet-stream"

    response = FileResponse(
        open(file_path, "rb"),
        content_type=content_type,
    )

    response["Content-Disposition"] = (
        f'inline; filename="{document.document.name.split("/")[-1]}"'
    )

    return response

@login_required
def view_navbar_document(request, document_id):

    document = get_object_or_404(
        NavbarDocument,
        id=document_id
    )

    file_path = document.document.path

    content_type, _ = mimetypes.guess_type(file_path)

    if content_type is None:
        content_type = "application/octet-stream"

    response = FileResponse(
        open(file_path, "rb"),
        content_type=content_type,
    )

    response["Content-Disposition"] = (
        f'inline; filename="{document.document.name.split("/")[-1]}"'
    )

    return response


@login_required
def delete_banner_button(request, button_id):

    button = get_object_or_404(
        BannerButton,
        id=button_id
    )

    banner_id = button.banner.id

    button.delete()

    return redirect(
        f"/edit-banner/{banner_id}/"
    )

@login_required
def delete_submenu_document(request, document_id):

    document = get_object_or_404(
        SubMenuDocument,
        id=document_id
    )

    submenu_id = document.submenu_content.submenu.id

    document.delete()

    return redirect(
        "submenu_content",
        submenu_id=submenu_id
    )