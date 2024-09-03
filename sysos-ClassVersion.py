"""
This code below is not made to replace the full functionality 
of an operating system, it is experimental and is made to spark 
your imagination. Please use it as such.
"""
#Import necessary modules
import time, random
import pyautogui as typer
from tqdm import tqdm
from os import system as run
import os
import sys
import difflib
import json
from termcolor import *

#Define variables
vsn = "2.1.2-Beta"           #The SYSOS version

ThrottleSpeed = 0       #How fast the computer can go through operations
cfgvsn = 1.0            #The version of the configuration tool
GITHUB = "https://github.com/jomielec/SYSOS/issues" #The name of the github repository
FirstTimeRunning = True #Is this the first time the program has been run?
modules = ["time", "random", "numpy", "json"]       #The list of used modules
CurrentCommands = ["con", "move", "dir", "wipe", "bam", "ch", "make", "rmv", "run", "view", "sysos", "errtest"] #The list of the current commands being used
SupportedFileExtensions = [".text", ".txt"]                                                                     #The list of supported file extensions
CmdPreset = "SYSOS Commands"    #The active command preset
SysosCommands = ["con", "move", "dir", "wipe", "bam", "ch", "make", "rmv", "run", "open", "sysos"]  #The list of (inactive) default SYSOS commands for switching presets
UnixCommands = ["ls", "cd", "pwd", "clear", "exit", "ch", "touch", "rm", "run", "open", "sysos"]    #The list of (inactive) Unix commands for switching presets




Directory = "/user/main"    #Current directory
LsCache = {}                #Directory content (for the "ls" command)

OUTPUT_COLORS = {"Error": "red", "Warning": "yellow", "SystemOut": "cyan", "Advice": "magenta", "Other": "white", "cPrompt": "dark_grey"}   #The colors for different types of output
FILE_COLORS = {"Direc": "blue", "Text": "magenta", "Runable": "green"}                                                                      #The colors for different types of files

#Define system classes
class necessaryFunctions():
    # def updatePrompt(self, username, version):
    #     """Updates the prompt to be displayed according to its formatted values
    #     """
    #     global prompt
    #     prompt = colored(f"{username}@SYsos{version}", "green") + colored(" $ ", "blue")        #Update the prompt to be displayed

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
        global usrN
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
if "--skipBackup" not in sys.argv[0:]:      #Run the system startup commands
    try:
        print(f"Loading SYSOS version {vsn}...")
        for i in tqdm(range (2), desc="Running systen scripts", ascii=True): time.sleep(random.randint(0,2))
        system.setCommandHelp()
        system.update_Colors()

        for i in tqdm(range (100), desc=f"Loading commands for {sys.platform} architectures...", ascii=True): time.sleep(random.uniform(0.01, 0.02))
        time.sleep(1)
        Computer = sys.platform
        if Computer == "win32":
            OperatingSystem = "Windows"
            clear = "cls"
        else:
            OperatingSystem = "Unix"
            clear = "clr"
        try:
            with open("user.sysos", "r+") as f:
                global usrN
                temp = json.load(f)
                usrN = temp["Username"]
        except Exception:
            with open("user.sysos", "w+") as f:
                usrN = input(colored("Enter your username: ", "black", f"on_{cPrompt}"))        #Save the username to a variable
                json.dump({"Username": usrN}, f)
        

    except Exception as e:
        system.reportError(message="Error while loading", code=e)
else:
    system.setCommandHelp()
    system.update_Colors()

