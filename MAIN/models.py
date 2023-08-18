from django.db import models
import datetime

# Create your models here.
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    img = models.ImageField(upload_to="profile_pictures")

    def __str__(self):
        return self.name
    

class Blog(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today())
    description = models.TextField(blank=True)
    main_img = models.ImageField(upload_to="blog")
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Paragraph(models.Model):
    text = models.TextField(blank=True)
    is_img = models.BooleanField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Paragraph {self.order} for {self.blog}"


class ParagraphImage(models.Model):
    img = models.ImageField(upload_to="blog")
    parargraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image {self.order} for paragraph order {self.parargraph.order} for {self.parargraph.blog}"
