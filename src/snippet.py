import customtkinter
import json
from tkinter import filedialog
import tkinter
import subprocess
import os
import keyboard
import webbrowser
from pathlib import Path
import threading

srcPath = Path(__file__).parent

f = open(srcPath / "snippets.json")
snippetsDict = json.loads(f.read())

f = open(srcPath / "temp.py", "r")
template = f.read()

binding = {}

endCode = "if stopKey != \"\": keyboard.wait(stopKey)"

width = 0
height = 0



def runCode(code):
    # print("Here!\n")
    # f = open(srcPath / "temp.file.py", "w")
    # f.write(code)
    # f.close()
    # subprocess.run(["python", srcPath / "temp.file.py"])
    print(code)
    exec(code)
    # os.remove(srcPath / "temp.file.py")

def runSnippet(*args):
    # print(args)
    # code = "".join(args)
    code = args[0]
    code = template + "\n" + f"hotkeyId = {args[1]}" + "\n" + code + "\n" + endCode
    t = threading.Thread(target=runCode, args=(code,))
    t.run()
    # runCode(code)

def initSnippetByName(name):
    snippetFileName = snippetsDict[name]["name"]
    snippetHotKey = snippetsDict[name]["hotkey"]
    f = open(srcPath / name / snippetFileName, "r")
    snippetFile = f.read()
    # for key, value in snippetHotKey.items():
    #     binding[key] = [snippetFile, value]
    binding[snippetHotKey] = [snippetFile, 0]

hotkeys = []

def registerAll():
    for key in snippetsDict:
        initSnippetByName(key)
    
    for key, value in binding.items():
        # print(type(value))
        hotkey = keyboard.add_hotkey(key, callback=runSnippet, args=(value))
        hotkeys.append(hotkey)

def clear():
    global hotkeys
    for i in hotkeys:
        keyboard.remove_hotkey(i)
    hotkeys = []

app = None

def reloadOnNew():
    global srcPath
    f = open(srcPath / "snippets.json")
    global snippetsDict
    res = f.read()
    print(res)
    snippetsDict = json.loads(res)
    clear()
    registerAll()
    app.reloadOnNew()

