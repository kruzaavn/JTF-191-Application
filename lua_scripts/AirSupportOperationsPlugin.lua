--[[

    This Lua file is intended to act as a air operations plugin to setup flight support operations for blue forces
    according to the MOOSE framework without additional user interface.

    principally it sets up TACAN and communications for tankers and early warning platforms.

    initial setup brony 2/26/2020

]]

env.info([[
=========================================================================================
AirSupportOperations:      Setting up Air SupportPlugin.
=========================================================================================]]
)

-- utility functions
function contains(list, x)
	for _, v in pairs(list) do
		if v == x then
			return true
		end
	end
	return false
end

function sec2HHMM(seconds)

    -- this function will take in number in seconds and convert to HH:MM string format and a datum set to start of the day
    local hour = math.floor(seconds / 3600)
    local minutes = math.floor( (seconds % 3600) / 60)

    if hour < 24 then
        return string.format('%02d:%02d', hour, minutes)
    else
        return string.format('%02d:%02d+1', hour % 24, minutes)
    end
end

function HHMM2sec(time)
    -- this function will take in a HH:MM string formatted time and return time in seconds, this format doesn't have a datum
    local hour = tonumber(string.sub(time, 1,2))
    local minutes = tonumber(string.sub(time, 4,5))

    return hour * 3600 + minutes * 60
end

-- vars

-- todo brony in the future i'd like to expand this to be cofigured programattically instead of in data
local frequencies = {
    ['Arco1-1'] = {101,'X', 256.1}, -- TACAN, BAND, COMMS
    ['Arco2-1'] = {102,'X', 256.2},
    ['Texaco1-1'] = {103,'X', 256.3},
    ['Shell1-1'] = {104,'X', 256.4},
    ['Shell2-1'] = {105,'X', 256.5}
}

local awacs_callsigns = {
    "Overloard",
    "Magic",
    "Darkstar",
    "Winzard",
    "Focus"
}

local msg

function setup_tankers(unit)

    -- this function will setup TACAN and Communications for each air force tanker


    if (unit:IsTanker() and unit:GetCoalition() == coalition.side.BLUE ) then


        local unit_frequencies = frequencies[unit:GetCallsign()]

        -- setup tacan
        unit:CommandActivateBeacon(
                BEACON.Type.TACAN,
                BEACON.System.TACAN_TANKER_X,
                UTILS.TACANToFrequency(unit_frequencies[1], unit_frequencies[2]),
                unit:GetID(),
                unit_frequencies[1],
                true,
                string.sub(unit:GetCallsign(), 1,3),
                true
        )

        -- setup comms
        unit:CommandSetFrequency(unit_frequencies[3])

        msg = MESSAGE:New(string.format(
                [[Tanker %s Communications Configured TACAN %d%s on %.2f Mhz]],
                unit:GetCallsign(),
                unit_frequencies[1],
                unit_frequencies[2],
                unit_frequencies[3]
            ) , 20
        )

        msg:ToAll()

    end

end


function setup_early_warning(unit)

    if contains(awacs_callsigns, string.sub(unit:GetCallsign(), 1, -4)) then

        local comms_frequency = 299.9
        unit:CommandSetFrequency(comms_frequency)

        msg = MESSAGE:New(string.format(
                [[AWACS %s AI Communications Configured on %.2f Mhz]],
                unit:GetCallsign(),
                comms_frequency
                )
        )

        msg:ToAll()

    end

end


_DATABASE:ForEachUnit(setup_tankers)
_DATABASE:ForEachUnit(setup_early_warning)

