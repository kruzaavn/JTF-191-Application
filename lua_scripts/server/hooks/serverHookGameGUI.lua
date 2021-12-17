--[[
    server hook file

    maintainers Beeej aleks.kruza@gmail.com

    Initial config Beeej 6/15/2020


    This file is meant to automate JTF 191 script management. This file will load the enumerated files below in the
    mission scripting environment
]]


function dcs_log(message)
    log.write('Server Management', log.INFO, message)
end

dcs_log('Loading')


function callbacks.onMissionLoadEnd()

    net.dostring_in('mission', 'local jutils = require("jtfutilities")')
    dcs_log('loaded jtfutilities')

    for file in lfs.dir()

end

