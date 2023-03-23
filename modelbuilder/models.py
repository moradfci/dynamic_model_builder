from django.db import models ,connection
# from django.db.models. import cache
from django.apps import apps 
from django.core import cache
# Create your models here.
class Table(models.Model):
    modelname =   models.CharField(max_length = 255)
    
    

    
    def __str__(self):
        return self.modelname

    



class Modelbuilder : 
    
    
    
    def create_model(modelname,fields):
        
        attrs = {'__module__': __name__,}
        
        for i in fields:
           
            if fields[i] == 'string':
                fields[i] = models.CharField(max_length=255)
            elif fields[i] == 'number':
                fields[i] = models.FloatField()
            elif fields[i] == 'boolean':
                
                fields[i] = models.BooleanField()
            else:
                fields[i] = models.CharField( max_length=255)
        # return 0 
        try:
            attrs.update(fields)
            
            model = type(modelname, (models.Model,), attrs)
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(model)
        

        except Exception as e:
            
            return(e)
        
        
        
        return model
   

    def alter_model(self,modelname,fields):
        
        
        try:
            
            
            
            attrs = {'__module__': __name__,}
            model = type(modelname['modelname'], (models.Model,), attrs)
            
            try:
                del apps.all_models['modelbuilder'][modelname['modelname']]
            except KeyError as err:
                raise LookupError("'{}' not found.".format(modelname['modelname'])) from err

            with connection.schema_editor() as schema_editor:
                # col = schema_editor.execute("SELECT * FROM sqlite_master WHERE tbl_name = 'modelbuilder_s1' AND type = 'table'")
                schema_editor.delete_model(model)
                
            
        except Exception as e:
             
            return(e)
       
        
        
        self.create_model(modelname['modelname'],fields)
        


    def add_rows(modelname,columns,values):

        
        try:
            s = ','.join(columns)
            values_in_query = ''
            values_temp = []
            values_list = []
            small_list = []
            count = 0
            print(len(columns))
            for i  in values:
                print(i,count)

                if count == len(columns)-1:
                    count = 0
                    small_list.append(i)
                    
                    values_temp.append(small_list)
                    small_list = []
                else:
                   
                   small_list.append(i)
                   count+=1
            
            for item in values_temp:
                values_list.append(tuple(item))

            res = str(values_list).strip('[]')
            query = "INSERT INTO {} ({}) VALUES {};".format(str(__package__)+'_'+modelname,s,res)
            print("we")
            with connection.schema_editor() as schema_editor:
                result = schema_editor.execute(query)
            
            print("we")
            return result

        except Exception as e:
            print(e)
            return e




    def get_all_row(modelname):
        try:
            modelname_inDB = str(__package__)+'_'+modelname
            
            query  = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{}';".format(modelname_inDB)
            
            rows = get_query_set(query,modelname)
            

            return rows
        except Exception as e:
            print(e)
        
            return e
        






def get_query_set (query,modelname):
    # print('3232323',modelname)
    with connection.cursor() as cursor:
                 cursor.execute(query)
                 rows = cursor.fetchall()
            
    attrs = {'__module__': __name__,}
    fields={}
    for row in rows[1:]:
        if row[1]=='double precision':
            fields[row[0]] = models.FloatField()
        elif row[1]== 'character varying':
                fields[row[0]] =models.CharField(max_length=255)
        else:
            fields[row[0]] =models.BooleanField()        
    
    attrs.update(fields)
    model = type(modelname, (models.Model,), attrs)
    queryset= model.objects.all()
    print('565656')
    
    return queryset
  