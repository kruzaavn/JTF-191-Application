--[[
    operation export script

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 12/13/2020

    purpose this file is intended to log kills and simulation state from mission to mission in order to support operation
    state tracking.
]]


function dcs_log(message)
    log.write('OPERATION', log.INFO, message)
end

dcs_log('Loading')

package.path  = package.path..";"..lfs.currentdir().."LuaSocket\\?.lua" .. ';' ..lfs.currentdir().. 'Scripts\\?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."LuaSocket\\?.dll"

local export_file = nil
JSON = require('JSON')

function Export2File(message)

	-- this function will write a json message to the export file

	local json = JSON:encode(message)

	if export_file then
		export_file:write(json .. '\n')
	end

end

function contains(list, x)

	-- this function will check if x exists in the array list

	for _, v in pairs(list) do
		if v == x then
			return true
		end
	end
	return false
end


local callbacks = {}


function ExportWorldObjects()

	-- get all units in dcs
	local o = Export.LoGetWorldObjects()
	local message = '['
	local json

	-- iterate through all units and compose json
	for k,v in pairs(o) do

		json = JSON:encode(v)

		message = message .. string.format('%s,', json)

	end

	message = message .. ']'

	return message
end



function callbacks.onSimulationStart()

	dcs_log('did i get here?')
	-- compute filename

	local filename = lfs.writedir() .. '/Logs/' .. DCS.getMissionName() .. '.log'

	-- create log file

	dcs_log(string.format('Create output file: %s', filename))

	export_file = io.open(filename, 'w')

end

function callbacks.onSimulationStop()

	dcs_log('closing out file')
	-- dump state of the sim

	export_file:write(ExportWorldObjects())


	-- close log filec

	export_file:close()
	export_file = nil

end

function callbacks.onGameEvent(eventName, arg1, arg2, arg3, arg4, arg5, arg6, arg7)
    -- this function is required to send data on event to the api-server depending on the event triggered the the
    -- name and arguments are listed below.
        --"friendly_fire", playerID, weaponName, victimPlayerID
        --"mission_end", winner, msg
        --"kill", killerPlayerID, killerUnitType, killerSide, victimPlayerID, victimUnitType, victimSide, weaponName
        --"self_kill", playerID
        --"change_slot", playerID, slotID, prevSide
        --"connect", playerID, name
        --"disconnect", playerID, name, playerSide, reason_code
        --"crash", playerID, unit_missionID
        --"eject", playerID, unit_missionID
        --"takeoff", playerID, unit_missionID, airdromeName
        --"landing", playerID, unit_missionID, airdromeName
        --"pilot_death", playerID, unit_missionID

  	local event = {}
	event.event = eventName
	event.time = DCS.getRealTime()

	if contains({'kill'}, eventName) then

		event.group = DCS.getUnitProperty(arg4, DCS.UNIT_GROUPNAME)
		event.victim = arg5
		event.unit = Export.LoGetObjectById(arg4)

	end

	Export2File(event)
	dcs_log(string.format('Event: %4s', eventName))

end

-- register callbacks to the DCS environment
DCS.setUserCallbacks(callbacks)


dcs_log('Loaded')