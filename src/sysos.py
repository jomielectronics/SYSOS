# -----------------------------
# NAMING SCHEME
# -----------------------------
# CustomClass           UpperCamelCase
# ClassInstance         UpperCamelCase
# custom_variable       lower_snake_case
# CONSTANT_VARIABLE     CONSTANT_CASE

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
from menus import Menu
import toml
import _curses

# -----------------------------
# DEFINE VARIABLES
# -----------------------------
vsn = "0.4.7"  # The SYSOS version
throttle_speed = 0  # Speed for processing operations
config_version = "0.9.11"  # Configuration tool version
GITHUB = "https://github.com/jomielec/SYSOS/"  # GitHub repository link
first_time_running = True  # Is this the first run of the program?
username = os.environ.get("LOGNAME") or os.environ.get(
    "USER") or os.environ.get("USERNAME")

# Modules and commands
modules = ["time", "random", "pyautogui", "pynput", "tqdm", "os", "sys",
           "difflib", "json", "termcolor", "dataclasses", "subprocess", "shutil"]

active_preset = "SYSOS"  # Current active command preset

sysos_commands = [
    "con",      # List files
    "rlc",      # Change directory
    "dir",      # Current directory
    "wipe",     # Clear output
    "bam",      # Exit SYSOS
    "ch",       # Change command
    "make",     # Make a file
    "rmv",      # Remove file
    "rmvdir",   # Remove directory
    "run",      # Run an executable
    "view",     # View a file
    "edit",     # Edit a file
    "aexe",     # Run the autosuggested command
    "help",     # Show help for passed command
    "sysos",    # SYSOS command
    "errtest"   # Test error catching
]

unix_commands = [
    "ls",       # List files (equivalent to "con")
    "cd",       # Change directory (equivalent to "rlc")
    "pwd",      # Current directory (equivalent to "dir")
    "clear",    # Clear output (equivalent to "wipe")
    "exit",     # Exit shell (equivalent to "bam")
    "alais",    # Change command (equivalent to "ch")
    "touch",    # Make a file (equivalent to "make")
    "rm",       # Remove file (equivalent to "rmv")
    "rmdir",    # Remove directory (equivalent to "rmvdir")
    "./",       # Run an executable (equivalent to "run")
    "cat",      # View a file (equivalent to "view")
    "nano",     # Edit a file (equivalent to "edit")
    "!!",       # Run the last command (equivalent to "aexe")
    "man",      # Show help for passed command (equivalent to "help")
    "sysos",    # System command (equivalent to "sysos")
    "false"     # Generate an error (equivalent to "errtest")
]

windows_commands = [
    "dir",      # List files
    "cd",       # Change directory
    "pwd",      # Current directory
    "cls",      # Clear output
    "exit",     # Exit SYSOS
    "chg",      # Change command
    "mkf",      # Make a file
    "del",      # Remove file
    "rmdir",    # Remove directory
    "exec",     # Run an executable
    "type",     # View a file
    "mod",      # Edit a file
    "auto",     # Run the autosuggested command
    "help",     # Show help for passed command
    "sysos",    # SYSOS command
    "errchk"    # Test error catching
]

current_commands = sysos_commands[:]

# System settings
HOME = os.environ.get("HOME")
directory = HOME  # Current directory
history = []  # History of executed commands
running = True
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml")

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

ERROR_CODES = {
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
    "This error is for internal use only.", ERROR_CODES["SUCCESS"])
DirectoryNonexistent = CustomError(
    "Directory doesn't exist.", ERROR_CODES["DIR_NOT_FOUND"])
InsufficientPermission = CustomError(
    "Lack of permissions", ERROR_CODES["PERM_DENIED"])
FileNonexistent = CustomError(
    "File doesn't exist", ERROR_CODES["FILE_NOT_FOUND"])
UnknownError = CustomError("An unknown error occurred", ERROR_CODES["GEN_ERR"])
UnsupportedFile = CustomError(
    "This file type is not supported", ERROR_CODES["INV_ARG"])
