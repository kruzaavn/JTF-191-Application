--[[
    muntions export file

    maintainers Brony aleks.kruza@gmail.com

    Initial config Brony 7/31/2021

    Include this file for munitions tracking during cruise missions.
]]

function dcs_log(message)

    env.info(message)

end

dcs_log("loading munitions export plugin")

package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"


local c = nil
local socket = require('socket')
local JSON = loadfile("Scripts\\JSON.lua")()
local host = 'relay.jtf191.com'  -- change to application dns name or ip
local port = 7225  -- change to app port


function connect_socket()

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


connect_socket()

event_names = {
	[3] = 'takeoff',
	[4] = 'landing'
}


EventHandler = {}
function EventHandler:onEvent(_event)

	if contains({3,4}, _event.id) then

		event = {
			['type'] = 'stores'
		}
		event.name = event_names[_event.id]

		unit = _event.initiator

		event.callsign = unit.getPlayerName()
		event.stores = unit.getAmmo()


		Export2Socket(event)

	end

	if contains({12}, _event.id) then
		
		disconnect_socket()

	end
	
end

world.addEventHandler(EventHandler)

dcs_log('Munitions export plugin loaded')