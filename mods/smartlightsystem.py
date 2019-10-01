""" 
Smart Lighting System package
Modify these value:
FLOORHUB - How many floors in the building
ROOMHUB - How many rooms per floor
LIGHTBULB - How many lightbulbs per room
"""

import json
import threading
import time

from pixel import standard

from .paho.mqtt import client as mqtt


# Change value here to test scalling
# Note that you will NOT be running this parallel. And too much might freeze your computer as it is just a simulation
FLOORHUB = 4
ROOMHUB = 2
LIGHTBULB = 3


SCHEDULETIMER = 100
devices = []
def Start(instance):
    standard.AddLabelWithText(
        instance=instance,
        tag="status",
        text="Please wait. Populating IoT devices...",
        x=700,
        y=850
    )
    global devices
    
    #Control center
    cloud = Cloud()
    devices.append(cloud)
    standard.AddLabelWithText(instance=instance, tag=cloud.ID, text=cloud, x=0, y=0)

    #Populate Floor Hub
    xfloorposition= 50
    yfloorposition = 20
    for floor in range(1, FLOORHUB+1):
        floorhub = FloorHub("FloorHub"+str(floor))
        devices.append(floorhub)
        standard.AddLabelWithText(instance=instance, tag=floorhub.ID, text=floorhub, x=xfloorposition, y=yfloorposition)
        
        #Populate Room Hub
        xroomposition = xfloorposition + 50
        yroomposition = yfloorposition + 20
        for room in range(1, ROOMHUB+1):
            roomhub = RoomHub("RoomHub"+str(2*(floor-1)+room), floor)
            devices.append(roomhub)
            standard.AddLabelWithText(instance=instance, tag=roomhub.ID, text=roomhub, x=xroomposition, y=yroomposition)
            
            #Populate Lightbulb
            xlightposition = xroomposition + 50
            ylightposition = yroomposition + 20
            for light in range(1, LIGHTBULB+1):
                lightbulb = Lightbulb("LightBulb"+str((ROOMHUB*LIGHTBULB)*(floor-1)+(LIGHTBULB)*(room-1)+light), 2*(floor-1)+room)
                devices.append(lightbulb)
                standard.AddLabelWithText(instance=instance, tag=lightbulb.ID, text=lightbulb, x=xlightposition, y=ylightposition)
                
                ylightposition += 20
            yroomposition = ylightposition
        yfloorposition = yroomposition
    
    standard.UpdateTextByTag(
        instance=instance,
        tag="status",
        text="Done."
    )
    standard.MoveLocationByTag(
        instance=instance,
        tag="status",
        x=850,
        y=850
    )

# Runs every SCHEDULETIMER seconds
def Loop(instance):
    global devices
    for i in devices:
        thread = threading.Thread(target= i.Loop, args=[instance], daemon=True)
        thread.start()