UserInterrupt = CustomError(
    "Program interrupted by user", ERROR_CODES["CTRL_C_TERM"])
NonexistentParameter = CustomError(
    "A parameter was needed, but not found.", ERROR_CODES["BAD_BUILTIN"])
InvalidCommand = CustomError(
    "Command not recognized", ERROR_CODES["CMD_NOT_FOUND"])
CacheEmpty = CustomError(
    "Cache is empty", ERROR_CODES["SEG_FAULT"])
ScreenSizeError = CustomError(
    "Screen size is too small to run this command", ERROR_CODES["IO_ERR"])
InvalidParameter = CustomError(
    "An unrecognized parameter was given", ERROR_CODES["INV_ARG"])

# -----------------------------
# DEFINE SYSTEM CLASSES
# -----------------------------
class NecessaryFunctions:
    def refresh_prefrences(self):
        global active_preset, OUTPUT_COLORS, FILE_COLORS, data
        """Refreshes the system's preferences."""
        try:
            with open(config_path, "r+") as f:
                data = toml.load(f)
        except Exception as e:
            data = {
                    "selected_preset": active_preset,
                    "output_colors": OUTPUT_COLORS,
                    "file_colors": FILE_COLORS
                }
            
            with open(config_path, "w+") as f:
                toml.dump(data, f)
            # print(e)
        # Assign sections to variables
        active_preset = data.get("selected_preset", "None")  # Default to "None" if missing
        OUTPUT_COLORS = data.get("output_colors", {})
        FILE_COLORS = data.get("file_colors", {})
        # print(FILE_COLORS)
        
        self.update_commands()
        self.update_colors()
    def disable_command_flow(self):
        os.system("stty -ixon")

    def update_prompt(self, error_code=None):
        global Prompt
        if error_code:
            Prompt = colored(f"{username}", "light_green") + "@" + colored(f"SYSOS",
                                                                       "dark_grey") + " \u276f " + colored(directory, DIREC) + " \u276f |" + colored(error_code, ERROR) + "| " + "$ "
        else:
            Prompt = colored(username, "light_green") + "@" + colored(f"SYSOS",
                                                                       "dark_grey") + " \u276f " + colored(directory, DIREC) + " \u276f " + "$ "

    def set_command_help(self):
        """Creates a dictionary of command names and their descriptions."""
        global command_help
        command_help = {
            current_commands[0]: "Lists the contents of the current directory",
            current_commands[1]: "Changes the current directory",
            current_commands[2]: "Displays the current directory",
            current_commands[3]: "Clears the system output",
            current_commands[4]: "Returns to your default terminal",
            current_commands[5]: "A generic command for renaming files,\n* editing commands,\n* or changing your username",
            current_commands[6]: "Creates files and folders",
            current_commands[7]: "Deletes files or folders",
            current_commands[8]: "Executes commands in the default terminal",
            current_commands[9]: "Displays the contents of a file",
            current_commands[11]: "Runs error-catching subroutines to ensure functionality",
            current_commands[12]: "Executes auto-suggested commands",
            current_commands[13]: "Displays help information the passed command\n* (It's kind of obvious)"
        }

    def clear_output_lines(self, lines=0):
        """Clears console output. Clears all lines if `lines` is 0."""
        if lines == 0:
            os.system("clear")
        else:
            for _ in range(lines):
                print("\033[A\033[2K", end="")
    def update_commands(self):
        global current_commands
        if active_preset == "SYSOS":
            current_commands = sysos_commands[:]
        elif active_preset == "Unix":
            current_commands = unix_commands[:]
        elif active_preset == "Windows":
            current_commands = windows_commands[:]
            
    def update_colors(self):
        """Updates global variables with current output and file colors."""
        global ERROR, WARNING, SYSTEM_OUT, ADVICE, OTHER, C_PROMPT, DIREC, TEXT, PROGRAM, OTHER
        ERROR = OUTPUT_COLORS["Error"]
        WARNING = OUTPUT_COLORS["Warning"]
        SYSTEM_OUT = OUTPUT_COLORS["SystemOut"]
        ADVICE = OUTPUT_COLORS["Advice"]
        OTHER = OUTPUT_COLORS["Other"]
        C_PROMPT = OUTPUT_COLORS["cPrompt"]
        # File Colors:
        DIREC = FILE_COLORS["Direc"]
        TEXT = FILE_COLORS["Text"]
        PROGRAM = FILE_COLORS["Program"]
        OTHER = FILE_COLORS["Other"]

    def did_you_mean(self, item, return_fix=False):
        matches = current_commands
        """Get closes command to the one entered

        Args:
            item (str): the command to search
            matches (list, optional): The list to search through. Defaults to CurrentCommands.

        Returns:
            str: A simple message describing that it couldn't find that
        """
        fix = difflib.get_close_matches(item, matches)[0]
        if return_fix:
            if fix:
                return fix
            else:
                return None
        else:
            if fix:
                return f"Maybe you meant '{fix}'?"
            return "No fixes available."


    def get_args(self, idx):
        """Extracts arguments from a user input string."""
        return idx.split(" ")[1:]

    def get_function(self, idx):
        """Extracts the command (function) from a user input string."""
        return idx.split()[0]

    def get_settings(self):
        """Returns the current system settings as a dictionary."""
        return {
            "Commands": current_commands,
            "Output Colors": OUTPUT_COLORS,
            "File Colors": FILE_COLORS
        }

    def report_fatal_error(self, error, custom_error_message=''):
        """Raises a fatal error that exists the program

        Args:
            error (custom error): The error that was raised
            customErrorMessage (str, optional): A custom error message. Defaults to ''.
        """
        if custom_error_message:
            print(colored(
                f"* FATAL INTERNAL ERROR!\n* Error msg: <{error.message}>\n* Program stated: <{custom_error_message}>\n* Compiler: <e{error.code}>", ERROR))
        else:
            print(colored(
                f"* FATAL INTERNAL ERROR!\n* Please report the issue on GitHub ({GITHUB}/issues)\n* Error msg: <{error.message}>\n* Compiler: <e{error.code}>", ERROR))
        sys.exit(error.code)

    def report_static_error(self, error, custom_error_message=''):
        """Raises a static error

        Args:
            error (custom error): The error that was raised
            customErrorMessage (str, optional): A custom error message. Defaults to ''.
        """
        if custom_error_message:
            print(colored(
                f"* Static Error:\n* Error msg: <{error.message}>\n* Program stated: <{custom_error_message}>\n* Compiler: <e{error.code}>", ERROR))
        else:
            print(colored(
                f"* Static Error:\n* Error msg: <{error.message}>\n* Compiler: <e{error.code}>", ERROR))
        return error.code
    @staticmethod
    def write(*ipt, color=None):
        """Prints a neatly formatted message to the console."""
        # if ipt[0] == "help":
        #     if color:
        #         print(colored("*", color))
        #         for i in current_commands:
        #             print(colored(f"* {i}", color))
        #         print(colored("*", color))
        #     else:
        #         print("*")
        #         for i in ipt:
        #             print(f"* {i}")
        #         print("*")
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
            self.write(colored("WARNING!", WARNING), colored(
                "This action is reserved for ROOT users. Continue?", WARNING))
            if input().lower().startswith("y"):
                return "continue"

    def change_user_name(self):
        """Changes the username of the user."""
        global usrN
        self.write(
            colored("Are you sure you want to change your username? [y/n]", WARNING))
        ans = input().lower()
        if ans == "y":
            usrN = input(colored("Enter your new username: ",
                         "black", f"on_{C_PROMPT}"))
            self.write(
                colored(f"Your username has been changed to {usrN}.", SYSTEM_OUT))
        elif ans == "n":
            self.write(colored("No changes made.", SYSTEM_OUT))
        else:
            self.write(colored("Invalid input.", ERROR))
            print(self.did_you_mean(ans, ["y", "n"]))

    class TypingFunctions:
        def typing_print(self, text, end="\n"):
            """Creates a smooth typing effect for console output."""
            text += end
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(throttle_speed)

        def typing_input(self, text):
            """Creates a smooth typing effect for input prompts."""
            for character in text:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(throttle_speed)
            return input()


