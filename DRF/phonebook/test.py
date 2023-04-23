from django.urls import include, path, reverse
from django.test import TestCase
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from phonebook.models import Phonebook,User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json

class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include('phonebook.urls')),
    ]

    
    def test_register(self):
        url = reverse("register")
        obj = User.objects.count()
        if obj == 0:
            data = {
                "username": "Abhishek",
                "email": "admin@gmail.com",
                "password": "abhi2410"
            }
            resp = self.client.post(url,data=data,format="json")
            self.assertEqual(resp.status_code,status.HTTP_201_CREATED)
        else:
            pass
    
    def test_login(self):
        self.test_register()
        url = reverse("login")
        data = {
            "username": "Abhishek",
            "password": "abhi2410"
        }
        resp = self.client.post(url,data = data,format="json")
        self.assertEqual(resp.status_code,status.HTTP_200_OK)
        return resp.data
        

    def test_phonbook_list(self,testcases = 0):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        url = reverse('list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url,format = "json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), testcases)
    
    def test_phonebook_add(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('add')
        count = 1
        name = ["Bruce Schneier","Schneier, Bruce","Schneier, Bruce Wayne","O’Malley, John F.","John O’Malley-Smith","Cher","Abhishek G. Patel","Thomas L. Jones","Lam"]
        phonenumber = ["12345","(703)111-2121","123-1234","+1(703)111-2121","+32 (21) 212-2324","1(703)123-1234","011 701 111 1234","12345.12345","011 1 703 111 1234"]
        for i in range(len(name)):
            response = self.client.post(url,data={"name":name[i],"phone_number":phonenumber[i]},format = "json")
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.test_phonbook_list(testcases=count)
            count += 1

    def test_phonebook_deletebyName(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.test_phonebook_add()
        url = reverse('deletebyName')
        obj = Phonebook.objects.count()
        name = ["Bruce Schneier","Schneier, Bruce","Schneier, Bruce Wayne","O’Malley, John F.","John O’Malley-Smith","Cher","Abhishek G. Patel","Thomas L. Jones","Lam"]
        for i in range(len(name)):
            response = self.client.put(url,data={"name":name[i]},format = "json")
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            self.test_phonbook_list(testcases=obj-i-1)

    def test_phonebook_deletebyNumber(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.test_phonebook_add()
        url = reverse('deletebyNumber')
        obj = Phonebook.objects.count()
        phonenumber = ["12345","(703)111-2121","123-1234","+1(703)111-2121","+32 (21) 212-2324","1(703)123-1234","011 701 111 1234","12345.12345","011 1 703 111 1234"]
        for i in range(len(phonenumber)):
            response = self.client.put(url,data={"phone_number":phonenumber[i]},format = "json")
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            self.test_phonbook_list(testcases=obj-i-1)
    
    def test_phonebook_invalid_name_add(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('add')
        name = ["Ron O’’Henry","Ron O’Henry-Smith-Barnes","L33t Hacker","<Script>alert(“XSS”)</Script>","Brad Everett Samuel Smith","select * from users"]
        phonenumber= ["12345","(703)111-2121","123-1234","+1(703)111-2121","+32 (21) 212-2324","1(703)123-1234"]
        for i in range(len(name)):
            response = self.client.post(url,data={"name":name[i],"phone_number":phonenumber[i]},format = "json")
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.test_phonbook_list(testcases=0)

    def test_phonebook_invalid_number_add(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('add')
        name = ["Bruce Schneier","Schneier, Bruce","Schneier, Bruce Wayne","O’Malley, John F.","John O’Malley-Smith","Cher","Abhishek G. Patel","Thomas L. Jones","Lam"]
        phonenumber = ["123","1/703/123/1234","Nr 102-123-1234","<script>alert(“XSS”)</script>","7031111234","+1234 (201) 123-1234","+01 (703) 123-1234","(703) 123-1234 ext 204","(001) 123-1234"]
        for i in range(len(name)):
            response = self.client.post(url,data={"name":name[i],"phone_number":phonenumber[i]},format = "json")
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.test_phonbook_list(testcases=0)


    ## Json based testing 

    def test_phonebook_add_json(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('add')
        count = 1
        file = open("./testdata/add.json","r")
        data = list(json.load(file).items())[0][1]
        for item in data:
            response = self.client.post(url,data=item,format = "json")
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.test_phonbook_list(testcases=count)
            count += 1

    def test_phonebook_deletebyName_json(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.test_phonebook_add_json()
        url = reverse('deletebyName')
        obj = Phonebook.objects.count()
        file = open("./testdata/deletebyname.json","r")
        data = list(json.load(file).items())[0][1]
        for i,item in enumerate(data):
            response = self.client.put(url,data=item,format = "json")
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            self.test_phonbook_list(testcases=obj-i-1)

    def test_phonebook_deletebyNumber_json(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.test_phonebook_add_json()
        url = reverse('deletebyNumber')
        obj = Phonebook.objects.count()
        file = open("./testdata/deletebynumber.json","r")
        data = list(json.load(file).items())[0][1]
        for i,item in enumerate(data):
            response = self.client.put(url,data=item,format = "json")
            self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
            self.test_phonbook_list(testcases=obj-i-1)
    
    def test_phonebook_invalid_name_add_json(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('add')
        file = open("./testdata/invalidname.json","r")
        data = list(json.load(file).items())[0][1]
        for item in data:
            response = self.client.post(url,data=item,format = "json")
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.test_phonbook_list(testcases=0)

    def test_phonebook_invalid_number_add_json(self):
        resp = self.test_login()
        token = resp.get("tokens").get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('add')
        file = open("./testdata/invalidnumber.json","r")
        data = list(json.load(file).items())[0][1]
        for item in data:
            response = self.client.post(url,data=item,format = "json")
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.test_phonbook_list(testcases=0)