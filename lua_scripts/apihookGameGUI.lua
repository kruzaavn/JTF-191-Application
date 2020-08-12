--[[
    api hook file

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 6/15/2020
    Update to communicate direct to tcpeter Brony 8/9/2020

    purpose this file is intended to send event based updates to the api-server, for continuous export data stream see
    gciexport.lua
]]


function dcs_log(message)
    log.write('API HOOK', log.INFO, message)
end

dcs_log('Loading')

package.path  = package.path..";"..lfs.currentdir().."LuaSocket\\?.lua" .. ';' ..lfs.currentdir().. 'Scripts\\?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."LuaSocket\\?.dll"

local c = nil
local socket = require('socket')
JSON = require('JSON')
local host = 'localhost'  -- change to tcpeter application dns name or ip
local port = 7225  -- change to tcpeter app port

function connect_socket()

	if not c then
		dcs_log('connecting to ' .. host .. ' ' .. port)
		c = socket.try(socket.connect(host, port)) -- connect to the listener socket
		c:setoption("tcp-nodelay",true) -- set immediate transmission mode
	end
end

function disconnect_socket()

	if c then
		c:close()
		c = nil
	end
	dcs_log('disconnected from api-relay')
end

function Export2Socket(message)

	local json = JSON:encode(message)

	if c then
		socket.try(c:send(json .. '\n'))
	end

end

function contains(list, x)
	for _, v in pairs(list) do
		if v == x then
			return true
		end
	end
	return false
end


local callbacks = {}

function callbacks.onSimulationStart()

    connect_socket()

end

function callbacks.onSimulationStop()

    disconnect_socket()

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

	if not contains({'mission_end'}, eventName) then

		-- only mission end doesn't attach a player callsign

		event.callsign = net.get_player_info(arg1, 'name')

	end

	if contains({'takeoff', 'landing', 'pilot_death', 'eject'}, eventName) then

		event.airframe = DCS.getUnitProperty(arg2, DCS.UNIT_TYPE)

	end

	if contains({'kill'}, eventName) then

		event.victim = arg5
		event.weapon_name = arg7

	end

	Export2Socket(event)
	dcs_log(string.format('Event: %4s', eventName))

end


function callbacks.onPlayerStart(id)
    -- this function is required to log player connection to the api-server

end


function callbacks.onPlayerStop(id)
    -- this function is required to log played disconnections to the api-server

end

-- register callbacks to the DCS environment
DCS.setUserCallbacks(callbacks)


dcs_log('API loaded')