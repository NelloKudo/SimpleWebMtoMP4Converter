# Simple WebM to MP4 Converter

Convert your WebM videos with ease.

![repobanner](https://user-images.githubusercontent.com/98063377/230535505-3fd27c61-f8d3-4102-9e1c-25dd9cf5248d.png)

# Index

- [Features](#features)
- [Installation](#installation)
- [Compiling from source](#compiling-from-source)
    - [Windows](#windows)
    - [Linux](#linux)
- [License](#license)


# Features

![convertvideo](https://user-images.githubusercontent.com/98063377/230535523-5f1026e2-f818-4c18-bc3f-b81b1868f371.gif)

_Well_, the title speaks for itself: given one (or more) WebM videos, the app simply converts them in MP4 using [ffmpeg](https://github.com/FFmpeg) binaries for both Windows and Linux.

This happens to be extremely useful especially with [animethemes](https://animethemes.moe/), [catbox](https://catbox.moe/) or [animemusicquiz](https://animemusicquiz.com/) files, to create Party Rankings or just share those bangers around.

The available presets for converting are **ffmpeg's default ones:**

- ultrafast
- superfast
- veryfast
- faster
- fast – default preset
- medium 
- slow
- slower
- veryslow 

A **slower compression** means a **better compression** (and, in some cases, quality): just use the one worth your time. You can read more about it at [here](https://trac.ffmpeg.org/wiki/Encode/H.264#FAQ)

You can also set [CRF](https://superuser.com/questions/677576/what-is-crf-used-for-in-ffmpeg) according to your needs: the apps bundles a brief summary of what it is.


# Installation

## Windows

Windows users can just **download the zip file** from [here](https://github.com/NelloKudo/SimpleWebMtoMP4Converter/releases/download/v.1.2.0/SimpleWebMtoMP4ConverterPortable-win.zip) or the compressed [.exe file](https://github.com/NelloKudo/SimpleWebMtoMP4Converter/releases/download/v.1.2.0/SimpleWebMtoMP4Converter.exe) and start converting 8)

## Linux

Linux users can instead use the `install.sh` script in the repo.

# Compiling from source

Compiling should be possible pretty much everywhere, but __MacOS__ isn't supported yet (it's coming soon tho).

## Windows

Install [Python](https://www.python.org/downloads/) and during installation, make sure to add Python to your PATH environment.

Install [Git](https://git-scm.com/download/win) too as it's needed to properly clone the repository.

Open Powershell and install [PyInstaller](https://pyinstaller.org/en/stable/):

```powershell
# Install PyInstaller
pip install pyinstaller

# Update pip and install Pillow
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

Then clone the repository and cd into it:

```powershell
git clone https://github.com/NelloKudo/SimpleWebMtoMP4Converter.git
cd SimpleWebMtoMP4Converter
```

Once in the folder, compile your  __executable__ with:

```powershell
# Using pyinstaller to point to binaries, theme and logo (run it as a whole command):

pyinstaller --add-binary "./bin/ffmpeg-2023-04-03-git-windows/bin/ffmpeg.exe;bin/" --add-data "theme/forest-dark/*;theme/forest-dark" --add-data "theme/forest-dark.tcl;theme" --add-data "misc/*;misc" --name=SimpleWebMtoMP4Converter --onefile --noconsole --icon="./misc/logo.ico" --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder .\SimpleWebMtoMP4Converter.py

# When it's done, finally finish creating the .exe with:

pyinstaller .\SimpleWebMtoMP4Converter.spec
```

If you want to compile the __portable version__ instead:

```powershell
# Using pyinstaller to point to binaries, theme and logo (run it as a whole command):

pyinstaller --add-binary "./bin/ffmpeg-2023-04-03-git-windows/bin/ffmpeg.exe;bin/" --add-data "theme/forest-dark/*;theme/forest-dark" --add-data "theme/forest-dark.tcl;theme" --add-data "misc/*;misc" --name=SimpleWebMtoMP4ConverterPortable --noconsole --icon="./misc/logo.ico" --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder .\SimpleWebMtoMP4Converter.py

# When it's done, finally finish creating the .exe with:

pyinstaller .\SimpleWebMtoMP4ConverterPortable.spec
```

You'll find your builds in the `dist` folder.

## Linux

Install `python`, `python-pip`, `python-tk` and `git` according to your distro; after that:

```bash
# Install PyInstaller
pip install pyinstaller

# Update pip and install Pillow
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```

Then clone the repository and cd into it:

```bash
git clone https://github.com/NelloKudo/SimpleWebMtoMP4Converter.git
cd SimpleWebMtoMP4Converter
```

Once in the folder, compile your __executable__ with:

```bash
# Using pyinstaller to point to binaries, theme and logo (run it as a whole command):

pyinstaller --add-binary "./bin/ffmpeg-2023-03-13-git-amd64-linux/ffmpeg:bin/" --add-data "theme/forest-dark/*:theme/forest-dark" --add-data "theme/forest-dark.tcl:theme" --add-data "misc/*:misc" --name=SimpleWebMtoMP4Converter --onefile --noconsole --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder ./SimpleWebMtoMP4Converter.py

# When it's done, create your binary:

pyinstaller SimpleWebMtoMP4Converter.spec
```

If you want to compile the __portable version__ instead:


```bash
# Using pyinstaller to point to binaries, theme and logo (run it as a whole command):

pyinstaller --add-binary "./bin/ffmpeg-2023-03-13-git-amd64-linux/ffmpeg:bin/" --add-data "theme/forest-dark/*:theme/forest-dark" --add-data "theme/forest-dark.tcl:theme" --add-data "misc/*:misc" --name=SimpleWebMtoMP4ConverterPortable --noconsole --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder ./SimpleWebMtoMP4Converter.py

# When it's done, create your binary:

pyinstaller SimpleWebMtoMP4ConverterPortable.spec
```

You'll find your builds in the `dist` folder.


# License

This program is licensed under [GNU General Public License v3.0](https://github.com/NelloKudo/SimpleWebMtoMP4Converter/blob/main/LICENSE.md), therefore allowed to bundle what needed for it to work.

Huge thanks to:

- [ffmpeg](https://github.com/FFmpeg)
- [forest-ttk-theme](https://github.com/rdbende/Forest-ttk-theme)
