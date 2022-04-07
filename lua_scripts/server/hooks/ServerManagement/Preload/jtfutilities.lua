jtfutils = {}
jtfutils.sockets = {}

package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"


socket = require('socket')

function jtfutils.log(message)
    -- This function will log a message into the dcs.log file
    env.info(message)

end


function jtfutils.uuid()

	-- This function will return a UUID each time it is called using the powershell UUID generation method

	local f = io.popen([["powershell New-Guid"]])
	--[[
	the response back from powershell will look like this

	"""

	Guid
	----
	xxxxx-xxxx-xxxx-xxx-xxxxxxxxxx
	"""

	read the first 3 lines and throw them away, save the last line
	]]
	f:read()
	f:read()
	f:read()

	local uuid = f:read()
	f:close()

	return uuid
end


function jtfutils.list_contains(list, x)
    -- This function will check to see if x is a member of list if it is the function will return true else false

	for _, v in pairs(list) do
		if v == x then
			return true
		end
	end
	return false
end

function jtfutils.list_empty(list)

	-- This function will check to see if a table is empty
	for key, value in pairs(list) do
		return false
	end
	return true

end

function jtfutils.concat_host_port(host, port)

    -- this function is a convenience function to concatenate host and port

    return string.format("%s:%d", host, port)
end

function jtfutils.connect_socket(host, port)

    -- this function will create a socket connection to host and port and save the reference for later use if not
    -- already created

    local c = jtfutils.sockets[jtfutils.concat_host_port(host, port)]

	if not c then
		jtfutils.log(string.format('connecting to %s', jtfutils.concat_host_port(host, port)))
		c = socket.try(socket.connect(host, port)) -- connect to the listener socket
		c:setoption("tcp-nodelay", true) -- set immediate transmission mode
		c:setoption("keepalive", true) -- set immediate transmission mode

		jtfutils.sockets[jtfutils.concat_host_port(host, port)] = c
	end
end

function jtfutils.disconnect_socket(host, port)

    -- this function will disconnect socket and remove the socket reference if it exists

    local c = jtfutils.sockets[jtfutils.concat_host_port(host, port)]

	if c then
		c:close()
		c = nil
		jtfutils.sockets[string.format("%s:%d", host, port)] = c
	end

	jtfutils.log(string.format('disconnected from %s', jtfutils.concat_host_port(host, port)))
end


function jtfutils.sec2HHMM(seconds)

    -- this function will take in number in seconds and convert to HH:MM string format and a datum set to start of the day
    local hour = math.floor(seconds / 3600)
    local minutes = math.floor( (seconds % 3600) / 60)

    if hour < 24 then
        return string.format('%02d:%02d', hour, minutes)
    else
        return string.format('%02d:%02d+1', hour % 24, minutes)
    end
end


function jtfutils.HHMM2sec(time)
    -- this function will take in a HH:MM string formatted time and return time in seconds, this format doesn't have a datum
    local hour = tonumber(string.sub(time, 1,2))
    local minutes = tonumber(string.sub(time, 4,5))

    return hour * 3600 + minutes * 60
end


function jtfutils.get_keys(_table)

	-- this function will return a list of keys from a table

	local keys={}
  	for key,_ in pairs(_table) do
    	table.insert(keys, key)
  	end
  	return keys
end

function jtfutils.Export2Socket(host, port, message)

	local json = net.lua2json(message)

    local c = jtfutils.sockets[jtfutils.concat_host_port(host, port)]

	if c then
		socket.try(c:send(json .. '\n'))
	end

end


jtfutils.log('JTF191 Utilities Loaded')