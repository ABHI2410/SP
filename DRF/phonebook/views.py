from .serializers import PhonebookSerializer
from .models import Phonebook
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,status,views,permissions
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from .serializers import RegisterSerializer,LoginSerializer,LogoutSerializer
import re
from django.http import HttpResponseRedirect
import logging
from ipware import get_client_ip

logger = logging.getLogger(__name__)
logger_django = logging.getLogger('django')
logger = logging.getLogger('phonebook')

class RegisterView(generics.GenericAPIView):
    permission_classes =()
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        logger.info(f"{request.user} registered")
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    permission_classes = ()
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.info(f"{request.user} loged in")
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    print("get request to logout")
    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"{request.user} loged out")
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def redirecttologin(request):
    if request.user == AnonymousUser:
        return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("list"))


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication,JWTAuthentication])
@permission_classes([IsAuthenticated])
def list(request):
    queryset = Phonebook.objects.all()
    serializer = PhonebookSerializer(queryset, many=True)
    CLIENT = get_client_ip(request)[0]
    logger.info(f"{CLIENT} {request.user} viewed the phonbook")
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def add(request):
    CLIENT = get_client_ip(request)[0]
    def nameValidator(name):
        if name.isalpha():
            return True
        else:
            pattern = "^(?!.*\s{2})(?!.*[-,.’]{2,})[a-zA-Z’'\-,\.]+(?:\s[a-zA-Z’'\-,\.]+){0,2}$"
            if re.match(pattern,name) is not None:
                if name.count("'")>1 or name.count("-")>1 or name.count(",")>1 or name.count(".")>1:
                    return False
                else:
                    return True
            else:
                return False
    def numberValidator(number):
        if any(char.isalpha() for char in number):
            return False
        elif number.isnumeric() and len(number)>5:
            return False
        else:
            pattern = "^(?:(?:\+?(?!0)\d{1,3}[\s.-]?)?(?:\(\d{2,3}\)|\d{2,3})[\s.-]?\d{3,4}[\s.-]?\d{4})|(?:\d{3}(-)?\d{4})|(\d{5})$"
            if re.match(pattern,number) is not None:
                matches =  "".join(re.findall(r'\d+', number))
                if int(matches[0]) == 0 and int(matches[1]) == 0:
                    return False
                else:
                    return True
            else:
                pattern = "^(?:(?:\+?(?!0)\d{1,3}[\s.-]?)|(?:\(\d{1,3}\)[\s.-]?))?(?:\d[\s.-]?){7,14}\d$"
                if re.match(pattern,number) is not None:
                    return True
                else:
                    return False
    serializer = PhonebookSerializer(data=request.data)
    if serializer.is_valid():
        name = request.data["name"]
        ph_no = request.data["phone_number"]
        validate_name = nameValidator(request.data["name"])
        validate_number = numberValidator(request.data["phone_number"])
        # print(validate_name,validate_number)
        if validate_name and validate_number:
            serializer.save()
            logger.info(f"{CLIENT} {request.user} added {name} to the phonbook")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if validate_name is False and validate_number is False:
                logger.warning(f"{CLIENT} {request.user} tried added invalid entries({name} and {ph_no}) to the phonbook")
                return Response("Invalid Name and Phone Number Provided",status=status.HTTP_400_BAD_REQUEST)
            elif validate_number is False:
                logger.warning(f"{CLIENT} {request.user} tried added invalid entries({ph_no}) to the phonbook")
                return Response("Invalid Phone Number Provided",status=status.HTTP_400_BAD_REQUEST)
            elif validate_name is False:
                logger.warning(f"{CLIENT} {request.user} tried added invalid entries({name}) to the phonbook")
                return Response("Invalid Name Provided",status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error("Unexpected Error Occured")
                return Response("Unexpected Error Occured Try again Later", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    logger.error(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def deleteByName(request):
    try:
        CLIENT = get_client_ip(request)[0]
        val = request.data["name"]
        Phonebook.objects.filter(name = val).delete()
        logger.info(f"{CLIENT} {request.user} removed {val} to the phonbook")
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Internal Server error {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def deleteByNunber(request):
    CLIENT = get_client_ip(request)[0]
    val = request.data["phone_number"]
    obj = Phonebook.objects.get(phone_number = val)
    try:
        Phonebook.objects.get(phone_number = val).delete()
        logger.info(f"{CLIENT} {request.user} removed {obj.name} to the phonbook")
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Internal Server error {e}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    



# ["12345","(703)111-2121","123-1234","+1(703)111-2121","+32 (21) 212-2324","1(703)123-1234","011 701 111 1234","12345.12345","011 1 703 111 1234","123","1/703/123/1234","Nr 102-123-1234","<script>alert(“XSS”)</script>","7031111234","+1234 (201) 123-1234","(001) 123-1234","+01 (703) 123-1234","(703) 123-1234 ext 204"]