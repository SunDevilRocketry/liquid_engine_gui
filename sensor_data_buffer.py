####################################################################################
#                                                                                  #
# sensor_data_buffer.py -- FIFO low-pass filter buffer for gauge readouts          #
#                                                                                  #
# Author: Nitish Chennoju, Colton Acosta                                           #
# Sun Devil Rocketry Avionics                                                      #
#                                                                                  #
####################################################################################


class Sensor_Data_Buffer:
    """FIFO buffer that applies a low-pass filter to incoming sensor data.

    Parameters
    ----------
    max_buffer_size : int   — maximum number of samples to keep
    tau             : float — time constant of the low-pass filter
    """

    def __init__( self, max_buffer_size=10, tau=1 ):
        self.data_buffer     = []
        self.filter_buffer   = []
        self.buffer_size     = 0
        self.max_buffer_size = max_buffer_size
        self.tau             = tau
        self.sensors         = ["pt0","pt1","pt2","pt3","pt4","pt5","pt6","pt7","lc","tc"]

    def add_data( self, sensor_data ):
        if self.buffer_size < self.max_buffer_size:
            self.data_buffer.append( sensor_data )
            self.buffer_size += 1
            if self.buffer_size == 1:
                self.filter_buffer.append( sensor_data )
            else:
                self.filter_buffer.append( self.filter_data() )
        else:
            self.data_buffer.pop( 0 )
            self.data_buffer.append( sensor_data )
            self.filter_buffer.append( self.filter_data() )

    def filter_data( self ):
        T     = self.data_buffer[-1]["t"] - self.data_buffer[-2]["t"]
        alpha = 2*self.tau + T
        beta  = T - 2*self.tau
        filtered_readouts = {}
        for sensor in self.sensors:
            filtered_readouts[sensor] = (
                (T/alpha) * (self.data_buffer[-1][sensor] + self.data_buffer[-2][sensor])
                - (beta/alpha) * self.filter_buffer[-1][sensor]
            )
        return filtered_readouts

    def get_data( self ):
        return self.filter_buffer[-1]
## Sensor_Data_Buffer ##
