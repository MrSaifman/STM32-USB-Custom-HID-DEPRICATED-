import usb.core
import usb.util
import usb.backend.libusb1
import time

# Define your custom HID USB device's Vendor ID and Product ID
VENDOR_ID = 0x0483
PRODUCT_ID = 0x575a

def find_custom_hid_device(vendor_id, product_id):
    # Set the backend to libusb1
    backend = usb.backend.libusb1.get_backend()

    # Find the HID device with the specified Vendor ID and Product ID
    device = usb.core.find(idVendor=vendor_id, idProduct=product_id, backend=backend)

    if device is not None:
        print(f"Custom HID USB device found: {device}")
    else:
        print("Custom HID USB device not found.")

    return device

def read_button_press(device):
    try:
        # Detach kernel driver if necessary
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)
    except NotImplementedError:
        print("Warning: is_kernel_driver_active is not implemented for the current backend.")

    # Set the active configuration
    device.set_configuration()

    # Get the interrupt IN endpoint
    cfg = device.get_active_configuration()
    intf = cfg[(0, 0)]

    endpoint = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
    )

    if endpoint is None:
        print("Interrupt IN endpoint not found.")
        return

    # Read data from the device
    while True:
        try:
            data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            button_pressed = data[0]

            if button_pressed == 49:
                print("Button pressed!")

            time.sleep(0.1)

        except usb.core.USBError as e:
            if e.args[0] != 110:  # Ignore timeout errors (110)
                raise

def main():
    device = find_custom_hid_device(VENDOR_ID, PRODUCT_ID)
    if device is not None:
        read_button_press(device)

if __name__ == "__main__":
    main()
