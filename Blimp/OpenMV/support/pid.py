import time, pid


class Controller():
    def __init__(self,up_p=1,up_i=0.001,up_d=0.1,up_imax=0.5,
                yaw_p=1,yaw_i=0.001,yaw_d=0.1,yaw_imax=0.5,
                thr_p=1,thr_i=0.001,thr_d=0.1,thr_imax=0.5):

        self.up_p = up_p
        self.up_i = up_i
        self.up_d = up_d
        self.up_imax = up_imax
        self.up_pid = pid.PID(p=self.up_p,i=self.up_i,d=self.up_d,imax=self.up_imax)

        self.yaw_p = yaw_p
        self.yaw_i = yaw_i
        self.yaw_d = yaw_d
        self.yaw_imax = yaw_imax
        self.yaw_pid = pid.PID(p=self.yaw_p,i=self.yaw_i,d=self.yaw_d,imax=self.yaw_imax)

        self.thr_p = thr_p
        self.thr_i = thr_i
        self.thr_d = thr_d
        self.thr_imax = thr_imax
        self.thr_pid = pid.PID(p=self.thr_p,i=self.thr_i,d=self.thr_d,imax=self.thr_imax)
        #TODO Need output clipping for each PID

    def get_pid(self, cntl_type, error, scaler):
        if cntl_type == 'yaw':
            return self.yaw_pid.get_pid(error,scaler)
        elif cntl_type == 'up':
            return self.thr_pid.get_pid(error,scaler)
        elif cntl_type == 'thr':
            return self.up_pid.get_pid(error,scaler)
        else:
            return None

