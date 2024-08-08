from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,name,number,**extra_fields):
        if not email:
            raise ValueError("ECN not found!")
        email=self.normalize_email(email)
        user=self.model(name=name,number=number,**extra_fields)
        # user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,number,password,gender,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        # extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(name,number,**extra_fields)