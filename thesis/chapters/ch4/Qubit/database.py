#option for storing symmetry
from string import Template as temp
import re
from subprocess import call
import numpy as np
import getpass

"""
database is gloabl class such that constraints and objective functions do
not get repeated more than once
"""
class Database:

    psql = __import__('psycopg2')

    create_table_temp = temp("create table if not exists $table_name($fields)")

    add_column_temp   = temp("alter table $table_name add column $new_column $type")

    insert_temp       = temp("insert into $table_name($fields) values($nfields) returning id")

    select_best_value = temp("select f,x from $table_name where f=(select $max(f) from $table_name) limit 1")

    select_best_value_on_condition = temp("select f,x from $table_name where $condition and f=(select $max(f) from $table_name where $condition) limit 1")

    update_status_temp= temp("update settings set status=$status where id=$idvalue")


    def __init__(self,settings,database_name=None,user=None,host=None,password=None):
        if database_name == None:
            raise ValueError('Please provide the name of the database')
        self.settings = {'method':"'PSO'",\
                         'seed':0,\
                         'dimension':-1,\
                         'lb':"'[0]'",\
                         'ub':"'[1]'",\
                         'note':"'default'",\
                         'status':"'running'",\
                         'f_value':9999,\
                         'best_value':9999,\
                         'extra fields':{},\
                         'insert type':'Best',\
                         'nth':10,\
                         'max':True}
        self.evaluations = 0
        for key,value in settings.iteritems():
            try:
                self.settings[key]=value
            except KeyError:
                pass

        self.host = host
        self.password = password
        self.database_name              = database_name

        if user == None:
            self.database_user = getpass.getuser()
        else:
            self.database_user              = user

        try:
            self.table_name                 = settings['table name']
        except KeyError:
            raise KeyError('Error: please include table name even if it is not created yet')

    def alter_table(self,attribute,table_name,command='add'):
        pass

    """
    create table: creates a table in given database with given attributes
    Please note: all attributes will have default values just in case values are not
    properly insterted by the user.

    defualt schema:


    given attributes:need to be given in a dictionary of this format 'name of the field':'data type as a string'

    """
    def set_table_name(self,table_name):
        self.table_name = table_name

    def create_table(self,table_name='settings'):
        if table_name == 'settings':
            fields = "id serial primary key, method text,seed int, data_size int, lb text,ub text, note text, status text default '%s',checkin timestamp"%('running')
        else:
            self.set_table_name(table_name)
            fields = 'id int references settings(id), x text, f real,evaluations integer,time timestamp default current_timestamp'
        for key,value in self.settings['extra fields'].iteritems():
            fields+= ','+key+' '+value
        create_table_input = self.create_table_temp.substitute({'table_name':table_name,'fields':fields})
        self.cursor.execute(create_table_input)
        print "="*32
        print " Created: ",table_name
        print "-"*32
        print "fields: ",fields


    def insert_min(self):
        if self.settings['f_value'] < self.settings['best_value']:
            self.settings['best_value'] = self.settings['f_value']
            self.insert()

    def insert_max(self):
        if self.settings['f_value'] > self.settings['best_value']:
            self.settings['best_value'] = self.settings['f_value']
            self.insert()

    def force_save(self,f,x,save_min=True,extra={}):
        self.update_status()
        self.evaluations += 1
        self.settings['f_value'] = f
        self.x = "'%s'"%str(x)
        self.settings['extra fields'] = extra
        self.insert()


    def save(self,f,x,save_min=True,extra={}):
        self.update_status()
        self.evaluations += 1
        self.settings['f_value'] = f
        self.x = "'%s'"%str(x)
        self.settings['extra fields'] = extra
        if self.settings['insert type'] == 'Best':
            if save_min:
                self.insert_min()
            else:
                self.insert_max()
        elif self.settings['insert type'] == 'nth iter':
            if self.evluations % self.settings['nth'] == 0:
                self.insert()
        else:
            self.insert()


    def connect_db(self):
        if self.host:
            try:
                self.connection = self.psql.connect(dbname=self.database_name,user=self.database_user,host=self.host,password=self.password)
            except:
                raise NameError("Error: Cannot connect to the remote server, please make sure it exists")
        else:
            try:
                self.connection = self.psql.connect(dbname=self.database_name,user=self.database_user)
            except:
                print "Could not connect to the Database ",self.database_name,", please sure all settings are correct"
                if call(["createdb",self.database_name])==1:
                    raise ValueError("Error: Could not create database please make sure you have privlidges and pgadmin3 is installed")
        """
        setup connection to the server the user has proved information on
        """
        self.cursor	= self.connection.cursor()


    """
    Setup the database connection such that it is persistant to save on time
    """
    def setup(self):
	print '='*32
        print '*'+' '*30+'*'
        print '*  setting up the Database   *'
        print '*'+' '*30+'*'
        print '='*32
        self.connect_db()
        self.create_table()
        self.create_table(self.table_name)
        self.id_value= self.initial_insert()

    def initial_insert(self):
        try:
            table_name = "settings"
            fields  = "method,seed,data_size,lb,ub,note"
            nfields = "'%s'"%self.settings['method'] + "," +\
                    str(self.settings['seed']) + "," +\
                    str(self.settings['dimension']) + \
                    "," + "'%s'"%self.settings['lb'] + "," +\
                    "'%s'"%self.settings['ub'] + "," + \
                    "'%s'"%self.settings['note']
            insert_input = self.insert_temp.substitute({'table_name':table_name,'fields':fields,'nfields':nfields})
            self.cursor.execute(insert_input)
	    self.connection.commit()
	    idval = self.cursor.fetchone()[0]
            print idval
            return idval
        except self.psql.OperationalError:
            print "Error in inserting settings values"

    def insert(self):
	#Database storage
        try:
            fields = "id,x,f,evaluations"
            nfields = str(self.id_value)+","+self.x+\
                      ","+str(self.settings['f_value'])+\
                      ","+str(self.evaluations)
            for key,value in self.settings['extra fields'].iteritems():
                fields  += ","+key
                nfields += ","+str(value)
            insert_query = self.insert_temp.substitute({'table_name':self.table_name,'fields':fields,'nfields':nfields})
	    self.cursor.execute(insert_query)
	    self.connection.commit()
	except:
	    print "could not connect to the database"
	    try:
		self.setup()
	        self.cursor.execute(insert_query)
	        self.connection.commit()
            except:
		print "tried to reconnect and failed"


    def close(self):
        try:
            self.update_status('finished')
            self.connection.close()
        except:
            pass
        print '='*50
        print '   Closing Database: ',self.database_name
        print '='*50

    def get_best_value(self,column=None):
        self.connect_db()
        if self.settings['max']:
            max_val = 'max'
        else:
            max_val = 'min'

        if column == None:
            select_best_query = self.select_best_value.substitute({'table_name':self.table_name,\
                                                                   'max':max_val})
        else:
            condition = ''
            for key,value in column.items():
                condition += key+'='+str(value)
            select_best_query = self.select_best_value_on_condition.substitute({'table_name':self.table_name,\
                                                                   'max':max_val,\
                                                                   'condition':condition})
        self.cursor.execute(select_best_query)
        result_list = self.cursor.fetchall()
        result = {'f':result_list[0][0],\
                  'x':result_list[0][1]}
        string_list = re.sub("\s\s+"," ",result['x'].replace("[","").replace("]","").replace(";"," ").replace('\n','')).split(" ")
        if string_list[0] == '':
            string_list = string_list[1:]
        result['x'] = np.array(map(lambda x: float(x),string_list))
        self.close()
        return result

    def update_status(self,status="'running'"):
        status = "%s"%status
        update_query= self.update_status_temp.substitute({'status':status,'idvalue':self.id_value})
        self.cursor.execute(update_query)
        self.connection.commit()

if __name__ == '__main__':
        import time
        settings = {'method':"'PSO'",\
                    'seed':150,\
                    'dimension':10,\
                    'lb':"'[1,1]'",\
                    'ub':"'[3,3]'",\
                    'note':"'test'",\
                    'f_value':0,\
                    'best_value':0,\
                    'table name':'t_5qubit'}


        d3 = Database(settings,'simlab_db','simlabuser1','db.cs.usask.ca','simlab_01')
        d3.get_best_value({'T':150})



