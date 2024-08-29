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
vsn = "2.0.0 Beta"           #The SYSOS versionc

ThrottleSpeed = 0       #How fast the computer can go through operations
cfgvsn = 1.0            #The version of the configuration tool
usrN = 'SYSOS.User'     #The name of the user
FirstTimeRunning = True #Is this the first time the program has been run?
prompt = colored(f'{usrN}@SYsos', 'green') + colored(' $ ', 'blue') #The prompt to be displayed
modules = ['time', 'random', 'numpy', 'json']       #The list of used modules
CurrentCommands = ['con', 'move', 'dir', 'wipe', 'bam', 'ch', 'make', 'rmv', 'run', 'view', 'sysos', 'errtest'] #The list of the current commands being used

CmdPreset = 'SYSOS Commands'    #The active command preset
SysosCommands = ['con', 'move', 'dir', 'wipe', 'bam', 'ch', 'make', 'rmv', 'run', 'open', 'sysos']  #The list of (inactive) default SYSOS commands for switching presets
UnixCommands = ['ls', 'cd', 'pwd', 'clear', 'exit', 'ch', 'touch', 'rm', 'run', 'open', 'sysos']    #The list of (inactive) Unix commands for switching presets

files = {'docs': ['/user/main', 'Direc'], 'Test.text': ['/user/main', 'Text'], 'user': ['/', 'Direc'], 'main': ['/user', 'Direc']}  #The internal files cache 
if FirstTimeRunning:                    #If first time running…
    with open('files.sysos', 'w+') as f: #then open files.sysos…
        json.dump(files, f)             #and save the internal files to the disk


Directory = '/user/main'    #Current directory
LsCache = {}                #Directory content (for the 'ls' command)

OUTPUT_COLORS = {'Error': 'red', 'Warning': 'yellow', 'SystemOut': 'cyan', 'Advice': 'magenta', 'Other': 'white', 'cPrompt': 'dark_grey'}   #The colors for different types of output
FILE_COLORS = {'Direc': 'blue', 'Text': 'magenta', 'Runable': 'green'}                                                                      #The colors for different types of files

