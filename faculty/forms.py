# from django import forms
# from .models import CustomUser
# from django.core.exceptions import ValidationError

# class SimpleUserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email', 'course_name', 'center_name')

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user


from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class SimpleUserCreationForm(forms.ModelForm):
    user_date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Date of today',
            'type': 'date',
        }),
        required=True
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username',
            'pattern': '[A-Za-z0-9]+',  # Allows letters and digits
        }),
        required=True
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }),
        required=True
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password Again'
        }),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'center_name', 'course_name', 'email', 'user_date')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter First Name',
                'pattern': '[A-Za-z]+'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Last Name',
                'pattern': '[A-Za-z]+'
            }),
            'center_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Center Name',
                'pattern': '[A-Za-z0-9 ]+'  # Allows letters, digits, and spaces
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Your Course Name',
                'pattern': '[A-Za-z ]+'  # Allows letters and spaces
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'user_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Date of today'
            }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user




# from django import forms
# from .models import CustomUser
# from django.core.exceptions import ValidationError

# class SimpleUserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter Password'
#         }),
#         required=True
#     )
#     password2 = forms.CharField(
#         label='Password confirmation',
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter Password Again'
#         }),
#         required=True
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'center_name', 'course_name', 'email')
#         widgets = {
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter First Name',
#                 'pattern': '[A-Za-z]+'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Last Name',
#                 'pattern': '[A-Za-z]+'
#             }),
#             'center_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Your Center Name',
#                 'pattern': '[A-Za-z0-9]+'
#             }),
#             'course_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Your Course Name',
#                 # 'pattern': '[A-Za-z0-9]+'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email Address'
#             }),
#         }

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user
