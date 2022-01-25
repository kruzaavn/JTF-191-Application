# JTF-191 Server Manager

## !Read the instructions below carefully!

## Purpose

The JTF-191 Server Manager automates loading JTF Standard Scripts and User Scripts into the mission scripting environment

Current JTF supported scripts.

1. [StatsPlugin](./ServerManagement/Load/StatsPlugin.lua) - This script will control the export of the following stats to the JTF-191 Website
for stats tracking and livery generation.
   * Flight Logs 
     * Unique Flights by aircraft, and by Role (Pilot / Flight Crew) 
     * Departure location and Name
     * Flight Termination Location and Status (Landing, Death, Eject)
     * Landing Location and Name
     * Carrier LSO Comments
     
   * Combat Logs
     * Own Location and Time at Kill
     * Victim location and Time at kill
     * Munition used
     * Victim name and type
     
2. [NavalOpsPlugin](./ServerManagement/Load/NavalOpsPlugin.lua) - This script will standardize
blue carrier operations setting the following items by default
   * Vessel TACAN set to <Hull Number>x and TRICODE, e.g. CVN-73 is set to 73X GWC
   * Vessels are set to tack into the wind and make 
     * 27 Kts relative wind for CVN
     * 20 Kts relative wind for LHA
   * Carriers are defaulted to 3hr deck operations with a 30 min reset

## Installation

1. Verify that `MissionScripting.lua` file is de-sanitized by commenting our the following block.
```lua

do
    --[[ 
    sanitizeModule('os')
    sanitizeModule('io')
    sanitizeModule('lfs')
    require = nil
    loadlib = nil
    ]]
end

```
**Note** This file is restored to its default state everytime DCS is updated Server managers will have to de-sanitize 
this file after every update. [OVGME](https://wiki.hoggitworld.com/view/OVGME) is a decent resource to manage this 
requirement.  

2. Install the Server Manager by copying the following files and directories in the Hooks directory of the DCS server 
install.

    ```~/Saved Games/DCS.openbeta/Scripts/Hooks
        |
        |-gciExportGameGUI.lua
        |-JTFServerManager.lua
        |-JTFServerConfig.lua
        |-ServerManagement
            |
            |-Preload
            |   |
            |   |- jtfutilities.lua
            |
            |-Load
                |
                |- NavalOpsPlugin.lua
                |- StatsPlugin.lua
   ```

3. Install MOOSE into the `Preload` directory.

## How does the Server Manager Work

When a dcs server starts a multiplayer mission the server manager will run all scripts in the `Preload` directory in 
the mission scripting environment. Files that are dependencies for other scripts, such as Moose and jtfutils, should be 
saved here so that they are available. Once all preload scripts are run all scripts in the `Load` directory are run 
including JTF Standard Scripts and any scripts you wish to add.





