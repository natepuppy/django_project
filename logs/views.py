from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Log
from .serializers import LogSerializer
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
    logs = Log.objects.all()
    serializer = LogSerializer(logs, many=True)
    return JsonResponse({
        'status': 'success',
        'message': 'Logs fetched successfully',
        'data': serializer.data
    })

def get_one(request, id):
    log = get_object_or_404(Log, id=id)
    serializer = LogSerializer(log)
    return JsonResponse({
        'status': 'success',
        'message': 'Log fetched successfully',
        'data': serializer.data
    })

def create(request):
    data = json.loads(request.body)
    serializer = LogSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Log created successfully',
            'data': serializer.data
        }, status=201)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Log creation failed',
            'errors': serializer.errors
        }, status=400)

def update(request, id):
    data = json.loads(request.body)
    log = get_object_or_404(Log, id=id)
    serializer = LogSerializer(log, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Log updated successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Log update failed',
            'errors': serializer.errors
        }, status=400)

def delete(request, id):
    log = get_object_or_404(Log, id=id)
    log.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Log deleted successfully'
    }, status=204)
