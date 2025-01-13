# Searching for Animas

Tintallë will automatically search for any attached saber Animas when it starts. The **Ports** dropdown box will display a list of ports where Tintallë found connected Animas.

!!! question "What is a Port?"
    "Port" or "COM port" refers to an internal address that your computer uses to identify and communicate with connected devices. On Windows, these will usually be in the form of `COM#` (`COM1`, `COM2`, etc..). For macOS, these will usually be `/dev/cu.usbmodem###`; for Linux, `/dev/ttyS#`.

## Refreshing the Ports List

![Screenshot](img/t_connection_refresh.png)

To re-scan for attached Animas, do any of the following to refresh the ports list:

- Click the **Refresh (:material-refresh:)** button.
- Use the menu bar: **Connection :material-arrow-right-thin: Refresh Ports**
- Press ++ctrl+r++ (Windows/Linux) / ++cmd+r++ (macOS)

## Troubleshooting Tips

!!! tip
    If Tintallë fails to recognize an Anima connected to your computer, try any or all of the following:

    - **Look for charging/LED blinking.** When first connected to your computer, the LED should cycle briefly through colors (Red/Green/Blue/White) and then flash every few seconds to indicate its charging status. If you do not see any LED lights, your Anima may not be properly connected to your computer.
    - **Check that the connector is fully engaged.** Make sure that the USB cable is fully seated in the Anima's plug. Some saber hilts have small openings around the charging port, and USB cables with large end pieces may have trouble fitting all the way into the plug.
    - **Restart the Anima.** Toggle the restart switch on the Anima off then back on.
    - **Make sure your USB cable supports data transfer.** Some USB cables only support charging and not data transfer. Make sure you are using a cable that has data transfer capability.
    - **Try a different cable.** USB cables wear out over time, or run into other issues. Sometimes you just have to try a different one.

!!! note "Anima NXT Notes"
    For Anima NXTs, here are a few additional specific notes:

    - **Check the NXT hardware version.** NXTs have a hardware version printed on the circuit board. You can see this from the bottom of the Anima, and it is usually printed near the switch.
        - **V0 does not support connecting to a computer.** Anima NXT V0 is meant for Academy-only use. It does not support connecting to a computer for updates or configuration changes. 
        - **V1 only supports USB A to USB C cables.** The NXT V1 will not charge or connect to computers through a USB C to USB C cable. It must use a USB A to USB C cable. See [this link](https://www.samsung.com/uk/support/mobile-devices/what-are-the-different-types-of-usb-cables/) for more information on USB connector types.
        - **V2 and higher.** NXT V2 and higher support USB C to USB C cables (in addition to USB A to USB C).