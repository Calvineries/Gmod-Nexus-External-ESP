import dearpygui.dearpygui as dpg
import helper
import offsets
from app import *
from local import *

def enableblatant():
    dpg.configure_item("c_triggerbot", enabled=True)
    dpg.configure_item("c_triggerbotkey", enabled=True)
    dpg.configure_item("c_triggerbotkey_z", enabled=True)
    dpg.configure_item("c_bhop", enabled=True)
    dpg.configure_item("c_norecoil", enabled=True)
    dpg.configure_item("c_aimassist", enabled=True)
    dpg.configure_item("c_fullbright", enabled=True)
    dpg.configure_item("blatantcheck", show=False)

def fullbright():
    mem = Memory(game_handle, client_dll, engine_dll, materialsystem_dll)
    lp = LocalPlayer(mem)
    lp.mat_fullbright()
    
class GUI():
    def __init__(self) -> None:
        self.random_string = helper.get_random_string()

    def init_menu(self) -> None:
        dpg.create_context()
        dpg.create_viewport(title=self.random_string, decorated=True, width=600, height=400)
        with dpg.window(tag='w_main'):
            with dpg.tab_bar():
                with dpg.tab(label='ESP'):
                    dpg.add_checkbox(label='Box ESP', tag='c_box', default_value=True)
                    with dpg.tooltip("c_box"):
                        dpg.add_text("Draws a box over players")
                    dpg.add_checkbox(label='Tracer ESP', tag='c_tracer')
                    with dpg.tooltip("c_tracer"):
                        dpg.add_text("Draws tracer lines to players")
                    dpg.add_checkbox(label='HP', tag='c_hp_text', default_value=True)
                    dpg.add_checkbox(label='Name', tag='c_name', default_value=True)
                    dpg.add_checkbox(label='Distance', tag='c_distance')
                    dpg.add_checkbox(label='Crosshair', tag='c_crosshair', default_value=True)
                    with dpg.tooltip("c_crosshair"):
                        dpg.add_text("Dynamic crosshair.\n\nWhen you look at a player the crosshair turns red.\nIf you activate the triggerbot:\nthe crosshair will be blue, if you look\nat a player it will be dark blue.")
                    dpg.add_text("")
                    dpg.add_checkbox(label='Hide Dormants', tag='c_hidedormant')
                    with dpg.tooltip("c_hidedormant"):
                        dpg.add_text("Hide Dormant Players on the ESP.\n\nPlayers become dormant when they leave\nthe Potential Visibility Set on the server.\nThis can also exclude fake players on the ESP.")
                    dpg.add_checkbox(label='Hide Invisible', tag='c_hideinvisible')
                    dpg.add_checkbox(label='Hide Noclipping', tag='c_hidenoclipping')
                    dpg.add_checkbox(label='Only Invisible', tag='c_showinvisible')
                    dpg.add_checkbox(label='Only Noclipping', tag='c_shownoclipping')
                    dpg.add_text("")
                    dpg.add_checkbox(label='Debug', tag='c_debug')
                    with dpg.tooltip("c_debug"):
                        dpg.add_text("Displays additional information\nabout players such as their team\nor visibility values.")   
                with dpg.tab(label='Blatant'):
                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(label='Triggerbot       ', tag='c_triggerbot', enabled=False)
                        with dpg.tooltip("c_triggerbot"):
                            dpg.add_text("Clicks for you when you are hovering over a target")
                        dpg.add_checkbox(label='Keybind ("Z")', tag='c_triggerbotkey_z', enabled=False)
                        with dpg.tooltip("c_triggerbotkey_z"):
                            dpg.add_text("Toggle Triggerbot when you press Z.")
                        dpg.add_checkbox(label='Keybind ("W")', tag='c_triggerbotkey', enabled=False)
                        with dpg.tooltip("c_triggerbotkey"):
                            dpg.add_text("Toggle Triggerbot when you press W.")
                    dpg.add_checkbox(label='Bhop             ', tag='c_bhop', enabled=False)
                    dpg.add_checkbox(label='No Recoil', tag='c_norecoil', enabled=False)
                    with dpg.tooltip("c_norecoil"):
                        dpg.add_text("Compensates the weapon's recoil automatically.\n\nNot perfect, easily detectable,\ndoesn't work with some weapons.")
                    dpg.add_checkbox(label='Aim Assist (experimental)', tag='c_aimassist', enabled=False)
                    with dpg.tooltip("c_aimassist"):
                        dpg.add_text("Lock a player.\n\nNot finished. Broken")
                    dpg.add_checkbox(label='Fullbright (detected)', tag='c_fullbright', enabled=False, callback=fullbright)
                    with dpg.tooltip("c_fullbright"):
                        dpg.add_text("Turns up brightness to see in the dark.\n\nYou can be detected very easily by many ways!")
                    dpg.add_text("")
                    dpg.add_text("Detected by some anticheats!", color=(240, 47, 28))
                    dpg.add_checkbox(label='Enable writing to game memory', tag="blatantcheck", callback=enableblatant)
                    with dpg.tooltip("blatantcheck"):
                        dpg.add_text("By default, Nexus External only lets you\nenable cheats that only read game memory,\nwhich is undetectable for a game like gmod.\n\nBy checking this box, you will be able to use\nother cheats that write to the game's memory,\ngood anticheats can detect this.")
                with dpg.tab(label='Config'):
                    dpg.add_checkbox(label='Notification when you are being screengrabbed', tag="c_screengrab", default_value=True)
                    with dpg.tooltip("c_screengrab"):
                        dpg.add_text("Show a message below the crosshair\nif the server try to take a screenshot\nof your game.\n\nThis is just for fun.\nThis cheat is completely external and\ncannot be screengrabbed. This feature\ndoes not prevent screengrabs,\nthat would be stupid.\n\nCan also be wrong if the\nserver does weird things.")
                    dpg.add_checkbox(label='Notification when someone is spectating you', tag="c_spectate", default_value=True)
                    with dpg.tooltip("c_spectate"):
                        dpg.add_text("Show a message below the crosshair\nif someone is spectating you.")
                    with dpg.group(horizontal=True):
                        dpg.add_text("ESP Color")
                        dpg.add_radio_button(tag="c_entcolor", items=['Unicolor', 'Visibility', 'Team'], default_value="Visibility")
                    dpg.add_text("")
                    with dpg.group(horizontal=True):
                        dpg.add_text("Max Distance")
                        dpg.add_slider_int(min_value=0, max_value=1000, tag="c_maxdistance", default_value=0)

                with dpg.tab(label='About'):
                    dpg.add_text("[Nexus External ESP]")
                    dpg.add_text("Version: 1.4")
                    dpg.add_text(f"Gmod version: {offsets.gversion}")
                    dpg.add_text("")
                    dpg.add_text("© Calvineries / Calvin Honecker\n(Forked from BetterGo of OpsecGuy.)")
                    dpg.add_text("")
                    dpg.add_text("This cheat is free. Resale = Scam!\nCe cheat est gratuit. Revente = Arnaque !", color=(240, 47, 28))
                    dpg.add_text("github.com/Calvineries/Gmod-Nexus-External-ESP", color=(28, 47, 240))

        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core) 
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 20, 7 , category=dpg.mvThemeCat_Core) 
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 20 , category=dpg.mvThemeCat_Core) 

        dpg.bind_theme(global_theme)

        #dpg.show_style_editor()
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("w_main", True)