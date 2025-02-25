# Gmod-Nexus-External-ESP  

### A new version is coming!
The current version will not receive any new features.  
  
I am currently working for a few days on a V2, a complete rewrite under another library.  
This new version fixes almost all the flaws of the cheat (non-exhaustive list: automatic offsets by pattern scanning, no more flickering, ESP based on bones, ...)  
The cheat will remain free and open source.  


## About
Nexus is an open-source Python external wallhack, triggerbot, aimassist and bhop compiled with PyInstaller **for GMOD x64**.  
It's external : nothing is injected, no lua code is used/edited.  
  
The visuals are not in the game: it's another application which is on top of gmod.  
So it's impossible to detect, impossible to screengrab.  

|Features|Methods|Undetectable
|-|-|-|
ESP|Reading game memory only|✅
Dynamic Crosshair|Reading game memory only|✅
Triggerbot|Read and Write to game memory|-
AimAssist|Read and Write to game memory|-
NoRecoil|Read and Write to game memory|-
Bhop|Read and Write to game memory|-
---

## Gameplays
<details>
<summary>Visuals - ESP</summary>
https://www.youtube.com/watch?v=-FNxdR3HOYo
</details>  
  
## Download
https://github.com/Calvineries/Gmod-Nexus-External-ESP/releases/
  
## Common issues
I don't see the wallhack  
- Use video setting: **Borderless window**.

The cheat don't detect gmod  
- Use the beta gmod version: **Chromium x64**.

Black overlay (non transparent)
- Change the "OpenGL GDI Compatibility" in Nvidia Control Panel to "Prefer compatibility".

or
- Make the application (if compiled), or python (if not compiled) use your integrated graphics card instead of your graphics card (or the opposite).

I can't use the uncompiled version:
- There is information on the BetterGo repo.

## Contributions to the code are welcome!
