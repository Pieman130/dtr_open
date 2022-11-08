import dataClasses
import time, pid
import logger




class Controller():
    def __init__(self,p=1,i=0.001,d=0.1,imax=0.5):

        self.p = p
        self.i = i
        self.d = d
        self.imax = imax        
        self.pid = pid.PID(p=self.p,i=self.i,d=self.d,imax=self.imax)
        #TODO Need output clipping for each PID
        self.error_scaling = 100
        self.error_rounding = 1
        self.pid_minimum = -1
        self.pid._last_derivative = 0


    def set_pid_gains(self,p=None,i=None,d=None):
        if p != None:
            self.pid._kp = p
        if i != None:
            self.pid._ki = i
        if d != None:
            self.pid._kd = d
        

    def get_pid_gains(self):
        return {'p':self.pid._kp, 
               'i':self.pid._ki, 
               'd':self.pid._kd}


    def get_pid(self, error, scaler=1):
        logger.log.verbose("in get pid")
        if(scaler == None):
            logger.log.warning('Scaler is none in get_pid')
            return 0
        error = round(error/self.error_scaling,self.error_rounding)
    
        logger.log.verbose('Error: ' + str(error))
        output = self.pid.get_pid(error,scaler)
        if output > 1:
            output = 1
            #self.reset_i() #prevent integrator windup
        elif output < -1:
            output = -1
            #self.reset_i() #prevent integrator windup

        if output < self.pid_minimum:
            output = self.pid_minimum
        return output


    def reset_i(self):
        self.pid.reset_I()


    



