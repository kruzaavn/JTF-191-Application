--[[

    This Lua file is intended to act as a helper for CAS operations.

    initial setup brony 2/26/2020

]]

env.info([[
=========================================================================================
CAS Operations:    Setting up CAS Plugin.
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

function smoke_group(group)


    -- this function will smoke friendly unit

    if (group:GetCoalition() == coalition.side.BLUE and group:IsGround() and group:IsAlive()) then

		group:SmokeGreen()

    end

end


_DATABASE:ForEachGroup(smoke_group)


