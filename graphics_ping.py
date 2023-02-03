# https://realpython.com/python-gui-tkinter/
# https://pythonistaplanet.com/rock-paper-scissors-game-using-python-tkinter/

import tkinter as tk
import random

window=tk.Tk()
text_box=tk.Text()
text_box.pack()

window.geometry("400x300")
window.title("Rock Papper Scissors")


USER_SCORE = 0
COMP_SCORE = 0
USER_CHOICE = "Rock"
COMP_CHOICE = "Paper" 

import paho.mqtt.client as mqtt
import time

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.

def player1(winner): 
    global USER_SCORE
    global COMP_SCORE

    if winner=="p1":
        print("naz won")
        USER_SCORE+=1

    elif winner=="p2":
        print ("Neil won")   
        COMP_SCORE+=1 

    else:
        print("Tie")

   

    text_area = tk.Text(master=window,height=12,width=30,bg="#FFFF99")
    text_area.grid(column=0,row=4)
    answer = "Your Choice: {uc} \nComputer's Choice : {cc} \n Your Score : {u} \n Computer Score : {c} ".format(uc=USER_CHOICE,cc=COMP_CHOICE,u=USER_SCORE,c=COMP_SCORE)    
    text_area.insert(tk.END,answer)


def on_connect(client, userdata, flags, rc):
  print("Connection returned result: " + str(rc))

  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("ece180d/central_graphics", qos=1)


def on_message(client, userdata, message):
    # global counter
    # print("ece180d/neil"==message.topic)
    # print('Received message: "' + str(message.payload) + '" on topic "' + message.topic + '" with QoS ' + str(message.qos))

    # if (message.topic=="ece180d/neil"):
    #     pass
    if (message.topic=="ece180d/central_graphics"):
        result=str(message.payload.decode())
        print(result)

        player1(result)

        frame = tk.Frame(master=window, width=150, height=150)
        frame.pack()

        label1 = tk.Label(master=frame, text=result, bg="red")
        label1.place(x=0, y=0)









def on_disconnect(client, userdata, rc):
  if rc != 0:
    print('Unexpected Disconnect')
  else:
    print('Expected Disconnect')





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

client.loop_start()

window.mainloop()


# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()