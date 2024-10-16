import pyperclip
import tkinter as tk
from tkinter import ttk
import threading
import time
import keyboard  # Importa la libreria keyboard

# Lista per mantenere la cronologia degli appunti
clipboard_history = []
previous_clip = ""
root = None  # Definisce la finestra inizialmente chiusa

# Funzione per salvare negli appunti e aggiungere alla cronologia
def save_clipboard():
    global previous_clip
    current_clip = pyperclip.paste()  # Prendi l'attuale contenuto degli appunti
    
    # Se il contenuto è diverso dall'ultimo copiato, lo aggiungiamo alla cronologia
    if current_clip != previous_clip and current_clip != "":
        clipboard_history.append(current_clip)
        previous_clip = current_clip
        update_listbox()

# Funzione per aggiornare la Listbox con la cronologia degli appunti
def update_listbox():
    if root:  # Verifica se la finestra è aperta
        listbox.delete(0, tk.END)  # Svuota la Listbox
        for i, clip in enumerate(clipboard_history):
            listbox.insert(tk.END, f"{i}: {clip}")  # Inserisci le nuove voci

# Funzione per gestire il click su un elemento della Listbox
def on_select(event):
    widget = event.widget
    if widget.size() > 0:
        selection = widget.curselection()
        if selection:
            index = selection[0]
            selected_clip = clipboard_history[index]
            pyperclip.copy(selected_clip)
            print(f"Copiato negli appunti: {selected_clip}")

# Funzione per aprire la finestra della cronologia
def show_history_window():
    global root, listbox
    if root is not None:
        root.lift()  # Porta in primo piano la finestra esistente
        return
    
    root = tk.Tk()
    root.title("Cronologia degli Appunti")
    root.geometry("400x300")  # Imposta la dimensione della finestra
    root.attributes('-topmost', True)  # Mantieni la finestra in primo piano
    root.configure(bg="#f0f0f0")  # Sfondo grigio chiaro

    # Stile del font
    font_style = ('Arial', 10)

    # Label titolo
    title_label = tk.Label(root, text="Cronologia degli Appunti", font=('Arial', 12, 'bold'), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Listbox per visualizzare la cronologia
    listbox = tk.Listbox(root, height=15, width=50, font=font_style, bg="#ffffff", selectbackground="#c0e4ff")
    listbox.pack(padx=10, pady=10)

    # Aggancia la selezione degli elementi alla funzione on_select
    listbox.bind('<<ListboxSelect>>', on_select)

    # Bottone per chiudere la finestra con testo modificato
    close_button = ttk.Button(root, text="Chiudi Finestra", command=lambda: close_window())
    close_button.pack(pady=10)

    # Modifica lo stile del pulsante
    close_button.configure(width=20, padding=5)

    # Avvia la finestra principale di Tkinter
    root.mainloop()

# Funzione per chiudere la finestra e ripristinare lo stato
def close_window():
    global root
    if root:
        root.destroy()
        root = None  # Resetta il riferimento alla finestra chiusa

# Funzione principale che monitora gli appunti
def monitor_clipboard():
    while True:
        save_clipboard()  # Salva ogni nuova copia negli appunti
        time.sleep(1)  # Controlla gli appunti ogni secondo (può essere regolato)

if __name__ == "__main__":
    # Avvia il monitoraggio degli appunti in background
    print("Monitoraggio degli appunti avviato. Premi Ctrl+Shift+H per aprire la cronologia.")
    
    # Avvia il monitoraggio in un thread separato per evitare blocchi
    clipboard_thread = threading.Thread(target=monitor_clipboard)
    clipboard_thread.daemon = True  # Permette al thread di chiudersi con il programma
    clipboard_thread.start()

    # Ciclo principale per ascoltare la combinazione di tasti
    while True:
        if keyboard.is_pressed('ctrl+shift+h'):
            show_history_window()  # Mostra la finestra quando si preme Ctrl+Shift+H
        time.sleep(0.1)  # Un breve ritardo per ridurre il carico della CPU