class FileSystem:
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
            return colored(file, DIREC)
        else:
            match self.fileExtension(file):
                case "txt" | "text" | "md" | "rst" | "log" | "csv" | "xml" | "json" | "html" | "css" | "yaml" | "ini" | "config" | "properties" | "toml" | "conf" | "info" | "markdown" | "asc" | "adoc":
                    return colored(file, TEXT)

                case "py" | "js" | "rs" | "java" | "c" | "cpp" | "go" | "rb" | "php" | "swift" | "pl" | "lua" | "sh" | "exe" | "bat" | "cmd" | "ps1" | "h" | "m" | "scala" | "ts" | "asm":
                    return colored(file, PROGRAM)

                case _:
                    return colored(file, OTHER)

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
system = NecessaryFunctions()
typing = system.TypingFunctions()
filestm = FileSystem()
typing = system.TypingFunctions()
sysos_menu = Menu(config_version)

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
# "aexe"        Run the auto-suggested command
# "help"        Show help for passed command
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
                    system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
                    return

                contents = os.listdir(directory + "/" + arg)
            else:
                contents = os.listdir(directory)
                

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
                        system.report_static_error(UnknownError)
                else:
                    for file in contents:
                        print(file)
        except Exception:
            system.report_static_error(DirectoryNonexistent)


