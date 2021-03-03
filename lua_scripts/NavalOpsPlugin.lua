--[[

    This Lua file is intended to act as a naval operations plugin to setup naval flight operations for blue forces
    according to the MOOSE AirBoss framework without additional user interface.

    initial setup brony 2/1/2020

]]

env.info([[
=========================================================================================
NavalOperations:      Setting up Naval Operations Plugin.
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

local morse = {
    ['CVN_71'] = 'TDR',
    ['CVN_72'] = 'AHL',
    ['CVN_73'] = 'GWC',
    ['CVN_74'] = 'JCS',
    ['LHA_Tarawa'] = 'TWA'
}

local StartDelay = "00:05" -- HH:MM from mission start time to begin recovery operations
local RecoveryWindowLength = "03:00" -- HH:MM for recovery window
local RecoveryWindowBreak = "00:30" -- HH:MM for recovery window break to reposition carrier
local MissionLength = "04:00" -- HH:MM mission length to plan for
local msg = nil

function setup_airboss(unit)

    -- this function will setup MOOSE airboss for each carrier unit in the game

    local boss = nil
    local TACAN = nil
    local ICLS = nil
    local DeckWind = nil
    local TurnIntoWind = true
    local uTurn = true
    local MissionStart = timer.getTime0()
    local MissionEnd = MissionStart + HHMM2sec(MissionLength)


    if (unit:IsShip() and unit:GetCoalition() == coalition.side.BLUE and contains({'CVN_71', 'CVN_72', 'CVN_73','CVN_74', 'LHA_Tarawa'}, unit:GetTypeName())) then

        -- create airboss instance
        boss = AIRBOSS:New(unit:GetCallsign(), morse[unit:GetTypeName()])
        TACAN = nil

        -- determine tacan and icls from hull number and ship type
        if contains({'CVN_71', 'CVN_72', 'CVN_73', 'CVN_74'}, unit:GetTypeName()) then
            TACAN = tonumber(string.sub(unit:GetTypeName(), -2))
            ICLS = 7
            DeckWind = 27
        else
            TACAN = 41
            ICLS = 4
            DeckWind = 20
        end

        -- setup frequencies
        boss:SetTACAN(TACAN, 'X', morse[unit:GetTypeName()])
        boss:SetICLS(ICLS, morse[unit:GetTypeName()])

        -- offset airboss comms from human frequencies
        boss:SetMarshalRadio(127.2, 'AM')
        boss:SetLSORadio(127.6, 'AM')


        -- setup recovery windows

        local PlannedTime = 0 + HHMM2sec(StartDelay) --accumulates the time that has been planned for
        local RecoveryWindowStart = nil
        local RecoveryWindowEnd = nil

        repeat

            RecoveryWindowStart = sec2HHMM( MissionStart + PlannedTime )
            RecoveryWindowEnd = sec2HHMM( MissionStart + PlannedTime + HHMM2sec(RecoveryWindowLength) )

            boss:AddRecoveryWindow(RecoveryWindowStart, RecoveryWindowEnd, 1, 0, TurnIntoWind, DeckWind, uTurn)

            msg = MESSAGE:New(string.format("Recovery Window from %s to %s for %s", RecoveryWindowStart, RecoveryWindowEnd, morse[unit:GetTypeName()] ), 10)
            msg:ToAll()
            PlannedTime = PlannedTime + HHMM2sec(RecoveryWindowLength) + HHMM2sec(RecoveryWindowBreak)

        until (PlannedTime > MissionEnd - MissionStart)

        boss:SetPatrolAdInfinitum(true)
        boss:Start()


        -- send config message
        msg = MESSAGE:New(string.format([[
            Carrier AIRBOSS Active for %s
            TACAN %dX %s
            ]],
            morse[unit:GetTypeName()],
            TACAN, morse[unit:GetTypeName()]
            ) , 20
        )

        msg:ToAll()
    end

end


_DATABASE:ForEachUnit(setup_airboss)

