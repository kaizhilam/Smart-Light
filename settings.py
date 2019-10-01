import configparser
from tkinter import ACTIVE, BOTTOM, Button, END, Entry, Frame, LEFT, Listbox, StringVar, Tk

class Settings():
    """Settings application to change the configuration.ini"""
    #tkinter
    __Root = None 
    __SectionListBox = None
    __KeyListBox = None

    #data
    __Config = None
    __SelectedSection = None
    __SelectedKey = None
    __Value = None

    def __init__(self):
        self.__LoadConfiguration()
        self.__Setup()

    def __Setup(self):
        self.__Root = Tk()

        self.__Value = StringVar(self.__Root)

        self.__Root.title("Configuration")

        bottomFrame = Frame(self.__Root)
        bottomFrame.pack(side = BOTTOM)
        
        self.__SectionListBox = Listbox(self.__Root)
        self.__SectionListBox.pack(side = LEFT)
        self.__KeyListBox = Listbox(self.__Root)
        self.__KeyListBox.pack(side = LEFT)

        self.__PopulateSection()

        self.__Poll()

        valueEntry = Entry(bottomFrame, textvariable = self.__Value)
        valueEntry.pack(side = LEFT)
        saveButton = Button(bottomFrame, text = "Save", command = self.__SaveConfiguration)
        saveButton.pack(side = LEFT)

        self.__Root.mainloop()
    
    def __Shutdown(self, e):
        self.__Root.destroy()
    
    def __LoadConfiguration(self):
        config = configparser.ConfigParser()
        config.read("configuration.ini")
        self.__Config = {s:dict(config.items(s)) for s in config.sections()}

    def __SaveConfiguration(self):
        self.__Config[self.__SelectedSection][self.__SelectedKey] = self.__Value.get()
        config = configparser.ConfigParser()
        configuration = self.__Config
        for section in configuration:
            config.add_section(section)
            for key in configuration[section]:
                config.set(section, key, str(configuration[section][key]))
        with open("configuration.ini", "w") as file:
            config.write(file)


    def __PopulateSection(self):
        for i in self.__Config:
            self.__SectionListBox.insert(END, i)
    
    def __Poll(self):
        selectedSection = self.__SectionListBox.get(ACTIVE)
        if selectedSection != self.__SelectedSection:
            self.__SelectedSection = selectedSection

            self.__KeyListBox.delete(0, END)
            for key in self.__Config[selectedSection]:
                self.__KeyListBox.insert(END, key)

        selectedKey = self.__KeyListBox.get(ACTIVE)
        if selectedKey != self.__SelectedKey:
            self.__SelectedKey = selectedKey
            self.__Value.set(self.__Config[selectedSection][selectedKey])

        self.__Root.after(100, self.__Poll)

if __name__ == "__main__":
    Settings()