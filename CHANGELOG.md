# Tintallë Changelog

## v0.6.1
### New Features
- For advanced users: Added an Anima Terminal (under the Connection menu) to send raw commands to the connected Anima.
- Reading the configuration will time out after 10 seconds if no response is received. No more having to force close!
### Bug Fixes
- Fix for Animas using firmware with debugging enabled.

## v0.6.0
### New Features
- Major under-the-hood rewrite to make threading more efficient. Not that this should be very visible, but trust me, it's important :)
### Bug Fixes
- Fix for multi-file uploads and reset function hanging after the first step is finished.

## v0.5.5
### Bug Fixes
- Fix error for missing "deprecated" module for Windows users (thanks, Tom!)

## v0.5.4
### Bug Fixes
- Fix file upload speed due to typo in baud rate settings in py2saber

## v0.5.3
### Bug Fixes
- Fix blank screen on Windows. Thanks to Andrea "AnFive" for the tip that pointed me to a fix!
- Now Tintallë searches for attached devices by hardware Vendor and Product IDs, rather than just pinging every port until it finds something that gives the right response. This should speed things up!

## v0.5.2
### Bug Fixes
- Fix Reset function. It wasn't finding the default sound font files. Now it is!
- When uploading default sound font, also move BEEP.RAW to last.

## v0.5.1
### New Features
- Added Reset command under Troubleshooting menu
- Include `tycmd` binaries in package -- no need to install separately for FW updates!
- Various minor display improvements (probably things no one but me would even notice)
### Bug Fixes
- Finally fixed uploads to NXTs! No more false starts/distorted beep (I hope).
- Auto-downloaded FW goes to system temp directory now. Should avoid an error message on at least some systems.
- Various minor bugfixes.

## v0.4.0
### New Features
- Automatically assign files to sound effects based on the default naming scheme. This happens automatically when uploading new files. (In the future, I plan to have an option to enable or disable this.) There is also a button to invoke the process on demand.
- Added a refresh button next to the ports list (thanks, @davidfolch for the suggestion!). You could already refresh the ports from the "Connection" menu, but it was easy to miss.

### Bug Fixes
- Now you cannot refresh the ports list when a saber is connected. This could lead to unpredictable behavior.

## v0.3.0
### New Features
- Save and load colors to file
- Save all color banks
- Export Anima's config.ini to file

### Bug Fixes
- Error windows were sometimes not being displayed
- Use explicit `SAVE` command after setting colors and sound effects. Hopefully this will improve stability.

## v0.2.0
### New Features
- Automatically add BEEP.RAW for Anima NXTs (if it is not already specified or present on saber)
- Ability to save output log to file

### Bug Fixes
- Fix erase progress bar stopping at 99%
- Fix progress bar appearing to jump backwards sometimes when uploading multiple files

## v0.1.1
### Bug Fixes
- Fix for not setting clash/swing colors (thanks, Rev.Dood!)

## v0.1.0
First release!
