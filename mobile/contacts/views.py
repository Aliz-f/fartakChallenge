from os import umask
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import contact
from .serializer import contactSerializer
from rest_framework import status

# Create your views here.
class contactlist(APIView):
    def get(self, request):
        contacts = contact.objects.all()
        print(contacts)
        serializer = contactSerializer(contacts, many=True)
        print(serializer)
        return Response(serializer.data)

    def post(self, request):
        serializer = contactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class contactDetail(APIView):
    def get_object(self, id):
        try:
            contactQ = contact.objects.get(id=id)
            return contactQ
        except Exception as e:
            return Response({"ERROR": str(e)}, status= status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        contactQ = self.get_object(id)
        serializer = contactSerializer(contactQ)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def put(self, request, id):
        contactQ = self.get_object(id)
        serializer = contactSerializer(contactQ)
        serializerUpdate = contactSerializer(serializer, data=request.data)
        if serializerUpdate.is_valid():
            serializerUpdate.save()
            return Response(serializerUpdate.data, status= status.HTTP_202_ACCEPTED)
        return Response(serializerUpdate.errors, status = status.HTTP_400_BAD_REQUEST)
        