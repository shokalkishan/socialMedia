from .models import *
from datetime import date
from django import forms
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    image=forms.ImageField()
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'password']
        
    
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_date_of_birth(self):
        """
        Custom clean method to validate the Date of Birth.
        """
        dob = self.cleaned_data.get('date_of_birth')
        if dob is not None:
            # Calculate the age from the Date of Birth
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Check if the age is less than 18
            if age < 18:
                raise ValidationError('You must be at least 18 years old.')
        return dob
    
    def clean_username(self):
        username=self.cleaned_data.get('username')
        user=Profile.objects.filter(username=username)
        if(len(user)==1):
            raise ValidationError(f'User with username {username} already exist.')
        return username


    def clean_password(self):
        """
        Validate that the password meets certain criteria.
        """
        # Define the criteria for a valid password
        min_length = 8
        min_uppercase = 1
        min_lowercase = 1
        min_digits = 1

        # Check the length of the password
        value=self.cleaned_data.get('password')
        if len(value) < min_length:
            raise ValidationError(f'The password must be at least {min_length} characters long.')

        # Check for at least one uppercase letter
        if sum(1 for char in value if char.isupper()) < min_uppercase:
            raise ValidationError(f'The password must contain at least {min_uppercase} uppercase letter.')

        # Check for at least one lowercase letter
        if sum(1 for char in value if char.islower()) < min_lowercase:
            raise ValidationError(f'The password must contain at least {min_lowercase} lowercase letter.')

        # Check for at least one digit
        if sum(1 for char in value if char.isdigit()) < min_digits:
            raise ValidationError(f'The password must contain at least {min_digits} digit.')
        return value


class LoginForm(forms.Form):

    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50,widget=forms.PasswordInput)
