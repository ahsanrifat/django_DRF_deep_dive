from auth_app.models import User
from django.http.response import JsonResponse
from auth_app.managers import UserManager
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class UserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    def put(self,request,id):
        user=User.objects.get(id=id)
        serializer = UserSerializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,id):
        try:
            user=User.objects.get(id=id)
            user.delete()
            return Response({"message":True})
        except Exception as e:
            return Response({"message":False})