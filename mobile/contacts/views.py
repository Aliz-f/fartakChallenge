from ast import Return
from os import umask
import stat
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import contact
from .serializer import contactSerializer
from rest_framework import status

# Create your views here.
class contactlist(APIView):
    def get(self, request):
        contacts = contact.objects.all()
        serializer = contactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = contactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class contactDetail(APIView):
    def get_object(self, id):
        try:
            return contact.objects.get(id=id)
        except Exception as e:
            return Response({"ERROR": str(e)}, status= status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            contactQ = self.get_object(id)
            serializer = contactSerializer(contactQ)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id):
        try:
            contactQ = self.get_object(id)
            serializerUpdate = contactSerializer(contactQ, data=request.data)
            if serializerUpdate.is_valid():
                serializerUpdate.save()
                return Response(serializerUpdate.data, status= status.HTTP_202_ACCEPTED)
            return Response(serializerUpdate.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            contactQ = self.get_object(id)
            contactQ.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response ({'Error': str(e)}, status=status.HTTP_404_NOT_FOUND)
