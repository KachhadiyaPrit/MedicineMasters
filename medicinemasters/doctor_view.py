from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Prescription,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Notification,Prescription
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from io import BytesIO

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
        prescription.prescription_status = "Pending"
        prescription.save()

        img_data = BytesIO(prescription_img.read())

        email = EmailMultiAlternatives(
            "Message To Medicine Masters",
            "Hello Dear " + prescription.user.username +" I am Send To Prescription As Per Your Request, Check And Submit To Your Order According..."
            'medicinemasters23@gmail.com',
            [prescription.user.email] 
        )
        html_content = render_to_string('doctor/prescription/email_template.html', {'prescription': prescription})
        email.send()

        context = {
            'prescription' : prescription,
        }
    return render(request, 'doctor/prescription/generate_prescription.html', context)