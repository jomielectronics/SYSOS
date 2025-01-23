# -----------------------------
# IMPORT NECESSARY MODULES
# -----------------------------
import time
import random
import pyautogui as typer
from dataclasses import dataclass
from pynput import keyboard
from tqdm import tqdm
from os import system as run, listdir
import os
import sys
import difflib
import json
from termcolor import *
import subprocess
import shutil
import curses
from nano_py import NanoPy
# -----------------------------
# DEFINE VARIABLES
# -----------------------------
vsn = "0.3.1"  # The SYSOS version
ThrottleSpeed = 0  # Speed for processing operations
cfgvsn = 1.0  # Configuration tool version
GITHUB = "https://github.com/jomielec/SYSOS/issues"  # GitHub repository link
FirstTimeRunning = True  # Is this the first run of the program?
username = os.environ.get("LOGNAME") or os.environ.get(
    "USER") or os.environ.get("USERNAME")

# Modules and commands
modules = ["time", "random", "pyautogui", "pynput", "tqdm", "os", "sys",
           "difflib", "json", "termcolor", "dataclasses", "subprocess", "shutil"]
CurrentCommands = ["con", "rlc", "dir", "wipe", "bam", "ch",
                   "make", "rmv", "rmvdir", "run", "view", "edit", "aexe", "sysos", "errtest"]
CmdPreset = "SYSOS Commands"  # Current active command preset
SysosCommands = ["con", "rlc", "dir", "wipe", "bam", "ch",
                   "make", "rmv", "rmvdir", "run", "view", "edit", "aexe", "sysos", "errtest"]  # Default SYSOS commands
UnixCommands = ["ls", "cd", "pwd", "clear", "exit", "ch",
                "touch", "rm", "run", "open", "sysos"]  # Unix commands

# System settings
HOME = os.environ.get("HOME")
Directory = HOME  # Current directory
LsCache = {}  # Cache for directory content (used by "ls" command)
History = []  # History of executed commands
running = True

# Output and file colors
OUTPUT_COLORS = {
    "Error": "red",
    "Warning": "orange",
    "SystemOut": "yellow",
    "Advice": "magenta",
    "Other": "white",
    "cPrompt": "dark_grey"
}
FILE_COLORS = {
    "Direc": "blue",
    "Text": "magenta",
    "Program": "green",
    "Other": "yellow"
}

error_codes = {
    "SUCCESS": 0,                     # The program executed successfully without errors.
    "GEN_ERR": 1,                     # General Error (catch-all for unspecified errors).
    "BAD_BUILTIN": 2,                 # Misuse of Shell Built-ins (incorrect usage of shell commands).
    "INV_ARG": 3,                     # Invalid Argument (invalid input passed to the program).
    "FILE_NOT_FOUND": 4,              # The required file or resource was not found.
    "IO_ERR": 5,                      # Input/Output Error (failure in file or device operation).
    "CONFIG_ERR": 6,                  # Configuration Error (issue with configuration settings).
    "AUTH_FAIL": 7,                   # Authentication Failed (incorrect credentials).
    "OUT_OF_MEM": 8,                  # Out of Memory (program couldn't allocate memory).
    "RES_LIMIT_EXCEEDED": 9,          # Resource Limit Exceeded (e.g., too many open files).
    "TIMEOUT": 10,                    # Timeout (operation exceeded its allowed time).
    "CONFLICT": 11,                   # Conflict (e.g., conflicting processes or states).
    "INT_APP_ERR_UNHANDLED": 50,      # Internal Application Error - Unhandled Exception.
    "DIR_NOT_FOUND": 51,              # Directory Not Found (specific directory missing).
    "INVALID_PERM": 52,               # Invalid File Permissions (lack of read/write access).
    "DEP_NOT_FOUND": 53,              # Dependency Not Found (required library or resource missing).
    "PERM_DENIED": 126,               # Permission Denied (lack of necessary permissions).
    "CMD_NOT_FOUND": 127,             # Command Not Found (command not recognized).
    "INV_EXIT_ARG": 128,              # Invalid Exit Argument (invalid argument passed on exit).
    "CTRL_C_TERM": 130,               # Terminated by Ctrl+C (Signal 2 - SIGINT, user interrupt).
    "KILL_TERM": 137,                 # Terminated by kill -9 (Signal 9 - SIGKILL, force kill).
    "SEG_FAULT": 139                  # Segmentation Fault (Signal 11 - SIGSEGV, memory error).
}

