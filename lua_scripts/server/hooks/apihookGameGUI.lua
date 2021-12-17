--[[
    api hook file

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 6/15/2020
    Update to communicate direct to gci-relay Brony 8/9/2020

    purpose this file is intended to send event based updates to the api-server, for continuous export data stream see
    gciexport.lua
]]


function dcs_log(message)
    log.write('API HOOK', log.INFO, message)
end

dcs_log('Loading')

package.path  = package.path..";"..lfs.currentdir().."LuaSocket\\?.lua" .. ';' ..lfs.currentdir().. 'Scripts\\?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."LuaSocket\\?.dll"

dofile(lfs.writedir() .. [[Config\serverSettings.lua]])

local c = nil
local socket = require('socket')


function set_host_name(api_server_hostname)

	local host = nil

	if DCS.isMultiplayer() then
		host = api_server_hostname or 'relay.jtf191.com'
		dcs_log('In multi player session')

	else
		host = 'localhost'
		dcs_log('In single player session')

	end

	return host
end

local port = 7225  -- change to app port

function connect_socket()

	local host = set_host_name('localhost')

	if not c then
		dcs_log('connecting to ' .. host .. ' ' .. port)
		c = socket.try(socket.connect(host, port)) -- connect to the listener socket
		c:setoption("tcp-nodelay", true) -- set immediate transmission mode
		c:setoption("keepalive", true) -- set immediate transmission mode
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

	local json = net.lua2json(message)

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
callbacks.keepalive_interval = 5
callbacks.keepalive_sent = false

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
        --"crash", playerID, unitID
        --"eject", playerID, unitID
        --"takeoff", playerID, unitID, airdromeName
        --"landing", playerID, unitID, airdromeName
        --"pilot_death", playerID, unitID

  	local event = {}
	event.event = eventName

	dcs_log(string.format('Event: %4s', eventName))

	if not contains({'mission_end'}, eventName) then

		-- only mission end doesn't attach a player callsign

		event.callsign = net.get_player_info(arg1, 'name')
		event.mission_name = DCS.getMissionName()
		event.server = cfg['name']


	end

	if contains({'takeoff', 'landing', 'pilot_death', 'eject'}, eventName) then

		event.airframe = DCS.getUnitProperty(arg2, DCS.UNIT_TYPE)
		event.platform = Export.LoGetObjectById(tonumber(DCS.getUnitProperty(arg2, DCS.UNIT_RUNTIME_ID)))

	end

	if contains({'takeoff', 'landing'}, eventName) then

		event.airfield = arg3

	end

	if contains({'kill'}, eventName) then

		event.victim = arg5
		event.killerID = arg1
		event.victimID = arg4
		event.airframe = arg2
		event.weapon_name = arg7

	end

	Export2Socket(event)
end


function callbacks.onPlayerStart(id)
    -- this function is required to log player connection to the api-server

end


function callbacks.onPlayerStop(id)
    -- this function is required to log played disconnections to the api-server

end

function callbacks.onSimulationFrame()

	local check_time = math.floor(DCS.getRealTime()) % callbacks.keepalive_interval

	if (check_time == 0 and not callbacks.keepalive_sent) then

		local event = {}
		event.event = 'keepalive'
		event.time = DCS.getRealTime()
		Export2Socket(event)
		callbacks.keepalive_sent = true

	elseif (check_time ~= 0 and callbacks.keepalive_sent ) then

		callbacks.keepalive_sent = false

	end

end
-- register callbacks to the DCS environment
DCS.setUserCallbacks(callbacks)


dcs_log('API loaded')