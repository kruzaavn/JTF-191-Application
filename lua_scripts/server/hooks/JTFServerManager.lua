--[[
    server hook file

    maintainers Beeej aleks.kruza@gmail.com

    Initial config Beeej 6/15/2020


    This file is meant to automate JTF 191 script management. This file will load the enumerated files below in the
    mission scripting environment
]]


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

    command = string.format("dofile([[%s]])", filepath)

    dcs_log(string.format("loading %s", filepath))

    response = net.dostring_in('server', command)


    if response then

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


callbacks = {}

function callbacks.onMissionLoadEnd()

    if DCS.isMultiplayer() then
        preload_directory_path = lfs.writedir() .. "\\Scripts\\Hooks\\ServerManagement\\Preload\\"
        load_directory_path = lfs.writedir() .. "\\Scripts\\Hooks\\ServerManagement\\Load\\"



        load_directory(preload_directory_path)
        load_directory(load_directory_path)

    end
end

DCS.setUserCallbacks(callbacks)


dcs_log('Loaded')