# -----------------------------
# DEFINE CUSTOM ERRORS
# -----------------------------


@dataclass
class CustomError:
    """A simple object to represent an error."""
    # type: str  # Type of the error (e.g., 'NotFound', 'Validation')
    message: str  # A human-readable error message
    code: int  # The error code


ImpliedDirectory = CustomError(
    "This error is for internal use only.", error_codes["SUCCESS"])
DirectoryNonexistent = CustomError(
    "Directory doesn't exist.", error_codes["DIR_NOT_FOUND"])
InsufficientPermission = CustomError(
    "Lack of permissions", error_codes["PERM_DENIED"])
FileNonexistent = CustomError(
    "File doesn't exist", error_codes["FILE_NOT_FOUND"])
UnknownError = CustomError("An unknown error occurred", error_codes["GEN_ERR"])
UnsupportedFile = CustomError(
    "This file type is not supported", error_codes["INV_ARG"])
UserInterrupt = CustomError(
    "Program interrupted by user", error_codes["CTRL_C_TERM"])
NonexistentParameter = CustomError(
    "A parameter was needed, but not found.", error_codes["BAD_BUILTIN"])
InvalidCommand = CustomError(
    "Command not recognized", error_codes["CMD_NOT_FOUND"])


# -----------------------------
# DEFINE SYSTEM CLASSES
# -----------------------------


