import pywinauto
import win32api
import win32con
import win32gui
import pyautogui
from pywinauto.application import Application
import warnings
import time
#from minimap import backpack
#from item_reader import *

# 23/11/2021: precisei usar as bibliotecas pyautogui e pywinauto juntas
# a pywinauto me permite clicar em posições relativas à janela, mas não tem ferramenta de busca por imagem
# a pyautogui busca por imagem, mas retorna a posição absoluta dela na tela, não na janela do jogo

warnings.simplefilter('ignore', category=UserWarning)

timetowait = 0
size_w = 960  # tamanho da janela, usa pra fazer o cálculo do lugar pra clicar
size_h = 960

coords_backpack_1 = (int(380), int(380))


def initialize_game():
    win.move_window(x=None, y=None, width=size_w, height=size_h, repaint=True)
    win.send_keystrokes("{I}")
    time.sleep(1)
    win.send_keystrokes("{I}")
    time.sleep(1)
    #faz com que os endereços da backpack sejam atualizados e a janela esteja no tamanho correto
#initialize_game()

def move_N():
    pass
    #win.send_keystrokes("{VK_NUMPAD8}")

def move_S():
    pass
    #win.send_keystrokes("{VK_NUMPAD2}")

def move_L():
    pass
    #win.send_keystrokes("{VK_NUMPAD6}")

def move_O():
    pass
    #win.send_keystrokes("{VK_NUMPAD4}")

def move_NL():
    pass
    #win.send_keystrokes("{VK_NUMPAD9}")

def move_SL():
    pass
    #win.send_keystrokes("{VK_NUMPAD3}")

def move_NO():
    pass
    #win.send_keystrokes("{VK_NUMPAD7}")

def move_SO():
    pass
    #win.send_keystrokes("{VK_NUMPAD1}")

def action_attack():
    pass
    #win.send_keystrokes("{a}")

def action_use():
    pass
    #win.send_keystrokes("{ENTER}")

def action_wait():
    pass
    #win.send_keystrokes("{Z}")

def action_throw():
    win.send_keystrokes("{1}")
    time.sleep(timetowait)
    win.send_keystrokes("{1}")

def action_ESC():
    pass
    #time.sleep(timetowait)
    #win.send_keystrokes("{ESC}")
    #time.sleep(timetowait)

def openInventory():
    pass
    #win.send_keystrokes("{i}")


def dead_newGame():
    win.set_focus()
    time.sleep(timetowait)
    win.move_window(x=None, y=None, width=None, height=None, repaint=True)
    win.send_keystrokes("{ESC}")
    time.sleep(timetowait)
    btn_deadNewGame = pyautogui.locateOnScreen('btn_deadNewGame.png')
    coords = pyautogui.center(btn_deadNewGame) # coordenadas centrais da imagem
    print(coords)
    time.sleep(timetowait)
    pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
    pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
    time.sleep(5)
    #win.send_keystrokes("{ESC}")
#dead_newGame()

def action_equip():
    backpack = read_backpack()
    if dictItemTypes[backpack[0]] == "weapon":
        win.send_keystrokes("{i}") # abre o inventário
        time.sleep(timetowait)
        win.click_input(coords=coords_backpack_1) # clica na coordenada do item x
        #btn_equip_loc = pyautogui.locateOnScreen('btn_equip.png') # busca pela imagem
        btn_equip_loc = pyautogui.locateOnWindow('btn_equip.png', "Pixel Dungeon")
        coords = pyautogui.center(btn_equip_loc) # coordenadas centrais da imagem
        print(coords)
        time.sleep(timetowait)
        pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
        pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
#action_equip()

def action_plant():
    backpack = read_backpack()
    if dictItemTypes[backpack[0]] == "seed":
        win.send_keystrokes("{i}") # abre o inventário
        win.click_input(coords=coords_backpack_1) # clica na coordenada do item x
        btn_equip_loc = pyautogui.locateOnWindow('btn_plant.png', "Pixel Dungeon")
        coords = pyautogui.center(btn_equip_loc) # coordenadas centrais da imagem
        print(coords)
        pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
        pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
#action_plant()

def action_eat():
    backpack = read_backpack()
    if dictItemTypes[backpack[0]] == "food":
        win.send_keystrokes("{i}") # abre o inventário
        win.click_input(coords=coords_backpack_1) # clica na coordenada do item x
        btn_equip_loc = pyautogui.locateOnWindow('btn_eat.png', "Pixel Dungeon")
        coords = pyautogui.center(btn_equip_loc) # coordenadas centrais da imagem
        print(coords)
        pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
        pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
#action_eat()

def action_drink():
    backpack = read_backpack()
    if dictItemTypes[backpack[0]] == "potion":
        win.send_keystrokes("{i}") # abre o inventário
        time.sleep(timetowait)
        win.click_input(coords=coords_backpack_1) # clica na coordenada do item x
        btn_equip_loc = pyautogui.locateOnWindow('btn_drinkp.png', "Pixel Dungeon")
        #locateonwindow??
        coords = pyautogui.center(btn_equip_loc) # coordenadas centrais da imagem
        print(coords)
        time.sleep(timetowait)
        pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
        pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
#action_drink()

def action_read():
    backpack = read_backpack()
    if dictItemTypes[backpack[0]] == "scroll":
        win.send_keystrokes("{i}") # abre o inventário
        time.sleep(timetowait)
        win.click_input(coords=coords_backpack_1) # clica na coordenada do item x
        btn_equip_loc = pyautogui.locateOnWindow('btn_read.png', "Pixel Dungeon")
        #locateonwindow??
        coords = pyautogui.center(btn_equip_loc) # coordenadas centrais da imagem
        print(coords)
        time.sleep(timetowait)
        pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
        pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
#action_read()

def action_drop():
    backpack = read_backpack()
    print(backpack)
    print(dictItemTypes[backpack[0]])
    if not dictItemTypes[backpack[0]] == "none":
        win.send_keystrokes("{i}") # abre o inventário
        time.sleep(timetowait)
        win.click_input(coords=coords_backpack_1) # clica na coordenada do item x
        btn_equip_loc = pyautogui.locateOnWindow('btn_drop.png', "Pixel Dungeon")
        coords = pyautogui.center(btn_equip_loc) # coordenadas centrais da imagem
        print(coords)
        time.sleep(timetowait)
        pyautogui.dragTo(coords.x, coords.y, button='middle') #move o mouse pra coordenada (precisa pois n estava clicando)
        pyautogui.click(coords.x, coords.y, button='left') # gambiarrastunadas.com.br
#action_drop()