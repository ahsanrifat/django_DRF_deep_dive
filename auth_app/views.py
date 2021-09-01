from auth_app.models import User
from django.http.response import JsonResponse
from rest_framework.views import APIView
from .serializers import UserSerializer, TokenUserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt, datetime
from django.views.generic.list import ListView


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("Authentication Error")
        if not user.check_password(password):
            raise AuthenticationFailed("Authentication Error")
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, "23hhjbjh323676shdhs", algorithm="HS256")
        response = Response()
        response.set_cookie(key="token", value=token, httponly=True)
        response.data = {"token": token}
        return response

    def get(self, request):
        token = request.COOKIES.get("token")
        if not token:
            raise AuthenticationFailed("Unauthenticated token")
        try:
            payload = jwt.decode(token, "23hhjbjh323676shdhs", algorithms="HS256")
        except Exception as e:
            raise AuthenticationFailed("Unauthenticated payload")
        user = User.objects.filter(id=payload["id"]).first()
        serializer = TokenUserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie("token")
        response.data = {"message": "success"}
        return response


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({"message": True})
        except Exception as e:
            return Response({"message": False})


class ListViewExample(ListView):
    model = User
    template_name = "auth_app/user_list.html"

    def get_queryset(self):
        return User.objects.filter(is_superuser=False)
