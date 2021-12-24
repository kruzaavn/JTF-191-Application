--[[
    muntions export file

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 7/31/2021

    Include this file for munitions tracking during cruise missions.
]]



jtfutils.log([[
===========================
loading stats export plugin
==========================
]])


local host = 'localhost'  -- change to application dns name or ip
local port = 7225  -- change to app port


StatsEventHandler = {}
StatsEventHandler.event_names = {
	[3] = 'takeoff',
	[4] = 'landing',
	[9] = 'pilot_death',
	[6] = 'ejection',
	[28] = 'kill',
	[2] = 'hit',
	[36] = 'trap'
}

StatsEventHandler.flight_log = {}


function StatsEventHandler:onEvent(_event)


	jtfutils.log(string.format("Event: %s", net.lua2json(_event)))

	if jtfutils.list_contains(jtfutils.get_keys(StatsEventHandler.event_names), _event.id) then

		event = {}
		event.event = StatsEventHandler.event_names[_event.id]
		event.mission = _server.mission
		event.server = _server.name


		event.unit = _event.initiator:getDesc()
		event.callsign =_event.initiator:getPlayerName()

		local lat, lon, alt = coord.LOtoLL(_event.initiator:getPoint())

		event.latitude = lat
		event.longitude = lon
		event.altitude = alt

		if event.event == 'takeoff' and event.callsign then

			local flight_id = jtfutils.uuid()
			StatsEventHandler.flight_log[event.callsign] = flight_id
			event.flight_id = flight_id

		elseif event.callsign then

			event.flight_id = StatsEventHandler.flight_log[event.callsign]

		end

		if jtfutils.list_contains({'takeoff', 'landing', 'trap'}, event.event) and _event.place then

			event.place = _event.place:getDesc()

		end

		if jtfutils.list_contains({'kill'}, event.event) then

		    event.comment = _event.comment

		end

		if jtfutils.list_contains({'kill', 'hit'}, event.event)  then

			event.target = _event.target:getDesc()

			lat, lon, alt = coord.LOtoLL(_event.target:getPoint())

			event.target_latitude = lat
			event.target_longitude = lon
			event.target_alt = alt

		end

		if jtfutils.list_contains({'kill'}, event.event) then

			event.munition = _event.weapon_name

		end

		if jtfutils.list_contains( {'hit'}, event.event) then

			event.munition = _event.weapon:getDesc()

		end

		if event.callsign then
			jtfutils.connect_socket(host, port)
			jtfutils.Export2Socket(host, port, event)
			jtfutils.disconnect_socket(host, port)
		end

	end

	if jtfutils.list_contains({12}, _event.id) then
		
		jtfutils.disconnect_socket(host, port)

	end
	
end

world.addEventHandler(StatsEventHandler)

jtfutils.log([[
==========================
Stats export plugin loaded
==========================]])