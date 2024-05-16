# Tintallë Changelog

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
