local utils = {}
utils.sockets = {}

package.path = package.path .. ";.\\LuaSocket\\?.lua"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll"


local socket = require('socket')
local JSON = loadfile("Scripts\\JSON.lua")


function utils.log(message)
    -- This function will log a message into the dcs.log file
    env.info(message)

end

function utils.list_contains(list, x)
    -- This function will check to see if x is a member of list if it is the function will return true else false

	for _, v in pairs(list) do
		if v == x then
			return true
		end
	end
	return false
end

function utils.concat_host_port(host, port)

    -- this function is a convenience function to concatenate host and port

    return string.format("%s:%d", host, port)
end

function utils.connect_socket(host, port)

    -- this function will create a socket connection to host and port and save the reference for later use if not
    -- already created

    local c = utils.sockets[utils.concat_host_port(host, port)]

	if not c then
		utils.log(string.format('connecting to %s', utils.concat_host_port(host, port)))
		c = socket.try(socket.connect(host, port)) -- connect to the listener socket
		c:setoption("tcp-nodelay", true) -- set immediate transmission mode
		c:setoption("keepalive", true) -- set immediate transmission mode

		utils.sockets[utils.concat_host_port(host, port)] = c
	end
end

function utils.disconnect_socket(host, port)

    -- this function will disconnect socket and remove the socket reference if it exists

    local c = utils.sockets[utils.concat_host_port(host, port)]

	if c then
		c:close()
		c = nil
		utils.sockets[string.format("%s:%d", host, port)] = c
	end

	utils.log(string.format('disconnected from %s', utils.concat_host_port(host, port)))
end

function Export2Socket(host, port, message)

	local json = JSON:encode(message)

    local c = utils.sockets[utils.concat_host_port(host, port)]

	if c then
		socket.try(c:send(json .. '\n'))
	end

end


utils.log('JTF191 Utilities Loaded')

return utils