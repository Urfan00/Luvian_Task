from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from services.generator import Generator


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_superuser=False, username=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.username=username
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,password=None):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password=password
        )
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=120)
    username = models.CharField(unique=True, max_length=40)
    photo = models.ImageField(upload_to='User_images', blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUser'

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_level):
        return True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=MyUser)
        return super(MyUser, self).save(*args, **kwargs)