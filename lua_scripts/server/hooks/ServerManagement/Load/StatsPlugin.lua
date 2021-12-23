--[[
    muntions export file

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 7/31/2021

    Include this file for munitions tracking during cruise missions.
]]

dofile(lfs.writedir() .. [[Config\serverSettings.lua]])

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
	[29] = 'kill'
}



function StatsEventHandler:onEvent(_event)


	jtfutils.log(string.format("Event ID: %d", _event.id))

	if jtfutils.list_contains(jtfutils.get_keys(StatsEventHandler.event_names), _event.id) then

		event = {}
		event.event = StatsEventHandler.event_names[_event.id]
		event.mission = MISSION:GetName()
		event.server = cfg.name


		if _event.initiator then

			event.unit = _event.initiator:getDesc()
			event.callsign =_event.initiator:getPlayerName()

			local lat, lon, alt = coord.LOtoLL(_event.initiator:getPosition())

			event.latitude = lat
			event.longitude = lon
			event.altitude = alt


		end

		if jtfutils.list_contains({'takeoff', 'landing'}, event.event) and _event.place then

			event.place = _event.place:getDesc()

		end

		if jtfutils.list_contains({'kill'}, event.event) and _event.target and _event.weapon then

			event.target = _event.target:getDesc()
			event.munition = _event.weapon:getDesc()

			lat, lon, alt = coord.LOtoLL(_event.target:getPosition())

			event.kill_latitude = lat
			event.kill_longitude = lon
			event.kill_alt = alt

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