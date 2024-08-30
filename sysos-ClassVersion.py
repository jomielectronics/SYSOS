"""
This code below is not made to replace the full functionality 
of an operating system, it is experimental and is made to spark 
your imagination. Please use it as such.
"""
#Import necessary modules
import time, random
from tqdm import tqdm
from os import system as run
import os
import sys
import difflib
import json
from termcolor import *

#Define variables
vsn = "2.0.2 Beta"           #The SYSOS version

ThrottleSpeed = 0       #How fast the computer can go through operations
cfgvsn = 1.0            #The version of the configuration tool
usrN = "SYSOS.User"     #The name of the user
GITHUB = "https://github.com/jomielec/SYSOS/issues" #The name of the github repository
FirstTimeRunning = True #Is this the first time the program has been run?
prompt = colored(f"{usrN}@SYsos", "green") + colored(" $ ", "blue") #The prompt to be displayed
modules = ["time", "random", "numpy", "json"]       #The list of used modules
CurrentCommands = ["con", "move", "dir", "wipe", "bam", "ch", "make", "rmv", "run", "view", "sysos", "errtest"] #The list of the current commands being used

CmdPreset = "SYSOS Commands"    #The active command preset
SysosCommands = ["con", "move", "dir", "wipe", "bam", "ch", "make", "rmv", "run", "open", "sysos"]  #The list of (inactive) default SYSOS commands for switching presets
UnixCommands = ["ls", "cd", "pwd", "clear", "exit", "ch", "touch", "rm", "run", "open", "sysos"]    #The list of (inactive) Unix commands for switching presets

files = {"docs": ["/user/main", "Direc"], "Test.text": ["/user/main", "Text"], "user": ["/", "Direc"], "main": ["/user", "Direc"]}  #The internal files cache 
if FirstTimeRunning:                     #If first time running…
    with open("files.sysos", "w+") as f: #then open files.sysos…
        json.dump(files, f)              #and save the internal files to the disk


Directory = "/user/main"    #Current directory
LsCache = {}                #Directory content (for the "ls" command)

OUTPUT_COLORS = {"Error": "red", "Warning": "yellow", "SystemOut": "cyan", "Advice": "magenta", "Other": "white", "cPrompt": "dark_grey"}   #The colors for different types of output
FILE_COLORS = {"Direc": "blue", "Text": "magenta", "Runable": "green"}                                                                      #The colors for different types of files

