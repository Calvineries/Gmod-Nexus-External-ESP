from memory import *
from entity import * 
from local import *
from gui import *
from overlay import *
from helper import ScreenSize
import threading
import keyboard
import math

#Unused in not compiled version.
'''''''''
import webbrowser
import requests

response = requests.get("https://pastebin.com/raw/8w0wMM9R")
content = response.text
if "1.3.1" not in content:
    webbrowser.open("https://github.com/Calvineries/Gmod-Nexus-External-ESP/releases")
    with open("Please download the latest version of the cheat.", 'w'):
        pass
    with open("Veuillez télécharger la dernière version du cheat.", 'w'):
        pass
    os._exit(0)
'''''''''

DEBUG_MODE = False

def entity_loop():
    while True:
        try:
            ent.entity_loop()
        except Exception as err:
            if DEBUG_MODE == True:
                print(entity_loop.__name__, err)
            pass
        #Default 0.001
        time.sleep(0.01)

def opengl_overlay():
    global ov
    ov = Overlay()
    center_x = ScreenSize.x/2-2.5
    center_y = ScreenSize.y/2-5.5
    global screengrabed
    screengrabed = False
    current_spectated = False
    while True:
        try:
            local_player = lp.local_player()
            view_matrix = lp.view_matrix()
            if dpg.get_value('c_screengrab'):
                if screengrabed == True:
                    ov.draw_text('SCREENGRAB', center_x-45, center_y-45, (0,1,0), 0.5)
            if dpg.get_value('c_spectate'):
                if current_spectated == True:
                    ov.draw_text('SPECTATED', center_x-40, center_y-25, (0,1,0), 0.5)
            if dpg.get_value('c_crosshair'):
                target = mem.game_handle.read_int(local_player + offsets.m_iIDEntIndex)

                if dpg.get_value('c_triggerbot'):
                    if target != 0 and target <= ent.get_server_slots():
                        crosshaircolor = (0.0, 0.0, 1.0)
                    else:
                        crosshaircolor = (0.0, 1.0, 1.0)
                else:
                    if target != 0 and target <= ent.get_server_slots():
                        crosshaircolor = (1.0, 0.0, 0.0)
                    else:
                        crosshaircolor = (0.0, 1.0, 0.0)
                ov.draw_full_box(center_x+3, center_y-4, 0.5, 16, 2, crosshaircolor)
                ov.draw_full_box(center_x-5, center_y+4, 16, 0.5, 2, crosshaircolor)

            for entity in ent.entity_list:
                if entity[1] == local_player:
                    continue

                if ent.is_spectating(entity[1]) != 0:
                    spectate_id = mem.game_handle.read_longlong(mem.client_dll + offsets.dwEntityList + (ent.spectating_target(entity[1]) - 1) * 0x20)
                    if spectate_id == lp.local_player():
                        current_spectated = True



                if ent.get_health(entity[1]) <= 0:
                    continue
                entity_position = ent.get_position(entity[1])
                if entity_position == Vector3(0,0,0) or entity_position == None:
                    continue
                w2s_position = ov.w2s(entity_position, view_matrix)
                if w2s_position is None:
                    continue
                #Filtres
                if dpg.get_value('c_hidenoclipping'):
                    if ent.is_noclipping(entity[1]) != "0xff00":
                        continue

                if dpg.get_value('c_hidedormant'):
                    if ent.is_dormant(entity[1]) == -65536:
                        continue

                if dpg.get_value('c_hideinvisible'):
                    #Hide invisibles on ESP
                    #If is_invisible != visible -> do not display
                    #If is_spectating != nospec -> do not display
                    if ent.is_invisible(entity[1]) != "0xffffffff":
                        continue
                    if ent.is_spectating(entity[1]) != 0:
                        continue

                if dpg.get_value('c_showinvisible'):
                    if ent.is_invisible(entity[1]) == "0xffffffff":
                        if ent.is_spectating(entity[1]) == 0:
                            continue

                if dpg.get_value('c_shownoclipping'):
                    if ent.is_noclipping(entity[1]) == "0xff00":
                        continue

                if dpg.get_value('c_maxdistance') != 0:
                    dist = distance(ent.get_position(local_player), entity_position)
                    if int(dist / 32) > dpg.get_value('c_maxdistance'):
                        continue
                #Colors
                if dpg.get_value('c_entcolor') == "Unicolor":
                    entcolor = (0,1,0)
                else:
                    if dpg.get_value('c_entcolor') == "Visibility":
                        if ent.is_invisible(entity[1]) != "0xffffffff":
                            entcolor = (1,0,0)
                        elif ent.is_spectating(entity[1]) != 0:
                            entcolor = (1,0,0)
                        else:
                            if ent.is_noclipping(entity[1]) != "0xff00":
                                entcolor = (1,0.5,0)
                            else:
                                entcolor = (0,1,0)
                    else:
                        team = ent.get_team(entity[1])
                        entcolor = ((team * 137) % 256 / 255.0, (team * 53) % 256 / 255.0, (team * 197) % 256 / 255.0)

                #ESP
                if dpg.get_value('c_tracer'):
                    ov.draw_line(center_x, 0, w2s_position[0], w2s_position[1], 1.3, entcolor)

                if dpg.get_value('c_hp_text'):
                    ov.draw_text(f'{ent.get_health(entity[1])}', w2s_position[0], w2s_position[1] - 15, entcolor, 1.0)

                if dpg.get_value('c_distance'):
                    dist = distance(ent.get_position(local_player), entity_position)
                    #Multiples lines
                    if dpg.get_value('c_hp_text'):
                        ov.draw_text(f'{int(dist / 32)} m', w2s_position[0], w2s_position[1] - 30, entcolor, 1.0)
                    else:
                        ov.draw_text(f'{int(dist / 32)} m', w2s_position[0], w2s_position[1] - 15, entcolor, 1.0)

                if dpg.get_value('c_box'):
                    dist = distance(ent.get_position(local_player), entity_position)
                    if dist == 0:
                        continue
                    length = 40000 / dist
                    center = length / -2
                    centerfix = center /2
                    ov.draw_full_box(w2s_position[0] + centerfix, w2s_position[1], length/2, length, 2, entcolor)
                    
                if dpg.get_value('c_debug'):
                    if dpg.get_value('c_distance'):
                        ov.draw_text(f'ID: {entity[0]} | Team: {ent.get_team(entity[1])}', w2s_position[0], w2s_position[1] - 45, entcolor, 1.0)
                        ov.draw_text(f'Visibility: {ent.is_invisible(entity[1])} | Spectating: {ent.is_spectating(entity[1])}', w2s_position[0], w2s_position[1] - 60, entcolor, 1.0)
                        ov.draw_text(f'NoClip: {ent.is_noclipping(entity[1])} | Dormant: {ent.is_dormant(entity[1])}', w2s_position[0], w2s_position[1] - 75, entcolor, 1.0)
                    else:
                        ov.draw_text(f'ID: {entity[0]} | Team: {ent.get_team(entity[1])}', w2s_position[0], w2s_position[1] - 30, entcolor, 1.0)
                        ov.draw_text(f'Visibility: {ent.is_invisible(entity[1])} | Spectating: {ent.is_spectating(entity[1])}', w2s_position[0], w2s_position[1] - 45, entcolor, 1.0)
                        ov.draw_text(f'NoClip: {ent.is_noclipping(entity[1])} | Dormant: {ent.is_dormant(entity[1])}', w2s_position[0], w2s_position[1] - 60, entcolor, 1.0)
        except Exception as err:
            if DEBUG_MODE == True:
                print(opengl_overlay.__name__, err)
            pass
        ov.refresh()
        time.sleep(0.001)

