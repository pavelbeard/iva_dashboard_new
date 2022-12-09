import uuid

from django.db import models
from django.db.models import fields

# Create your models here.


class Server(models.Model):
    id = fields.UUIDField(default=uuid.uuid4().hex, primary_key=True)
    hostname = fields.CharField(max_length=64, null=False)
    os = fields.CharField(max_length=32, null=False)
    kernel = fields.CharField(max_length=64, null=False)

