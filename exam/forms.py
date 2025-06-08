from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,Property,Request

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']




class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['deal_type', 'rooms', 'area', 'price', 'address', 'description',
                  'image1', 'image2', 'image3']




class PropertyFilterForm(forms.Form):
    deal_type = forms.ChoiceField(
        choices=[('', 'Тип сделки'), ('sale', 'Продажа'), ('rent', 'Аренда')],
        required=False
    )
    rooms = forms.ChoiceField(
        choices=[('', 'Комнат'), *( (i, f'{i} комн.') for i in range(1, 6) )],
        required=False
    )





class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваше сообщение'}),
        }


