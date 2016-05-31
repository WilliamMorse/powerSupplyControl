import time
import serial

class PowerSupply():

    def __init__(self, portAddress):
        
        self.portAddress = portAddress # the string that tells the self.serial library to open the correct port
        self.portOpen = False
        

    def openPort(self):
    
        # open the self.serial port with the settings for the bk-supplies
        self.ser = serial.Serial(port= self.portAddress,
                                 baudrate= 9600,
                                 parity= serial.PARITY_NONE,
                                 stopbits= serial.STOPBITS_ONE,
                                 bytesize= serial.EIGHTBITS)
        
        self.ser.isOpen()
        self.portOpen = True
        return

    def closePort(self):

        self.ser.close()
        self.portOpen = False
        return
        
    def writeToPort(self, commandToWrite):
        
        return
        

    def voltage(self, setVoltage = None):
        '''
        If no arguments are passed, this function queries the voltage and returns it.
        otherwise it will try to set the vo￿ltage of the powersupply and return a None type. 
        '''
        # the voltage value that the powersupply returns 
        getVoltage = None # will be none if we are setting the voltage
        
        initialPortOpen = self.portOpen # handles the port state so we can leave it open if it is already open.
        if initialPortOpen == False: # if the port is closed,
            self.openPort()        # open it!

        if setVoltage: # if we pass a value other than none, try to set the voltage
            voltage=str('%05.2f' % voltage) # formats the voltage to have 5 chars and 2 digits before and after the decimal
            self.ser.write(bytearray('VOLT ' + voltage, 'utf-8') + b'\r') #format and write to the port
        else: # querry the voltage from the powersupply.
            self.ser.write(bytearray('VOLT?', 'utf-8') + b'\r') # write command to 'get voltage' to the serial port. command is 'VOLT?' followed by a carrage return although a regular \r seems to do just fine. 
            out = bytearray() # empty bytearray to hold the returned bytes from the powersupply. 
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(.5) # seems to work for half a second. increese this time if we get errors
            while self.ser.inWaiting() > 0: # while we have bytes wating in the buffer to read
                out += self.ser.read() # add them one at a time to the output

            s = str(out[1:-2]) # trim the start and stop bits from the output, then cast the bytearray as a string
            getVoltage = float(s[12:-3]) # trim the non-numbers from the string, cast as a float. 

        if initialPortOpen == False and self.portOpen == True: # leave the port how we found it. 
            self.closePort() # if it was open before the call, keep it open. Else close it.
            
        return(getVoltage) # return the voltage (None if setting, float in volts if getting)

        
    def current(self, setCurrent = None):
        '''
        If no arguments are passed this function queries the current and returns it.
        otherwise it will try to set the current of the powersupply and return a None type.
        This is very similar to the voltage() function but has slightly differet formatting. 
        
        The current is set in milliamps with one digit of precision after the decimal
        (minimum precision = 0.1 mA). 
        
        The returned current float is also in milliamps.
        '''

        getCurrent = None # the current the powersupply returns 

        initialPortState = self.portOpen # handles the port state so we can leave it open if it is open 
        if initialPortState == False:
            self.openPort()

        if setCurrent: # if we pass a value other than none, try to set the current
            current=str('%05.1f' % setCurrent) # sets the current to have 5 chars and 3 digits before and 1 digit after the decimal
            self.ser.write(bytearray('CURR ' + current, 'utf-8') + b'\r') #format and write to the port
        else: # get the current from the powersupply if we are not tring to set it
            self.ser.write(bytearray('CURR?', 'utf-8') + b'\r')
            out = bytearray()
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(.5)
            while self.ser.inWaiting() > 0:
                out += self.ser.read()

            s = str(out[1:-2]) # truncate the output to remove stop and start bytes then cast as string
            getCurrent = (float(s[12:-4])) # strip the units and message from the output string and cast as a float

        if initialPortState == False and self.portOpen == True:
            self.closePort()
            
        return(getCurrent) # return the current (type is None if setting the current and float in milliamps if getting the voltage)

        
