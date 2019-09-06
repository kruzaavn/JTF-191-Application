
local JSON = require('JSON')

local export_file
local c
local socket

-- helper functions

function LuaObject2Json(object)

	local o = object

	local message = '{'

	for k,v in pairs(o) do

		json = JSON:encode(v)
		json = string.format('"%d": %s,', k, json)
		message = message .. json

	end
	message = string.sub(message,1, -2) ..'}'

	return message
end

function Export2File(message)

	if export_file then
		export_file:write(message)
	end

end

function Export2Socket(message)

	if c then
		socket.try(c:send(message))
	end

end

function ExportWorldObjects(t)
	local o = LoGetWorldObjects()
	o = LuaObject2Json(o)

	local message = string.format('{"sim_time": %d, "states": %s}', t, o)

	Export2File(message)
	Export2Socket(message)
end

-- export required functions

function LuaExportStart()
-- Works once just before mission start.

-- 1) File options, if you dont want to export a file to the hard drive comment the flowing line out

	-- export_file = io.open("C:/Users/Aleks/Saved Games/DCS/Logs/Export.log", "w")

-- 2) Socket

	package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua"
	package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"
	socket = require("socket")
	host = host or "localhost"
	port = port or 8081
	c = socket.try(socket.connect(host, port)) -- connect to the listener socket
	c:setoption("tcp-nodelay",true) -- set immediate transmission mode
end


function LuaExportActivityNextEvent(t)
	local tNext = t

	-- export functions
	ExportWorldObjects(t)

	-- increment time
	tNext = tNext + 1.0

	return tNext
end


function LuaExportStop()
-- Works once just after mission stop.
-- Close files and/or connections here.
-- 1) File
	if export_file then
		export_file:close()
		export_file = nil
	end
-- 2) Socket
	if c then
		c:close()
		c = nil
	end
end