class ChangeDirectory:
    def __init__(self):
        pass

    def run(self, new_directory):
        """Changes the directory variable

        Args:
            NewDirectory (str): The directory to be changed to
        """
        global directory
        if new_directory.startswith("/"):
            system.report_static_error(DirectoryNonexistent, "Directories are not to be prefixed with \"/\" character")
            return
        if new_directory.endswith("/"):
            new_directory = new_directory[:-1]

        if new_directory == "up":
            split = directory.split("/")
            del split[len(split)-1]
            split = "/".join(split)
            directory = split
        elif new_directory == "home":
            directory = HOME
        else:
            test = directory + "/" + new_directory
            print(test)

            if filestm.verifyDir(test) != DirectoryNonexistent:
                directory = test
            else:
                system.report_static_error(
                    DirectoryNonexistent, f"Attempted to relocate to <{test}>")


class CurrentDirectory:
    def __init__(self):
        pass

    def run(self):
        """Prints current directory from `Directory` variable
        """
        print(colored(directory, DIREC))


class ClearOutput:
    def __init__(self):
        pass

    def run(self, lines):
        """Clears `lines` of output

        Args:
            lines (int): The number of lines to clear
        """
        system.clear_output_lines(lines)


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
                    f"SYSTEM OUTPUT\n* Username changed from <{src}> to <{dst}>", color=SYSTEM_OUT)
                username = dst
            else:
                system.report_static_error(InsufficientPermission)

        elif src in current_commands:
            if hasRoot:
                system.write(
                    f"SYSTEM OUTPUT\n* Command changed from <{src}> to <{dst}>", color=SYSTEM_OUT)
                current_commands[src] = dst
            else:
                system.report_static_error(InsufficientPermission)

        else:
            if src.startswith("/"):
                system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
                return
            try:
                src_dir = directory + "/" + src
                dst_dir = directory + "/" + dst
                os.rename(src_dir, dst_dir)
                system.write(
                        f"SYSTEM OUTPUT\n* File <{src}> renamed to <{dst}>", color=SYSTEM_OUT)
            except FileNotFoundError:
                system.report_static_error(FileNonexistent)
            except PermissionError:
                system.report_static_error(InsufficientPermission)
            except Exception as e:
                system.report_static_error(UnknownError, e)


