from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Prescription,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Notification,Prescription
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Doctor
# Doctor Home Page
def doctor_home(request):
    prescription = Prescription.objects.all().count()
    send_prscription_count = Prescription.objects.filter(prescription_status = 'Sending Successfully').count()
    context = {
        'prescription' : prescription,
        'send_prscription_count' : send_prscription_count
    }
    return render(request, 'doctor/dashboard/doctor-home.html', context)

# View all prescription
def view_all_prescription(request):
    prescription = Prescription.objects.exclude(prescription_status__in = ['Pending', 'Sending Successfully'])

    context = {
        'prescription' : prescription,
    }
    return render(request, 'doctor/prescription/view_all_prescription.html',context)

# View prescription detail
def view_prescription_details(request, prescription_id):
    prescription_detail = Prescription.objects.get(prescription_id = prescription_id)
    context = {
        'prescription_detail' : prescription_detail
    }
    return render(request, 'doctor/prescription/view_prescription_details.html', context)

# Manage got prescription
def view_got_prescriptions(request):
    prescription = Prescription.objects.filter(prescription_status = 'Pending' , prescription_message__isnull = False)
    context = {
        'prescription' : prescription
    }
    return render(request, 'doctor/prescription/view_got_prescriptions.html', context)

# Generate prescription page
def generate_prescription_page(request, prescription_id):
    prescription = Prescription.objects.get(prescription_id = prescription_id)
    context = {
        'prescription' : prescription,
    }
    return render(request, 'doctor/prescription/generate_prescription.html', context)

# Send Prescription
def send_prescription(request):
    if request.method == "POST":
        prescription_id = request.POST.get('prescription_id')
        prescription_img = request.FILES.get('prescription_img')

        prescription = Prescription.objects.get(prescription_id = prescription_id)

        prescription.prescription_img = prescription_img
        prescription.prescription_status = "Sending Successfully"
        prescription.save()


        email = EmailMessage(
            "Message To Medicine Masters",
            "Hello Dear " + prescription.user.username +" I am Send To Prescription As Per Your Request, Check And Submit To Your Order According...",
            'medicinemasters23@gmail.com',
            [prescription.user.email] 
        )
        with prescription.prescription_img.open('rb') as f:
            email.attach(prescription.prescription_img.name, f.read(), 'image/jpeg')
        email.send()

        context = {
            'prescription' : prescription,
        }
    return render(request, 'doctor/prescription/generate_prescription.html', context)