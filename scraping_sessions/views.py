from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Session
from .serializers import SessionSerializer
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
    sessions = Session.objects.all()
    serializer = SessionSerializer(sessions, many=True)
    return JsonResponse({
        'status': 'success',
        'message': 'Sessions fetched successfully',
        'data': serializer.data
    })

def get_one(request, id):
    session = get_object_or_404(Session, id=id)
    serializer = SessionSerializer(session)
    return JsonResponse({
        'status': 'success',
        'message': 'Session fetched successfully',
        'data': serializer.data
    })

def create(request):
    data = json.loads(request.body)
    serializer = SessionSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Session created successfully',
            'data': serializer.data
        }, status=201)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Session creation failed',
            'errors': serializer.errors
        }, status=400)

def update(request, id):
    data = json.loads(request.body)
    session = get_object_or_404(Session, id=id)
    serializer = SessionSerializer(session, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Session updated successfully',
            'data': serializer.data
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Session update failed',
            'errors': serializer.errors
        }, status=400)

def delete(request, id):
    session = get_object_or_404(Session, id=id)
    session.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Session deleted successfully'
    }, status=204)