class necessaryFunctions:
    def disableCommandFlow(self):
        os.system("stty -ixon")

    def updatePrompt(self):
        global Prompt
        Prompt = colored(f"{username}", "light_green") + "@" + colored(f"SYSOS",
                                                                       "dark_grey") + " \u276f " + colored(Directory, Direc) + " \u276f " + "$ "

    def setCommandHelp(self):
        """Creates a dictionary of command names and their descriptions."""
        global CMDHelp
        CMDHelp = {
            CurrentCommands[0]: "Lists the contents of the current directory",
            CurrentCommands[1]: "Changes the current directory",
            CurrentCommands[2]: "Lists the current directory",
            CurrentCommands[3]: "Clears the system output",
            CurrentCommands[4]: "Returns to your default terminal",
            CurrentCommands[5]: "A generic command for renaming, editing commands, or changing username",
            CurrentCommands[6]: "Creates files and folders",
            CurrentCommands[7]: "Deletes files or folders",
            CurrentCommands[8]: "Executes commands in the default terminal",
            CurrentCommands[9]: "Displays the contents of a file",
            CurrentCommands[11]: "Runs error-catching subroutines to ensure functionality"
        }

    def clearOutputLines(self, lines=0):
        """Clears console output. Clears all lines if `lines` is 0."""
        if lines == 0:
            os.system("clear")
        else:
            for _ in range(lines):
                print("\033[A\033[2K", end="")

    def update_Colors(self):
        """Updates global variables with current output and file colors."""
        global Error, Warning, SystemOut, Advice, Other, cPrompt, Direc, Text, Program, Other
        Error = OUTPUT_COLORS["Error"]
        Warning = OUTPUT_COLORS["Warning"]
        SystemOut = OUTPUT_COLORS["SystemOut"]
        Advice = OUTPUT_COLORS["Advice"]
        Other = OUTPUT_COLORS["Other"]
        cPrompt = OUTPUT_COLORS["cPrompt"]
        # File Colors:
        Direc = FILE_COLORS["Direc"]
        Text = FILE_COLORS["Text"]
        Program = FILE_COLORS["Program"]
        Other = FILE_COLORS["Other"]

    def didYouMean(self, item, matches=CurrentCommands, returnFix=False):
        """Get closes command to the one entered

        Args:
            item (str): the command to search
            matches (list, optional): The list to search through. Defaults to CurrentCommands.

        Returns:
            str: A simple message describing that it couldn't find that
        """
        fix = difflib.get_close_matches(item, matches)
        if returnFix:
            if fix:
                return fix
            else:
                return None
        else:
            if fix:
                return f"Maybe you meant '{', '.join(fix)}'?"
            return "No fixes available."


    def getArgs(self, idx):
        """Extracts arguments from a user input string."""
        return idx.split(" ")[1:]

    def getFunction(self, idx):
        """Extracts the command (function) from a user input string."""
        return idx.split()[0]

    def getSettings(self):
        """Returns the current system settings as a dictionary."""
        return {
            "Commands": CurrentCommands,
            "Output Colors": OUTPUT_COLORS,
            "File Colors": FILE_COLORS
        }

    def reportFatalError(self, error, customErrorMessage=''):
        """Raises a fatal error that exists the program

        Args:
            error (custom error): The error that was raised
            customErrorMessage (str, optional): A custom error message. Defaults to ''.
        """
        if customErrorMessage:
            print(colored(
                f"* FATAL INTERNAL ERROR!\n* Error msg: <{error.message}>\n* Program stated: <{customErrorMessage}>\n* Compiler: <e{error.code}>", Error))
        else:
            print(colored(
                f"* FATAL INTERNAL ERROR!\n* Please report the issue on GitHub ({GITHUB})\n* Error msg: <{error.message}>\n* Compiler: <e{error.code}>", Error))
        sys.exit(error.code)

    def reportStaticError(self, error, customErrorMessage=''):
        """Raises a static error

        Args:
            error (custom error): The error that was raised
            customErrorMessage (str, optional): A custom error message. Defaults to ''.
        """
        if customErrorMessage:
            print(colored(
                f"* Static Error:\n* Error msg: <{error.message}>\n* Program stated: <{customErrorMessage}>\n* Compiler: <e{error.code}>", Error))
        else:
            print(colored(
                f"* Static Error:\n* Error msg: <{error.message}>\n* Compiler: <e{error.code}>", Error))

    @staticmethod
    def write(*ipt, color=None):
        """Prints a neatly formatted message to the console."""
        if color:
            print(colored("*", color))
            for i in ipt:
                print(colored(f"* {i}", color))
            print(colored("*", color))
        else:
            print("*")
            for i in ipt:
                print(f"* {i}")
            print("*")

    def prompt(self, idx):
        if idx == "RootUserError":
            self.write(colored("WARNING!", Warning), colored(
                "This action is reserved for ROOT users. Continue?", Warning))
            if input().lower().startswith("y"):
                return "continue"

    def changeUserName(self):
        """Changes the username of the user."""
        global usrN
        self.write(
            colored("Are you sure you want to change your username? [y/n]", Warning))
        ans = input().lower()
        if ans == "y":
            usrN = input(colored("Enter your new username: ",
                         "black", f"on_{cPrompt}"))
            self.write(
                colored(f"Your username has been changed to {usrN}.", SystemOut))
        elif ans == "n":
            self.write(colored("No changes made.", SystemOut))
        else:
            self.write(colored("Invalid input.", Error))
            print(self.didYouMean(ans, ["y", "n"]))

    class typingFunctions:
        def typingPrint(self, text, end="\n"):
            """Creates a smooth typing effect for console output."""
            text += end
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(ThrottleSpeed)

        def typingInput(self, text):
            """Creates a smooth typing effect for input prompts."""
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(ThrottleSpeed)
            return input()


