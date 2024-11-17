from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


# ユーザー管理用のマネージャー
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        通常のユーザーを作成するためのヘルパー関数。
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # パスワードをハッシュ化
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        スーパーユーザー（管理者）を作成するためのヘルパー関数。
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# カスタムUserモデル
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # メールアドレスでログイン
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # 管理者権限のフラグ

    # ユーザーマネージャーを設定
    objects = UserManager()

    USERNAME_FIELD = "email"  # ログインに使用するフィールド
    REQUIRED_FIELDS = ["name", "phone"]  # createsuperuserコマンドで要求されるフィールド

    def __str__(self):
        return self.name


# サービスモデル
class Service(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="service_images/", blank=True, null=True)

    def __str__(self):
        return self.name


# 予約モデル
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sevice = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("booked", "予約済み"),
            ("cancelled", "キャンセル"),
            ("completed", "Completed"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.date} {self.time}"


# 営業日程モデル
class Schedule(models.Model):
    day = models.CharField(max_length=10)
    is_open = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"{self.day}: {'Open' if self.is_open else 'Closed'}"


# 問い合わせモデル
class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.name if self.user else 'Anonymous'}"
