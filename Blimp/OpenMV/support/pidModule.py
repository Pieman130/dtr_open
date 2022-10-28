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


    def set_pid_gains(self,**kwargs):
        if 'p' in kwargs:
            self.pid._kp = kwargs['p']        
        if 'i' in kwargs:
            self.pid._ki = kwargs['i']
        if 'd' in kwargs:
            self.pid._kd = kwargs['d']


    def get_pid_gains(self):
        return {'p':self.pid.up_pid.up_p, 
               'i':self.pid.up_pid.up_i, 
               'd':self.pid.up_pid.up_d}


    def get_pid(self, error, scaler=1):
        if(scaler == None):
            logger.log.warning('Scaler is none in get_pid')
            return 0
        error = round(error/self.error_scaling,self.error_rounding)

        output = self.pid.get_pid(error,scaler)
        if output > 1:
            output = 1
            self.reset_i() #prevent integrator windup
        elif output < -1:
            output = -1
            self.reset_i() #prevent integrator windup

        if output < self.pid_minimum:
            output = self.pid_minimum
        return output


    def reset_i(self):
        self.pid.reset_I()


    



