from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, FileField, ForeignKey, DateTimeField


class DocumentTemplate(Model):
    name = CharField(max_length=100)
    description = TextField(blank=True)
    pdf_file = FileField(upload_to='document_templates/')
    created_by = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