def trigger_bot():
    global triggeractivated
    triggeractivated = 0
    while True:     
        try:
            if dpg.get_value('c_triggerbot'):
                target = mem.game_handle.read_int(lp.local_player() + offsets.m_iIDEntIndex)
                #If target player ID is less than max online player
                if target <= ent.get_server_slots():
                    #If target player ID is not 0
                    if target != 0:
                        lp.force_attack(5)
                        time.sleep(0.025)
                        triggeractivated = 1
                    else:
                        if triggeractivated == 1:
                            lp.force_attack(4)
                            triggeractivated = 0

        except Exception as err:
            if DEBUG_MODE == True:
                print(trigger_bot.__name__, err)
            pass
        time.sleep(0.01)

#Broken, unfinished
def aimassist():
    while True:
        try:
            if dpg.get_value('c_aimassist'):
                for entity in ent.entity_list:
                    if ent.get_health(entity[1]) <= 0:
                        continue
                    entcoords = ent.get_position(entity[1])
                    lpcoords = ent.get_position(lp.local_player())

                    angle1 = math.degrees(math.atan2(entcoords.y - lpcoords.y, entcoords.x - lpcoords.x))
                    #angle2dist = math.sqrt((entcoords.x - mycoords.x)**2 + (entcoords.y - mycoords.y))
                    #angle2 = math.degrees(math.atan2(entcoords.z - mycoords.z, angle2dist))
                    
                    subtraction = lp.get_view_angle1() - angle1
                    dist = distance(lpcoords, entcoords)
                    gradient = (7 - 2) / (5 - 45)
                    value = 2 + gradient * (dist/32 - 45)
                    if dist/32 < 46 and dist/32 > 2:
                        if subtraction < value and subtraction > -value:
                            lp.set_view_angle1(angle1)
                            #lp.set_view_angle2(angle2)
        except Exception as err:
            if DEBUG_MODE == True:
                print(aimassist.__name__, err)
            pass
        time.sleep(0.01)

