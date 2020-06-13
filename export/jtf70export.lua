
local lfs = require('lfs')

local export_file = io.open(lfs.writedir() .. [[Logs\jtf70export.log]], "w")
local c
local socket
local JSON
local host = 'localhost'
local port = 7224

package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua" .. ';' ..jtf70lfs.currentdir().. '/Scripts/?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"
socket = require("socket")
JSON = require('JSON')

-- helper functions

function Export2Socket(message)

	if c then
		socket.try(c:send(message))
	end

end

function Export2File(message)

	if export_file then
		export_file:write(message .. '\n')
	end

end


function ExportWorldObjects(t)
	local o = LoGetWorldObjects()
	local message
	local json

	for k,v in pairs(o) do

		json = JSON:encode(v)

		message = string.format('{"%d":{"sim_time": %d, "states": %s}}\n',k, t, json)

        Export2File(message)
		Export2Socket(message)

	end


end


function connect_socket()

	if not c then
		c = socket.try(socket.connect(host, port)) -- connect to the listener socket
		c:setoption("tcp-nodelay",true) -- set immediate transmission mode
	end
end


function disconnect_socket()

    if c then
		c:close()
		c = nil
	end

end


function close_export_file()
    if export_file then
		export_file:close()
		export_file = nil
	end

end


-- DCS EXPORT HOOKS

function LuaExportStart()
    -- connect socket
    Export2File('Export Started')
	connect_socket()

end


function LuaExportActivityNextEvent(t)

    local tNext = t + 1.0

	if t % 30 == 0 then
		connect_socket()
	end

	-- export functions
	ExportWorldObjects(t)

	return tNext
end


function LuaExportStop()
-- disconnect socket
    close_export_file()
    disconnect_socket()
end