class fileSystem:
    def init(self):
        pass

    def fileName(self, filename):
        """Returns the file name wihout the extension

        Args:
            filename (str): The full file name

        Returns:
            str: The file's name
        """
        fileParts = filename.split(".")
        try:
            return fileParts[0]
        except IndexError:
            return ImpliedDirectory

    def fileExtension(self, filename):
        """Returns the file extension without the name

        Args:
            filename (str): The full file name

        Returns:
            str: The file's extension
        """
        fileParts = filename.split(".")
        try:
            return fileParts[1]
        except IndexError:
            return ImpliedDirectory

    def isDir(self, filename):
        """Checks if a filename is a directory

        Args:
            filename (str): The file name

        Returns:
            bool: True if the file is a directory, False otherwise
        """
        if self.fileExtension(filename) == ImpliedDirectory:
            return True
        else:
            return False

    def colorize(self, file):
        """Colors filenames according to their extensions

        Args:
            file (str): The filename to be colorized

        Returns:
            str: The colorized filenames
        """
        if self.fileExtension(file) == ImpliedDirectory:
            return colored(file, Direc)
        else:
            match self.fileExtension(file):
                case "txt" | "text" | "md" | "rst" | "log" | "csv" | "xml" | "json" | "html" | "css" | "yaml" | "ini" | "config" | "properties" | "toml" | "conf" | "info" | "markdown" | "asc" | "adoc":
                    return colored(file, Text)

                case "py" | "js" | "rs" | "java" | "c" | "cpp" | "go" | "rb" | "php" | "swift" | "pl" | "lua" | "sh" | "exe" | "bat" | "cmd" | "ps1" | "h" | "m" | "scala" | "ts" | "asm":
                    return colored(file, Program)

                case _:
                    return colored(file, Other)

    def categorize(self, files):
        """Categorize files into directories and files

        Args:
            files (list): A list of file names

        Returns:
            dict: A dictionary with 'directories' and 'files' keys
        """
        categorized = {"directories": [], "files": []}
        for file in files:
            if self.isDir(file):
                categorized["directories"].append(file)
            else:
                categorized["files"].append(file)
        return categorized

    def verifyDir(self, dir):
        """Verifies if a directory exists

        Args:
            dir (str): The directory path

        Returns:
            bool: True if the directory exists, False otherwise
        """
        if not os.path.isdir(dir):
            return DirectoryNonexistent


# -----------------------------
# INSTANTIATE SYSTEM FUNCTIONS
# -----------------------------
system = necessaryFunctions()
typing = system.typingFunctions()
filestm = fileSystem()
typing = system.typingFunctions()
# -----------------------------
# COMMAND CLASSES
# Includes the following commands:
#
# "con"         List files
# "rlc"         Change directory
# "dir"         Current directory
# "wipe"        Clear output
# "bam"         Exit SYSOS
# "ch"          Change command
# "make"        Make a file
# "rmv"         Remove file
# "rmvdir"      Remove directory
# "run"         Run an executable
# "view"        View a file
# "edit"        Edit a file
# "sysos"       SYSOS command
# "errtest"     Test error catching
# -----------------------------


class ListContents:
    def __init__(self):
        pass

    def run(self, arg=None, colored=True, returned=False):
        """Lists or returns the contents of a directory

        Args:
            colored (bool, optional): Colorize output?. Defaults to True.
            returned (bool, optional): Return instead of printing?. Defaults to False.

        Returns:
            list: The list of files, only returned if `returned` is True
        """
        try:
            if arg:
                if arg.startswith("/"):
                    system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
                    return

                contents = os.listdir(Directory + "/" + arg)
            else:
                contents = os.listdir(Directory)
                

            for file in contents[:]:  # Iterating over a copy of the list
                if file.startswith('.'):
                    contents.remove(file)

            contents.sort()
            if returned:
                return contents
            else:
                sorted = filestm.categorize(contents)
                sorted["directories"].sort()
                sorted["files"].sort()
                if colored:
                    try:
                        if sorted["directories"]:
                            print("DIRECTORIES:")
                            count = 1
                            for direc in sorted["directories"]:
                                if count == len(sorted["directories"]):
                                    break
                                print("  \u251c\u2500" +
                                    filestm.colorize(direc) + "/")
                                count += 1

                            print("  \u2570\u2500" + filestm.colorize(direc) + "/")
                        else:
                            print("No directories found.")

                        if sorted["files"]:
                            count = 1
                            print("\nFILES:")
                            for file in sorted["files"]:
                                if count == len(sorted["files"]):
                                    break
                                print("  \u251c\u2500" + filestm.colorize(file))
                                count += 1

                            print("  \u2570\u2500" + filestm.colorize(file))
                        else:
                            print("No files found.")
                    except Exception:
                        system.reportStaticError(UnknownError)
                else:
                    for file in contents:
                        print(file)
        except Exception:
            system.reportStaticError(DirectoryNonexistent)


