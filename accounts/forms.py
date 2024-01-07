from django.contrib.auth.models import User
from django import forms


class MyUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name and not last_name:
            raise forms.ValidationError('Хотя бы одно из полей Имя или Фамилия должно быть заполнено.')

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
