--[[

	GCI export file

	maintainer Brony aleks.kruza@gmail.com

	Initial config Brony 6/15/2020

	add the following lines to the head of the export file at ~\saved_games\DCS.openbeta\Scripts
	local lfs = require('lfs')
	dofile(lfs.writedir() .. \[\[Mods\Tech\webgciexport\webgciexport.lua\]\])

]]


local c
local socket
local JSON
local host = 'relay.jtf191.com'  -- change to application dns name or ip
local port = 7224  -- change to gci-relay app port

package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua" .. ';' ..lfs.currentdir().. '/Scripts/?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"
socket = require("socket")
JSON = require('JSON')

dofile(lfs.writedir() .. [[Config\serverSettings.lua]])

-- helper functions

function Export2Socket(message)

	if c then
		socket.try(c:send(message..'\n'))
	end

end

function ExportWorldObjects(t)

	local o = LoGetWorldObjects()
	local message = '['
	local json

	for k,v in pairs(o) do

		json = JSON:encode(v)

		message = message .. string.format('{"id": %f, "state": %s},', k, json)

	end

	Export2Socket(string.sub(message, 1, -2) .. ']')

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


-- DCS EXPORT HOOKS

function LuaExportStart()

	-- connect socket

	connect_socket()

	message = JSON:encode(cfg)
	Export2Socket(message)

end


function LuaExportActivityNextEvent(t)

    local tNext = t + 1.0

	if t % 30 == 0 then
		connect_socket()
	end

	if t % 1 == 0 then
	-- export functions
		ExportWorldObjects(t)
	end

	return tNext

end


function LuaExportStop()

-- disconnect socket
    disconnect_socket()

end
