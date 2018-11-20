# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
# import mongoengine
from rest_framework import generics
from rest_framework.exceptions import ParseError
from rest_framework.utils import json

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

@csrf_exempt
@api_view(["POST"])
def logout(HttpRequest):
    try:
        HttpRequest.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    return Response({"success": "Successfully logged out."},
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

    # f = request.POST['image']
    # print(f)
    # mkimg.ImageURL.save(f.name, f, save=True)
    cropData = request.data["cropdata"]
    print(cropData)
    return Response({"success":"Image Successfully Uploaded","URL":"https://127.0.0.1:8000/"+up_file.name,"cropData":cropData,"Results":[
        {
            "ID":"1",
            "ImageURL":"data:image/png;base64,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",
            "CompanyName":"ABC",
            "Location":"Test Loc, Test",
            "FoundedIn":"1999"
        },
        {
            "ID": "2",
            "ImageURL": "http://webfeb.in/wp-content/uploads/2016/11/logo-design-for-it-company.jpg",
            "CompanyName": "DEF",
            "Location": "Test Loc, Test",
            "FoundedIn": "1999"
        },
        {
            "ID": "3",
            "ImageURL": "data:image/png;base64,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",
            "CompanyName": "GHI",
            "Location": "Test Loc, Test",
            "FoundedIn": "1999"
        }
        ,{
            "ID":"4",
            "ImageURL":"http://www.advertguru.co.zw/wp-content/uploads/2015/09/logo-designing-in-Harare-Zimbabwe.jpg",
            "CompanyName":"JKL",
            "Location":"Test Loc, Test",
            "FoundedIn":"1999"
        }
    ]},status=status.HTTP_201_CREATED)

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