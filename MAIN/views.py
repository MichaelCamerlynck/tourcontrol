from django.views.generic import TemplateView
import datetime



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
   