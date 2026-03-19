from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        help_text='Chỉ chứa chữ cái, số và gạch dưới.',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Tên đăng nhập chỉ được chứa chữ, số và các ký tự @_+.-',
            )
        ],
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email đã được sử dụng.')
        return email
