from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Action
from .serializers import ActionSerializer
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
    actions = Action.objects.all()
    serializer = ActionSerializer(actions, many=True)
    return JsonResponse({
        'status': 'success',
        'message': 'Actions fetched successfully',
        'data': serializer.data
    })

def get_one(request, id):
    action = get_object_or_404(Action, id=id)
    serializer = ActionSerializer(action)
    return JsonResponse({
        'status': 'success',
        'message': 'Action fetched successfully',
        'data': serializer.data
    })

def create(request):
    data = json.loads(request.body)
    serializer = ActionSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Action created successfully',
            'data': serializer.data
        }, status=201)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Action creation failed',
            'errors': serializer.errors
        }, status=400)

def update(request, id):
    data = json.loads(request.body)
    action = get_object_or_404(Action, id=id)
    serializer = ActionSerializer(action, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Action updated successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Action update failed',
            'errors': serializer.errors
        }, status=400)

def delete(request, id):
    action = get_object_or_404(Action, id=id)
    action.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Action deleted successfully'
    }, status=204)
