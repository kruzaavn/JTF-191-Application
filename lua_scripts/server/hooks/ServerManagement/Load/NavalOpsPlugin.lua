--[[

    This Lua file is intended to act as a naval operations plugin to setup naval flight operations for blue forces
    according to the MOOSE AirBoss framework without additional user interface.

    initial setup beeej 2/1/2020

]]

jtfutils.log([[
=========================================================================================
NavalOperations:      Setting up Naval Operations Plugin.
=========================================================================================]]
)

-- vars

local morse = {
    ['CVN_71'] = 'TDR',
    ['CVN_72'] = 'AHL',
    ['CVN_73'] = 'GWC',
    ['CVN_74'] = 'JCS',
    ['CVN_75'] = 'HST',
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
    local MissionEnd = MissionStart + jtfutils.HHMM2sec(MissionLength)


    if (unit:IsShip() and unit:GetCoalition() == coalition.side.BLUE and jtfutils.list_contains({'CVN_71', 'CVN_72', 'CVN_73','CVN_74', 'CVN_75', 'LHA_Tarawa'}, unit:GetTypeName())) then

        -- create airboss instance
        boss = AIRBOSS:New(unit:GetCallsign(), morse[unit:GetTypeName()])
        TACAN = nil

        -- determine tacan and icls from hull number and ship type
        if jtfutils.list_contains({'CVN_71', 'CVN_72', 'CVN_73', 'CVN_74', 'CVN_75'}, unit:GetTypeName()) then
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

        local PlannedTime = 0 + jtfutils.HHMM2sec(StartDelay) --accumulates the time that has been planned for
        local RecoveryWindowStart = nil
        local RecoveryWindowEnd = nil

        repeat

            RecoveryWindowStart = jtfutils.sec2HHMM( MissionStart + PlannedTime )
            RecoveryWindowEnd = jtfutils.sec2HHMM( MissionStart + PlannedTime + jtfutils.HHMM2sec(RecoveryWindowLength) )

            boss:AddRecoveryWindow(RecoveryWindowStart, RecoveryWindowEnd, 1, 0, TurnIntoWind, DeckWind, uTurn)

            msg = MESSAGE:New(string.format("Recovery Window from %s to %s for %s", RecoveryWindowStart, RecoveryWindowEnd, morse[unit:GetTypeName()] ), 10)
            msg:ToAll()
            PlannedTime = PlannedTime + jtfutils.HHMM2sec(RecoveryWindowLength) + jtfutils.HHMM2sec(RecoveryWindowBreak)

        until (PlannedTime > MissionEnd - MissionStart)

        boss:SetPatrolAdInfinitum(true)
        boss:Start()


        -- send config message

        setup_message = string.format([[
            Carrier AIRBOSS Active for %s
            TACAN %dX %s
            ]],
            morse[unit:GetTypeName()],
            TACAN, morse[unit:GetTypeName()])

        jtfutils.log(setup_message)
        msg = MESSAGE:New(setup_message, 20)

        msg:ToAll()
    end

end


_DATABASE:ForEachUnit(setup_airboss)

jtfutils.log([[
=========================================================================================
NavalOperations:      Naval Operations Plugin Loaded
=========================================================================================]])