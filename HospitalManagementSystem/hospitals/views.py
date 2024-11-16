from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
from datetime import date

# Create your views here.

def About(request):
    return render(request,'about.html')

def Index(request):
    return render(request,'index.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['email']
        s = request.POST['subject']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, contact=c, email=e, subject=s, message=m, msgdate=date.today(), isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())

def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request,'login.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    dc = Doctor.objects.all().count()
    pc = Patient.objects.all().count()
    ac = Appointment.objects.all().count()

    d = {'dc': dc, 'pc': pc, 'ac': ac}
    return render(request,'admin_home.html', d)

from django.contrib.auth import logout
from django.shortcuts import redirect

def Logout(request):
    if request.user.is_authenticated:
        logout(request)  # Log out the user
    return redirect('index')  # Redirect to homepage (or any other page)

def add_doctor(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    if request.method=='POST':
        n = request.POST['name']
        m = request.POST['mobile']
        sp = request.POST['special']
        try:
            Doctor.objects.create(name=n,mobile=m,special=sp)
            error="no"
        except:
            error="yes"
    return render(request,'add_doctor.html', locals())

from django.shortcuts import render, redirect
from .models import Doctor

def register(request):
    if request.method == 'POST':
        # Capture registration details
        name = request.POST['name']
        mobile = request.POST['mobile']
        special = request.POST['special']

        # Save the registration details to the Doctor model
        doctor = Doctor(name=name, mobile=mobile, special=special)
        doctor.save()

        # After successful registration, redirect to doctor login
        return redirect('doctor_login')  # Ensure 'doctor_login' is the correct URL pattern

    return render(request, 'register.html')


def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def edit_doctor(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        s1 = request.POST['special']

        doctor.name = n1
        doctor.mobile = m1
        doctor.special = s1

        try:
            doctor.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_doctor.html', locals())

def add_patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        g = request.POST['gender']
        m = request.POST['mobile']
        a = request.POST['address']
        try:
            Patient.objects.create(name=n, gender=g, mobile=m, address=a)
            error = "no"
        except:
            error = "yes"
    return render(request,'add_patient.html', locals())

def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    # Fetch all doctors from the database
    doc = Doctor.objects.all()
    d = {'doc': doc}

    # Render the view_doctor page with the list of doctors
    return render(request, 'view_doctor.html', d)


from django.shortcuts import render, redirect
from .models import Patient  # Make sure to import the Patient model

from django.shortcuts import render, redirect

def view_patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request,'view_patient.html', d)



def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def edit_patient(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        g1 = request.POST['gender']
        a1 = request.POST['address']

        patient.name = n1
        patient.mobile = m1
        patient.gender = g1
        patient.address = a1
        try:
            patient.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_patient.html', locals())



def add_appointment(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method=='POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            Appointment.objects.create(doctor=doctor, patient=patient, date1=d1, time1=t)
            error="no"
        except:
            error="yes"
    d = {'doctor':doctor1,'patient':patient1,'error':error}
    return render(request,'add_appointment.html', d)

def view_appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.all()
    d = {'appointment':appointment}
    return render(request,'view_appointment.html', d)

def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment1 = Appointment.objects.get(id=pid)
    appointment1.delete()
    return redirect('view_appointment')

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

def patient_login(request):
    return render(request,'patient_login.html')


# views.py

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Doctor


def doctor_login(request):
    if request.method == "POST":
        name = request.POST.get('username')
        contact_number = request.POST.get('contact')

        try:
            # Check if a doctor with the given name and contact number exists
            doctor = Doctor.objects.get(name=name, mobile=contact_number)
            # Log the doctor in (set session, etc.)
            request.session['doctor_id'] = doctor.id  # Save doctor ID in session
            return redirect('doctor_home')  # Redirect to doctor home page after login
        except Doctor.DoesNotExist:
            # If the doctor doesn't exist, show an error message
            return render(request, 'doctor_login.html', {'error': 'yes'})

    return render(request, 'doctor_login.html')


from django.shortcuts import render, redirect
from .models import Doctor

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor


def doctor_registration(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        special = request.POST.get('special')

        # Basic validation (you can make this more advanced as needed)
        if not name or not mobile or not special:
            messages.error(request, "All fields are required.")
            return render(request, 'doctor_registration.html')

        try:
            # Create and save a new doctor record
            doctor = Doctor(name=name, mobile=mobile, special=special)
            doctor.save()

            # Display success message
            messages.success(request, 'Registration successful! Please log in.')

            # Redirect to doctor login page after successful registration
            return redirect('index')  # Change 'doctor_login' to the correct URL name
        except Exception as e:
            # In case of any errors, provide feedback
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'doctor_registration.html')

    # If GET request, just render the registration page
    return render(request, 'doctor_registration.html')

    # views.py

from django.shortcuts import render, redirect
from .models import Doctor, Patient, Appointment  # Import your models


def doctor_home(request):
    # Check if the doctor is logged in by verifying the session
    if not request.session.get('doctor_id'):
        return redirect('doctor_login')  # Redirect to doctor login if not logged in

    # Fetch counts from your models
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()

    # Prepare context with counts
    context = {
        'dc': doctor_count,  # Total Doctors
        'pc': patient_count,  # Total Patients
        'ac': appointment_count,  # Total Appointments
    }

    return render(request, 'doctor_home.html', context)

    # Logic for registering, can redirect to add_doctor
def doctor_list_view(request):
    # Fetch all doctors from the database
    doctors = Doctor.objects.all()
    context = {'doc': doctors}

    # Render the doctor_list template without edit/delete actions
    return render(request, 'doctor_list.html', context)

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Patient  # Assuming you have a Patient model

# Patient registration view
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient

def patient_registration(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        # Basic validation
        if not name or not mobile or not gender or not address:
            messages.error(request, "All fields are required.")
            return render(request, 'patient_registration.html')

        try:
            # Create and save a new patient record
            patient = Patient(name=name, mobile=mobile, gender=gender, address=address)
            patient.save()

            # Display success message
            messages.success(request, 'Registration successful!')

            # Redirect to the view patients page after successful registration
            return redirect('index')  # Ensure this URL name matches your URL config
        except Exception as e:
            # Handle errors
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'patient_registration.html')

    # If GET request, render the registration page
    return render(request, 'patient_registration.html')



