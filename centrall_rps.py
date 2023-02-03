import paho.mqtt.client as mqtt
import time

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/neil", qos=1)
  client.subscribe("ece180d/naz", qos=1)


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')

choices = ['rock', 'paper', 'scissors']
neil_msg = -1
naz_msg = -1
processMove = False
# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
  global neil_msg
  global naz_msg
  if message.topic == "ece180d/neil":
    neil_msg = str(message.payload.decode())
  elif message.topic == "ece180d/naz":
    naz_msg = str(message.payload.decode())
  processMove = (neil_msg != -1) and (naz_msg != -1)
  if processMove:
    if neil_msg in choices and naz_msg in choices:
      client.publish("ece180d/central_info",'Neil: ' + neil_msg + '\nNaz: ' + naz_msg, qos=1)
      if neil_msg == naz_msg:
        client.publish("ece180d/central_info", 'Tie!', qos=1)
      elif (neil_msg == 'rock' and naz_msg == 'paper') or (neil_msg == 'paper' and naz_msg == 'scissors') or (neil_msg == 'scissors' and naz_msg == 'rock'):
        client.publish("ece180d/central_info", 'Naz won!', qos=1)
      else:
        client.publish("ece180d/central_info", 'Neil won!', qos=1)    
    elif neil_msg == 'q' or naz_msg == 'q':
      client.publish("ece180d/central_info", 'A user has disconnected...exiting', qos=1)
      client.loop_stop()
      client.disconnect()
    else:
      client.publish("ece180d/central_quit", "One (or more) invalid response(s)! Please input a move in ", choices, " or 'q' to quit.")
    client.publish("ece180d/central", "Enter a move: ", qos=1)
    neil_msg = -1
    naz_msg = -1



# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async('mqtt.eclipseprojects.io')
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()

time.sleep(1)
client.publish("ece180d/central", f"Welcome to RPS!\nPlease enter a move in {choices} or 'q' to quit", qos=1)

while True:  # perhaps add a stopping condition using some break or something.
  pass  # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.

# use publish() to publish messages to the broker.

# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()