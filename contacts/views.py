from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Contact
from .serializers import ContactSerializer
import json

@login_required
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "GET":
        return get_many(request)
    elif request.method == "POST":
        return create(request)

@login_required
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def show(request, id):
    if request.method == "GET":
        return get_one(request, id)
    elif request.method in ["PUT", "PATCH"]:
        return update(request, id)
    elif request.method == "DELETE":
        return delete(request, id)

def get_many(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    return JsonResponse({
        'status': 'success',
        'message': 'Contacts fetched successfully',
        'data': serializer.data
    })

def get_one(request, id):
    contact = get_object_or_404(Contact, id=id)
    serializer = ContactSerializer(contact)
    return JsonResponse({
        'status': 'success',
        'message': 'Contact fetched successfully',
        'data': serializer.data
    })

def create(request):
    data = json.loads(request.body)
    serializer = ContactSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Contact created successfully',
            'data': serializer.data
        }, status=201)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Contact creation failed',
            'errors': serializer.errors
        }, status=400)

def update(request, id):
    data = json.loads(request.body)
    contact = get_object_or_404(Contact, id=id)
    serializer = ContactSerializer(contact, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Contact updated successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Contact update failed',
            'errors': serializer.errors
        }, status=400)

def delete(request, id):
    contact = get_object_or_404(Contact, id=id)
    contact.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Contact deleted successfully'
    }, status=204)
