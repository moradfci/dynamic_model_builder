from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers.serializer import *
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import action
from rest_framework import serializers
from .models import *

# Create your views here.





class ModelBuilderViewset(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated, )
    
    
    def create(self, request):
        # serialezer = ShortageCreateSerializer(data=request.data, context={'user':request.user})
        # if serialezer.is_valid():
        #     serialezer.save()
        #     data = {"success": True, "data": serialezer.data}
        #     return Response(data, status=status.HTTP_201_CREATED)
        # else:
        #     data = {"success": False, "error": {"code": 400,
        #                                         "message": serialezer.errors}}
        #     return Response(data, status=status.HTTP_400_BAD_REQUEST)
        fields = request.data['fields']
        print('xxxx00000',request.data)
        print('xxxx',fields)
        # return Response('1')
        errors = ''
        serializer = ModelBuilderSerializer(data = request.data, context = {"fields":fields})
        if serializer.is_valid():
            
            try:
                serializer.save()
            except Exception as e:
                print('view')
                errors = str(e)
            # return Response(serializer.data)            
        else:
             print('not valid')
             return Response(str(serializer.errors))
        
        
        # serializer = ModelBuilderSerializer(data = request.data,context = fields)
        data = {"data":str(serializer.data),"errors":str(errors)}
        return Response(data)
        
    def list(self, request):
        # queryset =  Shortage.objects.filter(branch=request.user.branch_company)
        # serializer = ShortageCreateSerializer(queryset, many=True)
        # data = {"success": True, "data": serializer.data}
        # return Response(data, status=status.HTTP_200_OK)  
        return Response('list')
    
    
    
    
    def update(self,request,pk=None):
        fields = request.data['fields']
        print('xxxx00000',request.data)
        print('xxxx',fields)
        # return Response('1')
        errors = ''
        model = Table.objects.get(pk=pk)
        
        serializer = ModelBuilderSerializer(data = {"modelname": model.modelname}, context = {"fields":fields})
        
        if serializer.is_valid():
            
            try:
                serializer.update(validated_data= {"modelname": model.modelname})
            except Exception as e:
                print('view')
                errors = str(e)
            # return Response(serializer.data)            
        else:
             print('not valid')
             return Response(str(serializer.errors))
        
        
        # serializer = ModelBuilderSerializer(data = request.data,context = fields)
        data = {"data":str(serializer.data),"errors":str(errors)}
        return Response(data)
        


    @action(detail=False,methods=['POST'], url_path='(?P<pk>\d+)/row')
    def add_row(self,request,pk):
        
        
        model = Table.objects.get(pk=pk)
        print(request.data,model)
        try:
            ModelBuilderSerializer.add_row(request.data['rows'],model)
            return Response({"data":"succuess"})

        except Exception as e:
            print('error',e)
            return Response({"error":str(e)})
        
        

    
    @action(detail=False,methods=['GET'], url_path='(?P<pk>\d+)/rows')
    def get_rows(self,request,pk):

        model = Table.objects.get(pk=pk)
        # print(request.data,model)
        try:
            serializer = ModelBuilderSerializer.get_all_row(model)
            return Response({"data":serializer})

        except Exception as e:
            print('error',e)
            return Response({"error":str(e)})
        
        



