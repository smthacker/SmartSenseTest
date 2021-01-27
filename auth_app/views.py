from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.models import User
from auth_app.serializers import UserEmailExistsSerializer, UserSerializer, UserCreateSerializer, UserLoginSerializer


class UserEmailExixsts(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserEmailExistsSerializer
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        resp = {}
        try:
            data = request.data
            serializer = UserEmailExistsSerializer(data=data)

            if serializer.is_valid():
                # serializer.save()
                resp['status'] = True
                resp['message'] = 'Email existence checked Successfully'
                resp['data'] = serializer.data
                return Response(resp, status=status.HTTP_200_OK)
            else:
                resp['status'] = False
                resp['message'] = "User email already exists"
                return Response(resp, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            if 'unique constraint' in str(e):
                resp['status'] = False
                resp['message'] = "User email already exists"
            else:
                resp['status'] = False
                resp['message'] = 'Invalid data or email.'
            return Response(resp)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = ['title', 'first_name', 'last_name', 'email', 'isPaidUser', 'phone_number', 'profile_pic',
                            'bool_subscriptions_job', 'bool_relevant_info', 'education_name', 'language_name']
        return serializer_class(*args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        resp = {}
        try:
            response = super().retrieve(request, *args, **kwargs)
            if response.status_code in [200, 201]:
                resp['status'] = True
                resp['message'] = "User get detail Successfully"
                resp['data'] = response.data
            else:
                resp['status'] = False
                resp['message'] = response.detail
            return Response(resp)
        except Exception as e:
            print(str(e))
            resp['status'] = False
            resp['message'] = 'Invalid id or authentication not provided'
            return Response(resp)


class UserEdit(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = ['title', 'first_name', 'last_name', 'phone_number', 'profile_pic', 'bool_subscriptions_job',
                            'bool_relevant_info']
        return serializer_class(*args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        resp = {}
        try:
            response = super().update(request, *args, **kwargs)
            if response.status_code in [200, 201]:
                resp['status'] = True
                resp['message'] = "User Edited Successfully"
                resp['data'] = response.data
            else:
                resp['status'] = False
                resp['message'] = response.detail
            return Response(resp)
        except Exception as e:
            print(str(e))
            resp['status'] = False
            resp['message'] = 'Invalid data or id.'
            return Response(resp)

class UserCreate(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        resp = {}
        try:
            data = request.data
            serializer = UserCreateSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                resp['status'] = True
                resp['message'] = 'User created Successfully'
                resp['data'] = serializer.data
                return Response(resp, status=status.HTTP_200_OK)
            resp['status'] = False
            resp['message'] = serializer.errors
            return Response(resp, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():
                resp['status'] = False
                resp['message'] = "User alredy registered"
            else:
                resp['status'] = False
                resp['message'] = 'Invalid data or email.'
            return Response(resp)


class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            new_data = UserSerializer(user, fields = ['title', 'first_name', 'last_name', 'email', 'phone_number', 'profile_pic', 'bool_subscriptions_job', 'bool_relevant_info', 'isPaidUser']).data
            response = {
                'status' : True,
                'message': 'Logged in successfully',
                'data': [new_data]
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status':False,
            'message': 'Email or Password incorrect.'
        }
        return Response(response, status=status.HTTP_200_OK)


class UserLogout(APIView):
    def get(self, request):
        logout(request)
        response = {
            'stats' : True,
            'message': 'User logged out successfully',
            'data': []
        }
        return Response(response)