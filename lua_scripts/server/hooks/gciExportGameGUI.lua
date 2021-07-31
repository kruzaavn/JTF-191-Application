--[[

	GCI export file

	maintainer Brony aleks.kruza@gmail.com

	Initial config Brony 6/15/2020

    update to hook API 7/26/2021

]]


function dcs_log(message)
    log.write('GCI HOOK', log.INFO, message)
end

dcs_log('Loading')

package.path  = package.path..";"..lfs.currentdir().."LuaSocket\\?.lua" .. ';' ..lfs.currentdir().. 'Scripts\\?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."LuaSocket\\?.dll"

local c = nil
local socket = require('socket')
JSON = require('JSON')
local host = 'relay.jtf191.com'  -- change to application dns name or ip
local port = 7224  -- change to app port

dofile(lfs.writedir() .. [[Config\serverSettings.lua]])

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
	dcs_log('disconnected from gci-relay')
end

function Export2Socket(message)

	local json = JSON:encode(message)

	if c then
		socket.try(c:send(json .. '\n'))
	end

end

function register_server()

	server = {}
	server.name = cfg["name"]
	server.password = cfg["password"]
	server.description = cfg["description"]

	mission = DCS.getCurrentMission()
	server.theatre = mission["mission"]["theatre"]
	server.date = mission["mission"]["date"]
	server.start_time = mission["mission"]["start_time"]
	server.mission = DCS.getMissionName()

	Export2Socket(server)

end

function ExportWorldObjects()

	local o = Export.LoGetWorldObjects()
	local message = '['
	local json

	for k,v in pairs(o) do

		json = JSON:encode(v)

		message = message .. string.format('{"id": %f, "state": %s},', k, json)

	end

	Export2Socket(string.sub(message, 1, -2) .. ']')

end

local callbacks = {}
callbacks.send_time = -1

function callbacks.onSimulationStart()

    connect_socket()
	register_server()

end

function callbacks.onSimulationStop()

    disconnect_socket()

end


function callbacks.onSimulationFrame()

	local check_time = math.floor(DCS.getModelTime())

	if (check_time ~= callbacks.send_time) then

		ExportWorldObjects()
		callbacks.send_time = check_time
	end

end

DCS.setUserCallbacks(callbacks)

dcs_log('GCI Loaded')