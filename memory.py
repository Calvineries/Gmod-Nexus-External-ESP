import os, time
from pymem import Pymem, process, exception
from dataclasses import dataclass

while True:
    try:
        game_handle = Pymem('gmod.exe')
        client_dll = process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
        engine_dll = process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll
        materialsystem_dll = process.module_from_name(game_handle.process_handle, 'materialsystem.dll').lpBaseOfDll
        break
    except (exception.ProcessNotFound, AttributeError) as err:
        os.system('cls')
        print('gmod x64 not found')
        time.sleep(1)
        continue

@dataclass
class Memory:
    game_handle: 0
    client_dll: 0
    engine_dll: 0
    materialsystem_dll: 0