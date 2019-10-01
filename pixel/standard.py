import configparser
import datetime
import inspect
import json
import tkinter

def FormatSentence(sentence :str, max_letter :int):
    """Format sentence by automatically adding \"-\" 
    or a whitespace"""
    final = []
    placeholder = ""
    text = sentence.split(" ")
    for words in text:
        if len(words) > max_letter:
            full = []
            temp = ""
            for letters in words:
                if len(temp) + len(letters) + 1 < 10:
                    temp += letters
                else:
                    temp += "-"
                    full.append(temp)
                    temp = letters
            full.append(temp)
            final.append("\n".join(full))
        elif len(words) + len(placeholder) - 1 <= max_letter:
                placeholder += words+" "
        else:
            final.append(placeholder)
            placeholder = words+" "
    final.append(placeholder)
    final = "\n".join(final)
    return final
    
def ConvertDateToString(date_time :datetime):
    """Convert datetime.date to string"""
    if isinstance(date_time, datetime.date):
        return date_time.__str__()

def ConvertStringToDate(date_time :str):
    """Convert string to datetime.date
    Example: yyyy-mm-dd"""
    return datetime.datetime.strptime(date_time, "%Y-%m-%d")

def SaveProfile(first_name :str, last_name :str, birth_date :datetime.date):
    """Set profile for profile.json"""
    x = {"firstname":first_name, "lastname":last_name, "birthdate":ConvertDateToString(birth_date)}
    with open("profile.json","w") as file:
        json.dump(x, file)

def LoadProfile():
    """Load profile from profile.json as a dict"""
    with open("profile.json","r") as file:
        profile = json.load(file)
    profile["birthdate"] = ConvertStringToDate(profile["birthdate"])
    return profile

def ResetProfile():
    """Reset profile to default"""
    with open("profile - default.ini", "r") as file:
        default = file.read()
    with open("profile.ini", "w") as file:
        file.write(default)

def LoadConfiguration():
    """Load configuration from configuration.ini to dict"""
    mod = inspect.getmodule(inspect.stack()[1][0])
    config = configparser.ConfigParser()
    config.read("configuration.ini")
    if mod.__name__  in config.sections():
        return dict(config.items(mod.__name__))
    else:
        return None

def SaveConfiguration(configuration :dict = None):
    """Save configuration to configuration.ini"""
    config = configparser.ConfigParser()
    config.read("configuration.ini")
    towrite = {s:dict(config.items(s)) for s in config.sections()}
    mod = inspect.getmodule(inspect.stack()[1][0])
    towrite[mod.__name__] = configuration
    config = configparser.ConfigParser()
    for section in towrite:
        config.add_section(section)
        for key in towrite[section]:
            config.set(section, key, str(towrite[section][key]))
    with open("configuration.ini", "w") as file:
        config.write(file)

def ResetConfiguration():
    """Reset configuration to default"""
    with open("configuration - default.ini", "r") as file:
        default = file.read()
    with open("configuration.ini", "w") as file:
        file.write(default)
    
def LoadInterface():
    """Load profile from interface.json as a dict"""
    with open("interface.json","r") as file:
        profile = json.load(file)
    return profile

def AddLabelWithText(
    instance = None,
    tag :str = None,
    text :str = None,
    font = "Helvetica",
    font_size = 10,
    font_colour = "white",
    width :int = 0, 
    height :int = 0, 
    background_colour = "black", 
    x :int = 0,
    y :int = 0):
    """Add label widget to the interface"""
    extra = {}
    widget = tkinter.Label(
        instance.root,
        text = text,
        font = (font, font_size),
        fg = font_colour,
        width = width,
        height = height,
        bg = background_colour, 
        anchor=tkinter.W, 
        justify=tkinter.LEFT)
    widget.place(x = x, y = y)
    mod = inspect.getmodule(inspect.stack()[1][0])
    extra["module"] = mod.__name__
    tag = mod.__name__+"."+tag
    instance._AppendInterface((tag, widget, extra))

def UpdateTextByTag(instance = None, tag = None, text = None):
    interface = instance.interface
    mod = inspect.getmodule(inspect.stack()[1][0])
    for n, i in enumerate(interface):
        if tag != None and i[0] == mod.__name__+"."+tag:
            widget = i[1]
            if isinstance(widget, tkinter.Label):
                widget.config(text = text)
                i[2]["module"] = mod.__name__
                break

def UpdateColourByTag(instance = None, tag = None, colour = "white"):
    interface = instance.interface
    mod = inspect.getmodule(inspect.stack()[1][0])
    for n, i in enumerate(interface):
        if tag != None and i[0] == mod.__name__+"."+tag:
            widget = i[1]
            if isinstance(widget, tkinter.Label):
                widget.config(fg = colour)
                i[2]["module"] = mod.__name__
                break

def MoveLocationByTag(instance = None, tag = None, x = None, y = None):
    interface = instance.interface
    mod = inspect.getmodule(inspect.stack()[1][0])
    for n, i in enumerate(interface):
        if tag != None and i[0] == mod.__name__+"."+tag:
            widget = i[1]
            widget.place(x = x, y = y)
            i[2]["module"] = mod.__name__
            break

def GetLocationByTag(instance = None, tag = None):
    interface = instance.interface
    mod = inspect.getmodule(inspect.stack()[1][0])
    for i in interface:
        if tag != None and i[0] == mod.__name__+"."+tag:
            widget = i[1]
            return (widget.winfo_rootx(), widget.winfo_rooty())

def Log(obj = None):
    if LoadConfiguration()["log"] == "true":
        print(obj)

def ContainsNumeric(text):
    for i in text:
        try:
            int(i)
            return True
        except:
            pass
    return False