from django import forms
from map.models import EventInner
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from users.models import Profile


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прозвище'}))
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        strip=False,
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Проверить пароль'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прозвище'}),
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class EventForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Название'})
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local',
                                          'class': 'date-picker',
                                          'placeholder': 'Дата и время проведения'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text',
                                      'id': 'address',
                                      'oninput': 'delayedGeocode()',
                                      'placeholder': 'Адрес события'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Описание вашего события'})
    )

    class Meta:
        model = EventInner
        fields = ['title', 'description', 'address', 'date', 'image']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'background_image', 'first_name', 'last_name', 'status', 'city']
