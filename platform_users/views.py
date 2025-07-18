from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PlatformUser
from .serializers import PlatformUserSerializer
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
    platform_users = PlatformUser.objects.all()
    serializer = PlatformUserSerializer(platform_users, many=True)
    return JsonResponse({
        'status': 'success',
        'message': 'Platform users fetched successfully',
        'data': serializer.data
    })

def get_one(request, id):
    platform_user = get_object_or_404(PlatformUser, id=id)
    serializer = PlatformUserSerializer(platform_user)
    return JsonResponse({
        'status': 'success',
        'message': 'Platform user fetched successfully',
        'data': serializer.data
    })

def create(request):
    data = json.loads(request.body)
    serializer = PlatformUserSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Platform user created successfully',
            'data': serializer.data
        }, status=201)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Platform user creation failed',
            'errors': serializer.errors
        }, status=400)

def update(request, id):
    data = json.loads(request.body)
    platform_user = get_object_or_404(PlatformUser, id=id)
    serializer = PlatformUserSerializer(platform_user, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Platform user updated successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Platform user update failed',
            'errors': serializer.errors
        }, status=400)

def delete(request, id):
    platform_user = get_object_or_404(PlatformUser, id=id)
    platform_user.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Platform user deleted successfully'
    }, status=204)
