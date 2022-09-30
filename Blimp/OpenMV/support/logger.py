
LEVEL_DEBUG_ONLY = -1
LEVEL_SILENT = 0
LEVEL_ERROR = 1
LEVEL_WARNING = 2
LEVEL_HEARTBEAT = 3
LEVEL_INFO = 4 
LEVEL_VERBOSE = 5
LEVEL_SILLY = 6



class Logger():
    def __init__(self):
        self.level = LEVEL_VERBOSE

    def setLevel_silent(self):
        self.level = LEVEL_SILENT

    def setLevel_error(self):
        self.level = LEVEL_ERROR

    
    def setLevel_warning(self):
        self.level = LEVEL_WARNING


    def setLevel_heartbeat(self):
        self.level = LEVEL_HEARTBEAT
    
    def setLevel_info(self):
        self.level = LEVEL_INFO

        
    def setLevel_verbose(self):
        self.level = LEVEL_VERBOSE


    def setLevel_debugOnly(self):
        self.level = LEVEL_DEBUG_ONLY

    def setLevel_silly(self):
        self.level = LEVEL_SILLY

    
    #def silent(self): //don't need it.

    def debugOnly(self,str):
        if(self.level == LEVEL_DEBUG_ONLY):
            print(str)

    def error(self,str):
        if(self.level >= LEVEL_ERROR and self.level > 0):
            print(str)

    def warning(self,str):
        if(self.level >= LEVEL_WARNING  and self.level > 0):
            print(str)

    def heartbeat(self,str):
        if(self.level >= LEVEL_HEARTBEAT  and self.level > 0):
            print(str)

    def info(self,str):
        if(self.level >= LEVEL_INFO  and self.level > 0):
            print(str)

    def verbose(self,str):
        if(self.level >= LEVEL_VERBOSE  and self.level > 0):
            print(str)

    def silly(self,str):
        if(self.level >= LEVEL_SILLY and self.level > 0):
            print(str)


log = Logger()