class CreateFile:
    def __init__(self):
        pass

    def run(self, filename):
        """Creates a new file

        Args:
            filename (str): The name of the file to be created
        """
        if filename.startswith("/"):
            system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
            return

        filedir = directory + "/" + filename
        try:
            with open(filedir, 'w') as file:
                pass
            system.write(
                f"SYSTEM OUTPUT\n* Created file <{filename}>", color=SYSTEM_OUT)
        except Exception as e:
            system.report_static_error(UnknownError, e)


class DeleteFile:
    def __init__(self):
        pass

    def run(self, filename):
        """Removes a file

        Args:
            filename (str): The name of the file to be removed
        """
        if filename.startswith("/"):
            system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
            return

        filedir = directory + "/" + filename
        try:
            os.remove(filedir)
            system.write(
                f"SYSTEM OUTPUT\n* Deleted file <{filename}>", color=SYSTEM_OUT)
        except FileNotFoundError:
            system.report_static_error(FileNonexistent)
        except PermissionError:
            system.report_static_error(InsufficientPermission)
        except Exception as e:
            system.report_static_error(UnknownError, e)


class DeleteDirectory:
    def __init__(self):
        pass

    def run(self, dirname):
        """Removes a directory and all its contents

        Args:
            dirname (str): The name of the directory to be removed
        """
        if dirname.startswith("/"):
            system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
            return
        
        filedir = directory + "/" + dirname
        try:
            shutil.rmtree(filedir)
            system.write(
                f"SYSTEM OUTPUT\n* Deleted directory <{dirname}>", color=SYSTEM_OUT)
        except FileNotFoundError:
            system.report_static_error(FileNonexistent)
        except PermissionError:
            system.report_static_error(InsufficientPermission)
        except Exception as e:
            system.report_static_error(UnknownError, e)


class RunExecutable:
    def __init__(self):
        pass

    def run(self, filename):
        """Runs an executable file

        Args:
            filename (str): The name of the executable file to be run
        """
        if filename.startswith("/"):
            system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
            return

        filedir = directory + "/" + filename
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
            elif extn == "gleam":
                os.system(f"gleam run {filename}")
            else:
                system.report_static_error(
                    UnsupportedFile, f"{extn} is not supported")

        except FileNotFoundError:
            system.report_static_error(FileNonexistent)
        except PermissionError:
            system.report_static_error(InsufficientPermission)
        except subprocess.CalledProcessError as e:
            system.write(
                f"SYSTEM OUTPUT\n* <{filename}> exited with status {e.returncode}", color=SYSTEM_OUT)
        except Exception as e:
            system.report_static_error(UnknownError, e)


class ViewFile:
    def __init__(self):
        pass

    def run(self, filename):
        """Displays the contents of a file

        Args:
            filename (str): The name of the file to be displayed
        """
        if filename.startswith("/"):
            system.report_static_error(DirectoryNonexistent, "Directories are not to be specified with \"/\" character")
            return

        filedir = directory + "/" + filename
        try:
            with open(filedir, 'r') as file:
                contents = file.read()
                system.write(
                    f"SYSTEM OUTPUT\n* Contents of <{filename}>:\n\n{contents}", color=SYSTEM_OUT)
        except FileNotFoundError:
            system.report_static_error(FileNonexistent)
        except Exception as e:
            system.report_static_error(UnknownError, e)


def run_editor(stdscr, filename):
    editor = NanoPy(stdscr, current_dir=directory, filename=filename)
    editor.run()


class ShowHelp():
    def __init__(self):
        pass

    def run(self, command):
        """Show help for passed command

        Args:
            command (str): The command to search for help for
        """
        if command == "list":
            system.write(*current_commands, color=SYSTEM_OUT)
        else:
            system.write(command_help[command], color=SYSTEM_OUT)

class SYSOS():
    def __init__(self):
        pass

    def config(self):
        """Display system configuration"""
        curses.wrapper(sysos_menu.main_menu)
        
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
help = ShowHelp()
sysos = SYSOS()

