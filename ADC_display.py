import pygame
from ADCDevice import *

def setup():
    global adc
    adc = ADCDevice()
    if adc.detectI2C(0x48):  # Detect the pcf8591.
        adc = PCF8591()
    elif adc.detectI2C(0x4b):  # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found.\n"
              "Please use command 'i2cdetect -y 1' to check the I2C address!\n"
              "Program Exit.\n")
        exit(-1)

def loop():
    pygame.init()
    window = pygame.display.set_mode((800, 800))
    font = pygame.font.SysFont('arial', 36)
    clock = pygame.time.Clock()
    time_ref = time.time()
    volt_ps = 0
    time_reff = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        value = adc.analogRead(0)
        voltage = value / 255.0 * 3.3
        time_curr = time.time() - time_ref
        time_delta = time_curr - time_reff
        time_reff = time_curr
        volt_ps += voltage * time_delta
        avg_voltage = volt_ps / time_curr

        x = (time_curr % 10) / 10 * 600 + 100
        y = 700 - voltage / 3.3 * 600

        window.fill((100, 100, 100))
        pygame.draw.rect(window, (255, 0, 0), (x, y, 5, 5))
        text_surface = font.render(f"Average Voltage: {avg_voltage:.2f}", True, (255, 255, 255))
        window.blit(text_surface, (10, 10))
        pygame.display.flip()
        
        clock.tick(60)  # Control the loop at 60 frames per second

def destroy():
    if adc:
        adc.close()

if __name__ == '__main__':
    print('Program is starting...')
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
    finally:
        pygame.quit()