class ChangeDirectory:
    def __init__(self):
        pass

    def run(self, NewDirectory):
        """Changes the directory variable

        Args:
            NewDirectory (str): The directory to be changed to
        """
        global Directory
        if NewDirectory.startswith("/"):
            system.reportStaticError(DirectoryNonexistent, "Directories are not to be prefixed with \"/\" caracter")
            return

        if NewDirectory == "up":
            split = Directory.split("/")
            del split[len(split)-1]
            split = "/".join(split)
            Directory = split
        elif NewDirectory == "home":
            Directory = HOME
        else:
            test = Directory + "/" + NewDirectory
            print(test)

            if filestm.verifyDir(test) != DirectoryNonexistent:
                Directory = test
            else:
                system.reportStaticError(
                    DirectoryNonexistent, f"Attempted to relocate to <{test}>")


class CurrentDirectory:
    def __init__(self):
        pass

    def run(self):
        """Prints current directory from `Directory` variable
        """
        print(colored(Directory, Direc))


class ClearOutput:
    def __init__(self):
        pass

    def run(self, lines):
        """Clears `lines` of output

        Args:
            lines (int): The number of lines to clear
        """
        system.clearOutputLines(lines)


class Exit:
    def __init__(self):
        pass

    def run(self):
        """Exits SYSOS
        """
        sys.exit()


class Changer:
    def __init__(self):
        pass

    def run(self, src, dst, hasRoot=False):
        global username
        if src == username:
            if hasRoot:
                system.write(
                    f"SYSTEM OUTPUT\n* Username changed from <{src}> to <{dst}>", color=SystemOut)
                username = dst
            else:
                system.reportStaticError(InsufficientPermission)

        elif src in CurrentCommands:
            if hasRoot:
                system.write(
                    f"SYSTEM OUTPUT\n* Command changed from <{src}> to <{dst}>", color=SystemOut)
                CurrentCommands[src] = dst
            else:
                system.reportStaticError(InsufficientPermission)

        else:
            if src.startswith("/"):
                system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
                return
            try:
                os.rename(src, dst)
                system.write(
                    f"SYSTEM OUTPUT\n* File <{src}> renamed to <{dst}", color=SystemOut)
            except FileNotFoundError:
                system.reportStaticError(FileNonexistent)
            except PermissionError:
                system.reportStaticError(InsufficientPermission)
            except Exception as e:
                system.reportStaticError(UnknownError, e)


class CreateFile:
    def __init__(self):
        pass

    def run(self, filename):
        """Creates a new file

        Args:
            filename (str): The name of the file to be created
        """
        if filename.startswith("/"):
            system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
            return

        filedir = Directory + "/" + filename
        try:
            with open(filedir, 'w') as file:
                pass
            system.write(
                f"SYSTEM OUTPUT\n* Created file <{filename}>", color=SystemOut)
        except Exception as e:
            system.reportStaticError(UnknownError, e)


