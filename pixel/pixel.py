import configparser
import datetime
import importlib
import json
import os
import threading
import time
from tkinter import Label, Tk, FALSE, W, LEFT, PhotoImage, Button

from . import standard
from .standard import Log

class Pixel:
    __Configuration :dict = {}
    __CustomModules :list = []
    __GUIIsRunning = False
    __Interface :list = []
    __Profile :dict = {}
    __Root :Tk = None
    __ThreadingList : list = []
    __GUIThread = None

    @property
    def configuration(self):
        """Get __Configuration"""
        return self.__Configuration
    
    @property
    def customModules(self):
        """Get __CustomModules"""
        return self.__CustomModules

    @property
    def GUIIsRunning(self):
        """Get __GUIIsRunning"""
        return self.__GUIIsRunning
    
    @property
    def interface(self):
        """Get __Interface"""
        return self.__Interface

    @property
    def profile(self):
        """Get __Profile"""
        return self.__Profile

    @property
    def root(self):
        return self.__Root
    
    @property
    def threadingList(self):
        """Get __ThreadingList"""
        return self.__ThreadingList

    def __init__(self):
        """Initialise object"""
        standard.Log("Initialising Pixel...")
        self.__Configuration = self.__LoadConfiguration()
        self.__Profile = standard.LoadProfile()
        self.__GUIThread = threading.Thread(target=self.__SetupTkinter)
        standard.Log("Initialising Pixel... Done")
    
    def __LoadConfiguration(self):
        """Load configuration from configuration.ini to dict"""
        config = configparser.ConfigParser()
        config.read("configuration.ini")
        return {s:dict(config.items(s)) for s in config.sections()}
    
    def __SaveConfiguration(self):
        """Save configuration to configuration.ini"""
        config = configparser.ConfigParser()
        configuration = self.__Configuration
        for section in configuration:
            config.add_section(section)
            for key in configuration[section]:
                config.set(section, key, str(configuration[section][key]))
        with open("configuration.ini", "w") as file:
            config.write(file)

    def __Shutdown(self, e):
        """Shut down code"""
        Log("Shutting down Pixel...")
        self.__GUIIsRunning = False
        # self.__SaveInterface()
        self.__Root.destroy()
        Log("Shutting down Pixel... Done")
    
    def __SetupTkinter(self):
        """Setup initial tkinter"""
        standard.Log("Setting up Tkinter GUI...")
        self.__Root = Tk()
        self.__Root.title("Building simulator")
        self.__ScreenWidth = self.__Root.winfo_screenwidth()
        self.__ScreenHeight = self.__Root.winfo_screenheight()
        self.__Root.geometry(str(self.__Configuration["pixel.pixel"]["screen width"])+"x"+str(self.__Configuration["pixel.pixel"]["screen height"]))
        # self.__Root.resizable(width = FALSE, height = FALSE)
        self.__Root.config(bg = self.__Configuration["pixel.pixel"]["background colour"])
        # self.__Root.config(cursor = self.__Configuration["pixel.pixel"]["cursor"])
        self.__Root.bind("<Escape>", self.__Shutdown)
        # self.__Root.wm_attributes("-fullscreen", "true")
        self.__FirstTimeLaunch()
        # self.__LoadInterface()
        standard.Log("Setting up Tkinter GUI... Done")
        self.__GUIIsRunning = True
        self.__Root.mainloop()
    
    def __FirstTimeLaunch(self):
        """Check if first time launch"""
        standard.Log("Checking first time launch...")
        if self.__Configuration["pixel.pixel"]["first time launch"] == "true":
            self.__Configuration["pixel.pixel"]["first time launch"] = "false"
            self.__Configuration["pixel.pixel"]["screen width"] = self.__Root.winfo_screenwidth()
            self.__Configuration["pixel.pixel"]["screen height"] = self.__Root.winfo_screenheight()
            self.__SaveConfiguration()
        standard.Log("Checking first time launch... Done")
    
    def __LoadInterface(self):
        """ Load GUI interface from json instead of live"""
        standard.Log("Loading GUI interface...")
        interface = standard.LoadInterface()
        for n, i in enumerate(interface):
            extra = {}
            if i["x"] < 0:
                x = self.root.winfo_screenwidth()+i["x"]
            else:
                x = i["x"]
            if i["y"] < 0:
                y = self.root.winfo_screenheight()+i["y"]
            else:
                y = i["y"]
            if (i["type"] == "label"):
                widget = Label(
                    self.__Root,
                    width = i["width"],
                    height = i["height"],
                    bg=self.__Configuration["pixel.pixel"]["background colour"],
                    anchor=W,
                    justify=LEFT)
                extra["module"] = i["module"]
            elif i["type"] == "button":
                widget = Button(
                    self.__Root, 
                    width = i["width"],
                    height = i["height"],
                    bg=self.__Configuration["pixel.pixel"]["background colour"])
                    #relief="flat")
            elif i["type"] == "image":
                widget = Label(
                    self.__Root,
                    width = i["width"],
                    height = i["height"],
                    bg=self.__Configuration["pixel.pixel"]["background colour"],
                    anchor=W, 
                    justify=LEFT)
            if "text" in i:
                widget.config(
                    text = i["text"],
                    font = (i["font"], i["font size"]),
                    fg=i["font colour"])
            elif "image" in i:
                photo = PhotoImage(file = i["image"])
                extra["image"] = i["image"]
                if "zoom" in i:
                    photo = photo.zoom(i["zoom"])
                    extra["zoom"] = i["zoom"]
                if "subsample" in i:
                    photo = photo.subsample(i["subsample"])
                    extra["subsample"] = i["subsample"]
                widget.config(image = photo)
                widget.image = photo
            widget.place(x = i["x"], y = i["y"])
            self.__Interface.append((i["tag"], widget, extra))
        standard.Log("Loading GUI interface... Done")
    
    def __SaveInterface(self):
        """Save interface onto JSON file"""
        standard.Log("Saving GUI interface to file...")
        interface = []
        for i in self.__Interface:
            tag = i[0]
            widget = i[1]
            extra = i[2]
            if extra["module"] in self.__CustomModules:
                if isinstance(widget, Label):
                    item = {
                        "tag": tag,
                        "type": "label",
                        "x": int(widget.place_info()["x"]),
                        "y": int(widget.place_info()["y"]),
                        "width": int(widget["width"]),
                        "height": int(widget["height"]),
                        "module": extra["module"]
                        }
                    if standard.ContainsNumeric(widget["font"]) == True:
                        item["font"] = widget["font"].split(" ")[0]
                        item["font size"] = int(widget["font"].split(" ")[1])
                    if widget["image"] == "pyimage3":
                        item["image"] = extra["image"]
                        item["zoom"] = extra["zoom"]
                        item["subsample"] = extra["subsample"]                    
                    else:
                        item["text"] = widget["text"]
                        item["font colour"] = widget["fg"]
                else:
                    pass
                interface.append(item)
        with open("interface.json", "w") as file:
            json.dump(interface, file)
        standard.Log("Saving GUI interface to file... Done")

    def _AppendInterface(self, value):
        """Append interface onto __Interface"""
        self.__Interface.append(value)

    def AddModule(self, module):
        """Add custom third part module"""
        Log("Adding custom module \"{}\"...".format(module))
        if module+".py" not in os.listdir("mods"):
            Log("Custom module \"{}\" not found...".format(module))
        else:
            mod = importlib.import_module("mods."+module)
            self.__CustomModules.append(mod)
            Log("Adding custom module \"{}\"... Done".format(module))
    
    def AddAllModule(self):
        """Add all modules contained in /mods file"""
        for i in os.listdir("mods"):
            if i[-3:] == ".py":
                self.AddModule(i[:-3])

    def __Loop(self, mod):
        """Allows the Loop function in custom module to work"""
        if self.__GUIIsRunning == False:
            return
        mod.Loop(self)
        self.__Root.after(mod.SCHEDULETIMER, self.__Loop, mod)
    
    def Run(self):
        """Run Pixel"""
        Log("Running custom modules...")
        self.__GUIThread.start()
        success = False
        timeout = time.time() + 3
        while timeout > time.time():
            if self.__GUIIsRunning:
                for mod in self.__CustomModules:
                    if "Start" in dir(mod):
                        mod.Start(self)
                    else:
                        Log("Can't find \"Start\"")
                    if "Loop" in dir(mod) and "SCHEDULETIMER" in dir(mod):
                        self.__Loop(mod)
                    else:
                        Log("Can't fine either \"Loop\" or \"SCHEDULETIMER\"")
                success = True
                break
            else:
                Log("Running custom modules... Retry")
        if success == True:
            Log("Running custom module... Done")
        else:
            Log("Running custom module... Failed")