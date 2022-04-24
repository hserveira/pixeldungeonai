from utils import *
import time
start_time = time.time()
pm = pymem.Pymem("PD.exe")
rwm = ReadWriteMemory()

# 30/10/2021
# 01/11/2021 - ok!

process = rwm.get_process_by_name("PD.exe")
process.open()

baseAddress_player_pos = pymem.process.module_from_name(pm.process_handle, "java.dll").lpBaseOfDll
pointer_player_pos = pymem.process.module_from_name(pm.process_handle, "jvm.dll").lpBaseOfDll
#player_pos_value = process.read(process.get_pointer(pointer_player_pos + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc]))

# Mesma lógica do tile_reader.py

def read_playerPos():
    player_pos_value = process.read(process.get_pointer(pointer_player_pos + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc]))
    playerPos = []
    for pointer_num in range(2, 1026): #"java.dll"+0001CF4C + 0x0 + 0x144 + 0x7c
        acc_offset = 0x4 * pointer_num + 0x84
        pointer = process.read(process.get_pointer(baseAddress_player_pos + 0x0001CF4C, offsets=[0x0, 0x144, acc_offset]))

        # codificação one-hot [0: vazio | 1: player | 2: inimigo]
        if pointer == player_pos_value: #player
            playerPos.append(1)
        elif pointer == 0:  #vazio
            playerPos.append(pointer)
        else: #inimigo (não tem um id fixo)
            playerPos.append(2)

    playerPos = np.array(playerPos)
    playerPos.reshape(32, 32)
    playerPos = playerPos.astype(np.float32)
    return playerPos
#player_pos = read_playerPos()
#print(player_pos)


