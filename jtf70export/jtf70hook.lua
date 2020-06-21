package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua" .. ';' ..lfs.currentdir().. '/Scripts/?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"
local http = require("socket.http")



local callbacks = {}

function callbacks.onGameEvent()





end