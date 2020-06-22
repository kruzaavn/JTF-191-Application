-- jtf70 hook file
-- Initial config Brony 6/15/2020 aleks.kruza@gmail.com

-- purpose this file is intended to send updates to the api-server on specific game events, for
-- configuration of export data stream see jtf70export.lua

package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua" .. ';' ..lfs.currentdir().. '/Scripts/?.lua'
package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"

-- http interface to send http request to api-server
local http = require("socket.http")
local ltn12 = require("ltn12")

local api_server_url = "jtf70.eastus.cloudapp.azure.com"


function sendPostRequest(endpoint, payload)
--  local path = "http://requestb.in/12j0kaq1?param_1=one&param_2=two&param_3=three"
--  local payload = [[ {"key":"My Key","name":"My Name","description":"The description","state":1} ]]
local response_body = { }

local response, code, response_headers, status = http.request
  {
    url = "http://" .. api_server_url .. endpoint,
    method = "POST",
    headers =
    {
      ["Content-Type"] = "application/json",
      ["Content-Length"] = payload:len()
    },
    source = ltn12.source.string(payload),
    sink = ltn12.sink.table(response_body)
  }

end


local callbacks = {}

function callbacks.onGameEvent(eventName, arg1, arg2, arg3, arg4)
    -- this function is required to send data on event to the api-server depending on the event triggered the the
    -- name and arguments are listed below.
        --"friendly_fire", playerID, weaponName, victimPlayerID
        --"mission_end", winner, msg
        --"kill", killerPlayerID, killerUnitType, killerSide, victimPlayerID, victimUnitType, victimSide, weaponName
        --"self_kill", playerID
        --"change_slot", playerID, slotID, prevSide
        --"connect", playerID, name
        --"disconnect", playerID, name, playerSide, reason_code
        --"crash", playerID, unit_missionID
        --"eject", playerID, unit_missionID
        --"takeoff", playerID, unit_missionID, airdromeName
        --"landing", playerID, unit_missionID, airdromeName
        --"pilot_death", playerID, unit_missionID

end


function callbacks.onPlayerStart(id)
    -- this function is required to log player connection to the api-server

end


function callbacks.onPlayerStop(id)
    -- this function is required to log played disconnections to the api-server

end

-- register callbacks to the DCS environment
DCS.setUserCallbacks(callbacks)


