from flask import Flask
from flask.ext.spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer, Float,String
from spyne.model.complex import Iterable
import pymysql
import xml
from xml.dom.minidom import Document
conn = pymysql.connect(host= "localhost",
                  user="root",
                  passwd="1234",
                  db="mydb")
data = conn.cursor()
app = Flask(__name__)
spyne = Spyne(app)

class SomeSoapService(spyne.Service):
    __service_url_path__ = '/soap/someservice'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, _returns=Iterable(String))
    # @spyne.srpc(Float, Float, _returns=Iterable(Unicode))
    def query(words):
    	data.execute(""" SHOW COLUMNS  from mydb."""+words)
    	result=[]
    	for value in data:
    		result.append(value[0])
    	print len(result)
    	data.execute(""" SELECT * from """+words)
    	for value in data:
    		temp ='{'
    		for x in range(0, len(result)):
    			temp += '"'+result[x]+'":"'+str(value[x])+'"'
    			if x == len(result)-1:
    				temp += '}'
    			else:
    				temp += ','
    		print temp
        	yield temp
        	temp = ''
    	

if __name__ == '__main__':
    app.run(host = '127.0.0.1')