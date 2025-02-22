import requests
import json

response = requests.get("https://raw.githubusercontent.com/Calvineries/Gmod-Nexus-External-ESP/refs/heads/main/offsets.json")
githuboffsets = json.loads(response.text)

try:
    dwEntityList = int(githuboffsets["dwEntityList"], 16)
    dwLocalPlayer = int(githuboffsets["dwLocalPlayer"], 16)
    dwViewMatrix = int(githuboffsets["dwViewMatrix"], 16)
    server_slots = int(githuboffsets["server_slots"], 16)
    screengrab = int(githuboffsets["screengrab"], 16)
    dwForceAttack = int(githuboffsets["dwForceAttack"], 16)
    dwForceJump = int(githuboffsets["dwForceJump"], 16)
    m_angRotation = int(githuboffsets["m_angRotation"], 16)
    mat_fullbright = int(githuboffsets["mat_fullbright"], 16)
    m_iIDEntIndex = int(githuboffsets["m_iIDEntIndex"], 16)
    m_szCustomName = int(githuboffsets["m_szCustomName"], 16)
    m_iObserverMode = int(githuboffsets["m_iObserverMode"], 16)
    m_hObserverTarget = int(githuboffsets["m_hObserverTarget"], 16)
    gversion = str(githuboffsets["gversion"])
except:
    pass

try:
    with open("offsets.json", "r") as jsonfile:
        data = json.load(jsonfile)
    if data["dwEntityList"] != "":
        dwEntityList = int(data["dwEntityList"], 16)
    if data["dwLocalPlayer"] != "":
        dwLocalPlayer = int(data["dwLocalPlayer"], 16)
    if data["dwViewMatrix"] != "":
        dwViewMatrix = int(data["dwViewMatrix"], 16)
    if data["server_slots"] != "":
        server_slots = int(data["server_slots"], 16)
    if data["screengrab"] != "":
        screengrab = int(data["screengrab"], 16)
    if data["dwForceAttack"] != "":
        dwForceAttack = int(data["dwForceAttack"], 16)
    if data["dwForceJump"] != "":
        dwForceJump = int(data["dwForceJump"], 16)
    if data["m_angRotation"] != "":
        m_angRotation = int(data["m_angRotation"], 16)
    if data["mat_fullbright"] != "":
        mat_fullbright = int(data["mat_fullbright"], 16)
    if data["m_iIDEntIndex"] != "":
        m_iIDEntIndex = int(data["m_iIDEntIndex"], 16)
    if data["m_szCustomName"] != "":
        m_szCustomName = int(data["m_szCustomName"], 16)
    if data["m_iObserverMode"] != "":
        m_szCustomName = int(data["m_iObserverMode"], 16)
    if data["m_hObserverTarget"] != "":
        m_szCustomName = int(data["m_hObserverTarget"], 16)
    if data["dwEntityList"] or data["dwLocalPlayer"] or data["dwViewMatrix"] or data["server_slots"] or data["screengrab"] or data["dwForceAttack"] or data["dwForceJump"] or data["m_angRotation"] or data["mat_fullbright"] or data["m_iIDEntIndex"] or data["m_szCustomName"] or data["m_iObserverMode"] or data["m_hObserverTarget"] != "":
        gversion = "Custom offsets"
except FileNotFoundError:
    pass

#Netvars
m_vecOrigin = 0x308
m_iHealth = 0xC8
m_iTeamNum = 0xD4
m_fFlags = 0x440

#=Dormant
m_nRenderMode = 0xB4
#=Nocliping
m_nRenderFX = 0x84
#=Invisibility
m_clrRender = 0x88
