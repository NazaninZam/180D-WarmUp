import paho.mqtt.client as mqtt
import time

counter=0
# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/central", qos=1)
  client.subscribe("ece180d/central_info", qos=1)
  client.subscribe("ece180d/central_quit", qos=1)

def on_message(client, userdata, message):
    # global counter
    # print("ece180d/neil"==message.topic)
    # print('Received message: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))

    # if (message.topic=="ece180d/neil"):
    #     pass
    if (message.topic=="ece180d/central_info"):
        print(str(message.payload.decode()))

    if (message.topic=="ece180d/central_quit"):
        print(str(message.payload.decode()))
        client.loop_stop()
        client.disconnect()
        quit()

    if (message.topic=="ece180d/central"):
        print(str(message.payload.decode()))
        client.publish("ece180d/neil", input(), qos=1)
        # counter=counter+1
        # print("counter is "+ str(counter))
        # client.publish("ece180d/naz", "num", qos=1)


# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')


# The default message callback.
# (you can create separate callbacks per subscribed topic)


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


while True:  # perhaps add a stopping condition using some break or something.
    pass  # do your non-blocked other stuff here, like receive IMU data or something.
# use subscribe() to subscribe to a topic and receive messages.

# use publish() to publish messages to the broker.


# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()