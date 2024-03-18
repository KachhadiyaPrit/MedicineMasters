from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Prescription,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Notification,Prescription_Detail
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Doctor
# Doctor Home Page
@login_required(login_url='login_page')
def doctor_home(request):
    prescription = Prescription.objects.all().count()
    send_prscription_count = Prescription_Detail.objects.filter(prescription_status = 'Sending Successfully').count()
    approve_prscription_count = Prescription_Detail.objects.filter(prescription_status = 'Approve').count()
    context = {
        'prescription' : prescription,
        'send_prscription_count' : send_prscription_count,
        'approve_prscription_count' : approve_prscription_count
    }
    return render(request, 'doctor/dashboard/doctor-home.html', context)

# View all prescription
@login_required(login_url='login_page')
def view_all_prescription(request):
    prescription = Prescription.objects.all()

    context = {
        'prescription' : prescription,
    }
    return render(request, 'doctor/prescription/view_all_prescription.html',context)

# View prescription detail
@login_required(login_url='login_page')
def view_prescription_details(request, prescription_id):
    prescription = Prescription.objects.get(prescription_id = prescription_id)
    prescription_detail = Prescription_Detail.objects.filter(prescription_id = prescription_id)
    context = {
        'prescription_detail' : prescription_detail,
        'prescription' : prescription
    }
    return render(request, 'doctor/prescription/view_prescription_details.html', context)

# Manage got prescription
@login_required(login_url='login_page')
def view_got_prescriptions(request):
    prescription = Prescription_Detail.objects.filter(prescription_status = 'Pending' , prescription_message__isnull = False)
    context = {
        'prescription' : prescription
    }
    return render(request, 'doctor/prescription/view_got_prescriptions.html', context)

# Generate prescription page
@login_required(login_url='login_page')
def generate_prescription_page(request, prescription_detail_id):
    prescription = Prescription_Detail.objects.get(prescription_detail_id = prescription_detail_id)
    context = {
        'prescription' : prescription,
    }
    return render(request, 'doctor/prescription/generate_prescription.html', context)

# Send Prescription
@login_required(login_url='login_page')
def send_prescription(request):
    if request.method == "POST":
        prescription_detail_id = request.POST.get('prescription_detail_id')
        prescription_id = request.POST.get('prescription_id')
        prescription_img = request.FILES.get('prescription_img')

        prescription_detail = Prescription_Detail.objects.get(prescription_detail_id = prescription_detail_id)
        prescription = Prescription.objects.get(prescription_id = prescription_id)

        prescription.prescription_img = prescription_img
        prescription.save()

        prescription_detail.prescription_status = "Sending Successfully"
        prescription_detail.save()

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

# Approve Prescription
@login_required(login_url='login_page')
def approve_prescription(request, prescription_id ,prescription_detail_id):
    prescription = Prescription.objects.get(prescription_id = prescription_id)
    prescription_detail = Prescription_Detail.objects.filter(prescription_id = prescription_id)
    prescription_detail_approve = Prescription_Detail.objects.get(prescription_detail_id = prescription_detail_id)

    prescription_detail_approve.prescription_status = 'Approve'
    prescription_detail_approve.save()

    context = {
        'prescription_detail' : prescription_detail,
        'prescription' : prescription,
    }
    
    return render(request, 'doctor/prescription/view_prescription_details.html', context)

# Reject Prescription
@login_required(login_url='login_page')
def reject_prescription(request, prescription_id, prescription_detail_id):
    prescription = Prescription.objects.get(prescription_id = prescription_id)
    prescription_detail = Prescription_Detail.objects.filter(prescription_id = prescription_id)
    prescription_detail_approve = Prescription_Detail.objects.get(prescription_detail_id = prescription_detail_id)

    prescription_detail_approve.prescription_status = 'Reject'
    prescription_detail_approve.save()

    context = {
        'prescription_detail' : prescription_detail
    }
    return render(request, 'doctor/prescription/view_prescription_details.html', context)
