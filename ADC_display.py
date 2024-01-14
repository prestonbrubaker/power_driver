import time
import pygame
from ADCDevice import *

pygame.init()

window = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont('arial', 36)  # Use 'None' for the default font


adc = ADCDevice() # Define an ADCDevice class object
time_ref = time.time()

time_res = 0

time_reff = 0
volt_reff = 0

time_ps = 0
volt_ps = 0

window.fill((100, 100, 100))

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

def loop(time_res, time_ps, volt_ps, time_reff):
    while True:
        value = adc.analogRead(0)    # read the ADC value of channel 0
        voltage = value / 255.0 * 3.3  # calculate the voltage value
        
        time_curr = time.time() - time_ref
        time_delta = time_curr - time_reff
        time_reff = time_curr

        volt_ps += voltage * time_delta
        
        #print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))
        with open("vdata.txt", "a") as file:
            file.write(str(time_curr) + " " + str(voltage) + "\n")
        y = 700 - voltage / 3.3 * 600
        x = (time_curr % 10) / 10 * 600 + 100
        if(x < time_res):
            window.fill((100, 100, 100))
        time_res = x
        pygame.draw.rect(window, (255, 0, 0), (x, y, 5, 5))
        text_surface = font.render(str(volt_ps / time_curr), True, (255, 255, 255))
        
        pygame.display.flip()
        window.blit(window, (10, 10))
        time.sleep(0.001)

def destroy():
    adc.close()

if __name__ == '__main__':   # Program entrance
    print ('Program is starting ... ')
    try:
        setup()
        loop(time_res, time_ps, volt_ps, time_reff)
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
