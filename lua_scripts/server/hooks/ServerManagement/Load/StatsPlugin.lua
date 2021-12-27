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

function StatsEventHandler:get_crew(unit)
	local mission_id = unit:getID()
	local players = net.get_player_list()

	jtfutils.log(net.lua2json(mission_id))

	local crew = {}

	for key, player in pairs(players) do


		local slot_id = net.get_player_info(player, 'slot')
		local name = net.get_player_info(player, 'name')

		jtfutils.log(net.lua2json(slot_id))

		local start_string, end_string =  string.find(slot_id, '_')

		if start_string then
			slot_id = string.sub(slot_id, 1, start_string -1 )
		end

		if mission_id == slot_id then

			table.insert(crew, name)
		end

	end

	return crew
end

function StatsEventHandler:common(_event)

	local event = {}

	event.event = StatsEventHandler.event_names[_event.id]
	event.mission = _server.mission
	event.server = _server.name


	event.unit = _event.initiator:getDesc()
	event.crew = StatsEventHandler:get_crew(_event.initiator)

	local lat, lon, alt = coord.LOtoLL(_event.initiator:getPoint())

	event.latitude = lat
	event.longitude = lon
	event.altitude = alt

	return event

end


function StatsEventHandler:onEvent(_event)

	-- log event for debugging
	jtfutils.log(string.format("Raw DCS Event: %s", net.lua2json(_event)))

	if jtfutils.list_contains({20, 21}, _event.id) then

		event = StatsEventHandler:common(_event)
		jtfutils.log(net.lua2json(event))


	elseif jtfutils.list_contains(jtfutils.get_keys(StatsEventHandler.event_names), _event.id) then

		-- create an event object and populate with data common to all events tracked
		event = StatsEventHandler:common(_event)

		---- flight_log data
		if event.event == 'takeoff' and event.crew then
			--[[ a flight is defined by a single departure event "takeoff" and one of three termination events
			"landing","pilot death" and "ejection".  On every takeoff a unique flight id will be generated and stored
			in the mission runtime. If a pilot takes off, lands and takes off this is considered completing one flight
			and beginning another and a new id will be generated. If a flight is terminated by server error or shutdown
			or player leaving the flight is considered incomplete and wont be tracked for hours purposes]]

			local flight_id = jtfutils.uuid()
			StatsEventHandler.flight_log[_event.initiator:getID()] = flight_id
			event.flight_id = flight_id

		elseif event.crew then
			-- for all other events the flight_id is retreived and appended to the event
			event.flight_id = StatsEventHandler.flight_log[_event.initiator:getID()]

		end

		if jtfutils.list_contains({'takeoff', 'landing', 'trap'}, event.event) and _event.place then
			-- these events append the landing object details if exists
			event.place = _event.place:getDesc()

		end

		if jtfutils.list_contains({'trap'}, event.event) then
			-- lso grading comments
		    event.comment = _event.comment

		end

		-- combat_log data
		if jtfutils.list_contains({'kill', 'hit'}, event.event)  then

			event.target = _event.target:getDesc()

			lat, lon, alt = coord.LOtoLL(_event.target:getPoint())

			event.target_latitude = lat
			event.target_longitude = lon
			event.target_alt = alt

		end

		if jtfutils.list_contains({'kill'}, event.event) then
			-- for some reason this event doesn't reference the weapon object, the best we can do is get the name
			event.munition = _event.weapon_name

		end

		if jtfutils.list_contains( {'hit'}, event.event) then
			-- hits however provides the full object definition
			event.munition = _event.weapon:getDesc()

		end

		if event.crew then
			jtfutils.log(net.lua2json(event))
			jtfutils.connect_socket(host, port)
			jtfutils.Export2Socket(host, port, event)
			jtfutils.disconnect_socket(host, port)
		end


	-- connection cleanup
	elseif jtfutils.list_contains({12}, _event.id) then
		
		jtfutils.disconnect_socket(host, port)

	end
	
end

world.addEventHandler(StatsEventHandler)

jtfutils.log([[
==========================
Stats export plugin loaded
==========================]])