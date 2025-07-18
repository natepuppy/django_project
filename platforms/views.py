from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Platform
from .serializers import PlatformSerializer
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
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, many=True)
    return JsonResponse({
        'status': 'success',
        'message': 'Platforms fetched successfully',
        'data': serializer.data
    })

def get_one(request, id):
    platform = get_object_or_404(Platform, id=id)
    serializer = PlatformSerializer(platform)
    return JsonResponse({
        'status': 'success',
        'message': 'Platform fetched successfully',
        'data': serializer.data
    })

def create(request):
    data = json.loads(request.body)
    serializer = PlatformSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Platform created successfully',
            'data': serializer.data
        }, status=201)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Platform creation failed',
            'errors': serializer.errors
        }, status=400)

def update(request, id):
    data = json.loads(request.body)
    platform = get_object_or_404(Platform, id=id)
    serializer = PlatformSerializer(platform, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Platform updated successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Platform update failed',
            'errors': serializer.errors
        }, status=400)

def delete(request, id):
    platform = get_object_or_404(Platform, id=id)
    platform.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Platform deleted successfully'
    }, status=204)
