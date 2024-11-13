from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    code = models.CharField(max_length=13, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    time = models.PositiveIntegerField(default=0)
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class Variant(models.Model):
    savol = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    variant = models.CharField(max_length=200)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.variant

class Natija(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    soni = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return str(self.soni)
