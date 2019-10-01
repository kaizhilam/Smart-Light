import json
import threading
import time
from tkinter import *

import mods.paho.mqtt.client as mqtt

class Switch:
    """Simulating physical wire connection to the smart light"""

    __Root = None

    __ConnectValue = None

    __MQTTClient = None

    def __init__(self, connect = "LightBulb1"):
        self.__Root = Tk()
        self.__Root.title("Switch")

        self.__ConnectValue = StringVar(self.__Root)
        self.__ConnectValue.set(connect)

        frame1 = Frame(self.__Root)
        frame1.pack()

        Label(frame1, text = "Connect to: ").pack(side=LEFT)
        Entry(frame1, textvariable = self.__ConnectValue).pack(side = LEFT)

        frame2 = Frame(self.__Root)
        frame2.pack()

        Button(frame2, text = "Switch", command = self.__Publish).pack()
        
        broker_address="broker.mqttdashboard.com"
        self.__MQTTClient = mqtt.Client("Switch")
        self.__MQTTClient.connect(broker_address)

        self.__MQTTClient.loop_start()
        self.__Root.mainloop()
    
    def __Publish(self):
        message = "switch"
        print(message)
        self.__MQTTClient.publish(self.__ConnectValue.get(), "switch")

if __name__ == "__main__":
    app = Switch()
