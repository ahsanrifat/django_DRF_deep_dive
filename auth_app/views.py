from auth_app.models import User
from django.http.response import JsonResponse
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


class LoginView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("Authentication Error")
        if not user.check_password(password):
            raise AuthenticationFailed("Authentication Error")
        return Response({"message":True})
    
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