class DeleteFile:
    def __init__(self):
        pass

    def run(self, filename):
        """Removes a file

        Args:
            filename (str): The name of the file to be removed
        """
        if filename.startswith("/"):
            system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
            return

        filedir = Directory + "/" + filename
        try:
            os.remove(filedir)
            system.write(
                f"SYSTEM OUTPUT\n* Deleted file <{filename}>", color=SystemOut)
        except FileNotFoundError:
            system.reportStaticError(FileNonexistent)
        except PermissionError:
            system.reportStaticError(InsufficientPermission)
        except Exception as e:
            system.reportStaticError(UnknownError, e)


class DeleteDirectory:
    def __init__(self):
        pass

    def run(self, dirname):
        """Removes a directory and all its contents

        Args:
            dirname (str): The name of the directory to be removed
        """
        if dirname.startswith("/"):
            system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
            return
        
        filedir = Directory + "/" + dirname
        try:
            shutil.rmtree(filedir)
            system.write(
                f"SYSTEM OUTPUT\n* Deleted directory <{dirname}>", color=SystemOut)
        except FileNotFoundError:
            system.reportStaticError(FileNonexistent)
        except PermissionError:
            system.reportStaticError(InsufficientPermission)
        except Exception as e:
            system.reportStaticError(UnknownError, e)


class RunExecutable:
    def __init__(self):
        pass

    def run(self, filename):
        """Runs an executable file

        Args:
            filename (str): The name of the executable file to be run
        """
        if filename.startswith("/"):
            system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
            return

        filedir = Directory + "/" + filename
        extn = filestm.fileExtension(filedir)
        try:
            if extn == "py":
                os.system(f"python3 {filedir}")
            elif extn == "rs":
                os.system(f"rustc {filedir} -o output && ./output")
            elif extn == "c":
                os.system(f"gcc {filedir} -o output && ./output")
            elif extn == "cpp":
                os.system(f"g++ {filedir} -o output && ./output")
            elif extn == "java":
                os.system(f"javac {filedir} && java {filedir.split('.')[0]}")
            elif extn == "js":
                os.system(f"node {filedir}")
            elif extn == "ts":
                os.system(f"ts-node {filedir}")
            elif extn == "go":
                os.system(f"go run {filedir}")
            elif extn == "rb":
                os.system(f"ruby {filedir}")
            elif extn == "sh":
                os.system(f"bash {filedir}")
            else:
                system.reportStaticError(
                    UnsupportedFile, f"{extn} is not supported")

        except FileNotFoundError:
            system.reportStaticError(FileNonexistent)
        except PermissionError:
            system.reportStaticError(InsufficientPermission)
        except subprocess.CalledProcessError as e:
            system.write(
                f"SYSTEM OUTPUT\n* <{filename}> exited with status {e.returncode}", color=SystemOut)
        except Exception as e:
            system.reportStaticError(UnknownError, e)


class ViewFile:
    def __init__(self):
        pass

    def run(self, filename):
        """Displays the contents of a file

        Args:
            filename (str): The name of the file to be displayed
        """
        if filename.startswith("/"):
            system.reportStaticError(DirectoryNonexistent, "Directories are not to be specified with \"/\" caracter")
            return

        filedir = Directory + "/" + filename
        try:
            with open(filedir, 'r') as file:
                contents = file.read()
                system.write(
                    f"SYSTEM OUTPUT\n* Contents of <{filename}>:\n\n{contents}", color=SystemOut)
        except FileNotFoundError:
            system.reportStaticError(FileNonexistent)
        except Exception as e:
            system.reportStaticError(UnknownError, e)

def runEditor(stdscr, filename):
    editor = NanoPy(stdscr, current_dir=Directory, filename=filename)
    editor.run()
# -----------------------------
# INSTANTIATE COMMAND CLASSES
# -----------------------------
con = ListContents()
rlc = ChangeDirectory()
dir = CurrentDirectory()
wipe = ClearOutput()
bam = Exit()
ch = Changer()
make = CreateFile()
rmv = DeleteFile()
rmvdir = DeleteDirectory()
runExe = RunExecutable()
view = ViewFile()

