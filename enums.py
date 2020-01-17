import enum

class Regs(enum.Enum):
    
    DRUMFRQ            = 0
    PRESSROLLFRQ       = 1
    SLUDEGSUPPLYFRQ    = 2
    SLUDEGSPREADFRQ    = 3
    DCV                = 4
    DCA                = 5
    DRUMCOLLINGWATER   = 6
    TRANSFORMERSTEMP   = 7
    INPUT              = 10
    OUTPUT             = 11
    WATERRATE          = 12
    LEFTBALANCE        = 13
    RIGHTBALANCE       = 14
    


class Coils(enum.Enum):
    
    READY                   = 48
    FIELDMODE               = 49
    REMOTEMODE              = 50
    MANUAL                  = 51
    AUTO                    = 52
    CAMMOTER                = 53
    DRUMUNIT                = 54
    PRESSROLL               = 55
    TRANSFORMERS            = 56
    DCSUPPLY                = 57
    WASINGPUMP              = 58
    SLUDGESUPPLY            = 59
    SLUDGESPREAD            = 60
    SLIPRINGCOLLINGFAN      = 61
    AUTOMATICSTART          = 62
    AUTOMATICSTOP           = 63
    REMOTESTOP              = 80
    OUTPUTCONVEYOR          = 81
    RESET                   = 94
    WATCHDOG                = 95





class Alarms(enum.Enum):
    PANELEMERGENCYSTOP          = 0
    OPEMERGENCYSTOP             = 1
    LEFTEMERGENCYSTOP           = 2
    RIGHTEMERGENCYSTOP          = 3
    DRUMINVERTERFAULT           = 4
    PRESSROLLINVERTERFAULT      = 5
    SLUDGESPREADINVERTERFALUT   = 6
    SLUDGESUPPLYINVERTERFAULT   = 7
    CAMMOTEREOCRTRIP            = 8
    DRUMEOCRTRIP                = 9
    PRESSROLLEOCRTRIP           = 10
    WASH1EOCRTRIP               = 11
    WASH2EOCRTRIP               = 12
    PANELCOOLINGPANEOCRTRIP     = 13
    SLIPRINGCOOLINGPANFAULT     = 14
    SLUDEGSUPPLYEOCRTRIP        = 15
    SLUDEGSPREADEOCRTRIP        = 16
    TRANSFORMERSEOCRTRIP        = 19
    TRANSFORMERSTEMPOVER        = 20
    SCRCURRENTOVER              = 21
    SCRTEMPOVER                 = 22
    DCCURRENTOVER               = 23
    TRANSFORMERSFRONTDOOROPEN   = 24
    TRANSFORMERSBACKDOOROPEN    = 25
    SCRPANELDOOROPEN            = 26
    DEHYDRATORLEFTDOOROPEN      = 27
    DEHYDRATORRIGHTDOOROPEN     = 28
    BELTLEFTOUT                 = 29
    BELTRIGHTOUT                = 30
    AIRPRESSUREDROP             = 31
    COOLINGPANFAULT             = 32
    DRUMCOOLINGWATERTEMPOVER    = 33
    AIRPRESSURESOLVALVECPTRIP   = 34
    SLIPRINGTEMPOVER            = 35
    TRANSFORMERSACBTRIP         = 36
    ENDLIST                     = 37

    




class Machine(enum.Enum):

    ALARMCOUNTSTART             = 50

    FIRSTCOIL                   = 0
    SECONDCOIL                  = 160
    THRIDCOIL                   = 320

    FIRSTREG                    = 0
    SECONDREG                   = 100
    THIRDREG                    = 200


class OperatingTime(enum.Enum):

    ALARMCOUNT                  = 900
    TOTALMIN                    = 910
    TOTALHOUR                   = 911
    DRUMMIN                     = 912
    DRUMHOUR                    = 913
    FILTERMIN                   = 914
    FILTERHOUR                  = 915
    CLEANERMIN                  = 916
    CLEANERHOUR                 = 917
    WATERTANKMIN                = 918
    WATERTANKHOUR               = 919
    CLOSESENSORMIN              = 920
    CLOSESENSORHOUR             = 921