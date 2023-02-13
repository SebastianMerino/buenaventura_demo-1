import time
import random
from paho.mqtt import client as mqtt_client

# broker = 'f7fd1b8129784adba10ca1a7b2b0c0cc.s2.eu.hivemq.cloud'
# port = 8883
# client_id = f'buenaventura-mqtt-{random.randint(0, 10000)}'
# username = 'usuario'
# password = 'buenaventura'

broker = 'broker.emqx.io'
port = 1883
client_id = f'buenaventura-mqtt-{random.randint(0, 10000)}'
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
	# client.tls_set("C:\gaaa\isrgrootx1.crt")
	# client.tls_insecure_set(True)
	client.connect(broker, port)
	return client

# topic = "vehiculos/+/+"
topic = "vehiculos/placa/test"

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

def publish(client):
	# msg_count = 1675873765
	# msg_count = 1675873765123456789
	msg_str = 'a'*250
	msg_count = 0
	while True:
		time.sleep(0.2)
		msg = msg_str + str(msg_count)
		result = client.publish(topic, msg)
		# result: [0, 1]
		status = result[0]
		if status == 0:
			print(f"Send `{msg}` to topic `{topic}`")
		else:
			print(f"Failed to send message to topic {topic}")
		msg_count += 1

def run():
	client = connect_mqtt()
	client.loop_start()
	
	time.sleep(1)
	# client.subscribe(topic)
	# client.on_message = on_message
	# while True:
	# 	time.sleep(1)
	publish(client)


if __name__ == '__main__':
	run()
