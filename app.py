import pyMeow as pm
import dearpygui.dearpygui as dpg
from gui import *
import threading
import win32api
import json
import requests
import ctypes

class Offsets:
    response = requests.get("https://raw.githubusercontent.com/Calvineries/Gmod-Nexus-External-ESP/refs/heads/master/offsets.json")
    githuboffsets = json.loads(response.text)
    try:
        LocalPlayer = int(githuboffsets["LocalPlayer"], 16)
        EntityList = int(githuboffsets["EntityList"], 16)
        ViewMatrix = int(githuboffsets["ViewMatrix"], 16)
        ForceJump = int(githuboffsets["ForceJump"], 16)
        MatFullbright = int(githuboffsets["MatFullbright"], 16)
        Crosshair = int(githuboffsets["Crosshair"], 16)
        BoneMatrix = int(githuboffsets["BoneMatrix"], 16)
        m_hObserverTarget = int(githuboffsets["m_hObserverTarget"], 16)
        m_hActiveWeapon = int(githuboffsets["m_hActiveWeapon"], 16)
        Weaponname = int(githuboffsets["Weaponname"], 16)
        Playername = int(githuboffsets["Playername"], 16)
        SteamID = int(githuboffsets["SteamID"], 16)
        lastupdate = str(githuboffsets["lastupdate"])
    except:
        pass

    try:
        with open("custom_offsets.json", "r") as jsonfile:
            data = json.load(jsonfile)
        if data["LocalPlayer"] != "":
            LocalPlayer = int(data["LocalPlayer"], 16)
        if data["EntityList"] != "":
            EntityList = int(data["EntityList"], 16)
        if data["ViewMatrix"] != "":
            ViewMatrix = int(data["ViewMatrix"], 16)
        if data["ForceJump"] != "":
            ForceJump = int(data["ForceJump"], 16)
        if data["MatFullbright"] != "":
            MatFullbright = int(data["MatFullbright"], 16)
        if data["Crosshair"] != "":
            Crosshair = int(data["Crosshair"], 16)
        if data["BoneMatrix"] != "":
            BoneMatrix = int(data["BoneMatrix"], 16)
        if data["m_hObserverTarget"] != "":
            m_hObserverTarget = int(data["m_hObserverTarget"], 16)
        if data["m_hActiveWeapon"] != "":
            m_hActiveWeapon = int(data["m_hActiveWeapon"], 16)
        if data["Weaponname"] != "":
            Weaponname = int(data["Weaponname"], 16)
        if data["Playername"] != "":
            Playername = int(data["Playername"], 16)
        if data["SteamID"] != "":
            SteamID = int(data["SteamID"], 16)
        if data["LocalPlayer"] or data["EntityList"] or data["ViewMatrix"] or data["ForceJump"] or data["MatFullbright"] or data["Crosshair"] or data["BoneMatrix"] or data["m_hObserverTarget"] or data["m_hActiveWeapon"] or data["Weaponname"] or data["Playername"] or data["SteamID"] != "":
            lastupdate = "offline"
    except FileNotFoundError:
        pass


class Colors:
    red = pm.get_color("#FF0000")
    orange = pm.get_color("orange")
    green = pm.get_color("#00FF00")
    white = pm.get_color("white")
    blue = pm.get_color("#0000FF")
    light_blue = pm.get_color("#00FFFF")
    hud = pm.get_color("#f5f5ff")
    hud_fade = pm.fade_color(pm.get_color("black"), 0.6)

