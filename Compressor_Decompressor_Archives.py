# Software Name: Compressor-Decompressor-Archives
# Author: Luca Bocaletto
# Import necessary libraries
import tkinter as tk
from tkinter import ttk, filedialog
import zipfile
import os

# Function to compress selected files
def compress_files():
    try:
        # Ask the user to select files to compress
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Get the selected compression type
            compression_type = compression_var.get()
            output_extension = ".zip" if compression_type == "zip" else ".gz"
            # Ask the user to select the save location for the compressed archive
            output_path = filedialog.asksaveasfilename(defaultextension=output_extension)
            if output_path:
                # Create a zipfile object and add the selected files to the archive
                with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                    for file_path in file_paths:
                        zf.write(file_path, os.path.basename(file_path))  # Use only the file name
                result_label.config(text="Compression completed!")
    except Exception as e:
        result_label.config(text=f"Error during compression: {str(e)}")

# Function to decompress selected files
def decompress_files():
    try:
        # Ask the user to select files to decompress
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            decompression_type = decompression_var.get()
            for file_path in file_paths:
                if decompression_type == "zip":
                    output_path = file_path + "_decompressed"
                    # Extract files from the ZIP archive
                    with zipfile.ZipFile(file_path, 'r') as zf:
                        zf.extractall(output_path)
                elif decompression_type == "gz":
                    output_path = file_path[:-3]  # Remove the .gz extension
                    with open(output_path, 'wb') as output_file, open(file_path, 'rb') as input_file:
                        import zlib
                        decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
                        for data in iter(lambda: input_file.read(1024), b''):
                            output_file.write(decompressor.decompress(data))
                result_label.config(text="Decompression completed!")
    except Exception as e:
        result_label.config(text=f"Error during decompression: {str(e)}")

# Function to view archive information and its contents
def view_files():
    try:
        # Ask the user to select the archive to view
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Enable the text widget for output
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            archive_files = []

            for file_path in file_paths:
                output_text.insert(tk.END, f"Information about {file_path}:\n")
                with zipfile.ZipFile(file_path, 'r') as zf:
                    for info in zf.infolist():
                        output_text.insert(tk.END, f"Name: {info.filename}\n")
                        output_text.insert(tk.END, f"Compressed size: {info.compress_size} bytes\n")
                        output_text.insert(tk.END, f"Uncompressed size: {info.file_size} bytes\n")
                        output_text.insert(tk.END, f"Compression method: {info.compress_type}\n")
                        output_text.insert(tk.END, "\n")
                        archive_files.extend(zf.namelist())

            output_text.insert(tk.END, "Archive Contents:\n")
            for file_name in archive_files:
                output_text.insert(tk.END, file_name + "\n")

            # Disable the text widget for output
            output_text.config(state=tk.DISABLED)
    except Exception as e:
        result_label.config(text=f"Error during viewing: {str(e)}")

# Create the main window
app = tk.Tk()
app.title("Compression/Decompression Software")

# Create the main frame
file_frame = tk.Frame(app, padx=10, pady=10)
file_frame.grid(row=0, column=0, columnspan=4)

# Labels and options for compression and decompression
title_label = tk.Label(file_frame, text="Select files to compress, decompress, or view:")
title_label.grid(row=0, column=0, columnspan=4)

compression_label = tk.Label(file_frame, text="Select archive format:")
compression_label.grid(row=1, column=0)
compression_var = tk.StringVar()
compression_var.set("zip")
compression_options = ["zip", "gz"]
compression_menu = tk.OptionMenu(file_frame, compression_var, *compression_options)
compression_menu.grid(row=1, column=1)

decompression_label = tk.Label(file_frame, text="Select archive format:")
decompression_label.grid(row=2, column=0)
decompression_var = tk.StringVar()
decompression_var.set("zip")
decompression_options = ["zip", "gz"]
decompression_menu = tk.OptionMenu(file_frame, decompression_var, *decompression_options)
decompression_menu.grid(row=2, column=1)

# Buttons for compression, decompression, and viewing actions
compress_button = tk.Button(file_frame, text="Compress", command=compress_files)
compress_button.grid(row=1, column=2)

decompress_button = tk.Button(file_frame, text="Decompress", command=decompress_files)
decompress_button.grid(row=2, column=2)

view_button = tk.Button(file_frame, text="View", command=view_files)
view_button.grid(row=3, column=1)

# Progress bar
progress = ttk.Progressbar(app, length=300, mode='determinate')
progress.grid(row=1, column=0, columnspan=4, pady=10)

# Text widget for output
output_text = tk.Text(app, wrap=tk.WORD, width=40, height=10)
output_text.grid(row=2, column=0, columnspan=4, pady=10)
output_text.config(state=tk.DISABLED)

# Label for results
result_label = tk.Label(app, text="")
result_label.grid(row=3, column=0, columnspan=4)

# Run the app
app.mainloop()
