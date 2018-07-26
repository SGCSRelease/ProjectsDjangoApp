import string

from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from random import choice

# Create your models here.

def custom_path(instance, filename):
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    date = timezone.now()
    return 'file/%s/%s/%s/%s.%s' % (
        date.year,
        date.month,
        date.day,
        pid,
        extension,
    )

class Information(models.Model):
    secure_levels = (
        (1, '모두 참여 가능'),
        (2, '팀원 지정'),
        (3, '개인 진행'),
    )
    name = models.CharField(
        max_length=30,
        verbose_name='프로젝트 이름',
        unique=True,
    )
    project_manager = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='project_manager',
        verbose_name='총괄 디렉터',
    )
    directors = models.ManyToManyField(
        'auth.User',
        blank=True,
        related_name='project_directors',
        verbose_name='팀원',
    )
    description = models.TextField(
        blank=True,
        verbose_name='프로젝트 소개',
    )
    purpose = models.TextField(
        max_length=150,
        blank=True,
        verbose_name='목적',
    )
    reason = models.TextField(
        max_length=150,
        blank=True,
        verbose_name='주제 선정 이유',
    )
    plan = models.TextField(
        blank=True,
        verbose_name='진행계획',
    )
    secure_level = models.PositiveIntegerField(
        choices=secure_levels,
        verbose_name='참여 가능 범위',
    )
    file = models.FileField(upload_to=custom_path, validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, verbose_name='기획서')
    published_date = models.DateField(editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.published_date = timezone.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project-information', kwargs={'pk': self.pk})


class Feedback(models.Model):
    creation_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    content = models.TextField()
    project = models.ForeignKey(Information, on_delete=models.CASCADE)
