from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class UserWord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="ユーザー"
    )

    word = models.CharField(
        max_length=100,
        verbose_name="英単語"
    )

    meaning = models.TextField(
        verbose_name="意味"
    )

    source = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="登録元"
        # 例: api / manual / book
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.word} ({self.user.username})"
