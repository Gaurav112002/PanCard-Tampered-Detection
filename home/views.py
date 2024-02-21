from django.shortcuts import render, HttpResponse
from home.models import Insert
from datetime import datetime
from django.contrib import messages
from .model import predict
from PIL import Image
import os

# Create your views here.
def index(request):
    allowed_ext = {'.pdf', '.png', '.jpg', '.jpeg'}

    if request.method == 'POST':
        img = request.FILES.get('image')
        _, file_extension = os.path.splitext(img.name.lower())

        if file_extension in allowed_ext:
            output = predict(img)
            score = output * 100
            output = 450 - 450 * output
            objName = 'obj_img1'
            objImage = f'/static/{objName}.png'

            diffName = 'diff_img1'
            diffImage = f'/static/{diffName}.png'
                
            context = {
                'score': score,
                'output': output,
                'obj_img': objImage,
                'diff_img': diffImage,
            }
            return render(request, 'index.html', context)
        
        else:
            context = {
                'str': 'Please select pdf or image only.',
            }
            return render(request, 'index.html', context)

    return render(request, 'index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ins = Insert(name=name, email=email, subject=subject, message=message, date=datetime.today())
        ins.save()
        messages.success(request, ' Message send successfully. Thanks to contact us and don\'t hesitate to send message us.')

    return render(request, 'contact.html')

def about(request):
    return HttpResponse('This is about page.')