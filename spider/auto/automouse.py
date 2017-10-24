import pyautogui
import PIL

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

width, height = pyautogui.size()
pyautogui.moveTo(600, 550, duration=0.25)
# pyautogui.moveTo(400, 300, duration=0.25)
# pyautogui.moveTo(400, 400, duration=0.25)
# pyautogui.moveTo(300, 400, duration=0.25)
pyautogui.click()
pyautogui.typewrite("Every 5 seconds a computer gets infected with a virus. 13% of Americans actually believe that some parts of the moon are made of cheese. The world's youngest parents were 8 and 9 and lived in China in 1910. If you could count the number of times a cricket chirps in one minute, divide by 2, add 9 and divide by 2 again, you would have the correct temperature in Celsius degrees... How do they know that?", interval=0.06)
# while True:
