import pyautogui
btn_equip_loc = pyautogui.locateOnScreen('btn_equip.png')
#pyautogui.click(btn_equip_loc.x, btn_equip_loc.y)
coords = pyautogui.center(btn_equip_loc)
pyautogui.click(coords.x, coords.y)