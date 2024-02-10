from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Prescription,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Notification,Prescription
from django.core.mail import send_mail

# Doctor
# Doctor Home Page
def doctor_home(request):
    prescription = Prescription.objects.all().count()
    context = {
        'prescription' : prescription
    }
    return render(request, 'doctor/dashboard/doctor-home.html', context)

# View all prescription
def view_all_prescription(request):
    return render(request, 'doctor/prescription/view_all_prescription.html')

# View prescription detail
def view_prescription_details(request, prescription_id):
    return render(request, 'doctor/prescription/view_prescription_details.html')

# Manage got prescription
def view_got_prescriptions(request):
    prescription = Prescription.objects.filter(prescription_status = 'Pending')
    context = {
        'prescription' : prescription
    }
    return render(request, 'doctor/prescription/view_got_prescriptions.html', context)

# Generate prescription page
def generate_prescription_page(request, prescription_id):
    prescription = Prescription.objects.get(prescription_id = prescription_id)
    context = {
        'prescription' : prescription
    }
    return render(request, 'doctor/prescription/generate_prescription.html', context)