class Entity:
    def __init__(self, addr, mem, gmod):
        self.wts = None
        self.addr = addr
        self.mem = mem
        self.gmod = gmod

        self.health = pm.r_int(self.mem, self.addr + 0xC8)
        self.team = pm.r_int(self.mem, self.addr + 0xD4)
        self.dormant = pm.r_int(self.mem, self.addr + 0xB4)
        self.noclipping = hex(pm.r_int(self.mem, self.addr + 0x84))
        self.visiblity = hex(pm.r_int64(self.mem, self.addr + 0x88))
        self.pos = pm.r_vec3(self.mem, self.addr + 0x308)
        self.bone_base = pm.r_int64(self.mem, self.addr + Offsets.BoneMatrix)
        try:
            self.name = pm.r_string(self.mem, self.addr + Offsets.Playername)
            self.steamid = pm.r_string(self.mem, self.addr + Offsets.SteamID)
            self.get_spectated_player = pm.r_uint(self.mem, self.addr + Offsets.m_hObserverTarget) & 0xFFF
            self.active_weapon = pm.r_uint(self.mem, self.addr + Offsets.m_hActiveWeapon) & 0xFFF
        except:
            pass



    def bone_pos(self, bone_id):
        return pm.vec3(
            pm.r_float(self.mem, self.bone_base + bone_id * 0x30 + 0x0C),
            pm.r_float(self.mem, self.bone_base + bone_id * 0x30 + 0x1C),
            pm.r_float(self.mem, self.bone_base + bone_id * 0x30 + 0x2C),
        )

class Local:
    def __init__(self, addr, mem, gmod):
        self.wts = None
        self.addr = addr
        self.mem = mem
        self.gmod = gmod
        self.pos = pm.r_vec3(self.mem, self.addr + 0x308)

def get_players():
    gmod_exe = pm.open_process("gmod.exe")
    client_dll = pm.get_module(gmod_exe, "client.dll")
    players = []
    
    for i in range(0, 128):
        ent_addr = pm.r_int64(gmod_exe, client_dll["base"] + Offsets.EntityList + i * 0x20)
        if ent_addr:
            ent = Entity(ent_addr, gmod_exe, client_dll["base"])
            try:
                if ent.name and "STEAM_" in ent.steamid:
                    players.append((ent.name, ent.steamid))
            except:
                pass

    return players

def start():
    gui.init_menu()
    threading.Thread(target=main, name='main', daemon=True).start()
    dpg.start_dearpygui()

