--[[
    server hook file

    maintainers Beeej aleks.kruza@gmail.com

    Initial config Beeej 12/20/2021

    This file defines a Server Manager use to automate loading JTF 191 scripts into the mission scripting environment.

    A prereq for the server manager is that the MissionScripting file is de-sanitized.

    In order to use the server manager the following files and directories need to be installed in the hooks directory
    of the DCS server install

    ~/Saved Games/DCS.openbeta/Scripts/Hooks
        |
        |-JTFServerManager.lua
        |-JTFServerConfig.lua
        |-ServerManagement
            |
            |-Preload
            |   |
            |   |- Moose.lua
            |   |- jtfutilities.lua
            |
            |-Load
                |
                |- NavalOpsPlugin.lua
                |- StatsPlugin.lua


   When a dcs server loads a multiplayer environment it will then command the mission scripting environment to run all
   scripts in the preload directory first. Files that are dependencies for other scripts, such as Moose and jtfutils,
   should be saved here so that they are available scripts saved in load. Once all preload scripts have been run the
   files in load will then be run in the mission scripting environment.

]]

dofile(lfs.writedir() .. [[Config\serverSettings.lua]])
dofile(lfs.writedir() .. [[Scripts\Hooks\JTFServerConfig.lua]])


function dcs_log(message)

    -- setup convenient logger to the dcs.log file

    log.write('JTF 191 Server Manager', log.INFO, message)
end

dcs_log('Loading')

function contains(list, x)

    -- this function checks to see if x is a member of the list

	for _, v in pairs(list) do
		if v == x then
			return true
		end
	end
	return false
end

function load_file(filepath)

    -- this function will take a file_path and attempt to run it in dofile() in the dcs mission environment.

    command = string.format([[

    a_do_script([=[
            dofile([==[%s]==])
        ]=]
    )
    ]], filepath)

    dcs_log(string.format("loading %s", filepath))

    response = net.dostring_in('mission', command)


    if response ~= "" then

        dcs_log(string.format("%s | %s", filepath, response))

    end

end


function load_directory(directory_path)

    -- this function will scan a directory and call load_file for every file found in it.

    for file in lfs.dir(directory_path) do

        if not contains({".", ".."}) and string.sub(file, -4) == '.lua' then

            local file_path = directory_path .. file

            load_file(file_path)

        end

    end

end


function set_env_values()

    command = string.format([[

        a_do_script([=[

            _server = {}
            _server.mission = "%s"
            _server.name = "%s"
    	    host = "%s"

            for n in pairs(_G) do jtfutils.log(n) end

        ]=])

        ]],  DCS.getMissionName(), cfg.name, jtfServer.host)

      net.dostring_in("mission", command)

end


callbacks = {}

function callbacks.onMissionLoadEnd()

    if DCS.isMultiplayer() then
        preload_directory_path = lfs.writedir() .. "\\Scripts\\Hooks\\ServerManagement\\Preload\\"
        load_directory_path = lfs.writedir() .. "\\Scripts\\Hooks\\ServerManagement\\Load\\"

        load_directory(preload_directory_path)
        load_directory(load_directory_path)

        set_env_values()

    end

end

DCS.setUserCallbacks(callbacks)


dcs_log('Loaded')
