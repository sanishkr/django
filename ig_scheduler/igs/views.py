# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
# import mongoengine
from rest_framework import generics
from rest_framework.exceptions import ParseError

from .models import *
# from rest_framework import serializers
from .serializers import IGUserSerializer, MKImgSerializer
from rest_framework.views import APIView
from rest_framework import  status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    # print(request.data)
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

def logout(self, request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    logout(request)

    return Response({"success": _("Successfully logged out.")},
                    status=status.HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
def imagesearch(request):
    print(request.data)
    if 'image' not in request.data:
        raise ParseError("Empty content")
    up_file = request.FILES['image']
    destination = open('./' + up_file.name, 'wb+')
    for chunk in up_file.chunks():
        destination.write(chunk)
        destination.close()

    # f = request.data['image']
    # mkimg.ImageURL.save(f.name, f, save=True)
    return Response(status=status.HTTP_201_CREATED)

class UserDetail(APIView):
    def get_queryset(self):
        return IGuser.objects.filter(owner=self.request.user)

    def get_object(self, pk, *args, **kwargs):
        try:
            return IGuser.objects.get(pk=pk)
        except IGuser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = IGUserSerializer(user)
        return Response(serializer.data)

class MKImgDetail(APIView):
    def get_queryset(self):

        return mkimg.objects.filter(owner=self.request.user)

    def get_object(self, pk, *args, **kwargs):
        try:
            return mkimg.objects.get(pk=pk)
        except mkimg.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # print "this is MKImgDetail"
        MKImg = self.get_object(pk)
        serializer = MKImgSerializer(MKImg)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        MKImg = self.get_object(pk)
        serializer = MKImgSerializer(MKImg, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        MKImg = self.get_object(pk)
        MKImg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# user = authenticate(username=username, password=password)
# assert isinstance(user, mongoengine.django.auth.User)
# def testview(request):
#     # connect('ig-scheduler')
#     iguser = IGuser(username='test@title.com', password='test content', image_url='/ubuntu/img/1.jpg', comment='#test comment', pub_date='2018-07-24 10:30')
#     iguser.save()
#     return HttpResponse("SAVED")
#
# class IGpostList(generics.ListCreateAPIView):
#     serializer_class = IGpostSerializer
#
#     def get_queryset(self):
#         return IGuser.objects
#
# class IGpostSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=144)
#     password = serializers.CharField(max_length=144)
#     image_url = serializers.CharField(max_length=144)
#     comment = serializers.CharField(max_length=144)
#     pub_date = serializers.DateTimeField(required=False)
#     body = serializers.CharField()
#
#     def restore_object(self, attrs, instance=None):
#         if instance is not None:
#             for k, v in attrs.iteritems():
#                 setattr(instance, k, v)
#             return instance
#         return IGuser(**attrs)