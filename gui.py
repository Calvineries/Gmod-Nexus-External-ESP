import dearpygui.dearpygui as dpg
import app
import json
import os

FRIENDS_FILE = "friends.json"

def enableblatant():
    dpg.configure_item("c_triggerbot", enabled=True)
    dpg.configure_item("c_click_method", enabled=True)
    dpg.configure_item("c_bhop", enabled=True)
    dpg.configure_item("c_fullbright", enabled=True)
    dpg.configure_item("blatantcheck", show=False)

def bone_mode():
    if dpg.get_value('c_esp_method') == "BonesPos (experimental)":
        dpg.configure_item("c_skeleton", enabled=True)
    else:
        dpg.configure_item("c_skeleton", enabled=False, default_value=False)

def load_friends():
    if os.path.exists(FRIENDS_FILE):
        with open(FRIENDS_FILE, "r") as f:
            return json.load(f)
    return []

def save_friends(friends):
    with open(FRIENDS_FILE, "w") as f:
        json.dump(friends, f, indent=4)

def toggle_friend(sender, app_data, user_data):
    steam_id = user_data 
    friends = load_friends()
    if steam_id in friends:
        friends.remove(steam_id)
    else:
        friends.append(steam_id)
    save_friends(friends)
    get_playerlist() 

def get_playerlist():
    player_data = app.get_players()
    friends = load_friends()
    if dpg.does_item_exist("player_table"):
        children = dpg.get_item_children("player_table", 1)
        if children:
            for child in children:
                dpg.delete_item(child)
        for player_name, steam_id in player_data:
            with dpg.table_row(parent="player_table"):
                dpg.add_text(player_name)
                dpg.add_text(steam_id)
                label = "Unfriend" if steam_id in friends else "Friend"
                dpg.add_button(label=label, callback=toggle_friend, user_data=steam_id)



class GUI():
    def init_menu(self) -> None:
        dpg.create_context()
        dpg.create_viewport(title="Nexus External ESP - V2", decorated=True, width=600, height=400)
        with dpg.window(tag='w_main'):
            with dpg.tab_bar():
                with dpg.tab(label='Visuals'):
                    dpg.add_checkbox(label='Box ESP', tag='c_box', default_value=True)
                    with dpg.tooltip("c_box"):
                        dpg.add_text("Draws a box over players.")
                    dpg.add_checkbox(label='Skeleton ESP', tag='c_skeleton', enabled=False)
                    with dpg.tooltip("c_skeleton"):
                        dpg.add_text("Draws player skeletons.\nIf the server has a badly made model, it will show a messed up skeleton.")
                    dpg.add_checkbox(label='Tracer ESP', tag='c_tracer')
                    with dpg.tooltip("c_tracer"):
                        dpg.add_text("Draws tracer lines to players.")
                    dpg.add_checkbox(label='HP', tag='c_hp_text', default_value=True)
                    dpg.add_checkbox(label='Name', tag='c_name', default_value=True)
                    dpg.add_checkbox(label='Weapon', tag='c_weapon', default_value=True)
                    with dpg.tooltip("c_weapon"):
                        dpg.add_text("Draws the name of the held weapon.")
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
                    dpg.add_checkbox(label='Only Real Players', tag='c_onlyplayer', default_value=True)
                    with dpg.tooltip("c_onlyplayer"):
                        dpg.add_text("Show only entities with a SteamID.\n\nAllows you to hide entities that are\nnot real players.\nMust be unchecked if you want to do\ntesting with bots.")
                    dpg.add_checkbox(label='Only Friends', tag='c_onlyfriends')
                    dpg.add_checkbox(label='Only Invisible', tag='c_showinvisible')
                    dpg.add_checkbox(label='Only Noclipping', tag='c_shownoclipping') 

                with dpg.tab(label='Players'):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Refresh", callback=get_playerlist)
                        dpg.add_color_edit(default_value=(0, 255, 255), tag='c_friends_colors', label="Friend Color",display_type=dpg.mvColorEdit_uint8, no_inputs=True, no_alpha=True)
                    with dpg.table(tag="player_table", header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, resizable=True):
                        dpg.add_table_column(label="Name")
                        dpg.add_table_column(label="SteamID")
                        dpg.add_table_column(label="Action")

                with dpg.tab(label='Blatant'):
                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(label='Triggerbot', tag='c_triggerbot', enabled=False)
                        with dpg.tooltip("c_triggerbot"):
                            dpg.add_text("Clicks for you when you are hovering over a target.")
                        dpg.add_radio_button(tag="c_click_method", items=['Hold', 'Tap'], default_value="Hold", horizontal=True, enabled=False)
                        with dpg.tooltip("c_click_method"):
                            dpg.add_text("Should the triggerbot hold the click or spam click.")
                    dpg.add_checkbox(label='Bhop', tag='c_bhop', enabled=False)
                    dpg.add_text("")
                    with dpg.collapsing_header(label='Very dangerous', tag='c_verydangerous'):
                        with dpg.tooltip("c_verydangerous"):
                            dpg.add_text("These cheats are dangerous, do not\nuse them on a server with an anticheat!", color=(240, 47, 28))
                        dpg.add_checkbox(label='Fullbright', tag='c_fullbright', enabled=False)
                        with dpg.tooltip("c_fullbright"):
                            dpg.add_text("Turns up brightness to see in the dark.")
                    dpg.add_text("")
                    dpg.add_text("Detected by some anticheats!", color=(240, 47, 28))
                    dpg.add_checkbox(label='Enable writing to game memory and other sensitive features', tag="blatantcheck", callback=enableblatant)
                    with dpg.tooltip("blatantcheck"):
                        dpg.add_text("By default, Nexus External only lets you\nenable cheats that only read game memory,\nwhich is undetectable for a game like gmod.\n\nBy checking this box, you will be able to use\nother cheats that write to the game's memory,\ngood anticheats can detect this.")
                
                with dpg.tab(label='Config'):
                    dpg.add_checkbox(label='Notification when someone is spectating you', tag="c_spectate", default_value=True)
                    with dpg.tooltip("c_spectate"):
                        dpg.add_text("Show a message if someone is spectating you.")
                    dpg.add_checkbox(label='HUD', tag="c_hud", default_value=True)
                    with dpg.group(horizontal=True):
                        dpg.add_text("ESP Method")
                        dpg.add_radio_button(tag="c_esp_method", items=['EntityPos', 'BonesPos (experimental)'], default_value="Normal", callback=bone_mode)
                    with dpg.group(horizontal=True):
                        dpg.add_text("ESP Color")
                        dpg.add_radio_button(tag="c_entcolor", items=['Unicolor', 'Visibility', 'Team', 'Health'], default_value="Visibility")
                        dpg.add_color_edit(default_value=(0, 255, 0), tag='c_unicolor', display_type=dpg.mvColorEdit_uint8, no_inputs=True, no_alpha=True)
                    with dpg.group(horizontal=True):
                        dpg.add_text("Max ESP Distance")
                        dpg.add_slider_int(min_value=0, max_value=1000, tag="c_maxdistance", default_value=0)

                with dpg.tab(label='About'):
                    dpg.add_text("[Nexus External ESP]")
                    dpg.add_text("Version: 2.2.0")
                    if "offline" in {app.Offsets.lastupdate}:
                        dpg.add_text(f"Custom offsets mode.")
                    else:
                        dpg.add_text(f"Updated on: {app.Offsets.lastupdate}")
                    dpg.add_text("")
                    dpg.add_text("© Calvineries / Calvin Honecker.")
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
