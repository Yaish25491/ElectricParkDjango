import datetime
from django.shortcuts import render, redirect
from .forms import SignUpForm,ChargingStationForm, CarSelectionForm, CSVUploadForm, DBSelectionForm, ExportForm, ChargingStationUpdateForm,ChargingStationViewForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import csv 
import os
from django.core.management.base import BaseCommand
from django.db import connections
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection


# Create your views here.
def index(request):
    date = datetime.datetime.now()
    #msgs = get_messeges_query()
    return render(request, "index.html", {"date": date})

def landing_page(request):
    return render(request, "LandingPage.html", {})

def choose_a_car(request):
	form = CarSelectionForm()
	
	if request.method == 'POST':
		form = CarSelectionForm(request.POST)
		if form.is_valid():
			selected_car = form.cleaned_data['car']
            # Associate the selected car with the user's profile and save it
            # For example: user.profile.selected_car = selected_car
            # user.profile.save()
			messages.success(request, 'Car Added successfully!')
	
	context = {
        'form': form,
    }
	return render(request, "ChooseACar.html", context)

def create_charging_station(request):
    if request.method == 'POST':
        form = ChargingStationForm(request.POST)
        if form.is_valid():
            charging_station = form.save(commit=False)
            charging_station.user = request.user
            charging_station.save()
            messages.success(request, 'Charging station created successfully!')
            form = ChargingStationForm()
    else:
        form = ChargingStationForm()

    context = {'form': form}
    return render(request, 'CreateAChargingStation.html', context)
    

def home(request):
    return render(request, "Home.html", {})

def new_user(request):
    return render(request, "NewUser.html", {})

#def get_messeges_query():
 #   return Messege.objects.raw("SELECT * FROM myapp_messege")
   
#def tamplate_quary():
#    name = "Banana"
#    age = 0
#    return Messege.objects.raw("SELECT * \
#                               FROM myapp_messege \
#                               WHARE user = %s AND age = %s",[name, age])

def dropdown_view(request):
    items = Item.objects.all()
    return render(request, 'ChooseACar.html', {'Maker': items})

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('Choose A Car')
	
	return render(request, "register.html", {'form':form})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')	


	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('index')

def active_orders(request):
    return render(request, "ActiveOrders.html", {})


def order_history(request):
    return render(request, "OrderHistory.html", {})


def user_settings(request):
    return render(request, "UserSettings.html", {})

def your_charging_stations(request):
    return render(request, "YourChargingStations.html", {})

def test_page(request):
    return render(request, "testpage.html", {})

def DBcontrol(request):
    return render(request, "DBcontrol.html", {})


# charging_station/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ChargingStation
from .forms import ChargingStationForm

@login_required
def charging_stations(request):
    user = request.user
    charging_stations = ChargingStation.objects.filter(user=user)

    if request.method == 'POST':
        form = ChargingStationForm(request.POST)
        if form.is_valid():
            charging_station = ChargingStation.objects.get(id=form.cleaned_data['charging_station_id'])
            charging_station.working_hours_start = form.cleaned_data['working_hours_start']
            charging_station.working_hours_finish = form.cleaned_data['working_hours_finish']
            charging_station.save()

    form = ChargingStationViewForm()

    context = {
        'charging_stations': charging_stations,
        'form': form,
    }

    return render(request, 'charging_stations.html', context)



def update_charging_station(request):
    user = request.user
    
    if request.method == 'POST':
        form = ChargingStationUpdateForm(user, request.POST)
        if form.is_valid():
            charging_station = form.cleaned_data['charging_station']
            charging_station.working_hours_start = form.cleaned_data['working_hours_start']
            charging_station.working_hours_finish = form.cleaned_data['working_hours_finish']
            charging_station.save()
            return redirect('home')  # Redirect to your desired page
    else:
        form = ChargingStationUpdateForm(user)

    context = {'form': form}
    return render(request, 'update_charging_station.html', context)


class Command(BaseCommand):
    help = 'Updates Car database table from a CSV file'

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                brand = row['Brand']
                model = row['Model']
                plug_type = row['PlugType']
                battery_pack_kwh = row['Battery_Pack_Kwh']
                
                car, created = Car.objects.update_or_create(
                    brand=brand, car_model=model,
                    defaults={'plug_type': plug_type, 'battery_pack_kwh': battery_pack_kwh}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new Car: {car}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated Car: {car}'))

def custom_charging_stations_view(request):
    # Ensure the user is logged in

    user = request.user  # Get the currently logged-in user

    # Construct the SQL query
    sql_query = """
    SELECT id, address, charger_id, description, status, working_hours_start, working_hours_finish
    FROM your_app_chargingstation
    WHERE user_id = %s
    """

    # Execute the SQL query
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [user.id])

        # Fetch the results
        charging_stations = cursor.fetchall()

    # You can print the SQL query here for debugging
    print(sql_query)

    return render(
        request,
        "myapp/charging_stations.html",
        {"charging_stations": charging_stations},
    )

def edit_working_hours(request, charging_station_id):
    if request.method == 'POST':
        charging_station = ChargingStation.objects.get(pk=charging_station_id)
        form = ChargingStationForm(request.POST, instance=charging_station)
        if form.is_valid():
            form.save()
            return redirect('charging_stations')
    
    # Handle invalid form or GET request here
    return redirect('charging_stations')

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Save the uploaded file temporarily
            with open('temp.csv', 'wb') as temp_file:
                for chunk in csv_file.chunks():
                    temp_file.write(chunk)
            # Run the management command to update the database
            command = Command()
            command.handle(csv_file='temp.csv')
            # Delete the temporary file
            os.remove('temp.csv')
            messages.success(request, 'CSV file uploaded and database updated.')
            return redirect('upload_csv')
    else:
        form = CSVUploadForm()
    
    context = {'form': form}
    return render(request, 'upload_csv.html', context)


def export_csv(request):
    if request.method == 'POST':
        form = DBSelectionForm(request.POST)
        if form.is_valid():
            selected_table = form.cleaned_data['table']
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{selected_table}.csv"'

            cursor = connections['default'].cursor()
            cursor.execute(f'SELECT * FROM {selected_table}')
            
            csv_writer = csv.writer(response)
            csv_writer.writerow([desc[0] for desc in cursor.description])  # Write column headers
            csv_writer.writerows(cursor)

            return response
    else:
        form = DBSelectionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'export_csv.html', context)


def export_records(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            selected_table = form.cleaned_data['table']
            # Fetch records from the selected table
            cursor = connections['default'].cursor()
            cursor.execute(f'SELECT * FROM {selected_table}')
            records = cursor.fetchall()

            # Create a CSV content
            csv_content = '\n'.join([','.join(map(str, row)) for row in records])
            
            # Create the HTTP response with CSV content
            response = HttpResponse(csv_content, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{selected_table}_export.csv"'
            return response
    else:
        form = ExportForm()

    context = {
        'form': form,
    }
    return render(request, 'export_records.html', context)



def get_addresses(request):
    addresses = ChargingStation.objects.values_list('address', flat=True)
    return JsonResponse(list(addresses), safe=False)



def get_info(request):
    address = request.GET.get('address')
    try:
        charging_station = ChargingStation.objects.get(address=address)
        data = {
            'charger': charging_station.charger,
            'description': charging_station.description,
        }
        return JsonResponse(data)
    except ChargingStation.DoesNotExist:
        return JsonResponse({'error': 'Charging station not found'}, status=404)