class Cloud:
    """Cloud node"""
    __ID = "Cloud"
    __MQTTClient = None
    __MQTTSubscribe = None

    @property
    def ID(self):
        return self.__ID

    def __init__(self):
        self.__MQTTSetup()
        self.__MQTTSubscribe = "smarthome"
    
    def __MQTTSetup(self):
        """Setup MQTT client"""
        address = "broker.mqttdashboard.com"
        self.__MQTTClient = mqtt.Client(self.__ID)
        self.__MQTTClient.on_message = self.__MQTTOnMessage
        self.__MQTTClient.connect(address)
    
    def Loop(self, instance):
        self.__MQTTClient.loop_start()
        self.__MQTTClient.subscribe(self.__MQTTSubscribe)
        self.__MQTTClient.loop_stop()
    
    def __MQTTOnMessage(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        msg = json.loads(msg)
        self.__MQTTClient.publish("smarthome/cloud", json.dumps(msg))
    
    def __repr__(self):
        return "Cloud Node"

class FloorHub:
    """Fog node"""
    __ID = None
    __MQTTClient = None
    __MQTTSubscribe = None

    @property
    def ID(self):
        return self.__ID

    def __init__(self, id):
        self.__ID = str(id)
        self.__MQTTSetup()
        self.__MQTTSubscribe = "smarthome/cloud"
    
    def __MQTTSetup(self):
        """Setup MQTT client"""
        address = "broker.mqttdashboard.com"
        self.__MQTTClient = mqtt.Client(self.__ID)
        self.__MQTTClient.on_message = self.__MQTTOnMessage
        self.__MQTTClient.connect(address)
    
    def Loop(self, instance):
        self.__MQTTClient.loop_start()
        self.__MQTTClient.subscribe(self.__MQTTSubscribe)
        self.__MQTTClient.loop_stop()
    
    def __MQTTOnMessage(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        msg = json.loads(msg)
        if "FloorHub"+str(msg["floor"]) == self.__ID:
            self.__MQTTClient.publish("smarthome/FloorHub"+str(msg["floor"]), json.dumps(msg))
    
    def __repr__(self):
        return self.__ID

class RoomHub:
    """Fog node"""
    __ID = None
    __MQTTClient = None
    __MQTTSubscribe = None
    __Floor = None

    @property
    def ID(self):
        return self.__ID

    def __init__(self, id, floor):
        self.__ID = str(id)
        self.__Floor = floor
        self.__MQTTSetup()
        self.__MQTTSubscribe = "smarthome/FloorHub{}".format(self.__Floor)
    
    def __MQTTSetup(self):
        """Setup MQTT client"""
        address = "broker.mqttdashboard.com"
        self.__MQTTClient = mqtt.Client(self.__ID)
        self.__MQTTClient.on_message = self.__MQTTOnMessage
        self.__MQTTClient.connect(address)
    
    def Loop(self, instance):
        self.__MQTTClient.loop_start()
        self.__MQTTClient.subscribe(self.__MQTTSubscribe)
        self.__MQTTClient.loop_stop()
    
    def __MQTTOnMessage(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        msg = json.loads(msg)
        if "RoomHub"+str(msg["room"]) == self.__ID:
            self.__MQTTClient.publish("smarthome/RoomHub"+str(msg["room"]), json.dumps(msg))
    
    def __repr__(self):
        return self.__ID

class Lightbulb:
    """Edge node"""
    __ID = None
    __Room = None
    __MQTTClient = None
    __MQTTSubscribe = None
    __On :bool = False
    __Colour :str = "White"
    __Brightness :int = 100

    @property
    def ID(self):
        return self.__ID

    @property
    def On(self):
        return self.__On
    
    @property
    def Colour(self):
        return self.__Colour
    
    @property
    def Brightness(self):
        return self.__Brightness

    def __init__(self, id, room):
        self.__ID = str(id)
        self.__Room = room
        self.__MQTTSubscribe = "smarthome/RoomHub{}".format(self.__Room)
        self.__MQTTSetup()
    
    def __MQTTSetup(self):
        """Setup MQTT client"""
        address = "broker.mqttdashboard.com"
        self.__MQTTClient = mqtt.Client(self.__ID)
        self.__MQTTClient.on_message = self.__MQTTOnMessage
        self.__MQTTClient.connect(address)
    
    def Loop(self, instance):
        self.__MQTTClient.loop_start()
        self.__MQTTClient.subscribe(self.__MQTTSubscribe)
        self.__MQTTClient.subscribe(self.ID)
        self.__MQTTClient.loop_stop()
        standard.UpdateTextByTag(instance=instance, tag=self.__ID, text=self.__repr__())
        standard.UpdateColourByTag(instance=instance, tag=self.__ID, colour=self.__Colour)
    
    def __MQTTOnMessage(self, client, userdata, message):
        msg = message.payload.decode("utf-8")
        if msg == "switch":
            self.Switch()
        else:
            msg = json.loads(msg)
            print(msg)
            if "LightBulb"+str(msg["bulb"]) == self.__ID:
                if "on" in msg:
                    self.__On = msg["on"]
                if "colour" in msg:
                    self.__Colour = msg["colour"]
                if "brightness" in msg:
                    self.__Brightness = msg["brightness"]
                if "status" in msg and msg["status"] == True:
                    tosend = {"id":self.__ID, "on":self.__On, "colour":self.__Colour, "brightness":self.__Brightness}
                    self.__MQTTClient.publish("smarthome/client/"+str(msg["account"]), json.dumps(tosend))

    def Switch(self):
        self.__On = not self.__On
    
    def TurnOn(self):
        """Turn on lightbulb"""
        self.__On = True
    
    def TurnOff(self):
        """:Turn off lightbulb"""
        self.__On = False
    
    def ChangeColour(self, colour :str = "White"):
        self.__Colour = colour
    
    def Dim(self, percentage :int = 100):
        if percentage > 0 and percentage <= 100:
            self.__Brightness = percentage
    
    def __repr__(self):
        if self.__On == True:
            return "{} - {}".format(self.__ID, self.__Brightness)
        else:
            return "{} - OFF".format(self.__ID)

