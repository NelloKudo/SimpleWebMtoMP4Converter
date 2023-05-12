#!/usr/bin/env bash

function Echo(){
    echo -e '\033[1;34m'"Script:\033[0m $*";
}

function Quit(){
    echo -e '\033[1;31m'"Error:\033[0m $*"; exit 1;
}

function Setup(){

    # Looking for a previous install
    if [ -d "$HOME/.local/lib/SimpleWebMtoMP4ConverterPortable" ]; then
        Quit "SimpleWebMtoMP4Converter is already installed;
        If you want to uninstall, run the script using --uninstall..
        If you want to reinstall, run the script using --reinstall.."
    fi
    
    # Looking for user folders
    mkdir -p "$HOME/.local/bin"
    mkdir -p "$HOME/.local/lib"
    mkdir -p "$HOME/.local/share/applications"
    mkdir -p "$HOME/.local/share/icons"
    
    # Checking .local/bin..
    pathcheck=$(echo "$PATH" | grep -q "/home/$USER/.local/bin" && echo "y")

    # If ~/.local/bin is not in PATH:
    if [ "$pathcheck" != "y" ] ; then
        
        if grep -q "bash" "$SHELL" ; then
            touch -a "/home/$USER/.bashrc"
            echo "export PATH=/home/$USER/.local/bin:$PATH" >> "/home/$USER/.bashrc"
        fi

        if grep -q "zsh" "$SHELL" ; then
            touch -a "/home/$USER/.zshrc"
            echo "export PATH=/home/$USER/.local/bin:$PATH" >> "/home/$USER/.zshrc"
        fi

        if grep -q "fish" "$SHELL" ; then
            mkdir -p "/home/$USER/.config/fish" && touch -a "/home/$USER/.config/fish/config.fish"
            fish_add_path "/home/$USER/.local/bin"
        fi
    fi
} 

function Install(){

    # Downloading and extracting binaries..
    if [ -e "/tmp/SimpleWebMtoMP4ConverterPortable-amd64-linux.tar.xz" ]; then
        rm "/tmp/SimpleWebMtoMP4ConverterPortable-amd64-linux.tar.xz"
    fi

    Echo "Downloading binaries..."
    wget -O "/tmp/SimpleWebMtoMP4ConverterPortable-amd64-linux.tar.xz" "https://github.com/NelloKudo/SimpleWebMtoMP4Converter/releases/download/v.1.2.0/SimpleWebMtoMP4ConverterPortable-amd64-linux.tar.xz" || Quit "Download failed, please install wget or check your internet.."
    
    Echo "Extracting binaries.."
    tar -xf "/tmp/SimpleWebMtoMP4ConverterPortable-amd64-linux.tar.xz" -C "/tmp" || Quit "Please install tar and run the script again.."
    rm "/tmp/SimpleWebMtoMP4ConverterPortable-amd64-linux.tar.xz"
    
    Echo "Installing files.."

    # Executable..
    cp -r "/tmp/SimpleWebMtoMP4ConverterPortable" "$HOME/.local/lib"
    chmod +x "$HOME/.local/lib/SimpleWebMtoMP4ConverterPortable/SimpleWebMtoMP4ConverterPortable"
    ln -s "$HOME/.local/lib/SimpleWebMtoMP4ConverterPortable/SimpleWebMtoMP4ConverterPortable" "$HOME/.local/bin/SimpleWebMtoMP4ConverterPortable"
    
    # Icons..
    cp "/tmp/SimpleWebMtoMP4ConverterPortable/misc/logopng.png" "$HOME/.local/share/icons/SimpleWebMtoMP4ConverterPortable.png"
    rm -rf "/tmp/SimpleWebMtoMP4ConverterPortable"

    # Desktop..
    echo "[Desktop Entry]
    Name=SimpleWebMtoMP4Converter
    Comment=Convert your WebM videos with ease.
    Type=Application
    Exec=/home/$USER/.local/lib/SimpleWebMtoMP4ConverterPortable/SimpleWebMtoMP4ConverterPortable %U
    Icon=/home/$USER/.local/share/icons/SimpleWebMtoMP4ConverterPortable.png
    Terminal=false
    Categories=Video;" | tee "$HOME/.local/share/applications/SimpleWebMtoMP4Converter.desktop"
    chmod +x "$HOME/.local/share/applications/SimpleWebMtoMP4Converter.desktop"

    Echo "Installation completed! You can now launch SimpleWebMtoMP4Converter!"
}

function Uninstall(){

    # Cleaning old install
    rm -rf "$HOME/.local/lib/SimpleWebMtoMP4ConverterPortable"
    rm "$HOME/.local/share/applications/SimpleWebMtoMP4Converter.desktop"
    rm "$HOME/.local/share/icons/SimpleWebMtoMP4ConverterPortable.png"
    rm "$HOME/.local/bin/SimpleWebMtoMP4ConverterPortable"
    Echo "Script successfully uninstalled.."
}

function Reinstall(){
    Uninstall
    Setup
    Install
}

case "$1" in

    '')
    Setup
    Install
    ;;

    '--reinstall')
    Reinstall
    ;;

    '--uninstall')
    Uninstall
    ;;

esac


