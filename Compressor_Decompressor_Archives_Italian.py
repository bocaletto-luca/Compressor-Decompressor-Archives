# Software Name: Compressor-Decompressor-Archives
# Author: Bocaletto Luca
# Web Site: https://www.elektronoide.it

# Importazione delle librerie necessarie
import tkinter as tk
from tkinter import ttk, filedialog
import zipfile
import os

# Funzione per comprimere i file selezionati
def compress_files():
    try:
        # Chiede all'utente di selezionare i file da comprimere
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Ottiene il tipo di compressione selezionato
            compression_type = compression_var.get()
            output_extension = ".zip" if compression_type == "zip" else ".gz"
            # Chiede all'utente di selezionare la posizione di salvataggio dell'archivio compresso
            output_path = filedialog.asksaveasfilename(defaultextension=output_extension)
            if output_path:
                # Crea un oggetto zipfile e aggiunge i file selezionati all'archivio
                with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                    for file_path in file_paths:
                        zf.write(file_path, os.path.basename(file_path))  # Usiamo solo il nome del file
                result_label.config(text="Compressione completata!")
    except Exception as e:
        result_label.config(text=f"Errore durante la compressione: {str(e)}")

# Funzione per decomprimere i file selezionati
def decompress_files():
    try:
        # Chiede all'utente di selezionare i file da decomprimere
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            decompression_type = decompression_var.get()
            for file_path in file_paths:
                if decompression_type == "zip":
                    output_path = file_path + "_decompressed"
                    # Estrae i file dall'archivio ZIP
                    with zipfile.ZipFile(file_path, 'r') as zf:
                        zf.extractall(output_path)
                elif decompression_type == "gz":
                    output_path = file_path[:-3]  # Rimuovi l'estensione .gz
                    with open(output_path, 'wb') as output_file, open(file_path, 'rb') as input_file:
                        import zlib
                        decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
                        for data in iter(lambda: input_file.read(1024), b''):
                            output_file.write(decompressor.decompress(data))
                result_label.config(text="Decompressione completata!")
    except Exception as e:
        result_label.config(text=f"Errore durante la decompressione: {str(e)}")

# Funzione per visualizzare le informazioni dell'archivio e il suo contenuto
def view_files():
    try:
        # Chiede all'utente di selezionare l'archivio da visualizzare
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Abilita il widget di testo per l'output
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            archive_files = []

            for file_path in file_paths:
                output_text.insert(tk.END, f"Informazioni su {file_path}:\n")
                with zipfile.ZipFile(file_path, 'r') as zf:
                    for info in zf.infolist():
                        output_text.insert(tk.END, f"Nome: {info.filename}\n")
                        output_text.insert(tk.END, f"Dimensione compressa: {info.compress_size} bytes\n")
                        output_text.insert(tk.END, f"Dimensione non compressa: {info.file_size} bytes\n")
                        output_text.insert(tk.END, f"Metodo di compressione: {info.compress_type}\n")
                        output_text.insert(tk.END, "\n")
                        archive_files.extend(zf.namelist())

            output_text.insert(tk.END, "Contenuto dell'Archivio:\n")
            for file_name in archive_files:
                output_text.insert(tk.END, file_name + "\n")

            # Disabilita il widget di testo per l'output
            output_text.config(state=tk.DISABLED)
    except Exception as e:
        result_label.config(text=f"Errore durante la visualizzazione: {str(e)}")

# Creazione della finestra principale
app = tk.Tk()
app.title("Software di Compressione/Decompressione")

# Creazione del frame principale
file_frame = tk.Frame(app, padx=10, pady=10)
file_frame.grid(row=0, column=0, columnspan=4)

# Etichette e opzioni per la compressione e la decompressione
title_label = tk.Label(file_frame, text="Seleziona i file da comprimere, decomprimere o visualizzare:")
title_label.grid(row=0, column=0, columnspan=4)

compression_label = tk.Label(file_frame, text="Seleziona il formato di archivio:")
compression_label.grid(row=1, column=0)
compression_var = tk.StringVar()
compression_var.set("zip")
compression_options = ["zip", "gz"]
compression_menu = tk.OptionMenu(file_frame, compression_var, *compression_options)
compression_menu.grid(row=1, column=1)

decompression_label = tk.Label(file_frame, text="Seleziona il formato di archivio:")
decompression_label.grid(row=2, column=0)
decompression_var = tk.StringVar()
decompression_var.set("zip")
decompression_options = ["zip", "gz"]
decompression_menu = tk.OptionMenu(file_frame, decompression_var, *decompression_options)
decompression_menu.grid(row=2, column=1)

# Pulsanti per le azioni di compressione, decompressione e visualizzazione
compress_button = tk.Button(file_frame, text="Comprimi", command=compress_files)
compress_button.grid(row=1, column=2)

decompress_button = tk.Button(file_frame, text="Decomprimi", command=decompress_files)
decompress_button.grid(row=2, column=2)

view_button = tk.Button(file_frame, text="Visualizza", command=view_files)
view_button.grid(row=3, column=1)

# Barra di avanzamento
progress = ttk.Progressbar(app, length=300, mode='determinate')
progress.grid(row=1, column=0, columnspan=4, pady=10)

# Widget di testo per l'output
output_text = tk.Text(app, wrap=tk.WORD, width=40, height=10)
output_text.grid(row=2, column=0, columnspan=4, pady=10)
output_text.config(state=tk.DISABLED)

# Etichetta per i risultati
result_label = tk.Label(app, text="")
result_label.grid(row=3, column=0, columnspan=4)

# Esecuzione dell'app
app.mainloop()
