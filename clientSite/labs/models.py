from django.db import models

# # Create your models here.
# from django.db import models
#
# class LabModule(models.Model):
#     lab_name = models.CharField(max_length=128)  # Название для отображения
#     container_name = models.CharField(max_length=64)  # Внутреннее/техническое имя
#     TIER_CHOICES = [
#         ('easy', 'Easy'),
#         ('medium', 'Medium'),
#         ('hard', 'Hard'),
#     ]
#     tier = models.CharField(max_length=8, choices=TIER_CHOICES, default='easy')
#     description = models.TextField(blank=True)
#     full_description = models.TextField(blank=True)
#     def __str__(self):
#         return self.lab_name