class topRightButtonGroup(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class NewButtonForm(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Load New Snippet")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.snippetNameLabel = customtkinter.CTkLabel(self, text="Snippet File", font=("Montserrat", 12))
        self.snippetNameLabel.grid(row=0, column=0, columnspan=2, sticky="nwe", pady=5, padx=5)
        self.name = tkinter.StringVar(self, "")
        self.file = tkinter.StringVar(self, "")
        self.snippetFileLabel = customtkinter.CTkEntry(self, textvariable=self.file, placeholder_text="", font=("Montserrat", 12))
        self.snippetFileLabel.grid(row=1, column=0, sticky="nwe", pady=3, padx=5)
        self.snippetFileChooser = customtkinter.CTkButton(self, text="Choose File", font=("Montserrat", 12), command=self.snippetFileChooserCallback)
        self.snippetFileChooser.grid(row=1, column=1, sticky="nwe", pady=3, padx=5)

        self.HotkeyLabel = customtkinter.CTkLabel(self, text="Hotkey", font=("Montserrat", 12))
        self.HotkeyLabel.grid(row=2, column=0, columnspan=2, sticky="nwe", pady=5, padx=5)
        self.hotKey = tkinter.StringVar(self, "ctrl")
        self.hotkeyEntry = customtkinter.CTkEntry(self, textvariable=self.hotKey, placeholder_text="ctrl", font=("Montserrat", 12))
        self.hotkeyEntry.grid(row=3, column=0, columnspan=2, sticky="nwe", pady=5, padx=5)

        self.submitButton = customtkinter.CTkButton(self, text="Load", font=("Montserrat", 12), command=self.submitButtonCallback)
        self.submitButton.grid(row=4, column=0, columnspan=2, sticky="nwe", pady=5, padx=5)
    
    def snippetFileChooserCallback(self):
        self.file.set(filedialog.askopenfilename())

    def submitButtonCallback(self):
        f = open(self.file.get())
        jsonFile = json.loads(f.read())
        self.name.set(list(jsonFile.keys())[0])
        # print(type(snippetsDict[self.name.get()]))
        snippetsDict[self.name.get()] = {}
        snippetsDict[self.name.get()]["hotkey"] = self.hotKey.get()
        snippetsDict[self.name.get()]["description"] = jsonFile[self.name.get()]["description"]
        snippetsDict[self.name.get()]["name"] = jsonFile[self.name.get()]["name"]
        snippetsDict[self.name.get()]["usage"] = jsonFile[self.name.get()]["usage"]
        f = open(srcPath / "snippets.json", "w")
        f.write(json.dumps(snippetsDict))
        f.close()
        reloadOnNew()
        self.destroy()

class rebindForm(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Rebind Hotkey")

class topBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.leftLabel = customtkinter.CTkLabel(self, text="Snippet", font=("Montserrat", 18))
        self.leftLabel.grid(row=0, column=0, sticky="w", pady = 5, padx = 5)
        self.aboutButton = customtkinter.CTkButton(self, text="About", font=("Montserrat", 15), width=70, fg_color="transparent", text_color=("black", "white"), hover_color=self._bg_color, command=self.aboutButtomCallback)
        self.aboutButton.grid(row=0, column=1, padx=5, sticky="e")
        self.newButton = customtkinter.CTkButton(self, text="New", font=("Montserrat", 15), width=70, command=self.newButtonCallback)
        self.newButton.grid(row=0, column=2, padx=5, sticky="e")
        self.newButtonForm = None
    
    def newButtonCallback(self):
        # filename = filedialog.askopenfilename()
        # print(self)
        if self.newButtonForm == None or not self.newButtonForm.winfo_exists():
            self.newButtonForm = NewButtonForm()
            self.newButtonForm.focus()
        else:
            self.newButtonForm.focus()
    
    def aboutButtomCallback(self):
        webbrowser.open("https://github.com/IANYEYZ/Snippet")

class snippetFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, description):
        super().__init__(master)
        self.ttitle = title
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.titleLabel = customtkinter.CTkButton(self, text=title, font=("Montserrat", 15, "bold"), fg_color=self.cget("fg_color"), text_color=("black", "white"), hover=False, command=self.titleLabelCallback)
        self.titleLabel.grid(row=0, column=0, sticky="w", pady = 5, padx = 5)
        self.descriptionLabel = customtkinter.CTkLabel(self, text=description, font=("Montserrat", 12))
        self.descriptionLabel.grid(row=1, column=0, sticky="w", pady = 5, padx = 5)
        self.rebindButton = customtkinter.CTkButton(self, text="Rebind", font=("Montserrat", 15), width=70, command=self.rebindButtonCallback)
        self.rebindButton.grid(row=0, rowspan=2, column=1, padx=5, sticky="e")
        self.deleteButton = customtkinter.CTkButton(self, text="Delete", font=("Montserrat", 15), fg_color="#e53935", hover_color="#d32f2f", width=70, command=self.deleteButtonCallback)
        self.deleteButton.grid(row=0, rowspan=2, column=2, padx=5, sticky="e")
    
    def rebindButtonCallback(self):
        originalHotkey = snippetsDict[self.ttitle]["hotkey"]
        self.rebindForm = customtkinter.CTkInputDialog(text="New Hotkey", title=f"Rebind Hotkey for {self.ttitle}")
        newHotkey = self.rebindForm.get_input()
        if not newHotkey: newHotkey = originalHotkey
        snippetsDict[self.ttitle]["hotkey"] = newHotkey
        f = open(srcPath / "snippets.json", "w")
        f.write(json.dumps(snippetsDict))
    
    def deleteButtonCallback(self):
        snippetsDict[self.ttitle] = {}
        snippetsDict.pop(self.ttitle)
        f = open(srcPath / "snippets.json", "w")
        f.write(json.dumps(snippetsDict))
        f.close()
        reloadOnNew()
    
    def titleLabelCallback(self):
        if not snippetsDict[self.ttitle]["usage"]:
            return
        else:
            webbrowser.open(srcPath / self.ttitle / snippetsDict[self.ttitle]["usage"])

class snippetContainer(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=750)
        self.grid_columnconfigure(0, weight=1)
        self.snippetList = []
        for i, key in enumerate(snippetsDict):
            # self.snippetList.append(value)
            # value.grid(row = i, column = 0, padx = 10, pady = 5, sticky = "w")
            snippet = snippetFrame(self, key, snippetsDict[key]["description"])
            self.snippetList.append(snippet)
            snippet.grid(row=i, column=0, padx=10, pady=5, sticky="nwe")
        
    def reloadOnNew(self):
        for i in self.winfo_children():
            i.destroy()
        self.snippetList = []
        for i, key in enumerate(snippetsDict):
            # self.snippetList.append(value)
            # value.grid(row = i, column = 0, padx = 10, pady = 5, sticky = "w")
            snippet = snippetFrame(self, key, snippetsDict[key]["description"])
            self.snippetList.append(snippet)
            snippet.grid(row=i, column=0, padx=10, pady=5, sticky="nwe")

class mainPart(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.topLabel = customtkinter.CTkLabel(self, text="Welcome to Snippet", font=("Montserrat", 25))
        self.topLabel.grid(row=0, column=0, sticky="w", pady=5, padx=10)
        # self.testSnippet = snippetFrame(self, "Math Pie", "Do symbolic calculation anywhere")
        # self.testSnippet.grid(row=1, column=0, sticky = "w", pady=5, padx=10)
        self.snippetContainer = snippetContainer(self)
        self.snippetContainer.grid(row=1, column=0, sticky="nswe", pady=5, padx=10)
    
    def reloadOnNew(self):
        self.snippetContainer.reloadOnNew()

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global width, height
        # print(width, height)
        self.geometry(f"{width}x{height}+0+0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.entry = customtkinter.CTkEntry(self, height=38, font=("Montserrat", 15))
        self.entry.grid(column = 0, row = 0, sticky="swe", pady = 45)
        self.entry.bind("<Return>", self.entryCallback)

        self.configure(fg_color="#000000")
    
    def entryCallback(self, event):
        name = self.entry.get()
        if not (name in snippetsDict.keys()): 
            self.destroy()
            return
        snippetFileName = snippetsDict[name]["name"]
        f = open(srcPath / snippetFileName, "r")
        snippetFile = f.read()
        if snippetFile == "":
            return
        runSnippet(snippetFile, 0)
        self.destroy()

class App(customtkinter.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Snippet")
        self.geometry("800x480")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.topBar = topBar(self)
        self.topBar.grid(row=0, column=0, sticky="nwe")

        self.mainPart = mainPart(self)
        self.mainPart.grid(row=1, column=0, sticky="nswe")
        # self.form = ToplevelWindow(self)
    
    def reloadOnNew(self):
        self.mainPart.reloadOnNew()

def create():
    form = ToplevelWindow(app)
    form.lift()
    form.overrideredirect(True)
    form.attributes("-alpha", 0.5)

registerAll()

app = App()

keyboard.add_hotkey("ctrl+alt+i", create)

width = app.winfo_screenwidth()
height = app.winfo_screenheight()

app.mainloop()