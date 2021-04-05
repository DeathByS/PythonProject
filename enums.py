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
    INPUT              = 8
    OUTPUT             = 9  
    INPUTWATERRATE     = 10
    OUTPUTWATERRATE    = 11
    LEFTBALANCE        = 12
    RIGHTBALANCE       = 13
    KW                 = 36
    
    


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
    REMOTESTOP              = 64
    OUTPUTCONVEYOR          = 65
    SLUDGEOUTEMAILSIGN      = 69
    # RESET                   = 94
    # WATCHDOG                = 95





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
    DRUMEXC                     = 37
    SCRAPEREXC                  = 38
    WASHINGEXC                  = 39
    # 근접센서
    PSENSOREXC                  = 40
    # 물탱크센서
    WTSENSOREXC                 = 41
    FILTEREXC                   = 42
    DONTUSE1                    = 44
    DONTUSE2                    = 45
    DONTUSE3                    = 46
    DONTUSE4                    = 47
    # FULLTIMEON                  = 48
    ENDLIST                     = 47


class AbnormalSignAlarm(enum.Enum):

    OUTOFTIME                   = 66
    LEFTBALANCE                 = 67
    RIGHTBALANCE                = 68
    ENDLIST                     = 68
    




class Machine(enum.Enum):

    TERMOFREG                   = 100
    TERMOFCOIL                  = 160 

    ALARMCOUNTSTART             = 50
    EXCALARMSWITCHSTART         = 128

    FIRSTCOIL                   = 0
    SECONDCOIL                  = 160
    THRIDCOIL                   = 320

    FIRSTREG                    = 0
    SECONDREG                   = 100
    THIRDREG                    = 200


class OperatingTime(enum.Enum):

    TOTALMIN                    = 14
    TOTALHOUR                   = 15
    DRUMMIN                     = 16
    DRUMHOUR                    = 17
    SLUDGESCRAPERMIN            = 18
    SLUDGESCRAPERHOUR           = 19
    CLEANERMIN                  = 20
    CLEANERHOUR                 = 21
    CLOSESENSORMIN              = 22
    CLOSESENSORHOUR             = 23
    WATERTANKMIN                = 24
    WATERTANKHOUR               = 25
    FILTERMIN                   = 26
    FILTERHOUR                  = 27


class Monitoring(enum.Enum):

    NUMBEROFBUTTONS         =   9     
    NUMBEROFLABELS          =   36
    
    # 데이터 라인 줄 수, 현장 하나 추가할때마다 하나씩 추가
    NUMBEROFDATA            =   9

class OpTimeTab(enum.Enum):

    NUMBEROFLABELS          =   7


class OptimizerData(enum.Enum):

    AVGINPUTWATERRATE       =   3000
    AVGOUTPUTWATERRATE      =   3002
    AVGSLUDGEINPUT          =   3004
    AVGSLUDGEOUTPUT         =   3006
    AVGDCA                  =   3008
    BASEINPUTWATERRATE      =   3001
    BASEOUTPUTWATERRATE     =   3003
    BASESLUDGEINPUT         =   3005
    BASESLUDGEOUTPUT        =   3007
    BASEDCA                 =   3009
    BASEDCV                 =   3010
    BASEDRUMFRQ             =   3011
    BASEPUSSERFRQ           =   3012

class WriteValue(enum.Enum):

    VOLTAGE                 =   4000
    DRUMFRQ                 =   4001
    INPUTFRQ                =   4002
    SLUDGEOUTWEIGHT         =   4003

    STAGERESET              =   8000
    SLUDGEOUTRESET          =   8001
    SLUDGEOUTEMAILSTOP      =   8002
