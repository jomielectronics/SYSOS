import os

def clearLines(lines=0):
        """Clears console output. Clears all lines if `lines` is 0."""
        if lines == 0:
            os.system("clear")
        else:
            for _ in range(lines):
                print("\033[A\033[2K", end="")

def printWait(value):
    print(value)
    input()

global homedir, skillLevel, commandPreset
tasks = ["INSTALL_DEPS", "PUSH_USR_INFO"]
printWait("This guide will help setup and configure SYSOS (This symbol \u23ce means press enter or return)")

clearLines()

print("Enter the following information (Type \"help\" at anytime to get more information): ")

running = True
while running:
    homedir = input("The name of your home directory: ")

    if homedir.lower() == "help":
        print("\nYour home directory is the default directory where all your files and directories will be created. For example:")
        printWait("* /home/Jeffery on Raspberry Pi, Ubuntu, and other linux distros\n* /users/Jeffery on Apple Macintosh \u23ce")
        clearLines(6)

    elif not homedir.__contains__("/"):
        print("\nHmmm, this doesn't look like a valid directory")
        printWait("Please try again \u23ce")
        clearLines(5)
    
    else:
        if not os.path.isdir(homedir):
            print("\nYou entered a valid directory, but it doesn't appear to exist")
            printWait("Please try again \u23ce")
            clearLines(5)
        else:
            print("\nGreat, your home directory is set")
            printWait("Press Enter to continue \u23ce")
            clearLines(5)
            print(f"Home directory:\t\t{homedir}")
            running = False

running = True
while running:
    skillLevel = input("Your skill level with computers [beginner/intermediate/advanced]: ")

    if skillLevel.lower() == "help":
        print("\nSkill levels help determine the level of SYSOS functionality")
        printWait("Please choose a level \u23ce")
        clearLines(5)

    elif skillLevel.lower() not in ["beginner", "intermediate", "advanced"]:
        print("\nHmmm, this doesn't look like a valid skill level")
        printWait("Please try again \u23ce")
        clearLines(5)
    
    else:
        print("\nGreat, your skill level is set")
        printWait("Press Enter to continue \u23ce")
        clearLines(5)
        print(f"Skill level:\t\t{skillLevel}")
        running = False

running = True
while running:
    commandPreset = input("Please enter a desired command preset [unix/sysos/windows]: ")

    if commandPreset.lower() == "help":
        print("\nCommand presets are sets of different commands to do the same thing. For example:")
        printWait("* Unix\t\tThese commands are native to unix based operating systems\n* SYSOS\t\tThese commands are native to SYSOS, and beginner friendly\n* Windows\tThese commands are native to windows PowerShell \u23ce")
        clearLines(7)

    elif commandPreset.lower() not in ["unix", "sysos", "windows"]:
        print("\nHmmm, this doesn't look like a valid command preset")
        printWait("Please try again \u23ce")
        clearLines(5)
    
    else:
        print("\nGreat, your command preset is set")
        printWait("Press Enter to continue \u23ce")
        clearLines(5)
        print(f"Command preset:\t\t{commandPreset}")
        running = False

print("Great, the computer will take it from here")

print("Installing dependencies...")
os.system("bash src/Unix/dependencies.sh")
