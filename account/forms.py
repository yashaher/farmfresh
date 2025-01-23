from django import forms
from .models import contact
from .models import Customer
from django.contrib.auth.forms import UserCreationForm


class CustomerCreationForm(UserCreationForm):
       
    
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'contact','dob','gender','profile_picture']

        widgets={
            
            # 'address':forms.TextInput(attrs={'placeholder':'Building/flat no.','class':'form-control','required':True}),
            # 'landmark':forms.TextInput(attrs={'placeholder':'Area/nearby.','class':'form-control','required':True}),
            # 'pincode':forms.TextInput(attrs={'placeholder':'6 digit pincode','class':'form-control','required':True}),
            'profile_picture': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'dob':forms.DateInput(attrs={'class':'form-control','required':'True','type':'date'}),
            'gender':forms.Select(choices=(('male','Male'),('female','Female'),('others','Others')),attrs={'class':'form-control','required':'True'})
        }

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 px-4',
                'placeholder': 'Your Name',
                'style': 'height: 55px;',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-light border-0 px-4',
                'placeholder': 'Your Email',
                'style': 'height: 55px;',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 px-4',
                'placeholder': 'Oreder',
                'style': 'height: 55px;',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0 px-4 py-3',
                'rows': 2,
                'placeholder': 'Message',
            }),
        }


from product.models import Vegetable  
class WeeklyBasketForm(forms.Form):
    BASKET_CHOICES = [
        ('small', 'Small Basket - 500/'),
        ('medium', 'Medium Basket - 799/'),
        ('large', 'Large Basket - 950/'),
    ]
    basket_type = forms.ChoiceField(
        choices=BASKET_CHOICES,
        widget=forms.RadioSelect,
        label="Choose your basket type"
    )
    vegetables = forms.ModelMultipleChoiceField(
        queryset=Vegetable.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select vegetables"
    )
    
    from django import forms

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Enter your email address')