#Define system classes
class necessaryFunctions():
    def setCommandHelp(self):
        """
        Creates a dictionary of command names (in-case they change) and what they do
        """
        global CMDHelp
        CMDHelp = {CurrentCommands[0]: 'Lists the contents of the current directory', 
                CurrentCommands[1]: 'Changes the current directory', 
                CurrentCommands[2]: 'Lists the current directory', 
                CurrentCommands[3]: 'Clears the system output', 
                CurrentCommands[4]: 'Returns to your default terminal', 
                CurrentCommands[5]: 'A generic command that can: \n- Rename documents \n- Edit the commands\n- Change your username', 
                CurrentCommands[6]: 'This command can make files and folders', 
                CurrentCommands[7]: 'Can delete any thing from files to folders', 
                CurrentCommands[8]: 'Runs the command entered in the default terminal', 
                CurrentCommands[9]: 'Displays the contents of a file',
                CurrentCommands[11]: 'Runs the sub-routines that catch errors, in order to ensure functionality. \nGood to run every once and a while.'}
        
    def update_Colors(self):
        """
        This function updates each variable with the current color for that type.
        """
        global Error, Warning, SystemOut, Advice, Other, cPrompt, Direc, Text, Runable
        #Colors:
        Error = OUTPUT_COLORS['Error']
        Warning = OUTPUT_COLORS['Warning']
        SystemOut = OUTPUT_COLORS['SystemOut']
        Advice = OUTPUT_COLORS['Advice']
        Other = OUTPUT_COLORS['Other']
        cPrompt = OUTPUT_COLORS['cPrompt']
        #File colors:
        Direc = FILE_COLORS['Direc']
        Text = FILE_COLORS['Text']
        Runable = FILE_COLORS['Runable']

    def NotFound(self, ipt, error='Invalid CMD Error'):
        print(colored('*', Error))
        print(colored(f'*{error}!', Error))
        print(colored(f'*Command \'{ipt}\' not found.', Error))
        print(colored('*         ', Error), end='')
        for i in range(0, len(ipt)):
            print(colored('^', Error), end='')
        print()
        print(colored('*', Error))

    def didYouMean(self, item, matches=CurrentCommands):
        """Returns a colored message if the item is not found in the list of commands.

        Args:
            item (string): The misspelled command.
            matches (list, optional): The list of options to choose from. Defaults to Commands.

        Returns:
            String: The colored error message.
        """
        fix = difflib.get_close_matches(item, matches)
        if fix != []:
            return colored(f"Maybe you meant '" + colored(', '.join(fix), Advice, attrs=["bold"])+ colored("'?", Advice), Advice, attrs=[])
        else:
            return colored('No fixes available.', Advice)

    def getArgs(self, idx):
        """ Gets the arguments of a given prompt.

        Args:
            idx (string): The input entered by the user.

        Returns:
            RAW: a list of the arguments entered by the user.
        """
        raw = idx.split()
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
        sett = {'Commands': CurrentCommands,
                'Output Colors': OUTPUT_COLORS,
                'File Colors': FILE_COLORS}
        return sett
    
    def reportError(self, message, code, exit=True):
        """Creates a nicely formatted error message
        
        Args:
            message (str): The error message
            code (str): The error code
            exit (bool, optional): Wether or not to exit the program. Defaults to True.

        Returns:
            None (null): I forget what this does
        """
        print(colored(f"* FATAL INTERNAL ERROR!\n* PLEASE REPORT ISSUE ON GITHUB REPO (https://github.com/Arduinoz-R-Awsome/SYsos)\n* Exit status: <{message}> Compiler: <{code};> ", Error))
        if exit == True:
            sys.exit(1)
        else:
            return None
        
    @staticmethod
    def write(*ipt):
        """Displays a neatly formatted message to the console.
        
        """
        print('*')
        for i in ipt:
            print(f'* {i}')
        print('*')

    def prompt(self, idx):
        if idx == 'RootUserError':
            self.write(colored('WARNING!', Warning), colored('The action you are about to take is reserved for ROOT users. Are you sure you want to continue?', Warning))
            if input().lower().startswith('y'):
                return 'continue'
            
    def changeUserName(self):
        """Changes the username of the user.
        
        """
        self.write(colored('Are you sure you want to change your username? [y/n]', Warning))
        ans = input()
        if ans == 'y':
            
            usrN = input(colored('Enter your new username: ', 'black', f'on_{cPrompt}'))
            self.write(colored(f'Your username has been changed to {usrN}.', SystemOut))
        elif ans == 'n':
            self.write(colored('No changes made.', SystemOut))
        else:
            self.write(colored('Invalid input.', Error))
            print(self.didYouMean(ans, ['y', 'n']))

    class typingFunctions():
        def typingPrint(self, text, end='\n'):
            """Create a smooth typing action
            
            Args:
                text (str): The text to be typed
                end (str, optional): _description_. Defaults to '\n'.
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
try:
    print(f'Loading SYSOS version {vsn}...')
    for i in tqdm(range (2), desc="Running systen scripts"): time.sleep(random.randint(0,2))
    system.setCommandHelp()
    system.update_Colors()

    for i in tqdm(range (100), desc=f'Loading commands for {sys.platform} architectures...'): time.sleep(random.uniform(0.01, 0.02))
    time.sleep(1)
    Computer = sys.platform
    if Computer == 'win32':
        OperatingSystem = 'Windows'
        clear = 'cls'
    else:
        OperatingSystem = 'Unix'
        clear = 'clr'
    usrN = input(colored('Enter your username: ', 'black', f'on_{cPrompt}'))

except Exception as e:
    system.reportError(message="Error while loading", code=e)

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
                if CTemp == 'Direc':
                    ColorFiles.append(colored(key, Direc))
                elif CTemp == 'Text':
                    ColorFiles.append(colored(key, Text))
            index += 1
        return ColorFiles
    
    def list(self, prt=True):
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
        #write(' '.join(ColorFiles))
        if prt:
            print(' '.join(self.colorize(DirContent)))
        else:
            return DirContent 
contents = listContents()

class changeDirectory():    #Default: Move
    def move(self, destination):
        global Directory
        prompt = system.getArgs(destination)
        if prompt == []:
            system.write(colored(f'WARNING! Command \'{CurrentCommands[1]}\' needs a parameter', Warning))

        elif ''.join(prompt) == 'up':
            tmp = Directory.split('/')
            del tmp[-1]
            tmp = '/'.join(tmp)
            Directory = tmp
            print(colored(Directory, Direc))
        elif ''.join(prompt) in [k for d in contents.list(False) for k in d.keys()]:
                Directory += f'/{prompt[0]}'
                print(colored(Directory, Direc))
        elif ''.join(prompt) not in [k for d in contents.list(False) for k in d.keys()]:
            system.write(colored('No such directory', Error))
dir = changeDirectory()

class makeFile():           #Default: Make
    def make(self, i):
        """Makes a file in the list of files, as well as a text file.

        Args:
            i (String): The desired file name.
        """
        try:
            prompt = system.prompt
            filen = f'{prompt[0]}.{prompt[1].lower()}'
            files[filen] = list([Directory, prompt[1].capitalize()])
            with open(f'{prompt[0]}.txt', 'w') as f:
                f.write(f"FILE CREATED AT {time.strftime('%Y-%m-%d %H:%M')}\n")
        except IndexError:
            files[f'{prompt[0]}'] = list([Directory, 'Direc'])
        listContents.list()
newFile = makeFile()




dir.move(destination='move up')
while True:
    response = input(prompt)
    try:
        if system.getFunction(response) == CurrentCommands[0]:      #Con
            try:
                contents.list()
            except Exception as e:
                system.reportError(message="Unable to list commands", code=e)

        elif system.getFunction(response) == CurrentCommands[1]:    #Move
            try:
                dir.move(destination=system.getArgs(response))
            except Exception as e:
                system.reportError(message="Error during directory transposition", code=e)
        
    except Exception as e:
        system.reportError(message="Error during matchmaking", code=e)

        