def bhop():
    while True:
        try:
            if dpg.get_value('c_bhop'):
                while ctypes.windll.user32.GetAsyncKeyState(0x20):
                    if ent.is_noclipping(lp.local_player()) == "0xff00":
                        bhopstate = mem.game_handle.read_int(lp.local_player() + offsets.m_fFlags)
                        if bhopstate == 257 or bhopstate == 33025:
                            lp.force_jump(5)
                        else:
                            lp.force_jump(4)
        except Exception as err:
            if DEBUG_MODE == True:
                print(bhop.__name__, err)
            pass
        time.sleep(0.01)

def attackchecker():
    global is_attacking
    while True:
        try:
            if dpg.get_value('c_norecoil'):
                if lp.attack_state() == 5:
                    time.sleep(0.15)
                    if lp.attack_state() == 5:
                        is_attacking = True
                    else:
                        is_attacking = False
                else:
                    is_attacking = False
        except Exception as err:
            if DEBUG_MODE == True:
                print(attackchecker.__name__, err)        
        time.sleep(0.01)


def norecoil():
    global triggeractivated
    while True:
        try:
            if dpg.get_value('c_norecoil'):
                angle2 = lp.get_view_angle2()
                while ctypes.windll.user32.GetAsyncKeyState(0x01) or triggeractivated == 1:
                    if is_attacking == True:
                        punch_angle_base = mem.game_handle.read_longlong(lp.local_player()+0x40)
                        punch_angle_pointer1 = mem.game_handle.read_longlong(punch_angle_base+0x40)
                        punch_angle_pointer2 = mem.game_handle.read_longlong(punch_angle_pointer1+0x20)
                        punch_angle = mem.game_handle.read_float(punch_angle_pointer2+0x0)
                        if punch_angle < 0.0:
                            lp.set_view_angle2(abs(punch_angle) + angle2)
        except Exception as err:
            if DEBUG_MODE == True:
                print(norecoil.__name__, err)
        time.sleep(0.01)

def keys():
    while True:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
                if dpg.get_value('c_triggerbotkey'):
                    if dpg.get_value('c_triggerbot'):
                        dpg.set_value('c_triggerbot', False)
                    else:
                        dpg.set_value('c_triggerbot', True)
            if event.event_type == keyboard.KEY_DOWN and event.name == 'z':
                if dpg.get_value('c_triggerbotkey_z'):
                    if dpg.get_value('c_triggerbot'):
                        dpg.set_value('c_triggerbot', False)
                    else:
                        dpg.set_value('c_triggerbot', True)
        except Exception as err:
            if DEBUG_MODE == True:
                print(keys.__name__, err)        
        time.sleep(0.1)

def screengrab():
    global screengrabed
    while True:
        try:
            if dpg.get_value('c_screengrab'):
                screengrab_base = mem.game_handle.read_longlong(mem.engine_dll + offsets.screengrab)
                screengrab = mem.game_handle.read_uint(screengrab_base + 0x108)
                if screengrab == 2:
                    screengrabed = True
                else:
                    screengrabed = False
        except Exception as err:
            dpg.set_value('c_screengrab', False)
            if DEBUG_MODE == True:
                print(screengrab.__name__, err)
            pass
        time.sleep(1)
                    
def exit():
    ov.close()
    os._exit(0)  

def main():
    try:
        gui.init_menu()
        threading.Thread(target=opengl_overlay, name='opengl_overlay', daemon=True).start()
        time.sleep(0.5)
        threading.Thread(target=entity_loop, name='entity_loop', daemon=True).start()  
        threading.Thread(target=trigger_bot, name='trigger_bot', daemon=True).start()
        threading.Thread(target=aimassist, name='aimassist', daemon=True).start()
        threading.Thread(target=bhop, name='bhop', daemon=True).start()
        threading.Thread(target=norecoil, name='norecoil', daemon=True).start()
        threading.Thread(target=attackchecker, name='attackchecker', daemon=True).start()
        threading.Thread(target=screengrab, name='screengrab', daemon=True).start()

        threading.Thread(target=keys, name='keys', daemon=True).start()

        dpg.start_dearpygui()
    except Exception as err:
        print(err)
        os._exit(0)

if __name__ == '__main__':
    try:
        mem = Memory(game_handle, client_dll, engine_dll, materialsystem_dll)
        lp = LocalPlayer(mem)
        ent = Entity(mem)
        gui = GUI()
        main()
    except (Exception, KeyboardInterrupt) as err:
        print(err)
        os._exit(0)