def main():
    if not pm.process_exists("gmod.exe"):
        ctypes.windll.user32.MessageBoxW(0, "Please make sure that gmod is open. And that you are using the Chromium x64 branch.", "Gmod x64 not found.", 48)
        os._exit(0)
    gmod_exe = pm.open_process("gmod.exe")
    client_dll = pm.get_module(gmod_exe, "client.dll")
    engine_dll = pm.get_module(gmod_exe, "engine.dll")
    materialsystem_dll = pm.get_module(gmod_exe, "materialsystem.dll")

    pm.overlay_init("Garry's Mod (x64)", fps=60)

    pm.load_font(fileName="font/font.ttf", fontId=1)

    holding = False
    while pm.overlay_loop():
        if not pm.process_running(gmod_exe):
            os._exit(0)
        pm.begin_drawing()
        if dpg.get_value('c_hud'):
            pm.draw_rectangle_rounded(5, 5, 248, 30, 0.2, 4, Colors.hud_fade)
            pm.draw_rectangle_rounded_lines(5, 5, 248, 30, 0.2, 4, Colors.white, 2)
            pm.draw_text(f"Nexus ESP | {pm.get_fps()} fps", 12, 11, 24, Colors.hud)

            texts = []
            if dpg.get_value('c_box'):
                texts.append("ESP")
            if dpg.get_value('c_tracer'):
                texts.append("Tracer")
            if dpg.get_value('c_crosshair'):
                texts.append("Crosshair")
            if dpg.get_value('c_bhop'):
                texts.append("Bhop")
            if dpg.get_value('c_triggerbot'):
                if dpg.get_value('c_click_method') == "Hold":
                    texts.append("Triggerbot (Hold)")
                else:
                    texts.append("Triggerbot (Tap)")
            if dpg.get_value('c_fullbright'):
                texts.append("Fullbright")

            start_x = 5
            start_y = 37
            spacing = 27

            for i, text in enumerate(texts):
                y_offset = start_y + (i * spacing)

                pm.draw_rectangle_rounded(start_x, y_offset, pm.measure_text(text, 20) + 14, 24, 0.2, 4, Colors.hud_fade)
                pm.draw_rectangle_rounded_lines(start_x, y_offset, pm.measure_text(text, 20) + 14, 24, 0.2, 4, Colors.hud, 2)
                pm.draw_text(text, start_x + 7, y_offset + 4, 20, Colors.hud)

        try:
            local_player_addr = pm.r_int64(gmod_exe, client_dll["base"] + Offsets.LocalPlayer)
        except:
            continue
        if local_player_addr:
            view_matrix_base = pm.r_int64(gmod_exe, engine_dll["base"] + Offsets.ViewMatrix) + 0x2D4
            view_matrix = pm.r_floats(gmod_exe, view_matrix_base, 16)
            notif_offset = 5
            for i in range(0, 128):
                ent_addr = pm.r_int64(gmod_exe, client_dll["base"] + Offsets.EntityList + i * 0x20)
                if ent_addr == local_player_addr:
                    local_id = i
                if ent_addr > 0 and ent_addr != local_player_addr:
                    ent = Entity(ent_addr, gmod_exe, client_dll["base"])
                    try:
                        if not dpg.get_value('c_onlyplayer') or "STEAM_" in ent.steamid:
                            if dpg.get_value('c_spectate'):
                                if ent.get_spectated_player == local_id:
                                    if not isinstance(ent.name, bytes) and ent.name:
                                        name = f" Spectated by: {ent.name} "
                                        text_width = pm.measure_text(name, 24)
                                        x = pm.get_screen_width() // 2 - text_width // 2
                                        pm.draw_rectangle_rounded(x, notif_offset, text_width, 30, 0.2, 4, Colors.hud_fade)
                                        pm.draw_rectangle_rounded_lines(x, notif_offset, text_width, 30, 0.2, 4, Colors.white, 2)
                                        pm.draw_text(name, x, notif_offset + 6, 24, Colors.hud)
                                        notif_offset += 35
                            if not dpg.get_value('c_hidedormant') or ent.dormant != -65536:
                                if ent.health > 0:
                                    with open("friends.json", "r", encoding="utf-8") as f:
                                        friends = json.load(f)
                                    if not dpg.get_value('c_onlyfriends') or ent.steamid in friends:
                                        if dpg.get_value('c_maxdistance') != 0:
                                            local = Local(local_player_addr, gmod_exe, client_dll["base"])
                                            distance = pm.vec3_distance(local.pos, ent.pos)
                                            if int(distance / 32) > dpg.get_value('c_maxdistance') and ent.steamid not in friends:
                                                continue
                                        if dpg.get_value('c_entcolor') == "Unicolor":
                                            if ent.steamid in friends:
                                                color = dpg.get_value('c_friends_colors')
                                                r, g, b = map(int, color[:3])
                                                hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
                                                ent.color = pm.get_color(hex_color)
                                            else:
                                                color = dpg.get_value('c_unicolor')
                                                r, g, b = map(int, color[:3])
                                                hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
                                                ent.color = pm.get_color(hex_color)
                                        else:
                                            if dpg.get_value('c_entcolor') == "Visibility":
                                                if ent.visiblity != "0xffffffff":
                                                    ent.color = Colors.red
                                                    if dpg.get_value('c_hideinvisible'):
                                                        continue
                                                else:
                                                    if ent.noclipping != "0xff00":
                                                        ent.color = Colors.orange
                                                        if dpg.get_value('c_hidenoclipping'):
                                                            continue
                                                    else:
                                                        if ent.steamid in friends:
                                                            color = dpg.get_value('c_friends_colors')
                                                            r, g, b = map(int, color[:3])
                                                            hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
                                                            ent.color = pm.get_color(hex_color)
                                                        else:
                                                            ent.color = Colors.green

                                                if dpg.get_value('c_showinvisible'):
                                                    if ent.visiblity == "0xffffffff":
                                                        continue
                                                if dpg.get_value('c_shownoclipping'):
                                                    if ent.noclipping == "0xff00":
                                                        continue
                                            elif dpg.get_value('c_entcolor') == "Team":
                                                color = ((ent.team * 137) % 256 , (ent.team * 53) % 256, (ent.team * 197) % 256)
                                                r, g, b = map(int, color[:3])
                                                hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
                                                ent.color = pm.get_color(hex_color)
                                            else:
                                                health = max(0, min(ent.health, 100))
                                                g = int(health * 2.55)
                                                r = 255 - g
                                                b = 0
                                                ent.color = pm.get_color("#{:02X}{:02X}{:02X}".format(r, g, b))
                                        if dpg.get_value('c_esp_method') == "BonesPos (experimental)":
                                            try:
                                                local = Local(local_player_addr, gmod_exe, client_dll["base"])
                                                dist = pm.vec3_distance(local.pos, ent.pos)
                                                ent.wts = pm.world_to_screen(view_matrix, ent.pos, 1)
                                                head_pos = pm.world_to_screen(view_matrix, ent.bone_pos(7), 1)
                                                head = ent.wts["y"] - head_pos["y"]
                                                width = head / 2
                                                center = width / 2
                                                text_offset = 5
                                                if dpg.get_value('c_box'):
                                                    pm.draw_rectangle(
                                                        posX=head_pos["x"] - center,
                                                        posY=head_pos["y"] - center / 2,
                                                        width=width,
                                                        height=head + center / 2,
                                                        color=pm.fade_color(ent.color, 0.3),
                                                    )
                                                    pm.draw_rectangle_lines(
                                                        posX=head_pos["x"] - center,
                                                        posY=head_pos["y"] - center / 2,
                                                        width=width,
                                                        height=head + center / 2,
                                                        color=ent.color,
                                                        lineThick=1.8,
                                                    )
                                                if dpg.get_value('c_tracer'):
                                                    pm.draw_line(
                                                        startPosX=pm.get_screen_width() // 2,
                                                        startPosY=pm.get_screen_height() // 2,
                                                        endPosX=head_pos["x"] - center / 6,
                                                        endPosY=head_pos["y"] - center / 2,
                                                        color=ent.color,
                                                        thick=1.1,
                                                    )
                                                if dpg.get_value('c_hp_text'):
                                                    pm.draw_font(
                                                        fontId=1,
                                                        text=f"{ent.health}",
                                                        posX=ent.wts["x"],
                                                        posY=ent.wts["y"] + text_offset,
                                                        fontSize=15,
                                                        spacing=1,
                                                        tint=ent.color,
                                                    )
                                                    text_offset += 15
                                                if dpg.get_value('c_name'):
                                                    if ent.name:
                                                        pm.draw_font(
                                                            fontId=1,
                                                            text=ent.name,
                                                            posX=ent.wts["x"],
                                                            posY=ent.wts["y"] + text_offset,
                                                            fontSize=15,
                                                            spacing=1,
                                                            tint=ent.color,
                                                        )
                                                        text_offset += 15
                                                if dpg.get_value('c_weapon'):
                                                    weapon_handle = pm.r_int64(gmod_exe, client_dll["base"] + Offsets.EntityList + (ent.active_weapon - 1) * 0x20)
                                                    weapon_name = pm.r_string(gmod_exe, weapon_handle + Offsets.Weaponname)
                                                    if not isinstance(weapon_name, bytes) and weapon_name:
                                                        pm.draw_font(
                                                            fontId=1,
                                                            text=weapon_name,
                                                            posX=ent.wts["x"],
                                                            posY=ent.wts["y"] + text_offset,
                                                            fontSize=15,
                                                            spacing=1,
                                                            tint=ent.color,
                                                        )
                                                        text_offset += 15
                                                if dpg.get_value('c_distance'):
                                                    pm.draw_font(
                                                        fontId=1,
                                                        text=f"{int(dist/32)} m",
                                                        posX=ent.wts["x"],
                                                        posY=ent.wts["y"] + text_offset,
                                                        fontSize=15,
                                                        spacing=1,
                                                        tint=ent.color,
                                                    )
                                                    text_offset += 15
                                                if dpg.get_value('c_skeleton'):
                                                    if dpg.get_value('c_box'):
                                                        ent.color = Colors.white
                                                    neck = pm.world_to_screen(view_matrix, ent.bone_pos(5), 1)
                                                    shoulderRight = pm.world_to_screen(view_matrix, ent.bone_pos(9), 1)
                                                    shoulderLeft = pm.world_to_screen(view_matrix, ent.bone_pos(14), 1)
                                                    elbowRight = pm.world_to_screen(view_matrix, ent.bone_pos(10), 1)
                                                    elbowLeft = pm.world_to_screen(view_matrix, ent.bone_pos(15), 1)
                                                    handRight = pm.world_to_screen(view_matrix, ent.bone_pos(11), 1)
                                                    handLeft = pm.world_to_screen(view_matrix, ent.bone_pos(40), 1)
                                                    crotch = pm.world_to_screen(view_matrix, ent.bone_pos(0), 1)
                                                    kneeRight = pm.world_to_screen(view_matrix, ent.bone_pos(19), 1)
                                                    kneeLeft = pm.world_to_screen(view_matrix, ent.bone_pos(23), 1)
                                                    ankleRight = pm.world_to_screen(view_matrix, ent.bone_pos(21), 1)
                                                    ankleLeft = pm.world_to_screen(view_matrix, ent.bone_pos(25), 1)

                                                    pm.draw_line(neck["x"], neck["y"], shoulderRight["x"], shoulderRight["y"], ent.color, 1)
                                                    pm.draw_line(neck["x"], neck["y"], shoulderLeft["x"], shoulderLeft["y"], ent.color, 1)
                                                    pm.draw_line(elbowLeft["x"], elbowLeft["y"], shoulderLeft["x"], shoulderLeft["y"], ent.color, 1)
                                                    pm.draw_line(elbowRight["x"], elbowRight["y"], shoulderRight["x"], shoulderRight["y"], ent.color, 1)
                                                    pm.draw_line(elbowRight["x"], elbowRight["y"], handRight["x"], handRight["y"], ent.color, 1)
                                                    pm.draw_line(elbowLeft["x"], elbowLeft["y"], handLeft["x"], handLeft["y"], ent.color, 1)
                                                    pm.draw_line(neck["x"], neck["y"], crotch["x"], crotch["y"], ent.color, 1)
                                                    pm.draw_line(kneeRight["x"], kneeRight["y"], crotch["x"], crotch["y"], ent.color, 1)
                                                    pm.draw_line(kneeLeft["x"], kneeLeft["y"], crotch["x"], crotch["y"], ent.color, 1)
                                                    pm.draw_line(kneeLeft["x"], kneeLeft["y"], ankleLeft["x"], ankleLeft["y"], ent.color, 1)
                                                    pm.draw_line(kneeRight["x"], kneeRight["y"], ankleRight["x"], ankleRight["y"], ent.color, 1)

                                            except Exception as err:
                                                continue


                                        else:
                                            try:
                                                local = Local(local_player_addr, gmod_exe, client_dll["base"])
                                                dist = pm.vec3_distance(local.pos, ent.pos)
                                                width = 48000 / dist
                                                center = width / -2
                                                centerfix = center / 2
                                                ent.wts = pm.world_to_screen(view_matrix, ent.pos, 1)
                                                text_offset = 5
                                                if dpg.get_value('c_box'):
                                                    pm.draw_rectangle(
                                                        posX=ent.wts["x"] + centerfix,
                                                        posY=ent.wts["y"] - width,
                                                        width=width / 2,
                                                        height=width,
                                                        color=pm.fade_color(ent.color, 0.3),
                                                    )
                                                    pm.draw_rectangle_lines(
                                                        posX=ent.wts["x"] + centerfix,
                                                        posY=ent.wts["y"] - width,
                                                        width=width/2,
                                                        height=width,
                                                        color=ent.color,
                                                        lineThick=1.8,
                                                    )
                                                if dpg.get_value('c_tracer'):
                                                    pm.draw_line(
                                                        startPosX=pm.get_screen_width() // 2,
                                                        startPosY=pm.get_screen_height() // 2,
                                                        endPosX=ent.wts["x"],
                                                        endPosY=ent.wts["y"] - width,
                                                        color=ent.color,
                                                        thick=1.1,
                                                    )
                                                if dpg.get_value('c_hp_text'):
                                                    pm.draw_font(
                                                        fontId=1,
                                                        text=f"{ent.health}",
                                                        posX=ent.wts["x"],
                                                        posY=ent.wts["y"] + text_offset,
                                                        fontSize=15,
                                                        spacing=1,
                                                        tint=ent.color,
                                                    )
                                                    text_offset += 15
                                                if dpg.get_value('c_name'):
                                                    if ent.name:
                                                        pm.draw_font(
                                                            fontId=1,
                                                            text=ent.name,
                                                            posX=ent.wts["x"],
                                                            posY=ent.wts["y"] + text_offset,
                                                            fontSize=15,
                                                            spacing=1,
                                                            tint=ent.color,
                                                        )
                                                        text_offset += 15
                                                if dpg.get_value('c_weapon'):
                                                    weapon_handle = pm.r_int64(gmod_exe, client_dll["base"] + Offsets.EntityList + (ent.active_weapon - 1) * 0x20)
                                                    weapon_name = pm.r_string(gmod_exe, weapon_handle + Offsets.Weaponname) 
                                                    if not isinstance(weapon_name, bytes) and weapon_name:
                                                        pm.draw_font(
                                                            fontId=1,
                                                            text=weapon_name,
                                                            posX=ent.wts["x"],
                                                            posY=ent.wts["y"] + text_offset,
                                                            fontSize=15,
                                                            spacing=1,
                                                            tint=ent.color,
                                                        )
                                                        text_offset += 15
                                                if dpg.get_value('c_distance'):
                                                    pm.draw_font(
                                                        fontId=1,
                                                        text=f"{int(dist/32)} m",
                                                        posX=ent.wts["x"],
                                                        posY=ent.wts["y"] + text_offset,
                                                        fontSize=15,
                                                        spacing=1,
                                                        tint=ent.color,
                                                    )
                                                    text_offset += 15
                                            except Exception as err:
                                                continue
                    except Exception as err:
                        continue
        if dpg.get_value('c_crosshair'):
            try:
                if dpg.get_value('c_triggerbot'):
                    target = pm.r_int(gmod_exe, local_player_addr + Offsets.Crosshair)
                    if target <= 128 and target != 0:
                        color = Colors.blue
                        if dpg.get_value('c_click_method') == "Hold":
                            if not holding:
                                pm.mouse_down(button="left")
                                holding = True
                        else:
                            pm.mouse_click(button="left")
                    else:
                        color = Colors.light_blue
                        if dpg.get_value('c_click_method') == "Hold":
                            if holding:
                                pm.mouse_up(button="left")
                                holding = False

                else:
                    target = pm.r_int(gmod_exe, local_player_addr + Offsets.Crosshair)
                    if target <= 128 and target != 0:
                        color = Colors.red
                    else:
                        color = Colors.green
                    
                pm.draw_text(
                    text="+",
                    posX=pm.get_screen_width() // 2 - 10,
                    posY=pm.get_screen_height() // 2 - 18,
                    fontSize=40,
                    color=color,
                )
            except Exception as err:
                continue
        pm.end_drawing()


        if dpg.get_value('blatantcheck'):
            if dpg.get_value('c_bhop'):
                if win32api.GetAsyncKeyState(0x20) == 0:
                    continue
                noclipping = hex(pm.r_int(gmod_exe, local_player_addr + 0x84))
                if noclipping == "0xff00":
                    flag = pm.r_int(gmod_exe, local_player_addr + 0x440)
                    if flag == 257 or flag == 263 or flag == 33025 or flag == 1280 or flag == 1281:
                        pm.w_int(gmod_exe, client_dll["base"] + Offsets.ForceJump, 5)
                    else:
                        pm.w_int(gmod_exe, client_dll["base"] + Offsets.ForceJump, 4)

            if dpg.get_value('c_fullbright'):
                if pm.r_byte(gmod_exe, materialsystem_dll["base"] + Offsets.MatFullbright) == 32:
                    pm.w_byte(gmod_exe, materialsystem_dll["base"] + Offsets.MatFullbright, 33)
            else:
                if pm.r_byte(gmod_exe, materialsystem_dll["base"] + Offsets.MatFullbright) == 33:
                    pm.w_byte(gmod_exe, materialsystem_dll["base"] + Offsets.MatFullbright, 32)

if __name__ == "__main__":
    gui = GUI()
    start()