#Define system classes
class necessaryFunctions():
    def setCommandHelp(self):
        """
        Creates a dictionary of command names (in-case they change) and what they do
        """
        global CMDHelp
        CMDHelp = {CurrentCommands[0]: "Lists the contents of the current directory", 
                CurrentCommands[1]: "Changes the current directory", 
                CurrentCommands[2]: "Lists the current directory", 
                CurrentCommands[3]: "Clears the system output", 
                CurrentCommands[4]: "Returns to your default terminal", 
                CurrentCommands[5]: "A generic command that can: \n- Rename documents \n- Edit the commands\n- Change your username", 
                CurrentCommands[6]: "This command can make files and folders", 
                CurrentCommands[7]: "Can delete any thing from files to folders", 
                CurrentCommands[8]: "Runs the command entered in the default terminal", 
                CurrentCommands[9]: "Displays the contents of a file",
                CurrentCommands[11]: "Runs the sub-routines that catch errors, in order to ensure functionality. \nGood to run every once and a while."}
        
    def clearOutputLines(self, lines):
        if lines == 'a':
            if str(sys.platform) == "win32":
                os.system("cls")
            else:
                os.system("clear")
        else:
            for i in range(0, int(lines)):
                print ("\033[A                             \033[A")

    def update_Colors(self):
        """
        This function updates each variable with the current color for that type.
        """
        global Error, Warning, SystemOut, Advice, Other, cPrompt, Direc, Text, Runable
        #Colors:
        Error = OUTPUT_COLORS["Error"]
        Warning = OUTPUT_COLORS["Warning"]
        SystemOut = OUTPUT_COLORS["SystemOut"]
        Advice = OUTPUT_COLORS["Advice"]
        Other = OUTPUT_COLORS["Other"]
        cPrompt = OUTPUT_COLORS["cPrompt"]
        #File colors:
        Direc = FILE_COLORS["Direc"]
        Text = FILE_COLORS["Text"]
        Runable = FILE_COLORS["Runable"]

    def CommandNotFound(self, ipt, errID="Invalid CMD Error"):
        print(colored("*", Error))
        print(colored(f"*{errID}!", Error))
        print(colored(f"*Command \"{ipt}\" not found.", Error))
        print(colored("*         ", Error), end="")
        for i in range(0, len(ipt)):
            print(colored("^", Error), end="")
        print()
        print(colored("*", Error))

    def didYouMean(self, item, matches=CurrentCommands):
        """Returns a colored message if `item` is not found in the list of commands.

        Args:
            item (string): The misspelled command.
            matches (list, optional): The list of options to choose from. Defaults to Commands.

        Returns:
            String: The colored error message.
        """
        fix = difflib.get_close_matches(item, matches)
        if fix != []:
            return colored("Maybe you meant '" + colored(', '.join(fix), Advice, attrs=["bold"])+ colored("'?", Advice), Advice, attrs=[])
        else:
            return colored("No fixes available.", Advice)

    def getArgs(self, idx):
        """ Gets the arguments of a given prompt.

        Args:
            idx (string): The input entered by the user.

        Returns:
            RAW: a list of the arguments entered by the user.
        """
        raw = idx.split(" ")
        return raw[1:]

    def getFunction(self, idx):
        """ Gets the function of a given prompt.

        Args:
            idx (string): The input entered by the user.

        Returns:
            RAW: a string (the function name) entered by the user.
        """
        raw = idx.split()
        return raw[0]
    
    def getSettings(self):
        """Returns the system settings in a dictionary

        Returns:
            Dict: The system settings
        """ 
        sett = {"Commands": CurrentCommands,
                "Output Colors": OUTPUT_COLORS,
                "File Colors": FILE_COLORS}
        return sett
    
    def reportError(self, message, code, exit=False):
        """Creates a nicely formatted error message
        
        Args:
            message (str): The error message
            code (str): The error code
            exit (bool, optional): Wether or not to exit the program. Defaults to True.

        Returns:
            None (null): I forget what this does
        """
        print(colored(f"* FATAL INTERNAL ERROR!\n* PLEASE REPORT ISSUE ON GITHUB REPO ({GITHUB})\n* Exit status: <{message}> Compiler: <{code};> ", Error))
        if exit == True:
            sys.exit(1)
        else:
            return None
        
    @staticmethod
    def write(*ipt):
        """Displays a neatly formatted message to the console.
        
        """
        print("*")
        for i in ipt:
            print(f"* {i}")
        print("*")

    def prompt(self, idx):
        if idx == "RootUserError":
            self.write(colored("WARNING!", Warning), colored("The action you are about to take is reserved for ROOT users. Are you sure you want to continue?", Warning))
            if input().lower().startswith("y"):
                return "continue"
            
    def changeUserName(self):
        """Changes the username of the user.
        
        """
        self.write(colored("Are you sure you want to change your username? [y/n]", Warning))
        ans = input()
        if ans == "y":
            
            usrN = input(colored("Enter your new username: ", "black", f"on_{cPrompt}"))
            self.write(colored(f"Your username has been changed to {usrN}.", SystemOut))
        elif ans == "n":
            self.write(colored("No changes made.", SystemOut))
        else:
            self.write(colored("Invalid input.", Error))
            print(self.didYouMean(ans, ["y", "n"]))

    class typingFunctions():
        def typingPrint(self, text, end="\n"):
            """Create a smooth typing action
            
            Args:
                text (str): The text to be typed
                end (str, optional): _description_. Defaults to "\n".
            """
            text += end  
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(ThrottleSpeed)
  
        def typingInput(self, text):
            """Creates the same typing action as typingPrint(), but for input
            
            Args:
                text (str): The text to print

            Returns:
                str: The value inputted by the user
            """
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(ThrottleSpeed)
            value = input()
            return value

#Create system class instances
system = necessaryFunctions()
typing = system.typingFunctions()

