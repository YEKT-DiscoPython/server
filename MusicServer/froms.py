from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignInForm(AuthenticationForm):
    err_msg = dict(invalid='Логин содержит недопустмые символы',
                   required='Поле обязательно для заполнения',
    )
    username = forms.CharField(error_messages=err_msg,
                               label='Логин',
                               max_length=30,
                               widget=forms.TextInput,
                               required=True
    )

    err_msg = dict(invalid='Пароль содержит недопустмые символы',
                   required='Поле обязательно для заполнения',
    )
    password = forms.CharField(label='Пароль',
                               max_length=40,
                               error_messages=err_msg,
                               widget=forms.PasswordInput,
                               required=True
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    error_messages = dict(invalid='Логин содержит недопустмые символы',
                          required='Поле обязательно для заполнения',
                          unique='Пользователь с таким логином уже зарегистрирован'
    )
    username = forms.CharField(error_messages=error_messages,
                               label='Логин',
                               max_length=30,
                               widget=forms.TextInput,
                               required=True
    )

    error_messages = dict(invalid='Введите правильный email',
                          required='Поле обязательно для заполнения',
    )
    email = forms.EmailField(label='Email',
                             error_messages=error_messages,)

    error_messages = dict(invalid='Пароль содержит недопустмые символы',
                   required='Поле обязательно для заполнения',
    )
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                error_messages=error_messages,)

    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput,
                                error_messages=error_messages,)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TrackForm(forms.Form):
    # track = forms.FileField()
    source = forms.FileField()
