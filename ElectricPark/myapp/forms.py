# users/forms.py

from django import forms
from .models import User,ChargingStation,Charger, Car
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import connections

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import Profile  # Import your Profile model

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<li span class="form-text text-muted"><small>Required: 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span li>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<li span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span li>'
		

def save(self, commit=True):
	user = super(SignUpForm, self).save(commit=False)
	user.email = self.cleaned_data['email']
	if commit:
		user.save()

            # Create the associated Profile for the user
	profile = Profile.objects.create(user=user)

	return user


class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

class ChargingStationForm(forms.ModelForm):

	address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}))
	description =  forms.CharField(label="", max_length=200, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write anything to describe your charging station'}))
    
	def	__init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['charger'].queryset = Charger.objects.all()

	class Meta:
		model = ChargingStation
		fields = ('address', 'charger', 'description')


class ChargingStationViewForm(forms.ModelForm):
    class Meta:
        model = ChargingStation
        fields = ['working_hours_start', 'working_hours_finish']

class ChargingStationUpdateForm(forms.Form):
    charging_station = forms.ModelChoiceField(queryset=None, empty_label=None)
    working_hours_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control datetimepicker-input'}))
    working_hours_finish = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control datetimepicker-input'}))

    def __init__(self, user, *args, **kwargs):
        super(ChargingStationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['charging_station'].queryset = ChargingStation.objects.filter(user=user)



class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'car_model', 'plug_type']

class CarSelectionForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all(), empty_label=None, label="Select a Car")
    


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()



class DBSelectionForm(forms.Form):
	table = forms.ChoiceField(choices=[], label='Select a table')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['table'].choices = self.get_table_choices()

	def get_table_choices(self):
		table_names = connections.introspection.table_names()
		#return [(table_name, table_name) for table_name in table_names]
		return table_names


class ExportForm(forms.Form):
    table = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].choices = self.get_table_choices()

    def get_table_choices(self):
        table_names = connections['default'].introspection.table_names()
        return [(table_name, table_name) for table_name in table_names]


