from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import viewsets
from bike_api.serializers import UserSerializer, GroupSerializer
# Create your views here.

# from django.shortcuts import render
from django.conf import settings
# from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import (
    Count,
    Q,
    When,
    Case,
    F,
    CharField,
    BooleanField,
    Sum,
    Max,
    Min,
    Value as V
)
from django.db.models.functions import Coalesce
from django.db.models.expressions import RawSQL
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.dateformat import DateFormat
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    GenericAPIView
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from bike_api.models import (
    Users,
    Bikes,
    Location,
    Zone
)
import arrow
import binascii
import base64
import datetime
import hmac
import hashlib
from itertools import groupby
import json
import math


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class Hello(ListCreateAPIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset = None
        return queryset

    def get(self, request):
        return Response(
            {
                'success': True,
                'message': 'Ceaules bulan!'
            },
            status=status.HTTP_200_OK
        )


class BikeRequest(ListCreateAPIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset = None
        return queryset

    def get(self, request):
        bike_id = request.query_params.get('bike_id', None)
        action = request.query_params.get('action', None)

        if bike_id is None or action is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        bike = Bikes.objects.filter(pk=bike_id).first()

        if bike is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if action == 'reserve':
            if bike.damaged is False:
                bike.free = False
                bike.save()
                message = 'reserved'
                success = True
            else:
                message = 'is damaged and cannot be reserved'
                success = False
        elif action == 'free':
            if bike.damaged is True:
                message = 'is damaged and cannot be made available'
                success = False
            else:
                bike.free = True
                bike.save()
                message = 'available'
                success = True
        elif action == 'damaged':
            bike.free = False
            bike.damaged = True
            bike.save()
            message = 'reported damaged'
            success = True

        return Response(
            {
                'success': success,
                'message': 'Bike %s %s.' % (bike.id, message)
            },
            status=status.HTTP_200_OK
        )

class BikesRequest(ListCreateAPIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset = None
        return queryset

    def get(self, request):
        longitude = request.query_params.get('longitude', None)
        latitude = request.query_params.get('latitude', None)

        if longitude is None or latitude is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        bikes = Bikes.objects.filter(location__point__distance_lt=(Point(float(latitude), float(longitude)),Distance(km=5))).values('id', 'location__point')

        if bikes is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_404_NOT_FOUND
            )

        for e in bikes:
            e['latitude'] = json.loads(e['location__point'].json)['coordinates'][0]
            e['longitude'] = json.loads(e['location__point'].json)['coordinates'][1]
            del e['location__point']

        return Response(
            {
                'success': True,
                'bikes': bikes
            },
            status=status.HTTP_200_OK
        )


class LocationRequest(ListCreateAPIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset = None
        return queryset

    def post(self, request):
        longitude = request.data.get('longitude', None)
        latitude = request.data.get('latitude', None)
        bike_id = request.data.get('bike_id', None)

        if longitude is None or latitude is None or bike_id is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        longitude = float(longitude)
        latitude = float(latitude)

        bike = Bikes.objects.filter(pk=bike_id).first()

        if bike is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_404_NOT_FOUND
            ) 
        
        location = bike.location
        location.point = Point(latitude, longitude)
        location.save()

        return Response(
            {
                'success': True
            },
            status=status.HTTP_200_OK
        )

        
class UserRequest(ListCreateAPIView):
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset = None
        return queryset

    def post(self, request):
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        telephone = request.data.get('telephone', None)
        email = request.data.get('email', None)

        if first_name is None or last_name is None or telephone is None or email is None:
            return Response(
                {
                    'success': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        user = Users.objects.create(
            first_name=first_name,
            last_name=last_name,
            telephone=telephone,
            email=email
        )

        return Response(
            {
                'user': user.uid
            },
            status=status.HTTP_200_OK
        )        