#Load everything
if "--skipBackup" not in sys.argv[0:]:
    try:
        print(f"Loading SYSOS version {vsn}...")
        for i in tqdm(range (2), desc="Running systen scripts"): time.sleep(random.randint(0,2))
        system.setCommandHelp()
        system.update_Colors()

        for i in tqdm(range (100), desc=f"Loading commands for {sys.platform} architectures..."): time.sleep(random.uniform(0.01, 0.02))
        time.sleep(1)
        Computer = sys.platform
        if Computer == "win32":
            OperatingSystem = "Windows"
            clear = "cls"
        else:
            OperatingSystem = "Unix"
            clear = "clr"
        usrN = input(colored("Enter your username: ", "black", f"on_{cPrompt}"))

    except Exception as e:
        system.reportError(message="Error while loading", code=e)
else:
    system.setCommandHelp()
    system.update_Colors()

#Define Function classes
class listContents():       #Default: Con
    def colorize(self, input):
        """Adds colors to the Ls() output, but it may work for other functions
        
        Args:
            input (list): Needs to be the DirContent list of dictionaries.

        Returns:
            List: Use this to nest in a parameter of a function.
        """
        ColorFiles = []
        index = 0
        while index < len(input):
            for key in input[index].keys():
                CTemp = input[index][key]
                if CTemp == "Direc":
                    ColorFiles.append(colored(key, Direc))
                elif CTemp == "Text":
                    ColorFiles.append(colored(key, Text))
            index += 1
        return ColorFiles
    
    def run(self, prt=True):
        """Saves the contents of the current directory to DirContent

        Args:
            prt (bool, optional): If true, then it will print the contents as well. Defaults to True.

        Returns:
            List: Returns the contents of the current directory
        """
        DirContent = []
        for item in files.keys():
            if files[item][0] == Directory:
                TmpDic = {item: files[item][1]}
                DirContent.append(TmpDic)
            TmpDic = {}
        #colorize(DirContent)
        #write(" ".join(ColorFiles))
        if prt:
            print(" ".join(self.colorize(DirContent)))
        else:
            return DirContent 
con = listContents()

class changeDirectory():    #Default: move
    def run(self, destination):
        global Directory
        prompt = system.getArgs(destination)
        if prompt == []:
            system.write(colored(f"WARNING! Command \"{CurrentCommands[1]}\" needs a parameter", Warning))
            type(Directory)
        elif "".join(prompt) == "up":
            tmp = Directory.split("/")
            del tmp[-1]
            tmp = "/".join(tmp)
            Directory = tmp
            print(colored(Directory, Direc))
        elif "".join(prompt) in [k for d in con.run(False) for k in d.keys()]:
                Directory += f"/{prompt[0]}"
                print(colored(Directory, Direc))
        elif "".join(prompt) not in [k for d in con.run(False) for k in d.keys()]:
            system.write(colored("No such directory", Error))
move = changeDirectory()

class CurrentDirectory():   #Default: dir
    def run():
        """Prints the current directory to the console
        """
        print(colored(Directory, SystemOut))
dir = CurrentDirectory()

class makeFile():           #Default: make
    def run(self, i):
        """Makes a file in the list of files, as well as a text file.

        Args:
            i (String): The desired file name.
        """
        try:
            prompt = system.prompt
            filen = f"{prompt[0]}.{prompt[1].lower()}"
            files[filen] = list([Directory, prompt[1].capitalize()])
            with open(f"{prompt[0]}.txt", "w") as f:
                f.write(f"FILE CREATED AT {time.strftime("%Y-%m-%d %H:%M")}\n")
        except IndexError:
            files[f"{prompt[0]}"] = list([Directory, "Direc"])
        listContents.run()
make = makeFile()

class clearOutput():        #Default: wipe
    def run(self):
        """Clears the output of the program
        """
        if OperatingSystem == "Windows":
            os.system("cls")
        elif OperatingSystem == "Unix":
            os.system("clear")
wipe = clearOutput()

class endProgram():         #Default: bam
    def run(self):
        raise SystemExit
bam = endProgram()

