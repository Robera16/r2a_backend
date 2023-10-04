from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, password, first_name,  phone_number, username, last_name, email = '', can_create=True, country = None, is_admin=False, is_active=True, is_staff=False, role=3, is_anonymous=False, foreign_user = False):
        if not username and password and first_name and phone_number:
            raise ValueError('username, phone number/email, password, first_name are required ')
        user_obj = self.model(
            first_name = first_name,
            username=username,
            phone_number=phone_number
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.role = role
        user_obj.last_name = last_name
        user_obj.email = email
        user_obj.anonymous = is_anonymous
        user_obj.can_create = can_create
        user_obj.country = country
        user_obj.foreign_user = foreign_user
        user_obj.save(using=self._db)
        return user_obj


    def create_superuser(self, phone_number, username, password, first_name):
        user_obj = self.create_user (
            phone_number=phone_number,
            username=username,
            password=password,
            last_name="",
            first_name = first_name,
            is_admin = True,
            is_staff = True
        )
        return user_obj

    def create_staffuser(self, phone_number, username, password, first_name):
        user_obj = self.create_user (
            phone_number=phone_number,
            username = username,
            password=password,
            last_name="",
            first_name = first_name,
            is_staff = True
        )
        return user_obj

    def create_politicaluser(self, phone_number, username, password, first_name):
        user_obj = self.create_user (
            username = username,
            phone_number = phone_number,
            password=password,
            last_name="",
            first_name = first_name,
            role = 1
        )
        return user_obj
    
    def create_medicaluser(self, username, password, first_name):
        user_obj = self.create_user (
            username = username,
            password=password,
            first_name = first_name,
            last_name="",
            role = 2
        )
        return user_obj