from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Constituency, State, Country, District, UserProfile, PhoneOtp

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username','phone_number','first_name', 'created_at', 'updated_at', 'foreign_user', )
    list_filter = ('staff', 'active', 'role', 'admin', 'foreign_user')
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'first_name', 'country',  'email', 'last_name', 'foreign_user',)}),
        ('Permissions', {'fields': ('staff', 'active', 'admin', 'role')}),
        ('OTP', {'fields': ('otp', 'attempts')}),
        ('Can Create Post', {'fields': ('can_create', )}),
        ('Anonymous Status', {'fields': ('anonymous', )}),
    )
    filter_horizontal = () 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','phone_number', 'password1', 'password2', 'country',  'staff', 'active', 'admin', 'can_create', 'role', 'first_name', 'email', 'foreign_user',)}
        ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)

admin.site.site_header = "R2A Administration"
admin.site.site_title = "Right2Ask  Administration Portal"
admin.site.index_title = "Right2Ask Admin"
admin.site.register(User, CustomUserAdmin)
admin.site.register(PhoneOtp)
admin.site.register(Constituency)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(District)
admin.site.register(UserProfile)
admin.site.unregister(Group)