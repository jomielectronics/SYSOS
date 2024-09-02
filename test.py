# import pyautogui as typer

# typer.typewrite('pyautogui')
import json

with open("user.sysos", "r+") as f:
    temp = json.load(f)
    usrN = temp["Username"]

print(usrN)