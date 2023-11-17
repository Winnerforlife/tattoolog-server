from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, role, password=None, **extra_fields):
        if '@' in username:
            extra_fields.setdefault('email', username)
        else:
            extra_fields.setdefault('phone_number', username)

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, role, password=None, **extra_fields):
        user = self.create_user(username, first_name, last_name, role, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
