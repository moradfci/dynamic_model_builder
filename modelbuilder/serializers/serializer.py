from rest_framework import serializers
from ..models import *
from django.core import serializers as serializerx

import json





class ModelBuilderSerializer(serializers.Serializer):


    modelname = serializers.CharField(max_length=255)
    

    def create(self,validated_data):

        
        fields = self.context.get('fields')
       
        
        
       
        
        
        try:
           
            model  = Modelbuilder.create_model(validated_data['modelname'],fields)
            if  isinstance(model,Exception):
                
                errors = str(model)
                raise serializers.ValidationError(detail ={"error":"{}, Please choose another name.".format(str(model))})
                
            else:
                
                table = Table.objects.create(modelname=validated_data['modelname']) 
                return table       
        except Exception as e:
            
            print( "error in serialiazer",e)
            raise Exception(e)

        
    


    def update(self, validated_data, pk=None):
        
        fields = self.context.get('fields')
        try:
            Modelbuilder.alter_model(Modelbuilder,validated_data,fields)
        except Exception as e:
            print(e)
            pass
        

    def add_row(rows,modelname):
       
        modelname = modelname.modelname
        columns = []
        values =[]
       
        for i in rows:
            for key in i.keys():
                if key not in columns:
                    columns.append(key)
                values.append(i[key])
        
        # return 0 
        try:
            Modelbuilder.add_rows(modelname , columns,values)
            
        except Exception as e:
            return e
    
    
    def get_all_row(modelname):
        modelname= modelname.modelname
        print('010101')
        try:
            rows = Modelbuilder.get_all_row(modelname)
            
            print(rows)
            js = serializerx.serialize('json',rows)
            print('111')
            return json.loads(js)
            
        except Exception as e:
            print(e)
            return e