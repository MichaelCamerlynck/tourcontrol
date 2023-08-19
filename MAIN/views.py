from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import translation
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.templatetags.static import static
from django.core.files.base import ContentFile

from MAIN.models import *

import datetime
import requests
import os
import base64
import json
import uuid


# Create your views here.
class IndexView(TemplateView):
   template_name = "index.html"

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Home | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year
        context["splash"] = True
        context["members"] = TeamMember.objects.all()

        return context
   

class IndexHomeView(TemplateView):
   template_name = "index.html"

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Home | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year
        context["splash"] = False
        context["members"] = TeamMember.objects.all()

        return context
   

class Contact(TemplateView):
   template_name = "contact.html"

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Contact | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year

        return context


class BlogListView(ListView):
    template_name = "blog/list.html"
    model = Blog
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(hide=False)  
        return filtered_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Blogs | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year
        return context
    

class BlogDetailView(DetailView):
    template_name = "blog/detail.html"
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Tourcontrol Consulting Blog"
        context["year"] = datetime.datetime.now().year
        return context


class HomeSecret(LoginRequiredMixin, TemplateView):
    template_name = "secret/home.html"
    login_url = "/admin/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Admin | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year

        return context
    

class ManageMembers(LoginRequiredMixin, ListView):
    template_name = "secret/manage_members.html"
    model = TeamMember
    context_object_name = "members"
    login_url = "/admin/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Manage Memebers | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year

        return context
    

class ManageBlogList(LoginRequiredMixin, ListView):
    template_name = "secret/blog_list.html"
    model = Blog
    context_object_name = "blogs"
    login_url = "/admin/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Manage Blogs List | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year

        return context


class ManageBlog(LoginRequiredMixin, DetailView):
    template_name = "secret/manage_blog.html"
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Manage Blog"
        context["year"] = datetime.datetime.now().year
        return context


def switch_language(request, language_code):
    if language_code in [lang_code for lang_code, _ in settings.LANGUAGES]:
        translation.activate(language_code)
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('home')))
        if response.url[-1] == "/":
            response = HttpResponseRedirect(reverse("home"))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
        return response


def send_email_to_user(receiver, subject, context, template):
    sender = 'tourcontrol.system@gmail.com'
    html_content = render_to_string(template, context)
    email = EmailMultiAlternatives(subject, 'This is the plain text version of the email.', sender, [receiver])
    email.attach_alternative(html_content, 'text/html')
    email.send()


def send(request):
   name = request.GET["name"]
   email = request.GET["email"]
   topic = request.GET["topic"]
   tel = request.GET["tel"]
   message = request.GET["message"]

   formatted_message =  f"@everyone\n" \
                        f"```\n" \
                        f"Name: {name} \n" \
                        f"Email: {email} \n" \
                        f"Topic: {topic}\n" \
                        f"Phone Number: {tel}\n\n" \
                        f"Message: \n" \
                        f"{message}\n" \
                        f"```"

   data = {
        "content": formatted_message
    }

   url = "https://discord.com/api/webhooks/1141008820395581470/wnS4sh54LNr-68Kjx4ED7CWDyWsJoi_IYvx76YOLVMnKrxDviP-zRHHRURTZDAOUlL1G"
   requests.post(url, json=data)

   receiver = os.getenv('SEND_EMAIL_TO')
   context = {
        "name": name,
        "email" : email,
        "topic" : topic,
        "message" : message
    }
   template = "email.html"
   
   send_email_to_user(receiver, topic, context, template)

   return JsonResponse({"data" : "success"}, status=200)


@require_POST
def delete_member(request):
    id = request.POST["id"]

    team_member = TeamMember.objects.get(id=id)
    team_member.delete()

    data = {
        "status" : 200
        }

    return JsonResponse(data, status=200)


@require_POST
def manage_member(request):
    id = request.POST["id"]
    name = request.POST["name"]
    position = request.POST["position"]
    img = request.FILES.get("img")

    if id == "new":
        team_member = TeamMember(
            name = name,
            position = position
        )
    else:
        team_member = TeamMember.objects.get(id=id)
        team_member.name = name
        team_member.position = position
    
    if img:
        team_member.img = img
    elif not img and id == "new":
        team_member.img = static("imgs/placeholder.jpg")

    team_member.save()

    data = {
        "status" : 200
    }

    return JsonResponse(data, status=200)


@require_POST
def new_blog(request):
    title = request.POST["title"]

    blog = Blog(title=title, hide=True)
    blog.save()

    data = {
        "id" : blog.id
    }

    return JsonResponse(data, status=200)


@require_POST
def save_blog(request):
    data = json.loads(request.body.decode('utf-8'))
    main_img = base64.b64decode(data["main_img"].split(',')[1])
    detail_img = base64.b64decode(data["detail_img"].split(',')[1])

    blog = Blog.objects.get(id=data["id"])
    blog.title = data["title"]
    blog.description = data["description"]
    blog.date = data["date"]
    blog.hide = data["hide"]
    
    # if blog.main_img:
    #     os.remove(blog.main_img.path)
    # if blog.detail_img:
    #     os.remove(blog.detail_img.path)

    blog.main_img.save(f'{uuid.uuid4()}.{data["main_img"].split(",")[0].split(";")[0].split("/")[-1]}', ContentFile(main_img), save=False)
    blog.detail_img.save(f'{uuid.uuid4()}.{data["main_img"].split(",")[0].split(";")[0].split("/")[-1]}', ContentFile(detail_img), save=False)
    blog.save()

    paragraphs_to_delete = Paragraph.objects.filter(blog=blog)
    images_to_delete = ParagraphImage.objects.filter(paragraph__blog=blog)
    for image in images_to_delete:
        pass
        # os.remove(image.img.path)
    images_to_delete.delete()
    paragraphs_to_delete.delete()

    for paragraph_object in data["paragraphs"]:
        if paragraph_object["type"] == "text":
            paragraph = Paragraph(
                blog = blog,
                is_img = False,
                text = paragraph_object["text"],
                order = paragraph_object["order"]
            )
            paragraph.save()
        else:
            paragraph = Paragraph(
                blog = blog,
                is_img = True,
                order = paragraph_object["order"]
            )
            paragraph.save()

            for image_object in paragraph_object["images"]:
                image = base64.b64decode(image_object['image_data'].split(',')[1])
                paragraph_image = ParagraphImage(
                    img = static("imgs/placeholder.jpg"),
                    paragraph = paragraph,
                    order = image_object["image_order"]
                )
                img_title = f'{uuid.uuid4()}.{image_object["image_data"].split(",")[0].split(";")[0].split("/")[-1]}'
                paragraph_image.img.save(img_title, ContentFile(image), save=False)
                paragraph_image.save()

    return JsonResponse({"id" : blog.id}, status=200)

@require_POST
def delete_blog(request):
    id = request.POST["id"]
    blog = Blog.objects.get(id=id)
    blog.delete()

    return JsonResponse({"status": "success"}, status=200)