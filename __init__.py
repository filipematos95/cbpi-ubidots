import time, sys
from ubidots import ApiClient
import os
import time

from modules import cbpi
from modules.core.hardware import  SensorActive
from modules.core.props import Property


def ubidots_init(api_key='A1E-09d8db204cf11e8edbbe3e71e0eedfd61b6f'):
	try:
		print "Requesting Ubidots token"
		api = ApiClient(api_key)
	except:
		print "No internet connection"

def ubidots_get_value(api_key='A1E-09d8db204cf11e8edbbe3e71e0eedfd61b6f',variable_key ='5a46431e76254254b5ae38dd' ):
	try:
		api = ApiClient(api_key)
		output2_control = api.get_variable(variable_key)
		lastValue2 = output2_control.get_values(1)
		temp = lastValue2[0]['value']
		print temp
		return temp
	except:
		print "No internet connection"

@cbpi.sensor
class UbidotsTempSensor(SensorActive):

	temp = Property.Number("Temperature", configurable=True, default_value=5)
	API_KEY = Property.Text('API KEY',configurable=True,description = 'Enter your Ubidots API KEY')
	sensorType = Property.Select("Data Type", options=["Temperature", "Gravity", "Battery"], description="Select which type of data to register for this sensor")
	UNIT_KEY = Property.Text('UNIT KEY',configurable=True,description = 'Enter your Variable KEY')
	
	def get_unit(self):
		if self.sensorType == "Temperature":
			return "C" if self.get_config_parameter("unit", "C") == "C" else "F"
		elif self.sensorType == "Gravity":
			return self.unitsGravity
		elif self.sensorType == "Battery":
			return "V"
		else:
			return " "

	def stop(self):
		'''
		Stop the sensor. Is called when the sensor config is updated or the sensor is deleted
		:return: 
		'''
		pass

	def execute(self):
		'''
		Active sensor has to handle its own loop
		:return: 
		'''
		while self.is_running():
			self.data_received(ubidots_get_value(api_key=self.API_KEY,variable_key=self.UNIT_KEY))
			self.sleep(30)

@cbpi.initalizer()
def init_global(cls):
	'''
	Called one at the startup for all sensors
	:return: 
	'''
	ubidots_init()


