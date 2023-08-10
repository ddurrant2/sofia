from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import subprocess
import re
import webbrowser
import pathlib

version = "v0.8 Alpha"
WIN_HEIGHT = 540
WIN_WIDTH = 960
COL_MAX = 11

WINDOW_BAR = '#3F58C8'
WINDOW_BAR_TEXT = '#FFFFFF'
UPPER_NOTEBOOK_FILLER = '#95A1DB'
UPPER_TAB_INACTIVE = '#BAC6FF'
UPPER_TAB_ACTIVE = '#F0F3FF'
LOWER_NOTEBOOK_OUTLINE = '#6471A8'
ACTIVE_TAB_TEXT = '#000000'
FLAG_FILLER_TEXT = '#CACCD6'
BUILD_BUTTON_FILLER = '#BAC6FF'
BUILD_BUTTON_TEXT = '#000000'
STANDARD_BG = '#F0F3FF' 


class GUI:
    """
    The GUI class creates and maintains all Tkinter features of the app.
    """

    def __init__(self, json_file):
        # self.TestJson(json_file)
        self.json = json_file
        """Initializes and creates the Tkinter window and Notebook sections"""
        root = Tk()
        #Set document style
        s = ttk.Style()
        s.theme_create("yummy", parent="alt", settings={
            "Lower.TNotebook": {"configure": {"background": STANDARD_BG, "bordercolor": LOWER_NOTEBOOK_OUTLINE}},
            "Upper.TNotebook": {"configure": {"background": UPPER_NOTEBOOK_FILLER, "bordercolor": LOWER_NOTEBOOK_OUTLINE}},
            "TNotebook.Tab": {
                "configure": {"background": UPPER_TAB_INACTIVE, "bevelamount": 0},
                "map": {"background": [("selected", UPPER_TAB_ACTIVE)]}
            },
            "TFrame": {"configure": {"background": STANDARD_BG}},
            "TLabel": {"configure": {"background": STANDARD_BG}},
            "Info.TFrame": {"configure": {"background": UPPER_NOTEBOOK_FILLER}},
        })
        s.theme_use("yummy")

        root.geometry("+25+25")
        root.configure(background=UPPER_NOTEBOOK_FILLER,
                       width=WIN_WIDTH, height=WIN_HEIGHT)
        root.option_add('*tearOff', False)
        root.title("SOFIA - Support Over FIA")
        root.resizable(False, False)
        try:
            icon = PhotoImage(
                file=os.path.join(os.path.dirname(__file__), "squarelogo.gif"))  # file="C:\\Users\\ddurrant\\Documents\\squarelogo.gif"
            root.iconphoto(True, icon)
        except:
            pass
        self.notebook = ttk.Notebook(root, style="Upper.TNotebook")
        self.notebook.grid(sticky='ew')
        self.SetupWindows(root)
        self.SetupCommandBuilder()
        self.SetupLower()
        self.SetupHash()
        self.SetupCVEParse()

        root.mainloop()

    def TestJson(self, json_file):
        for key, value in json_file.items():
            print(json_file[key]["title"])
            f'The {json_file[key]["title"]} command has the following flags:'
            for flag in json_file[key]["flags"]:
                print(f'{flag[0]}{"*" if flag[1] == True else ""}: {flag[2]}')

    def SetupWindows(self, root):
        """Initializes frames for each tab"""
        # Info footer
        self.infoFooter = ttk.Frame(root, style="Info.TFrame")
        # Create frames for each tab
        self.lowerFrame = ttk.Frame(self.notebook)
        self.hashFrame = ttk.Frame(self.notebook)
        self.commandBuilderFrame = ttk.Frame(self.notebook)
        self.cveBodySearchFrame = ttk.Frame(self.notebook)

        # add frames to notebook with tab names
        self.notebook.add(self.commandBuilderFrame, text="Command Builder")
        self.notebook.add(self.lowerFrame, text="Lower()")
        self.notebook.add(self.hashFrame, text="Hash a File")
        self.notebook.add(self.cveBodySearchFrame, text="CVE Body Search")

        # Add descriptions to each tab
        Label(self.lowerFrame, text="Find a Vendor Hash that's in caps? \nPaste it below to get the lower case version!", font=(
            "Helvetica", 12)).grid(pady=15, sticky='news')
        Label(self.hashFrame, text="Hash a file with ease! \nSelect your file below.", font=(
            "Helvetica", 12)).grid(pady=15, sticky='news')
        Label(self.commandBuilderFrame, text="Handy tool for crafting CLI commands!", font=(
            "Helvetica", 12), bg=STANDARD_BG).grid(padx=10, pady=15, sticky='news')
        Label(self.cveBodySearchFrame, text="Got a changelog with too many CVE's? \nPaste the whole body here and we'll give you a comma-separated list!",
              font=("Helvetica", 12)).grid(pady=15, sticky='news')
        self.infoFooter.grid()
        Label(self.infoFooter, background=UPPER_NOTEBOOK_FILLER,
              text=f"Created by Dillon Durrant - {version}").grid()

    def SetupLower(self):
        """Sets up and maintains the frame for lowering a file hash"""

        # Entry field where users will put their uppercase hashes
        Label(self.lowerFrame, text="Uppercase Hash:").grid(row=1, column=0)
        self.upperText = StringVar()
        self.upper = Entry(
            self.lowerFrame, textvariable=self.upperText, width=64)
        self.upper.grid(row=3, column=0)

        # Button that carries out the .lower() method
        self.lowerButton = ttk.Button(
            self.lowerFrame, text="Go!", command=self.LowerText)
        self.lowerButton.grid(row=4, column=0, pady=10)

        # Done message says that the operation is done.
        self.done = Label(self.lowerFrame)
        self.done.grid(row=5, column=0)

        # Displays the result of the .lower() method
        Label(self.lowerFrame, text="Lowercase Hash:").grid(row=6, column=0)
        self.result = Text(self.lowerFrame, height=1)
        self.result.grid(row=7, column=0, padx=10)

    def SetupHash(self):
        """Sets up and maintains the frame for retrieving file hashes"""
        # Set up frames inside window
        self.md5Frame = ttk.Frame(self.hashFrame)
        self.md5Frame.grid(row=3, column=0)
        self.sha1Frame = ttk.Frame(self.hashFrame)
        self.sha1Frame.grid(row=4, column=0)
        self.sha256Frame = ttk.Frame(self.hashFrame)
        self.sha256Frame.grid(row=5, column=0)

        # Set up label and button for finding file
        self.hashFileName = Label(self.hashFrame, text="No file selected")
        self.hashFileName.grid(row=1, column=0)
        self.hashButton = ttk.Button(
            self.hashFrame, text="Select File", command=self.HashFile)
        self.hashButton.grid(row=2, column=0)

        # Set up labels and fields for hash values
        Label(self.md5Frame, text="MD5: ").grid(row=0, column=0)
        Label(self.sha1Frame, text="SHA1: ").grid(row=0, column=0)
        Label(self.sha256Frame, text="SHA256: ").grid(row=0, column=0)
        self.md5Hash = Text(self.md5Frame, width=64, height=1)
        self.md5Hash.grid(row=0, column=1)
        self.md5Hash.insert(1.0, "NA")
        self.sha1Hash = Text(self.sha1Frame, width=64, height=1)
        self.sha1Hash.grid(row=0, column=1)
        self.sha1Hash.insert(1.0, "NA")
        self.sha256Hash = Text(self.sha256Frame, width=64, height=1)
        self.sha256Hash.grid(row=0, column=1)
        self.sha256Hash.insert(1.0, "NA")

    def SetupCVEParse(self):
        """Sets up and maintains the frame for retrieving list of CVEs from body text"""

        Label(self.cveBodySearchFrame, text="Input Text:").grid(row=1, column=0)
        self.bodyText = Text(self.cveBodySearchFrame, height=3, width=64)
        self.bodyText.grid(row=2, column=0)
        self.CVEparseButton = Button(
            self.cveBodySearchFrame, text="List CVEs", command=self.ParseCVEs)
        self.CVEparseButton.grid(row=3, column=0)
        Label(self.cveBodySearchFrame, text="CVEs Found:").grid(row=4, column=0)
        self.parsedText = Text(self.cveBodySearchFrame, height=3, width=64)
        self.parsedText.grid(row=5)

    def SetupCommandBuilder(self):
        """Sets up and maintains the frame for holding the notebook of different commands"""

        # set up notebook of commands
        self.commandNotebook = ttk.Notebook(self.commandBuilderFrame, style="Lower.TNotebook")
        self.commandNotebook.grid(sticky='ew', ipadx=10)

        # establish frames of notebook FOR
        self.commandFrames = []
        self.commandObjects = {}
        self.commandFlags = {}
        for key, value in self.json.items():
            self.commandFrames.append(ttk.Frame(self.commandNotebook))
            self.commandNotebook.add(
                self.commandFrames[-1], text=self.json[key]["title"])

            # Populate flag frames
            self.commandFlags[f"{self.json[key]['title']}"] = []
            for i, flag in enumerate(self.json[key]["flags"]):
                col = i // COL_MAX
                Label(self.commandFrames[-1], text=f'{flag[0]}*' if flag[1] == True else flag[0], background=STANDARD_BG).grid(
                    row=(i-(COL_MAX*col)), column=(col*4), padx=5, pady=5)
                self.commandFlags[f"{self.json[key]['title']}"].append(
                    Text(self.commandFrames[-1], height=1, width=32, highlightbackground=FLAG_FILLER_TEXT, highlightcolor=ACTIVE_TAB_TEXT, highlightthickness=1))
                self.commandFlags[f"{self.json[key]['title']}"][-1].grid(
                    row=(i-(COL_MAX*col)), column=(col*4)+1)
            self.commandObjects[f"{self.json[key]['title']}"] = self.json[key]

            Button(self.commandFrames[-1], text="Build!", command=lambda: self.Build(self.commandObjects[self.commandNotebook.tab(
                self.commandNotebook.select(), "text")]), background=BUILD_BUTTON_FILLER).grid(column=(col*3), sticky='ew', ipadx=10, ipady=5, pady=5)
        self.commandResults = Text(
            self.commandBuilderFrame, height=3, width=64)
        self.commandResults.grid(row=3, pady=5)

    def Build(self, comm):
        """Constructs a command for use in CLI"""
        isSuccessful = True
        commandList = f'{comm["prepend"]}'
        for j, c in enumerate(self.commandFlags[comm["title"]]):
            # if blank but required
            if c.get(1.0, "end").strip() == "" and comm["flags"][j][1] == True:
                commandList = f'Required flag missing: {comm["flags"][j][2]}'
                isSuccessful = False
                break
            # if blank but not required
            elif c.get(1.0, "end").strip() == "" and comm["flags"][j][1] == False:
                pass
            else:  # if not blank
                commandList += " "
                commandList += comm["flags"][j][2]
                commandList += f' "{c.get(1.0, "end").strip()}"'
        if isSuccessful:
            commandList += f' {comm["append"]}'
        self.commandResults.delete(1.0, "end")
        self.commandResults.insert(
            1.0, commandList)

    def LowerText(self):
        """Lowers text of file hash, then displays that value in the self.result field"""
        self.done.config(text="Done!")
        self.result.delete(1.0, "end")
        self.result.insert(1.0, self.upperText.get().lower())

    def HashFile(self):
        """Retrieves MD5, SHA1, and SHA256 hashes for selected file"""
        try:
            # Get file name from user
            self.filename = filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("executables", "*.exe"), ("all files", "*.*")))
            self.hashFileName.config(text=self.filename)

            # md5
            self.md5Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" md5', stdout=subprocess.PIPE)
            self.md5Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.md5Hash.delete(1.0, 2.0)
            self.md5Hash.delete(3.0, "end")

            # SHA1
            self.sha1Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" sha1', stdout=subprocess.PIPE)
            self.sha1Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.sha1Hash.delete(1.0, 2.0)
            self.sha1Hash.delete(3.0, "end")

            # SHA256
            self.sha256Hash.delete(1.0, "end")
            result = subprocess.run(
                f'certutil -hashfile "{self.filename}" sha256', stdout=subprocess.PIPE)
            self.sha256Hash.insert(1.0, result.stdout.decode('utf-8'))
            self.sha256Hash.delete(1.0, 2.0)
            self.sha256Hash.delete(3.0, "end")

        except:
            print("Not happening, sport.")

    def ParseCVEs(self):
        """Parses body text to find CVEs, deletes duplicates, then creates comma-separated list of CVEs"""

        self.parsedText.delete(1.0, "end")
        cveRegex = re.compile(r'CVE-\d+-\d+', re.VERBOSE)
        self.parsedText.insert(1.0, ', '.join(
            list(set(cveRegex.findall(self.bodyText.get(1.0, "end"))))))

