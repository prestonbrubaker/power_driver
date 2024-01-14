import time
from ADCDevice import *

adc = ADCDevice() # Define an ADCDevice class object
time_ref = time.time()

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n")
        exit(-1)

def loop():
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3  # calculate the voltage value
        time_curr = time.time() - time_ref
        print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))
        with open("vdata.txt", "a") as file:
            file.write(str(time_curr) + " " + str(voltage) + "\n")
        time.sleep(0.001)

def destroy():
    adc.close()

if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
