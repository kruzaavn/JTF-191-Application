
local export_file
local c
local socket
local JSON

-- helper functions

function Export2Socket(message)

	if c then
		socket.try(c:send(message))
	end

end

function ExportWorldObjects(t)
	local o = LoGetWorldObjects()
	local message
	local json

	for k,v in pairs(o) do

		json = JSON:encode(v)

		message = string.format('{"%d":{"sim_time": %d, "states": %s}}',k, t, json)

		Export2Socket(message)

	end


end

function connect_socket()

	if not c then
		c = socket.try(socket.connect(host, port)) -- connect to the listener socket
		c:setoption("tcp-nodelay",true) -- set immediate transmission mode
	end

end

-- export required functions

function LuaExportStart()

	-- Works once just before mission start.

	-- Socket config
	local host
	local port
	JSON = require('JSON')

	package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua" .. ';' ..lfs.currentdir().. '/Scripts/?.lua'
	package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"
	socket = require("socket")

	host = host or "localhost"
	port = port or 8081

	connect_socket()

end


function LuaExportActivityNextEvent(t)

	local tNext = t

	if t % 30 == 0 then

		connect_socket()

	end

	-- export functions
	ExportWorldObjects(t)

	-- increment time
	tNext = tNext + 1.0

	return tNext
end


function LuaExportStop()
-- Works once just after mission stop.

-- Socket
	if c then
		c:close()
		c = nil
	end
end