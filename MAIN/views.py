from django.views.generic import TemplateView
import datetime
from django.http import JsonResponse
import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import os


# Create your views here.
class IndexView(TemplateView):
   template_name = "index.html"

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year
        context["splash"] = True

        return context
   

class IndexHomeView(TemplateView):
   template_name = "index.html"

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year
        context["splash"] = False

        return context
   

class Contact(TemplateView):
   template_name = "contact.html"

   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Contact | Tourcontrol Consulting"
        context["year"] = datetime.datetime.now().year

        return context


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
   # requests.post(url, json=data)

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