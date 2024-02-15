from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from medicine_masters.models import Users,DeliveryAddress,Prescription,Category,Sub_Category,Company,Product,Offer,Order,Order_Detail,Notification,Prescription
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa

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

def generate(request):
    if request.method == 'POST':
        medicine1_name = request.POST.get('medicine1_name')
        medicine1_quantity = request.POST.get('medicine1_quantity')
        medicine1_time = request.POST.get('medicine1_time')

        medicine2_name = request.POST.get('medicine2_name')
        medicine2_quantity = request.POST.get('medicine2_quantity')
        medicine2_time = request.POST.get('medicine2_time')

        medicine3_name = request.POST.get('medicine3_name')
        medicine3_quantity = request.POST.get('medicine3_quantity')
        medicine3_time = request.POST.get('medicine3_time')

        medicine4_name = request.POST.get('medicine4_name')
        medicine4_quantity = request.POST.get('medicine4_quantity')
        medicine4_time = request.POST.get('medicine4_time')

        medicine5_name = request.POST.get('medicine5_name')
        medicine5_quantity = request.POST.get('medicine5_quantity')
        medicine5_time = request.POST.get('medicine5_time')

        template_path = 'doctor/prescription/pdfgenerate.html'
        context = {
            'medicine1_name': medicine1_name,
            'medicine1_quantity': medicine1_quantity,
            'medicine1_time': medicine1_time,
            'medicine2_name': medicine2_name,
            'medicine2_quantity': medicine2_quantity,
            'medicine2_time': medicine2_time,
            'medicine3_name': medicine3_name,
            'medicine3_quantity': medicine3_quantity,
            'medicine3_time': medicine3_time,
            'medicine4_name': medicine4_name,
            'medicine4_quantity': medicine4_quantity,
            'medicine4_time': medicine4_time,
            'medicine5_name': medicine5_name,
            'medicine5_quantity': medicine5_quantity,
            'medicine5_time': medicine5_time,
        }
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Prescription.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

    return render(request, 'doctor/prescription/generate_prescription.html')