class changer():            #Default: ch
    def run(self, index):
        prompt = system.getArgs(index)
        if prompt == []:
            system.write(colored(f'WARNING! Command \'{CurrentCommands[5]}\' needs a parameter', Warning))

        if prompt == ['usern']: system.changeUserName()
        if prompt[0] == 'cmds':
            if '-super' not in prompt:

                if prompt('RootUserError') == 'continue':
                    print(colored('LISTING CurrentCommands:', SystemOut))

                    for i in range(0, len(CurrentCommands)):
                        print(colored(CurrentCommands[i], SystemOut, attrs=['bold']), end=colored(', ', SystemOut, attrs=['bold']))
                        time.sleep(0.1)
                    print()

                    editCmd = typing.typingInput(colored('Command to edit: ', cPrompt))

                    if editCmd == '': pass

                    elif editCmd == 'done': flag = 'done'; pass

                    elif editCmd not in CurrentCommands:
                        system.CommandNotFound(editCmd)
                        print(system.didYouMean(editCmd))

                    changeCmd = input(colored(f'Change \'{editCmd}\' to: ', cPrompt))
                    CurrentCommands[CurrentCommands.index(editCmd)] = changeCmd
                    system.setCommandHelp()

            elif '-super' in prompt:
                print(colored('LISTING CurrentCommands:', SystemOut))

                for i in range(0, len(CurrentCommands)):
                    print(colored(CurrentCommands[i], SystemOut, attrs=['bold']), end=colored(', ', SystemOut, attrs=['bold']))
                print()
                editCmd = input(colored('Command to edit: ', cPrompt))

                if editCmd == '': pass
                elif editCmd == 'done': flag = 'done'; pass
                elif editCmd not in CurrentCommands:
                    system.CommandNotFound(editCmd)
                    print(system.didYouMean(editCmd))
                changeCmd = input(colored(f'Change \'{editCmd}\' to: ', cPrompt))
                CurrentCommands[CurrentCommands.index(editCmd)] = changeCmd
                system.setCommandHelp()
ch = changer()

try:
    if OperatingSystem == "Windows":
        os.system("cls")
    elif OperatingSystem == "Unix":
        os.system("clear")
except Exception as e:
    system.reportError("Unable to clear shell output.", code=e)
    system.write(colored(f"Maybe program was run with '{colored("--skipBackup", SystemOut)}{colored("' flag?", Error)}", Error))

while True: 
    try:
        response = input(prompt)
        if system.getFunction(response) not in CurrentCommands:
            system.CommandNotFound(response, errID="Invalid command!")
            system.didYouMean(item=response)
        elif system.getFunction(response) == CurrentCommands[0]:        #Default: Con
            try:
                con.run()
            except Exception as e:
                system.reportError(message="Unable to list contents", code=e)

        elif system.getFunction(response) == CurrentCommands[1]:        #Default: Move
            try:
                move.run(destination=response)
            except Exception as e:
                system.reportError(message="Error during directory transposition", code=e)

        elif system.getFunction(response) == CurrentCommands[2]:        #Default: Dir
            try:
                dir.run()
            except Exception as e:
                system.reportError(message="Directory name not found or invalid", code=e)
        
        elif system.getFunction(response) == CurrentCommands[3]:        #Default: Wipe
            try:
                wipe.run()
            except Exception as e:
                system.reportError(message="Unable to clear program output", code=e)
        
        elif system.getFunction(response) == CurrentCommands[4]:        #Default: Bam
            try:
                bam.run()
            except Exception as e:
                system.reportError(message="Problem with sysos exit. (Sorry 'bout that!)", code=e)

        elif system.getFunction(response) == CurrentCommands[5]:        #Default: Ch
            ch.run(response)
    except Exception as e:
        system.reportError(message="Error during matchmaking", code=e)
    except KeyboardInterrupt: #CTRL+C Pressed
        system.write(colored("CTRL+C pressed, data may be lost in case of improper shutdown!", Error), 
                     colored(f"The proper way to shutdown is run '{colored(CurrentCommands[4], SystemOut)}{colored("' in the console!", Error)}", Error), 
                     colored("Are you sure you want to continue? [y/N]", Error))
        while True:
            response = input('> ')
            if response in ['y', 'N']: break
            else: 
                typing.typingPrint(colored("Invalid input!", Error)); 
                time.sleep(1)
                system.clearOutputLines(2)
        if response == 'y':
            sys.exit(1)
        else:
            continue