# -----------------------------
# RUN SETUP SCRIPTS
# -----------------------------
system.setCommandHelp()
system.update_Colors()
system.updatePrompt()
system.disableCommandFlow()
# -----------------------------
# MAIN LOOP
# -----------------------------
autorun = ""
while running:
    system.updatePrompt()  # Update the prompt with current directory and username
#TODO: Fix problem that arrises when dirname starts with "/"
    try:
        tmp = input(Prompt)
        command = system.getFunction(tmp)
        args = system.getArgs(tmp)

        if command == CurrentCommands[12]:
            command = autorun

        if command == CurrentCommands[0]:  # con, List files
            try:
                con.run(arg=args[0])
            except Exception as e:
                con.run()

        elif command == CurrentCommands[1]:  # rlc, Change directory
            try:
                rlc.run(args[0])
            except IndexError:
                system.reportStaticError(NonexistentParameter)
            except Exception as e:
                system.reportStaticError(UnknownError, e)

        elif command == CurrentCommands[2]:  # dir, Print current directory
            dir.run()

        elif command == CurrentCommands[3]:  # wipe, Clear output
            try:
                wipe.run(int(args[0]))
            except Exception as e:
                wipe.run(0)

        elif command == CurrentCommands[4]:  # bam, Exit SYSOS
            bam.run()

        elif command == CurrentCommands[5]:  # ch, Change username or command
            try:
                ch.run(args[0], args[1], args[2] == "root")
            except Exception as e:
                try:
                    ch.run(args[0], args[1])
                except IndexError:
                    system.reportStaticError(NonexistentParameter)
                except Exception as e:
                    system.reportStaticError(UnknownError, e)

        elif command == CurrentCommands[6]:  # make, Create a new file
            try:
                make.run(args[0])
            except IndexError:
                system.reportStaticError(NonexistentParameter)
            except Exception as e:
                system.reportStaticError(UnknownError, e)

        elif command == CurrentCommands[7]:  # rmv, Remove a file
            try:
                rmv.run(args[0])
            except IndexError:
                system.reportStaticError(NonexistentParameter)
            except Exception as e:
                system.reportStaticError(UnknownError, e)

        
        elif command == CurrentCommands[8]:  # rmvdir, Remove a directory and all its contents
            try:
                rmvdir.run(args[0])
            except IndexError:
                system.reportStaticError(NonexistentParameter)
            except Exception as e:
                system.reportStaticError(UnknownError, e)

        elif command == CurrentCommands[9]:  # run, Run an executable file
            try:
                runExe.run(args[0])
            except IndexError:
                system.reportStaticError(NonexistentParameter)
            except Exception as e:
                system.reportStaticError(UnknownError, e)

        # view, View the contents of a file
        elif command == CurrentCommands[10]:
            try:
                view.run(args[0])
            except IndexError:
                system.reportStaticError(NonexistentParameter)
            except Exception as e:
                system.reportStaticError(UnknownError, e)

        elif command == CurrentCommands[11]:
            filetoopen = args[0]
            try:
                curses.wrapper(lambda stdscr: runEditor(stdscr, filename=filetoopen))
            except Exception as e:
                system.reportStaticError(UnknownError, {e})

        # elif command == CurrentCommands[11]:    #help, Display help message
        else:
            system.reportStaticError(InvalidCommand)
            fixed = system.didYouMean(command)
            if fixed == "No fixes available.":
                system.write(fixed)
            else:
                system.write(f"{system.didYouMean(command)}", "If you want to automatically execute this,", "type \"aexe\"", color=Advice)

                autorun = system.didYouMean(command, returnFix=True)[0]
                print(autorun)
                

    except KeyboardInterrupt:
        print()
        system.reportStaticError(UserInterrupt)
        system.write(
            "SYSTEM ADVICE", f"If you want to terminate, please use <{CurrentCommands[4]}>", color=Advice)
    except IndexError:
        system.reportStaticError(InvalidCommand)