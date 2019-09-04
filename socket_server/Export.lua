local export_file
local c
local socket

function prepend_header(message)

	local message_header = string.len(message)

	while string.len(message_header) < 10 do
		message_header = message_header .. ' '

	end

	return message_header .. message
end


function convert2json(k,v,t)
	-- convert LoGetWorldObjects into json format

	local template = '{"id": %d, "simtime": %.2f, "name": "%s", "country": %s, "coalition_id": %d, "position": [%f,%f,%f], "heading": %f}\n'
	local output =  string.format(template, k, t, v.Name, v.Country, v.CoalitionID, v.LatLongAlt.Lat, v.LatLongAlt.Long, v.LatLongAlt.Alt, v.Heading)

	output = prepend_header(output)

	return output
end


function LuaExportStart()
-- Works once just before mission start.

-- 1) File

	export_file = io.open("C:/Users/Aleks/Saved Games/DCS/Logs/Export.log", "w")
	export_file:write(prepend_header("begin export \n"))

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

-- 1) get world objects

		local o = LoGetWorldObjects()
		for k,v in pairs(o) do

			json = convert2json(k,v,t)
			message = prepend_header(json)

			if export_file then
				export_file:write(message)
			end
			if c then
				socket.try(c:send(message))
			end
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
		export_file:write(prepend_header("end export\n"))
		export_file:close()
		export_file = nil
	end
-- 2) Socket
	if c then
		c:close()
		c = nil
	end
end