# -----------------------------
# RUN SETUP SCRIPTS
# -----------------------------
system.set_command_help()
system.update_colors()
system.update_prompt()
system.disable_command_flow()
system.refresh_prefrences()
# -----------------------------
# MAIN LOOP
# -----------------------------
autorun = ""
error=0
while running:
    system.update_prompt(error)  # Update the prompt with current directory and username
    error = 0
    #TODO: Fix problem that arrises when dirname starts with "/"
    try:
        tmp = input(Prompt)
        if tmp == current_commands[12]:
            if not autorun:
                error = system.report_static_error(CacheEmpty, f"Command \"{current_commands[12]}\" has nothing to run")
                continue
            tmp = autorun
            autorun = ""

        command = system.get_function(tmp)
        args = system.get_args(tmp)        

        if command == current_commands[0]:  # con, List files
            try:
                con.run(arg=args[0])
            except Exception as e:
                con.run()

        elif command == current_commands[1]:  # rlc, Change directory
            try:
                rlc.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        elif command == current_commands[2]:  # dir, Print current directory
            dir.run()

        elif command == current_commands[3]:  # wipe, Clear output
            try:
                wipe.run(int(args[0]))
            except Exception as e:
                wipe.run(0)

        elif command == current_commands[4]:  # bam, Exit SYSOS
            bam.run()

        elif command == current_commands[5]:  # ch, Change username or command
            try:
                ch.run(args[0], args[1], args[2] == "root")
            except Exception as e:
                try:
                    ch.run(args[0], args[1])
                except IndexError:
                    error = system.report_static_error(NonexistentParameter)
                except Exception as e:
                    error = system.report_static_error(UnknownError, e)

        elif command == current_commands[6]:  # make, Create a new file
            try:
                make.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        elif command == current_commands[7]:  # rmv, Remove a file
            try:
                rmv.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        
        elif command == current_commands[8]:  # rmvdir, Remove a directory and all its contents
            try:
                rmvdir.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        elif command == current_commands[9]:  # run, Run an executable file
            try:
                runExe.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        # view, View the contents of a file
        elif command == current_commands[10]:
            try:
                view.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        elif command == current_commands[11]:
            filetoopen = args[0]
            try:
                curses.wrapper(lambda stdscr: run_editor(stdscr, filename=filetoopen))
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        elif command == current_commands[13]:    #help, Display help message
            try:
                help.run(args[0])
            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)
        
        elif command == current_commands[14]:    #sysos, Display system info
            try:
                if args[0] == "config":
                    try:
                        sysos.config()
                        system.refresh_prefrences()
                        
                    except _curses.error as e:
                        error = system.report_static_error(ScreenSizeError, e)

                elif args[0] == "active-preset":
                    system.write(F"Currently using \"{active_preset}\" commands", color=SYSTEM_OUT)

                elif args[0] == "version":
                    system.write(f"Currently running SYSOS version {vsn}", f"On {GITHUB}", color=SYSTEM_OUT)
                
                else:
                    error = system.report_static_error(InvalidParameter)

            except IndexError:
                error = system.report_static_error(NonexistentParameter)
            except Exception as e:
                error = system.report_static_error(UnknownError, e)

        else:
            error = system.report_static_error(InvalidCommand)
            fixed = system.did_you_mean(command)
            print(fixed)
            if fixed == "No fixes available.":
                system.write(fixed)
            else:
                system.write(f"{system.did_you_mean(command)}", "If you want to automatically execute this,", f"type \"{current_commands[12]}\"", color=ADVICE)
                if args != []:
                    autorun = system.did_you_mean(command, return_fix=True) + " " + " ".join(args)
                else:
                    autorun = system.did_you_mean(command, return_fix=True)

    except KeyboardInterrupt:
        print()
        system.report_static_error(UserInterrupt)
        system.write(
            "SYSTEM ADVICE", f"If you want to terminate, please use <{current_commands[4]}>", color=ADVICE)
    except IndexError:
        system.report_static_error(InvalidCommand)