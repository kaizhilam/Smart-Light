import json
import threading
import time
from tkinter import *

import mods.paho.mqtt.client as mqtt

class App:
    """Simulating web app or mobile app to control smart light"""

    __Root = None
    __Log = None

    __FloorValue = None
    __RoomValue = None
    __BulbValue = None
    __OnValue = None
    __ColourValue = None
    __BrightnessValue = None
    __StatusValue = None
    __AuthenticationValue = None

    __Account = None

    __MQTTClient = None

    def __init__(self, account = "test"):
        self.__Account = account
        self.__Root = Tk()
        self.__Root.title("Mobile App/Web Interface simulator")

        self.__FloorValue = IntVar(self.__Root)
        self.__RoomValue = IntVar(self.__Root)
        self.__BulbValue = IntVar(self.__Root)
        self.__OnValue = BooleanVar(self.__Root)
        self.__ColourValue = StringVar(self.__Root)
        self.__BrightnessValue = IntVar(self.__Root)
        self.__StatusValue = BooleanVar(self.__Root)
        self.__AuthenticationValue = StringVar(self.__Root)

        self.__FloorValue.set(1)
        self.__RoomValue.set(1)
        self.__BulbValue.set(1)
        self.__OnValue.set(True)
        self.__ColourValue.set("Yellow")
        self.__BrightnessValue.set(100)
        self.__StatusValue.set(False)
        self.__AuthenticationValue.set("password")
        
        frameleft = Frame(self.__Root)
        frameleft.pack(side=LEFT)

        frameright = Frame(self.__Root)
        frameright.pack(side=LEFT)

        frame1 = Frame(frameleft)
        frame1.pack(side=TOP)
        Label(frame1, text = "Floor :").pack(side=LEFT)
        Entry(frame1, textvariable = self.__FloorValue).pack(side=LEFT)

        frame2 = Frame(frameleft)
        frame2.pack(side=TOP)
        Label(frame2, text = "Room :").pack(side=LEFT)
        Entry(frame2, textvariable = self.__RoomValue).pack(side=LEFT)

        frame3 = Frame(frameleft)
        frame3.pack(side=TOP)
        Label(frame3, text = "Bulb :").pack(side=LEFT)
        Entry(frame3, textvariable = self.__BulbValue).pack(side=LEFT)

        radioOnOption = [("On", True),("Off", False)]
        frame4 = Frame(frameleft)
        frame4.pack(side=TOP)
        Label(frame4, text = "Power :").pack(side=LEFT)
        self.__OnValue.set(True)
        for text, mode in radioOnOption:
            radio = Radiobutton(frame4, text = text, variable = self.__OnValue, value = mode)
            radio.pack(side=LEFT)

        frame5 = Frame(frameleft)
        frame5.pack(side=TOP)
        Label(frame5, text = "Colour :").pack(side=LEFT)
        Entry(frame5, textvariable = self.__ColourValue).pack(side=LEFT)

        frame6 = Frame(frameleft)
        frame6.pack(side=TOP)
        Label(frame6, text = "Brightness :").pack(side=LEFT)
        Entry(frame6, textvariable = self.__BrightnessValue).pack(side=LEFT)

        radioStatusOption = [("Reply", True),("Ignore", False)]
        frame7 = Frame(frameleft)
        frame7.pack(side=TOP)
        Label(frame7, text = "Status :").pack(side=LEFT)
        self.__StatusValue.set(False)
        for text, mode in radioStatusOption:
            radio = Radiobutton(frame7, text = text, variable = self.__StatusValue, value = mode)
            radio.pack(side=LEFT)

        frame8 = Frame(frameleft)
        frame8.pack(side=TOP)
        Label(frame8, text = "Auth :").pack(side=LEFT)
        Entry(frame8, textvariable = self.__AuthenticationValue).pack(side=LEFT)

        frame9 = Frame(frameleft)
        frame9.pack(side=RIGHT)
        Button(frame9, text = "Publish", command = self.__Publish).pack(side=LEFT)

        frame10 = Frame(frameright)
        frame10.pack(side=RIGHT)
        self.__Log = Text(frame10)
        self.__Log.pack(side=LEFT)
        self.__Log.config(state=DISABLED)

        def OnMessage(client, userdata, message):
            print("message received: {}".format(message.payload.decode("utf-8")))
            print("message topic: {}".format(message.topic))
            print("message qos: {}".format(message.qos))
            print("message retain flag: {}".format(message.retain))
            self.__Log.config(state=NORMAL)
            self.__Log.insert(1.0, message.payload.decode("utf-8")+"\n")
            self.__Log.config(state=DISABLED)
        
        broker_address="broker.mqttdashboard.com"
        self.__MQTTClient = mqtt.Client(self.__Account)
        self.__MQTTClient.on_message=OnMessage
        self.__MQTTClient.connect(broker_address)
        self.__MQTTClient.subscribe("smarthome/client/"+str(self.__Account))
        # self.__MQTTClient.subscribe("smarthome/client/#")

        self.__MQTTClient.loop_start()
        self.__Root.mainloop()
    
    def __Publish(self):
        message = {
            "account":self.__Account,
            "floor":self.__FloorValue.get(),
            "room":self.__RoomValue.get(),
            "bulb":self.__BulbValue.get(),
            "on":self.__OnValue.get(),
            "colour":self.__ColourValue.get(),
            "brightness":self.__BrightnessValue.get(),
            "status":self.__StatusValue.get(),
            "authentication": self.__AuthenticationValue.get()
            }
        payload = json.dumps(message)
        print(message)
        self.__MQTTClient.publish("smarthome", payload)

if __name__ == "__main__":
    app = App()
