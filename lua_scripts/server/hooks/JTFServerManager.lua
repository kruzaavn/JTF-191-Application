--[[
    server hook file

    maintainers Beeej aleks.kruza@gmail.com

    Initial config Beeej 6/15/2020


    This file is meant to automate JTF 191 script management. This file will load the enumerated files below in the
    mission scripting environment
]]


function dcs_log(message)
    log.write('JTF 191 Server Manager', log.INFO, message)
end

dcs_log('Loading')

callbacks = {}

function callbacks.onMissionLoadEnd()


    response = net.dostring_in('server', 'local jutils = require("jtfutilities")')

    dcs_log(response)

    for file in lfs.dir(lfs.writedir() .. '/Scripts') do

        dcs_log(file)

    end

end

DCS.setUserCallbacks(callbacks)


dcs_log('Loaded')