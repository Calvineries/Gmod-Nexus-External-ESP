# Gmod-Nexus-External-ESP V2

## About
Nexus is an open-source Python external ESP **for GMOD x64**. Other minor features are also included like a triggerbot, and a bhop.  

It's an external: nothing is injected, no lua function are used.  
In the [GLua programming language](https://wiki.facepunch.com/gmod/), there is no way to know if a player is using software that is reading the game's memory.
  
The visuals are displayed in another application, as an overlay.  
Screengrab scripts use the lua [render.Capture](https://wiki.facepunch.com/gmod/render.Capture) function, which only capture what is rendered by the game.  

|Features|Methods|Undetectable
|-|-|-|
ESP|Reading game memory only|✅
Dynamic Crosshair|Reading game memory only|✅
Triggerbot|Reading game memory and sends inputs|-
Bhop|Read and Write to game memory|-
---

## Screenshots
<p align="center">
  <img src="pictures/Esp.png" width="500" >
  <img src="pictures/Playerlist_Menu.png" width="350" >
</p>
<p align="center">
  <img src="pictures/Visuals_Menu.png" width="400" >
  <img src="pictures/Skeleton_esp.png" width="250" >
</p>
  
## Download
There is [a version compiled with PyInstaller](https://github.com/Calvineries/Gmod-Nexus-External-ESP/releases) for those who don't know how to use Python.
  
## Common issues
|Issue|Solution|
|-|-|
I don't see the ESP.|Use video setting: **Borderless window**.
The cheat doesn't detect gmod.|Use the beta gmod version: **Chromium x64**.
The offsets are outdated.|You can use my "offset dumper" to get the new offsets: https://github.com/Calvineries/gmod-x64-offsets-dumper.
How to install dependencies for the uncompiled version.|- Install the "dearpygui", "pywin32" and "requests" modules using pip.<br>- Download and install pyMeow : https://github.com/qb-0/pyMeow.
In Singleplayer the ESP doesn't work.<br>Bots are not displayed on the ESP.|Uncheck "Only Real Players".
How to enable the Skeleton ESP.|In the "Config" tab you must put the ESP in "BonesPos" mode.
The overlay is black (non transparent).|- Solution 1: Change the "OpenGL GDI Compatibility" in Nvidia Control Panel to "Prefer compatibility".<br>- Solution 2: Make the application (if compiled), or python (if not compiled) use your integrated graphics card instead of your graphics card (or the opposite).
Some player names appear as "______".|These names contain non-Latin characters.<br>To display them, you must place a font file named "font.ttf" in the "font" folder.
Where is the old version.|https://github.com/Calvineries/Gmod-Nexus-External-ESP/tree/v1-(old-version).

## Contributions to the code are welcome!

[UnknownCheats forum page](https://www.unknowncheats.me/forum/garry-s-mod/690093-nexus-external-esp-v2-pymeow.html).
