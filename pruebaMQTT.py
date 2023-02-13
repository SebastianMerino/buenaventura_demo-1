import time
import datetime
import random
from paho.mqtt import client as mqtt_client
import requests

broker = 'broker.emqx.io'
port = 1883
client_id = f'buenaventura-mqtt-a-{random.randint(0, 10000)}'
print("CLIENTE: ",client_id)
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

def subscribe(client: mqtt_client, topic: str):
	client.subscribe(topic)
	client.on_message = on_message

def on_message(client, userdata, msg):
	try:
		print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
		resultado=''
		topic_arr = msg.topic.split('/')
		# name = topic_arr[1]
		if topic_arr[2] == "encendido":
			resultado = str(msg.payload.decode())
			resultado_arr = resultado.split(',') 
			estado = resultado_arr[1]
			timestamp = resultado_arr[0]
			res = requests.get(f'http://localhost:8000/iotVehiculos/registrarDatos?mensaje={estado}&tiempo={timestamp}')
			print(res)
	except:
		print("ERROR")



if __name__ == '__main__':
	client = connect_mqtt()
	time.sleep(1)
	client.loop_start()

	subscribe(client, "testing/+/encendido")
	subscribe(client, "testing/+/conectado")
	while True:
		time.sleep(1)


