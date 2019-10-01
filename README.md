# Smart-Light

## SIT314 - Final Project

### Using my Pixel repository as base

## Getting started

### Prerequisite
- Python 3.6 and above

### Instructions
1. Launch [building.pyw](building.pyw) to simulate lights in building. Wait for it to populate.
2. Launch [interface.pyw](interface.pyw) to simulate web app or mobile app.
    - Floor - signifies the floor that user wants to control
    - Room - signifies the room that user wants to control
    - Bulb - signifies the light bulb that user wants to control
    - Power - On/Off the light bulb
    - Colour - Change the colour of the light bulb. [List of colours](http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter)
    - Brightness - Change the brightness of the lightbulb
    - Status - If you want the light bulb to reply
    - Auth - password (not working at the moment)
3. Launch [switch.pyw](switch.pyw) to simulate physical switch. (Still uses MQTT to communicate because it's a simulation)
    - Connect To - connect to different lightbulb. Simulating a physical switch connecting to a lightbulb
4. To tweak the number of nodes, open [mods/smartlightsystem.py](mods/smartlightsystem.py) and modify: FLOORHUB, ROOMHUB, LIGHTBULB
    - FLOORHUB - Number of floors in the building
    - ROOMHUB - Number of rooms in a floor
    - LIGHTBULB - Number of lightbulbs in a room

## Note
The reason it takes a while to launch is because populating lightbulb isn't running parallel.

But the system will run close to parallel when it is done populating