import time
import datetime
import random
from paho.mqtt import client as mqtt_client
import requests

broker = 'broker.emqx.io'
port = 1883
# topic = "python/mqtt"
#client_id = 'python-mqtt-666asfdzdssdfsd'
client_id = f'buenaventura-mqtt-{random.randint(0, 10000)}'
username = 'emqx'
password = 'public'

def connect_mqtt():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code %d\n", rc)
	# Set Connecting Client ID
	client = mqtt_client.Client(client_id)
	client.username_pw_set(username, password)
	client.on_connect = on_connect
	client.connect(broker, port)
	return client


def Vehiculo():
	def __init__(self, nombre: str):
		self.name = nombre

	

def subscribe(client: mqtt_client, topic: str):
	client.subscribe(topic)
	client.on_message = on_message

estado = []
timestamp = []
def on_message(client, userdata, msg):
	print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
	resultado=''
	topic_arr = msg.topic.split('/')
	name = topic_arr[1]
	print(name)
	if topic_arr[2] == "conectado":
		if msg.payload.decode() == "Y":
			return
		if msg.payload.decode() == "N":
			resultado = '-'
			estado.append('-')
	if topic_arr[2] == "encendido":
		resultado = str(msg.payload.decode())
		resultado_arr = resultado.split(',') 
		estado.append(resultado_arr[1])
		timestamp.append(resultado_arr[0])

		print(estado,timestamp)
		# res = requests.get(f'http://localhost:8000/iotVehiculos/registrarDatos?mensaje={resultado}&tiempo={datetime.datetime.now().strftime("%d-%m-%Y:%H-%M-%S")}')
		res = requests.get(f'http://localhost:80/iotVehiculos/registrarDatos?mensaje={resultado_arr[1]}&tiempo={resultado_arr[0]}')
		print(res)



if __name__ == '__main__':
	client = connect_mqtt()
	client.loop_start()

	subscribe(client, "vehiculos/+/encendido")
	subscribe(client, "vehiculos/+/conectado")
	while True:
		time.sleep(1)


