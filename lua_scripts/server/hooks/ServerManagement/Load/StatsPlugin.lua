--[[
    muntions export file

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 7/31/2021

    Include this file for munitions tracking during cruise missions.
]]



jtfutils.log([[\n
===========================
loading stats export plugin
==========================
]])



local port = 7225  -- change to app port


StatsEventHandler = {}
StatsEventHandler.event_names = {
	[world.event.S_EVENT_TAKEOFF] = 'takeoff',
	[world.event.S_EVENT_LAND] = 'landing',
	[world.event.S_EVENT_PILOT_DEAD] = 'pilot_death',
	[world.event.S_EVENT_EJECTION] = 'ejection',
	[world.event.S_EVENT_KILL] = 'kill',
	[world.event.S_EVENT_LANDING_QUALITY_MARK] = 'trap',
}

StatsEventHandler.flight_log = {}
StatsEventHandler.departure_log = {}

function StatsEventHandler:get_crew(unit)
	local mission_id = unit:getID()
	local players = net.get_player_list()

	local crew = {
		pilot=nil,
		flight_crew={}
	}

	for key, player in pairs(players) do


		local slot_id = net.get_player_info(player, 'slot')
		local name = net.get_player_info(player, 'name')

		local start_string, end_string =  string.find(slot_id, '_')

		if start_string then
			slot_id = string.sub(slot_id, 1, start_string -1 )

			if slot_id == mission_id then
				table.insert(crew.flight_crew, name)
			end

		elseif mission_id == slot_id then

			crew.pilot = name
		end

	end

	if crew.pilot then

		return crew

	else
		return {}
	end
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

	if jtfutils.list_contains({world.event.S_EVENT_BIRTH} , _event.id) then

		-- this is to make sure that any birthed unit departure is set to nil
		StatsEventHandler.departure_log[_event.initiator:getID()] = nil


	elseif jtfutils.list_contains(jtfutils.get_keys(StatsEventHandler.event_names), _event.id) then

		-- create an event object and populate with data common to all events tracked
		event = StatsEventHandler:common(_event)

		---- flight_log data
		if event.event == 'takeoff' and
				not jtfutils.list_empty(event.crew) and
				not StatsEventHandler.departure_log[_event.initiator:getID()] then

			--[[ a flight is defined by a single departure event "takeoff" and one of three termination events
			"landing","pilot death" and "ejection".  On every takeoff a unique flight id will be generated and stored
			in the mission runtime and a departure will be flagged. If a pilot takes off, lands and takes off this is
			considered completing one flight abd beginning another and a new id will be generated. If a flight is
			terminated by server error or shutdown or player leaving the flight is considered incomplete and wont be
			tracked for hours purposes]]


			local flight_id = jtfutils.uuid()
			StatsEventHandler.flight_log[_event.initiator:getID()] = flight_id
			StatsEventHandler.departure_log[_event.initiator:getID()] = true
			event.flight_id = flight_id

		elseif not jtfutils.list_empty(event.crew) then
			-- for all other events the flight_id is retrieved and appended to the event
			event.flight_id = StatsEventHandler.flight_log[_event.initiator:getID()]

		end

		if jtfutils.list_contains({'landing', 'pilot_death', 'eject'}, event.event) then
			-- when any of the following events occurs reset departure to nil
			StatsEventHandler.departure_log[_event.initiator:getID()] = nil
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
		if jtfutils.list_contains({'kill'}, event.event)  then

			event.target = _event.target:getDesc()

			lat, lon, alt = coord.LOtoLL(_event.target:getPoint())

			event.target_latitude = lat
			event.target_longitude = lon
			event.target_alt = alt
			event.munition = _event.weapon_name

		end

		if not jtfutils.list_empty(event.crew) then
			jtfutils.log(net.lua2json(event))
			jtfutils.connect_socket(host, port)
			jtfutils.Export2Socket(host, port, event)
			jtfutils.disconnect_socket(host, port)
		end


	-- connection cleanup
	elseif jtfutils.list_contains({world.event.S_EVENT_MISSION_END}, _event.id) then
		
		jtfutils.disconnect_socket(host, port)

	end
	
end

world.addEventHandler(StatsEventHandler)

jtfutils.log([[\n
==========================
Stats export plugin loaded
==========================]])