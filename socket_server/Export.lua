
local export_file
local c
local socket

-- helper functions
function convert2json(k,v,t)

	-- convert LoGetWorldObjects into json format

	local template = ' "%d": {"simtime": %.2f, "name": "%s", "country": %s, "coalition_id": %d, "position": [%f,%f,%f], "heading": %f} '
	local output =  string.format(template, k, t, v.Name, v.Country, v.CoalitionID, v.LatLongAlt.Lat, v.LatLongAlt.Long, v.LatLongAlt.Alt, v.Heading)

	return output
end

-- export required functions

function LuaExportStart()
-- Works once just before mission start.

-- 1) File options, if you dont want to export a file to the hard drive comment the flowing line out

	export_file = io.open("C:/Users/Aleks/Saved Games/DCS/Logs/Export.log", "w")

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
	local message = '{'

-- 1) get world objects

	local o = LoGetWorldObjects()
	for k,v in pairs(o) do

		json = convert2json(k,v,t)

		message = message .. json .. ','

		if export_file then
			export_file:write(json)
		end

	end

	message = string.sub(message,1, -2) ..'}'

	if c then
		socket.try(c:send(message))
	end

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