#Define Function classes
class listContents():       #Default: con
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
                elif CTemp == SupportedFileExtensions[0] or CTemp == SupportedFileExtensions[1]:
                    ColorFiles.append(colored(key, Text))
            index += 1
        return ColorFiles
    
    def run(self, prt=True, colors=False, showExtensions=False):
        """Saves the contents of the current directory to DirContent

        Args:
            prt (bool, optional): If true, then it will print the contents as well as returning them. Defaults to True.

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
            if colors:
                print(f"Text documents:\t {colored(Text.capitalize(), Text)}")
                print(f"Directories:\t {colored(Direc.capitalize(), Direc)}\n")

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

class makeFile():           #Default: make
    def run(self, ipt):
        """Makes a file in the list of files, as well as a text file.

        Args:
            i (String): The desired file name.
        """
        WholeFile = system.getArgs(ipt)[0]
        Name = WholeFile.split('.')[0]
        try:
            ValidExtensions = SupportedFileExtensions
            Extension = str('.' + WholeFile.split('.')[1])
            
            if Extension not in ValidExtensions:
                system.reportError(f"File does not have a valid extension.>\n* Please choose a valid extension: <{SupportedFileExtensions}", code=f"Invalid file extension: {Extension}")
                
            else:
                # print(WholeFile, ''.join(WholeFile))

                files[Name] = list([Directory, Extension])
                con.run()
                with open(''.join(WholeFile), "w") as f:
                    f.write(f"FILE CREATED AT {time.strftime("%Y-%m-%d %H:%M")}\n")

                with open("files.sysos", "w+") as f:
                    json.dump(files, f)
                
                

        except Exception:
            files[f"{Name}"] = list([Directory, "Direc"])
            con.run()
            with open("files.sysos", "w+") as f:
                json.dump(files, f)
make = makeFile()

class removeFile():         #Default: rmv
    def run(self, file):
        try:
            if system.getArgs(file)[0].split('.')[0] in files and f'.{system.getArgs(file)[0].split('.')[1]}' in files[system.getArgs(file)[0].split('.')[0]][1]:
                del files[system.getArgs(file)[0].split('.')[0]]
                os.remove(' '.join(system.getArgs(file)))
                with open("files.sysos", "w+") as f:
                    json.dump(files, f)
                con.run()
            else:
                system.write(colored(f'No such file or directory: {system.getArgs(file)[0]}', Error))
                print(system.getArgs(file)[0].split('.')[0])
                print(files[system.getArgs(file)[0].split('.')[0]][1])
        except IndexError:
            system.write(colored(f'WARNING! Command \'{CurrentCommands[7]}\' needs a parameter', Warning))
rmv = removeFile()

class runCommand():         #Default: run
    def run(self, command):
        """Runs the inputted command in the system shell.

        Args:
            command (str): The raw shell input
        """
        if system.getArgs(command) != []:
                run(' '.join(system.getArgs(command)))
        else:
            system.write(colored(f'WARNING! Command \'{CurrentCommands[8]}\' needs a parameter', Warning))
runCmd = runCommand()

class ViewFile():           #Default: view
    def run(self, ipt):
        fileToView = system.getArgs(ipt)[0]
        with open(fileToView, 'r') as f:
            print(f.read())

        if fileToView not in files.keys():
            system.reportError("File does not exits")
view = ViewFile()

try:                        #Attempt to clear shell output
    if OperatingSystem == "Windows":
        os.system("cls")
    elif OperatingSystem == "Unix":
        os.system("clear")
except Exception as e:      #If unable, report error
    system.reportError("Unable to clear shell output.", code=e)
    system.write(colored(f"Maybe program was run with '{colored("--skipBackup", SystemOut)}{colored("' flag?", Error)}", Error))

try:
    with open("files.sysos", "r") as f:
        files = json.load(f)
except FileNotFoundError:
    system.write(colored("Could not load files from filesystem backup file.", Error),
                 colored("Would you like to create a new archive instead? [y/N]", Error))
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
    if response == 'y':
        files = {"docs": ["/user/main", "Direc"], "Test": ["/user/main", ".txt"], "user": ["/", "Direc"], "main": ["/user", "Direc"]}  #The internal files cache 
        with open('files.sysos', "w+") as f:
            json.dump(files, f)
    else:
        system.reportError("SYSOS IS CORRUPTED! PLEASE DO NOT CONTINUE TO USE, YOU MAY DAMAGE YOUR SYSTEM!", code="Backup file not found")


while True: 
    try:
        prompt = colored(f"{usrN}@SYsos{colored(vsn, 'light_cyan')}", "green") + colored(" $ ", "blue")        #Update the prompt to be displayed
        response = input(prompt)

        if system.getFunction(response) not in CurrentCommands:
            system.CommandNotFound(response, errID="Invalid command!")
            print(system.didYouMean(response))

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
            try:
                ch.run(response)

            except Exception as e:
                system.reportError(message="Error detected during renaming process")

        elif system.getFunction(response) == CurrentCommands[6]:        #Default: Make
            try:
                make.run(response)
            except Exception as e:
                system.reportError(message="Unable to touch file, (\"Can't touch this.\")", code=e)

        elif system.getFunction(response) == CurrentCommands[7]:        #Default: Rmv
            try:
                rmv.run(response)
            except Exception as e:
                system.reportError(message="Error detected during file deletion", code=e)

        elif system.getFunction(response) == CurrentCommands[8]:        #Default: Run
            try:
                runCmd.run(response)
            except Exception as e:
                system.reportError(message="Unable to run desired command in system shell", code=e)

        elif system.getFunction(response) == CurrentCommands[9]:        #Default: View
            try:
                view.run(response)
            except Exception as e:
                system.reportError(message="Unable to locate file", code=e)

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