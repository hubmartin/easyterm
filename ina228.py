#Example for reading I2C device, extracting value from read bytes and displaying it as an GUI text widget.
#SHT40 thermometer should be connected to side interface connector in order to work (part of Airsense module).
print('INA228 script executed')

#Declare init as False just once (so script might be executed several times)
try:
    sht40_init #Declared previously -> try passes
except:
    sht40_init = False #First run -> no init variable -> try fails -> declare it as False

# For debug
#sht40_init=False

#Display LogWin, enable 3V3 VOUT, configure I2C (initialize, set address to 0x44)
#This can be done just once
if sht40_init==False:
    et.cmd('ClearScreenPage') #Just to be sure there are no widgets
    et.cmd('DisplayPlot x=10 y=0 width=310 height=240 graphicsColor=100,93,5 xScale=2 mode=Approximated parseMask="voltage=%f"')
    et.cmd('DisplayLog y=240 h=240')
    # Enable VOUT 3V3
    et.cmd('sys vs=1')
    # Initialize I2C (i=1) with address 0x40
    et.cmd('I2C i=1 a=40')
    sht40_init = True

# Read die temperature register
# Read from I2C addres 0x06
et.cmd('I2C WR=06')
# Read 2 bytes
replies = et.cmd('I2C RD=2')
reply = et.get_reply(replies, "I2C rd=")
bytes = et.reply_to_bytes(reply)
temp = 0.0078125 * (bytes[0] * 256 + bytes[1]) 

# Read voltage
et.cmd('I2C WR=05')
replies = et.cmd('I2C RD=3')
reply = et.get_reply(replies, "I2C rd=")
bytes = et.reply_to_bytes(reply)
# div 16 to ignore low 4 bits
voltage = 0.0001953125 * (bytes[0] * 65536 + bytes[1] * 256 + bytes[2]) / 16  

# Read current
et.cmd('I2C WR=04')
replies = et.cmd('I2C RD=3')
reply = et.get_reply(replies, "I2C rd=")
bytes = et.reply_to_bytes(reply)
# div 16 to ignore low 4 bits
shunt_v = 0.0000003125 * (bytes[0] * 65536 + bytes[1] * 256 + bytes[2]) / 16  
current = shunt_v * 1  # Assuming shunt resistor of 1Ohm

print("Temperature is: %f C" % temp)
print("Voltage is: %f V" % voltage)
print("Current is: %f A" % current)

# Print, so that DisplayPlot can read the values (parseMask parameter)
et.cmd('temperature=%f' % temp)
et.cmd('voltage=%f' % voltage)
et.cmd('current=%f' % current)