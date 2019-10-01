filestring = """\"\"\" 
Custom module template
To create custom module:

Start - One time run
Loop - Runs after every milliseconds. Use SCHEDULETIMER as schedule timer
\"\"\"

from pixel import standard

SCHEDULETIMER = 5000

# One time run
def Start(instance):
    pass

# Runs every SCHEDULETIMER seconds
def Loop(instance):
    pass
"""

print(filestring.replace("\n","\n"))

file = open("examplemodule.py", "w")
file.write(filestring)
file.close()
