import numpy as np
import sys
#from PIL import Image as im
from ReadWriteMemory import ReadWriteMemory
import pymem
from utils import *
from enum import Enum, unique
import time
start_time = time.time()
#pm = pymem.Pymem("PD.exe")
#rwm = ReadWriteMemory()

# 10/11/2021


process = rwm.get_process_by_name("PD.exe")
process.open()

baseAddress_equipment_1 = pymem.process.module_from_name(pm.process_handle, "jvm.dll").lpBaseOfDll
baseAddress_bag_1 = pymem.process.module_from_name(pm.process_handle, "jvm.dll").lpBaseOfDll

n_itens_bag = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0036E654, offsets=[0x40, 0x48, 0x28, 0x48, 0x44, 0x38, 0x74, 0x30, 0xc]))
#print(n_itens_bag)

equipment_1 = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x10]))
equipment_1_id = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x10, 0x8]))
equipment_1_upg = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x10, 0x10]))
#print(hex(equipment_1), ItemId(equipment_1_id).name, dictItemTypes[equipment_1_id], equipment_1_upg)

equipment_2 = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x14]))
equipment_2_id = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x14, 0x8]))
equipment_2_upg = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x14, 0x10]))
#print(hex(equipment_2), ItemId(equipment_2_id).name, dictItemTypes[equipment_2_id], equipment_2_upg)

equipment_3 = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x18]))
equipment_3_id = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x18, 0x8]))
equipment_3_upg = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x18, 0x10]))
#print(hex(equipment_3), ItemId(equipment_3_id).name, dictItemTypes[equipment_3_id], equipment_3_upg)

equipment_4 = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x1C]))
equipment_4_id = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x1C, 0x8]))
equipment_4_upg = process.read(process.get_pointer(baseAddress_equipment_1 + 0x0037B434, offsets=[0xb0, 0xc0, 0x34, 0xcc, 0x74, 0x1C, 0x10]))
#print(hex(equipment_4), ItemId(equipment_4_id).name, dictItemTypes[equipment_4_id], equipment_4_upg)

bag_1 = process.read(process.get_pointer(baseAddress_bag_1 + 0x0036E714, offsets=[0xc, 0x24, 0x28c, 0xec, 0x14, 0x14, 0x24, 0x30, 0xC]))
#print(dictItemTypes[bag_1])

def read_backpack():
    pass
    backpack = []
    for pointer_num in range(1, 20): #são 19 slots na backpack #fazer loop só até o n de itens na bag, o resto substituir por 0
        acc_offset = 0x4 * pointer_num + 0x8

        if pointer_num <= n_itens_bag: #quando chega no nº de itens na bag, substitui o resto por 0
            pointer_backpack = process.read(process.get_pointer(baseAddress_bag_1 + 0x0036E654, offsets=[0x40, 0x48, 0x28, 0x48, 0x44, 0x38, 0x74, 0x30, 0x10, acc_offset]))
            backpack_id = process.read(process.get_pointer(baseAddress_bag_1 + 0x0036E654, offsets=[0x40, 0x48, 0x28, 0x48, 0x44, 0x38, 0x74, 0x30, 0x10, acc_offset, 0x8]))
            backpack_qt = process.read(process.get_pointer(baseAddress_bag_1 + 0x0036E654, offsets=[0x40, 0x48, 0x28, 0x48, 0x44, 0x38, 0x74, 0x30, 0x10, acc_offset, 0xc]))
            backpack_dura = process.read(process.get_pointer(baseAddress_bag_1 + 0x0036E654, offsets=[0x40, 0x48, 0x28, 0x48, 0x44, 0x38, 0x74, 0x30, 0x10, acc_offset, 0x14]))

            #print(hex(acc_offset))
            #print(pointer)
            #backpack.append(pointer_backpack)
            backpack.append(backpack_id)
            #print(ItemId(backpack_id), backpack_qt, backpack_dura)
            #print(ItemId(backpack_id).name, dictItemTypes[backpack_id])
        else:
            #pointer_backpack = 0
            backpack_id = 0
            #backpack.append(pointer_backpack)
            backpack.append(backpack_id)
    return backpack
backpack = read_backpack()


