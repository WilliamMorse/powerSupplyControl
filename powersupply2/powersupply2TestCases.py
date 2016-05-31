import powersupply2 as powersupply # import the library for testing

# Setup the powersupply serial ports!
try:
    # these two are for the horizontal field adustment 
    xCoil = powersupply.PowerSupply('/dev/tty.usbserial-FTBZ1G1B')
    yCoil = powersupply.PowerSupply('/dev/tty.usbserial-FTBYZZIN')

    # this one stays locked at a value to keep the laser centered on the sensor
    zCoil = powersupply.PowerSupply('/dev/tty.usbserial-FTFBPHDT') # assign the correct port the the z powersupply
    
except:
    print('Error setting up serial device. Please check the serial port adresses in the setup function.')

    
# put the pendulum in it's starting position
try:
    def set_angle(angle):
    
        currentAmplitude = 400
        currentOffset = 400
    
        xCoil.current( currentOffset + (currentAmplitude * np.sin(angle)) )
        yCoil.current( currentOffset + (currentAmplitude * np.cos(angle)) )
    
    

    # open the ports! 
    xCoil.openPort()
    yCoil.openPort()
    zCoil.openPort()
        
    set_angle(0)
    # set the z coil to be at it's nominal value:
    zCoil.current(465)

except:
    print('set_angle failed!')


#close the ports
xCoil.closePort()
yCoil.closePort()
zCoil.closePort()


'''# reset the cois to zero position
set_angle(0)
print('sleeping for 5 seconds')
time.sleep(5)

# make the penduleum go in a circle (wind it up).

angles = np.linspace(0,np.pi*2,2000)

# circle one way

print('starting circle')
for i in angles:
    set_angle(i)

    
    
# wait a bit
print('waiting')
time.sleep(6)

# circle is the other way
print('other circle')
angles = np.linspace(np.pi*2,0,2000)

for i in angles:
    set_angle(i)
    
    
print('done! and HI')'''
