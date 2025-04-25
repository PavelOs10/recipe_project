from django import forms
from .models import Recipe, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Категории'
    )
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'preparation_time', 'image', 'ingredients', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'steps': forms.Textarea(attrs={'rows': 5}),
        }

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label='Имя пользователя')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']