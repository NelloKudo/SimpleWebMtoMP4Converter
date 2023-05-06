import os
import subprocess
import platform
import sys
import wmi
import signal
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

class ConverterGUI:

    # Definint a tooltip class to properly call them later on
    class ToolTip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tooltip = None
            self.widget.bind("<Enter>", self.show_tooltip)
            self.widget.bind("<Leave>", self.hide_tooltip)

        def show_tooltip(self, event):
            x, y, _, _ = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 25

            self.tooltip = tk.Toplevel(self.widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = tk.Label(self.tooltip, text=self.text, background="#141414", relief="solid", borderwidth=2)
            label.pack()

        def hide_tooltip(self, event):
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip = None


    def __init__(self, master):

        self.master = master
        self.gpu_info = wmi.WMI()
        master.title("Simple WebM to MP4 Converter")
        
        # This will be used to call the stop_conversion and gpu function
        self.process = None
        self.processstatus = True
        self.gpu = "None"
        self.errorlogs = 0

        # Saving OS information to make checks easier
        self.os_info = platform.system()

        # Defining bundled ffmpeg's path based on OS
        self.ffmpeg_path = ""

        if self.os_info == "Windows":
            # Get the path to the bundled ffmpeg binaries
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller creates a temporary folder to extract the bundled files
                self.ffmpeg_path = os.path.join(sys._MEIPASS, "bin/ffmpeg.exe")
            else:
                # Checks if it's running the portable version
                if os.path.isdir("./tcl"):
                    self.ffmpeg_path = "./bin/ffmpeg.exe"
                else:
                    self.ffmpeg_path = "./bin/ffmpeg-2023-04-03-git-windows/bin/ffmpeg.exe"
        else:
            # Get the path to the bundled ffmpeg binaries
            if getattr(sys, 'frozen', False):
                # Running as a bundled executable
                self.binary_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
                self.ffmpeg_path = os.path.join(self.binary_path, 'bin', 'ffmpeg')
            else:
                # Checks if it's running the portable version
                if os.path.isdir("./tcl"):
                    self.ffmpeg_path = "./bin/ffmpeg"
                else:
                    self.ffmpeg_path = "./bin/ffmpeg-2023-03-13-git-amd64-linux/ffmpeg"

        # Label to greet the user
        self.greet_label = ttk.Label(master, anchor="center", text="\n                Welcome to the converter!\nChoose your files, output and start converting 8)")
        self.greet_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Add a button to select input files
        self.select_files_button = ttk.Button(master, text="Select Files", style='Accent.TButton', command=self.select_files)
        self.select_files_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

        # Add a button to select the output directory
        self.select_output_button = ttk.Button(master, text="Select Output Folder", style='Accent.TButton', command=self.select_output_folder)
        self.select_output_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

        # Add a dropdown to select the preset
        self.preset_label = ttk.Label(master, text="Preset: ")
        self.preset_label.grid(row=2, column=1, columnspan=1, padx=(0, 220), pady=10)

        self.preset_var=tk.StringVar(master)
        self.preset_dropdown = ttk.Combobox(master, width=20, textvariable=self.preset_var)
        self.preset_dropdown['values'] = ("ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow")
        self.preset_dropdown.current(4)
        self.preset_dropdown.grid(row=2, column=1, columnspan=5, padx=10, pady=10)

        # Add a slider to set quality
        self.quality_var=tk.IntVar()
        self.quality_var.set(23)
        
        # Label to show quality CRF (text)
        self.quality_label = ttk.Label(master, text="   Quality (CRF): 🛈 ")
        self.quality_label.grid(row=3, column=1, columnspan=1, padx=(0, 180), pady=10)
        
        # Creating a tooltip to show info about the Quality box
        self.quality_tooltip = self.ToolTip(self.quality_label, "CRF stands for 'Constant Rate Factor', an enconding \n method used for x264 which makes settings the video's quality really simple. \n Its range varies from 0 to 51, where 0 is 'Lossless quality' and 51 'Worst quality possible'. \n The one used by default is *23*, feel free to change tho as 18-28 is usually the best.")

        # Label to show quality CRF (value)
        self.quality_label_pop = ttk.Label(master, text=f"{self.quality_var.get()}")
        self.quality_label_pop.grid(row=3, column=1, columnspan=6, padx=(170, 0), pady=10)

        # Slider to set quality CRF
        self.quality_slider = ttk.Scale(master, from_=0, to=51, orient="horizontal", variable=self.quality_var)
        self.quality_slider.grid(row=3, column=1, columnspan=5, padx=(30, 0), pady=10)
        self.quality_slider.bind("<Button-1>", self.update_quality_label)
        self.quality_slider.bind("<B1-Motion>",self.update_quality_label)

        # Label to show resolution info
        self.res_info = ttk.Label(master, text="Resolution:")
        self.res_info.grid(row=4, column=0, columnspan=3, padx=(0, 140), pady=5)

        # Label to set resolution
        self.res_var = tk.StringVar(master)
        self.res_dropdown = ttk.Combobox(master, width=20, textvariable=self.res_var)
        self.res_dropdown['values'] = ("Default", "1920x1080", "1280x720", "640x480", "480x360", "Custom, write here.")
        self.res_dropdown.current(0)
        self.res_dropdown.grid(row=4, column=0, columnspan=3, padx=(120, 0), pady=5)

        # Label to show encoding info
        self.encoding_info = ttk.Label(master, text="   Encoding device: 🛈   ")
        self.encoding_info.grid(row=5, column=0, columnspan=3, padx=(0, 180), pady=10)
        self.encoding_tooltip = self.ToolTip(self.encoding_info, "Please set this to CPU in case converted \n files are not working properly.")

        # Label to set encoding
        self.encoding_var = tk.StringVar(master)
        self.encoding_dropdown = ttk.Combobox(master, width=20, textvariable=self.encoding_var)
        self.encoding_dropdown['values'] = ("Default (GPU/CPU)", "CPU")
        self.encoding_dropdown.current(0)
        self.encoding_dropdown.grid(row=5, column=0, columnspan=3, padx=(120, 0), pady=10)

        # Add a label to display the selected input files and output directory
        self.input_files_label = ttk.Label(master, text="No files selected.")
        self.input_files_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

        # Add a label to display the selected output folder
        self.output_dir_label= ttk.Label(master, text=f"No output folder selected, using default: {os.getcwd()}")
        self.output_dir_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        self.output_dir = os.getcwd()

        # Add a button to start the conversion process
        self.convert_button = ttk.Button(master, text="Convert", style='Accent.TButton', command=self.convert_files, state="disabled")
        self.convert_button.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

        # Add a button to abort conversion
        self.abort_button = ttk.Button(master, text="Abort conversion", style='Accent.TButton', command=self.stop_conversion, state="disabled")
        self.abort_button.grid(row=9, column=1, columnspan=4, padx=90, pady=0)

        # Add a progress bar to show conversion progress
        self.progress_label = ttk.Label(master, text="Conversion Progress:")
        self.progress_label.grid(row=9, column=0, padx=90, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress = Progressbar(master, mode="determinate", variable=self.progress_var)
        self.progress.grid(row=9, column=0, columnspan=3, padx=50, pady=10)

        # Add a label to display the currently converting file
        self.converting_label = ttk.Label(master, text="")
        self.converting_label.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

        # Call the update_label method every second
        self.master.after(1000, self.update_gui)
        
        # Theme switcher (not implemented)
        # self.themeswitch = ttk.Checkbutton(root, text='Switch Theme', style='Switch', command=self.change_theme)
        # self.themeswitch.grid(row=8, rowspan=4, column=0, columnspan=3, padx=10, pady=10)

    # Function to update the quality CRF value
    def update_quality_label(self, event=None):
        if event:
            # If called as an event handler, update the label text based on the event
            self.quality_label_pop.config(text=f"{self.quality_var.get()}")
        else:
            # If called as a callback, update the label text without event-specific text
            self.quality_label_pop.config(text=f"{self.quality_var.get()}")


    # "Recursive" function updating the GUI every second
    def update_gui(self):
        # Updating the GUI
        self.master.update()
        # Call the update_label method again after one second
        self.master.after(1000, self.update_gui)


    # Simple function to update the label showing which file is being converted
    def update_label(self, input):
        self.converting_label.config(text=f"Currently converting: {input}")

    # Function to set main GPU 
    def use_hw_accel(self):
        
        if self.os_info == "Windows":
            # Retrieving GPU list on Windows
            gpu_list=self.gpu_info.Win32_VideoController()
            for gpu in gpu_list:
                if "NVIDIA" in gpu.Name:
                    self.gpu = "NVIDIA"
                    break
                elif "AMD" in gpu.Name:
                    self.gpu = "AMD"
                    break
        else:
            # Retrieving GPU list on Linux
            try:
                lspci_output = subprocess.check_output(["lspci", "-vnn"], stderr=subprocess.STDOUT)
                lspci_output = lspci_output.decode("utf-8")
                if "NVIDIA" in lspci_output:
                    self.gpu = "NVIDIA"
                elif "AMD" in lspci_output:
                    self.gpu = "AMD"
            except subprocess.CalledProcessError:
                return

    # Function to stop conversion if wanted
    def stop_conversion(self):

        # Ask with messagebox about the confirm    
        confirm_stop=messagebox.askyesno("Abort conversion", "Are you sure you want to stop conversion of your files?")
        
        if confirm_stop:
            # Kills the conversion process
            os.kill(self.process.pid, signal.SIGTERM)
            messagebox.showinfo("Conversion aborted", "Your conversion has been stopped.")
            self.processstatus = False

            # Reverts changes to buttons
            self.convert_button.config(state="normal")
            self.abort_button.config(state="disabled")
            
            # Initialize the progress bar
            self.progress_var.set(0)
            self.progress.configure(maximum=100)
        
        else:
            pass

    # Function to check if the resolution is valid
    def is_valid_resolution(self, res):
        
        res_list = res.split("x")
        if len(res_list) != 2:
            return False
        
        try:
            t1 = int(res_list[0])
            t2 = int(res_list[1])
            if t1 < 0 or t2 < 0:
                return False
        except ValueError:
            return False
        
        return True

    # Well...it converts file i guess?
    def convert_files(self):

        # Disables conversion button
        self.convert_button.config(state="disabled")

        # Enables abort conversion button
        self.abort_button.config(state="normal")

        # Get GPU information
        self.use_hw_accel()

        for idx, input_file in enumerate(self.input_files):            
            
            # Changing currently converted file label
            self.update_label(input_file)
            self.master.after(1000, self.update_gui)

            ffmpeg_cmd = [self.ffmpeg_path, "-y"]
            ffmpeg_cmd += ["-i", input_file]

            # Using encoder based on GPU/choice
            if self.encoding_var.get() == "Default (GPU/CPU)":
                if self.gpu == "NVIDIA":    
                    ffmpeg_cmd += ["-c:v", "h264_nvenc"]
                elif self.gpu == "AMD":
                    ffmpeg_cmd += ["-c:v", "h264_amf"]
                else:
                    ffmpeg_cmd += ["-c:v", "libx264"]
            else:
                ffmpeg_cmd += ["-c:v", "libx264"]

            # Set resolution according to GUI
            if self.res_var.get():
                resolution = self.res_var.get()
                if resolution != "Default" or self.is_valid_resolution(resolution):
                    ffmpeg_cmd += ["-s", self.res_var.get()]

            # Creating output file
            output_file = os.path.join(self.output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".mp4")
            ffmpeg_cmd += ["-preset", self.preset_var.get(), "-crf", str(self.quality_var.get()), output_file]

            try:    
                # Starting the FFmpeg process
                if self.os_info == "Windows":
                    # Hides FFmpeg cmd spawning on Windows during conversion
                    startupinfo = subprocess.STARTUPINFO()  
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE 
                    self.process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, universal_newlines=True)
                else:
                    self.process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                # Initialize the progress bar
                self.progress_var.set(0)
                self.progress.configure(maximum=100)

                while self.process.poll() is None:
                    # Read the progress information from the process
                    line = self.process.stderr.readline()

                    # Extract the progress information from the line
                    if "Duration" in line:
                        duration = line.split("Duration: ")[1].split(",")[0]
                        hours, minutes, seconds = duration.split(":")
                        total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

                    if "time=" in line:
                        time_str = line.split("time=")[1].split(" ")[0]
                        hours, minutes, seconds = time_str.split(":")
                        current_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

                        # Update the progress bar
                        progress_percent = (current_seconds / total_seconds) * 100
                        self.progress_var.set(progress_percent)

                    # Update the GUI
                    self.master.update()

                # Check if the progress has been ended by stop_conversion
                if self.processstatus:

                    # Update the progress bar to 100% after the conversion is complete
                    self.progress_var.set(100)

                    # Show a message box when the conversion is complete 
                    if idx == len(self.input_files) - 1:
                        messagebox.showinfo("Conversion Complete", "Conversion completed successfully!")

            except subprocess.CalledProcessError as e:
                
                # Updating label to display current converting file
                messagebox.showerror("Error", f"Conversion failed: {e}")

                # Upgrading error logs if related to GPU

            # Cleaning label
            self.converting_label.config(text=" " * len(input_file))

        # Re-enable the convert button
        self.convert_button.config(state="normal")

        # Initialize the progress bar
        self.progress_var.set(0)
        self.progress.configure(maximum=100)


    def select_files(self):

        # Open the file chooser dialog to select WebM files
        
        if self.os_info == "Windows":
            input_files = filedialog.askopenfilenames(defaultextension=".webm", filetypes=[("WebM files", "*.webm")])
        else:
            try:
                # If zenity is installed on the system, use that:
                zenitycheck = subprocess.check_output(['zenity', '--version'])
                zenitycommand = "zenity --file-selection --file-filter='WebM files | *.webm' --multiple"
                
                # Run the command and capture the output
                zenityoutput = subprocess.check_output(zenitycommand, shell=True, text=True)
                input_files = zenityoutput.strip().split("|")

            except subprocess.CalledProcessError as e:
                # If zenity isn't installed, fallback to default file chooser
                input_files = filedialog.askopenfilenames(defaultextension=".webm", filetypes=[("WebM files", "*.webm")])


        if input_files:
            # Check if all selected files are WebM files
            if all(os.path.splitext(input_file)[1].lower() == ".webm" for input_file in input_files):
                self.input_files = input_files
                self.input_files_label.config(text=f"Selected files: {len(input_files)}")
                self.convert_button.config(state="normal")
                if len(input_files):
                    self.select_files_button.config(text=f"Select Files ✅") 
            else:
                messagebox.showerror("Error", "Only WebM files can be converted.")
    
    def select_output_folder(self):

        # Open the file chooser dialog to select the output directory
        if self.os_info == "Windows":
            self.output_dir = filedialog.askdirectory()
        else:
            try:
                # If zenity in installed on the system:
                zenitycheck = subprocess.check_output(['zenity', '--version'])
                zenitycommand = "zenity --file-selection --directory"

                # Run the command and capture the output
                zenityoutput = subprocess.check_output(zenitycommand, shell=True, text=True)
                self.output_dir = zenityoutput.strip()
            
            except subprocess.CalledProcessError as e:
                self.output_dir = filedialog.askdirectory()

        if self.output_dir:
            self.output_dir_label.config(text=" " * len(self.output_dir_label.cget("text")))
            self.output_dir_label.config(text=f"Output folder: {self.output_dir} ✅")
            self.select_output_button.config(text=f"Select Output Folder ✅")
            self.output_dir_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
            self.convert_button.config(state="normal")
    

if __name__ == '__main__':
    
    window = tk.Tk()

    # Setting theme and logo path
    if platform.system() == "Windows":
            if hasattr(sys, '_MEIPASS'):
                themepath = os.path.join(sys._MEIPASS, "theme/forest-dark.tcl")
                logopath = os.path.join(sys._MEIPASS, "misc/logotaskbar.png")
            else:
                themepath = "./theme/forest-dark.tcl"
                logopath = "./misc/logotaskbar.png"
    else:
        if getattr(sys, 'frozen', False):
            themedir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            themepath = os.path.join(themedir, 'theme', 'forest-dark.tcl')
            logopath = os.path.join(themedir, 'misc', 'logotaskbar.png')
        else:
            themepath = "./theme/forest-dark.tcl"
            logopath = "./misc/logotaskbar.png"

    logo = ImageTk.PhotoImage(Image.open(logopath))
    window.iconphoto(True, logo)
    
    window.tk.call('source', themepath)
    theme = "forest-dark"
    ttk.Style().theme_use(theme) 
    
    app = ConverterGUI(window)
    window.mainloop()
