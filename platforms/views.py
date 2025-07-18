from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Platform
from .serializers import PlatformSerializer
import json


@require_http_methods(["GET"])
def index(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, many=True)

    return JsonResponse({
        'status': 'success',
        'message': 'Platforms fetched successfully',
        'data': serializer.data
    })

@require_http_methods(["GET"])
def show(request, id):
    platform = get_object_or_404(Platform, id=id)
    serializer = PlatformSerializer(platform)

    return JsonResponse({
        'status': 'success',
        'message': 'Platform fetched successfully',
        'data': serializer.data
    })

@require_http_methods(["POST"])
def create(request):
    data = json.loads(request.body)
    serializer = PlatformSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Platform created successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Platform creation failed',
            'errors': serializer.errors
        }, status=400)

@require_http_methods(["PUT", "PATCH"])
def update(request, id):
    data = json.loads(request.body)
    platform = get_object_or_404(Platform, id=id)

    serializer = PlatformSerializer(platform, data=data)

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

@require_http_methods(["DELETE"])
def delete(request, id):
    platform = get_object_or_404(Platform, id=id)
    platform.delete()

    return JsonResponse({
        'status': 'success',
        'message': 'Platform deleted successfully'
    })
