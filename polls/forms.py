from django import forms
from django.core.exceptions import ValidationError
from .models import User, Order
from .models import user_registrated


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                                help_text='Повторите тот же самый пароль еще раз')

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = User
        fields = ('username', 'avatar')


class OrderForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = Order
        fields = ['quantity']
