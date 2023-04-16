#include <stdint.h>
#include "LP5024_driver.h"

// I2C address
#define LP5024_I2C_ADDRESS 0x30

// Register addresses
#define LP5024_CONTROL 0x00
#define LP5024_LED_OUTPUT_0 0x01

extern I2C_HandleTypeDef hi2c1;

// Initialization function for the LP5024 driver
void LP5024_Init(void) {
    uint8_t buffer[2];

    // Set the control register to enable the LEDs
    buffer[0] = LP5024_CONTROL;
    buffer[1] = 0x03;
    HAL_I2C_Master_Transmit(&hi2c1, LP5024_I2C_ADDRESS << 1, buffer, 2, 1000);

    // Set the LED output registers to zero to turn off all LEDs
    buffer[0] = LP5024_LED_OUTPUT_0;
    buffer[1] = 0x00;
    HAL_I2C_Master_Transmit(&hi2c1, LP5024_I2C_ADDRESS << 1, buffer, 2, 1000);
}

// Function to set the color of the LEDs connected to the LP5024
void LP5024_SetColor(uint8_t red, uint8_t green, uint8_t blue) {
    uint8_t buffer[25];

    // Fill the buffer with the RGB color values
    buffer[0] = LP5024_LED_OUTPUT_0;
    for (int i = 0; i < 8; i++) {
        buffer[i * 3 + 1] = blue;
        buffer[i * 3 + 2] = green;
        buffer[i * 3 + 3] = red;
    }

    // Transmit the buffer to the LP5024
    HAL_I2C_Master_Transmit(&hi2c1, LP5024_I2C_ADDRESS << 1, buffer, 25, 1000);
}