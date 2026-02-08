from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Person
from home.serializer import PersonSerializer,RegisterSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination


@api_view(['GET','POST','PUT','DELETE'])
def index(request):
    if request.method=='GET':
        people_detail={
            'name':'Rishan',
            'age':26,
            'job':'Developer'
        }
        return Response(people_detail)
    
    elif request.method=='POST':
        return Response('This is post method')
    elif request.method=='PUT':
        return Response('This is put method')
     
    elif request.method=='DELETE':
        return Response('This is DELETE method')
    

#function based api      i also did code for permission


@api_view(['GET','POST','PUT','PATCH','DELETE'])


@authentication_classes([TokenAuthentication]) #-----------------------------
@permission_classes([IsAuthenticated])          #---------------------------

def person(request):
    if request.method=='GET':
        objPerson=Person.objects.filter(team__isnull=False)
        serializer=PersonSerializer(objPerson,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        data=request.data
        serializer=PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='PUT':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PersonSerializer(obj,data=data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method=='PATCH':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PersonSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'messege':'person delete'})



#to study -- to get persons of particular team
@api_view(['GET'])
def persons_by_team(request, team_id):
    persons = Person.objects.filter(team_id=team_id)
    serializer = PersonSerializer(persons, many=True)
    return Response(serializer.data)

     


#class based api(APIView)      ----- here permission also done here

class ClassPerson(APIView):

    permission_classes=[IsAuthenticated]                 #------------
    authentication_classes=[TokenAuthentication]         #------------
      
    def get(self,request):
        objPerson=Person.objects.filter(team__isnull=False)
        serializer=PersonSerializer(objPerson,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        return Response('this is post')
        # data=request.data
        # serializer=PersonSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors)
    
    def patch(self,request):
        return Response('this is patch')


#ModelViewSet

# class PersonViewSets(viewsets.ModelViewSet):
#     serializer_class=PersonSerializer
#     queryset=Person.objects.all()

#     #---------just filtering----------
#     def list(self,request):
#         search=request.GET.get("search")
#         queryset=self.queryset

#         if search:
#             queryset=queryset.filter(name__startswith=search)
#         serializer=PersonSerializer(queryset,many=True)
#         return Response({'status':200,'data':serializer.data})
    


#custom class for pagination

class CustomPagination(PageNumberPagination):
    page_size=3
    page_query_param='page'


# PAGINATION   ModelViewSet
class PersonViewSets(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    serializer_class=PersonSerializer
    queryset=Person.objects.all()
    pagination_class=CustomPagination

    def list(self,request):
        search=request.GET.get("search")
        queryset=self.queryset

        if search:
            queryset=queryset.filter(name__startswith=search)

        #paginate queryset
        paginated_queryset=self.paginate_queryset(queryset)

        #he paginated querysetserialize t
        serializer=PersonSerializer(paginated_queryset,many=True)

        #return the paginated ewsponse
        return self.get_paginated_response(serializer.data)



#authencation

class RegisterAPI(APIView):
    def post(self,request):
        _data=request.data
        serializer=RegisterSerializer(data=_data)

        if not serializer.is_valid():
            return Response({'message':serializer.errors},status=status.HTTP_404_NOT_FOUND)
        
        serializer.save()
        return Response({'message':'user created'},status=status.HTTP_201_CREATED)
    

#loginapi            here permission also uncluded

class LoginAPI(APIView):

    permission_classes=[AllowAny]

    def post(self,request):
        _data=request.data
        serializer=LoginSerializer(data=_data)

        if not serializer.is_valid():
            return Response({'message':serializer.errors},status=status.HTTP_404_NOT_FOUND)
        
        user=authenticate(username=serializer.data['username'],password=serializer.data['password'])

        if not user:
            return Response({'message':'Invalid'},status=status.HTTP_404_NOT_FOUND)

        token,_=Token.objects.get_or_create(user=user)
        return Response({'message':'login successfull','token':str(token)},status=status.HTTP_200_OK)



