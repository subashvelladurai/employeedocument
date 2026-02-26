from django.db import models
from django.utils.timezone import now


class Document(models.Model):
    title = models.CharField(max_length=255 ,null=True)
    description = models.TextField()
    status=models.BooleanField(default=False)
    created_by = models.IntegerField(null=True)
    created_date = models.DateTimeField(default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    pdf_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
