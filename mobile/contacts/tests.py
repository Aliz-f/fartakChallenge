import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .serializer import contactSerializer
from .models import contact

# Create your tests here.
class contactTestcase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username', password='password')
        self.contact1 = contact.objects.create(user = self.user, firstName='fname1', lastName='lname1', number='09131170825')
        self.contact2 = contact.objects.create(user = self.user, firstName='fname2', lastName='lname2', number='09131170826')
        self.validContactUpdate = {
            'firstName': 'update',
            'lastName':'update',
            'number': '09131170825',
            'note': None,
            'address': None,
            'birthDate' : None
        }
        self.inValidContact = {
            'firstName': 'invalid',
            'lastName':'invalid',
            'number': '091311708259888888',
            'note': None,
            'address': None,
            'birthDate' : None
        }
        self.validContact = {
            'firstName': 'create',
            'lastName':'create',
            'number': '09131170823',
            'note': None,
            'address': None,
            'birthDate' : None
        }
        self.inValidContact = {
            'firstName': 'create',
            'lastName':'create',
            'number': '091311708237777777',
            'note': None,
            'address': None,
            'birthDate' : None
        }
    
    def testValid_getAllContacts(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(reverse('contact-get'))
        contacts = contact.objects.all()
        serializer = contactSerializer(contacts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testValid_getSingleContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
                reverse('contact-id', kwargs={'id': self.contact1.id}))
        contacts = contact.objects.get(id=self.contact1.id)
        serializer = contactSerializer(contacts)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testInValid_getSingleContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
                reverse('contact-id', kwargs={'id': 85}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    def testValid_updateContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
                reverse('contact-id', kwargs = {'id': self.contact1.id}), 
                data=json.dumps(self.validContactUpdate), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
    def testInValid_updateContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
                reverse('contact-id', kwargs = {'id': self.contact1.id}), 
                data=json.dumps(self.inValidContact), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testValid_createContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('contact-get'), data =json.dumps(self.validContact),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testInValid_createContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            reverse('contact-get'), data =json.dumps(self.inValidContact),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testValid_deleteContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(
                reverse('contact-id', kwargs={'id': self.contact1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testInValid_deleteContact(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(
                reverse('contact-id', kwargs={'id': 85}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)