from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Person
from home.serializer import PersonSerializer



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
    


@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method=='GET':
        objPerson=Person.objects.all()
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



     