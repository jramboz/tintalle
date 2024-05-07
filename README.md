# Tintallë
This is a Python-based alternative to [Gilthoniel](https://github.com/Nuntis-Spayz/gilthoniel) for managing OpenCore-based light sabers.

This is still very much a work in progress at the moment. It's getting close to what I want for the base features. Maybe there will be an actual release soon?

<a href="https://www.flaticon.com/free-icons/lightsaber" title="lightsaber icons">Lightsaber icons created by Nhor Phai - Flaticon</a>

## Current Features
- Scan ports for sabers
- Connect to saber
- Erase all files on saber
- Upload files to saber
- Check for latest firmware release
- Update firmware on saber (requires [tycmd](https://github.com/Koromix/tytools/releases) to be installed)
- Manage saber colors
- Set sounds to corresponding effects

## Status
This is not guaranteed to be bug-free. In fact, it's practically guaranteed to have bugs! I'm just an amateur coder who's doing his best to make a thing. I'm sure there's sloppy code in here, and probably a lot of things that can be done better. But I'm learning as I go, and maybe down the road someone more knowlegable can clean things up.

## Requirements
- Pyside6
- py2saber
- requests
- wget
- asgiref
- AsyncioPySide6
- pydub

Use `pip install -r requirements.txt` to automatically install requirements.

## Why Tintallë?
Because the original software that inspired it is Gilthoniel.

### What?
What?

### I don't get it.
"Gilthoniel" means "star-kindler" in [Sindarin](https://www.glyphweb.com/arda/s/sindarin.html). "Tintallë" is the equivalent in [Quenya](https://www.glyphweb.com/arda/q/quenya.html).

### Okay, but there's already Gilthoniel. Why have another app?
First, I have all the appreciation for Nuntis and his amazing work. However, Gilthoniel is written in Pascal, which doesn't really have as wide a user base as it once did, and also seems to be lagging behind in more modern programming features. I originally wanted to make some tweaks to Gilthoniel, but... I don't know Pascal.

Besides that, I'm hoping that switching to a more widely-used language will make it easier for others to help maintain and update as both LudoSport and the Polaris Anima continue to evolve. 

Gilthoniel is (as far as I know) not going anywhere! Tintallë isn't meant as a replacement for it, but rather as an alternative. Use whichever one you like!

One Name, One Sky.