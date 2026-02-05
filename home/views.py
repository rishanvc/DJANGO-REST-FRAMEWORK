from rest_framework.decorators import api_view
from rest_framework.response import Response



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
     