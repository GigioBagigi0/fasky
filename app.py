import time, threading, ctypes, string
from pynput import keyboard
from pynput.keyboard import Controller
import customtkinter as ctk
import os
import subprocess

charDict = {}
noreps_process = None
def start_noreps():
    global noreps_process
    noreps_process = subprocess.Popen(["noreps.exe"], creationflags=subprocess.CREATE_NO_WINDOW) # noreps.exe = It is the program that allows you not to repeat keys (if you hold down an alphanumeric character it will not be written multiple times before releasing it, including accented letters)

def defaultKbv():

    with open("./.kbv", "w") as file:
        for i in string.ascii_lowercase:
            file.writelines(f"{i}|{i.upper()}\n")

    with open("./.kbv", "r") as file:
        initConfig = file.readlines()

    simboliNumCor = { # = default symbols corresponding to numbers dicionary
        '0': '0',
        '1': '←',
        '2': '↑',
        '3': '↓',
        '4': '→',
        '5': 'Ω',
        '6': '≤',
        '7': '≥',
        '8': '♫',
        '9': '₿',
    }

    with open("./.kbv", "w", encoding='utf-8') as file:
        for i in initConfig:
            file.writelines(i)
        for i in simboliNumCor.items():
            file.writelines(i[0] + '|' + str(i[1]) + '\n')


    with open("./.kbv", "r", encoding='utf-8') as file:
        initConfig = file.readlines()

        for i in initConfig:
            try:
                a, b = i.split('|')
                charDict[a] = b.split('\n')[0]
            except:
                pass

if not os.path.exists("./.kbv"):
    f = open("./.kbv", "x")
    defaultKbv()
    ctypes.windll.user32.MessageBoxW(0, "IMPORTANT\nUsing this program with games or software that prohibit virtual keyboards or macros may result in bans. The developer assumes no responsibility for any consequences. Stop the program when using such software.", "WARNING", 48)


window = ctk.CTk()
window.title("Fasky")
#window.iconbitmap("./icon.ico") #ico file

with open("./.kbv", "r", encoding='utf-8') as file:
    initConfig = file.readlines()



for i in initConfig:
    try:
        a, b = i.split('|')
        charDict[a] = b.split('\n')[0]
    except:
        pass

def modifyKeyValue(key, keyOnHold, modifyKeyMenuWindows):
    try:
        key = str(key)
        if key.isalnum():
            charDict[key] = str(keyOnHold)
            with open("./.kbv", "w", encoding='utf-8') as file:
                for i in charDict.items():
                    file.writelines(i[0] + '|' + str(i[1]) + '\n')
        else:
            ctypes.windll.user32.MessageBoxW(0, "Invalid key", "ERROR", 0)
            print(key, "\n", keyOnHold)
    except:
        print(key, "\n", keyOnHold)
    modifyKeyMenuWindows.destroy()



def modifyKeyWindow(key = "", keyboardMapWin = False):
    if keyboardMapWin != False:
        keyboardMapWin.destroy()
    def limit_input(*args):
        value = entry_var.get()
        if len(value) > 1:
            entry_var.set(value[:1])
    entry_var = ctk.StringVar()
    entry_var.trace("w", limit_input)

    modifyKeyMenuWindows = ctk.CTkToplevel(window)
    #modifyKeyMenuWindows.after(250, lambda: modifyKeyMenuWindows.iconbitmap("./icon.ico"))
    modifyKeyMenuWindows.attributes('-topmost', 'true')
    modifyKeyMenuWindows.title("Custom Keys")


    keyToModifyLabel = ctk.CTkLabel(modifyKeyMenuWindows, text="insert the letter/number you\nwant to modify while holding:")
    keyToModifyLabel.grid(row=0, column = 0, pady = 20, padx = (20, 2))


    keyToModify = ctk.CTkEntry(modifyKeyMenuWindows, textvariable=entry_var, width=10) # key to modify on holding
    keyToModify.grid(row = 0, column = 1, pady = 20, padx = (0.5, 20))
    keyToModify.insert(0, key)

    valueOnHoldingLbl = ctk.CTkLabel(modifyKeyMenuWindows, text="value on holding:")
    valueOnHoldingLbl.grid(row = 1, column = 0,pady = 20, padx = (0.5, 20))


    valueOnHolding = ctk.CTkEntry(modifyKeyMenuWindows, width=100)
    valueOnHolding.grid(row = 1, column = 1, pady = 20, padx = (0.5, 20))

    changeBtn = ctk.CTkButton(modifyKeyMenuWindows, text="change", command=lambda: modifyKeyValue(keyToModify.get(), valueOnHolding.get(), modifyKeyMenuWindows)) 
    changeBtn.grid(row = 3, pady = 20, padx = 20, columnspan = 2)

    def dfAndClose():
        defaultKbv()
        modifyKeyMenuWindows.destroy()

    defaultKeys = ctk.CTkButton(modifyKeyMenuWindows, text="set all keys to default", command=lambda: dfAndClose(), fg_color='transparent', text_color="lightblue", bg_color="transparent", hover_color="black")
    defaultKeys.grid(row = 4, columnspan = 2, pady = 5, padx = 5)

    modifyKeyMenuWindows.mainloop()


def mapKeyboard():
    keysMap = []
    with open('./.kbv', 'r', encoding='utf-8') as file:
        keysMap = file.readlines()
    for i, e in enumerate(keysMap):
        keysMap[i] = e.split('\n')[0]

    keyboardMapWin = ctk.CTkToplevel()
    #keyboardMapWin.after(250, lambda: keyboardMapWin.iconbitmap("./icon.ico"))
    keyboardMapWin.title("Map")
    keyboardMapWin.attributes('-topmost', 'true')
    column = 0
    row = -1
    for i, e in enumerate(keysMap):
        if i % 10 == 0:
            row += 1
            column = 0
        key = e.split('|')[0]
        btn = ctk.CTkButton(keyboardMapWin, text=f"{e}", command = lambda key=key: modifyKeyWindow(key, keyboardMapWin) )
        btn.grid(pady = 10, padx = 10, column=column, row=row)
        
        column+=1

    keyboardMapWin.mainloop()
    


window.update_idletasks()

# Initialize the controller to simulate input
kb_controller = Controller()

# Dictionary to track the last press of each key and the pressing time
tempo_ultimo_tasto = {}
pressed_keys = {}
# Minimum interval between pressing the same key to avoid repetitions 
intervallo_minimo = 0.1 # in seconds
# Time threshold for conversion to uppercase 
THRESHOLD = 0.3 # in seconds
# Set to keep track of keys already registered for a press
tasti_premuti = set()

def on_press(tasto):
    try:
        if hasattr(tasto, 'char') and tasto.char:
            carattere = tasto.char
            tempo_corrente = time.time()

            # Check if the key is alphanumeric (letter or number)
            if carattere.isalnum():
                # If the key was pressed recently, we do not record it
                if (carattere not in tempo_ultimo_tasto or
                        (tempo_corrente - tempo_ultimo_tasto[carattere]) > intervallo_minimo):
                    if carattere not in tasti_premuti:
                        # Record the pressure time
                        pressed_keys[tasto] = tempo_corrente
                        tasti_premuti.add(carattere)
                        tempo_ultimo_tasto[carattere] = tempo_corrente
            else:
                pass
        else:
            pass
    except AttributeError:
        pass

def on_release(tasto):
    try:
        if tasto in pressed_keys:

            press_duration = time.time() - pressed_keys[tasto]

            if hasattr(tasto, 'char') and tasto.char:
                
                carattere = tasto.char
                # Se il tempo di pressione è sufficiente, converte in maiuscolo
                if press_duration >= THRESHOLD:
                    kb_controller.type('\b')  # Elimina la lettera minuscola
                    try:
                        kb_controller.type(charDict[tasto.char])
                    except:
                        kb_controller.type(carattere.upper())
            # Remove the key from dictionaries
            del pressed_keys[tasto]
            tasti_premuti.discard(carattere)
            if carattere in tempo_ultimo_tasto:
                del tempo_ultimo_tasto[carattere]

    except AttributeError:
        pass
    
"""    if tasto == keyboard.Key.esc:
        return False"""

def main():
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True  # Si assicura che il thread si chiuda con l'applicazione principale
    listener_thread.start()

def start_listener():
    global status
    status.set("current status: active")
    text.configure(text_color="Green")
    startBtn.configure(fg_color="Grey")
    stopBtn.configure(fg_color="Red")

    start_noreps()

    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

def stop_listener():
    global status, noreps_process
    status.set("current status: inactive")
    text.configure(text_color="Red")
    stopBtn.configure(fg_color="Gray")
    startBtn.configure(fg_color="Green")

    noreps_process.terminate()  # terminates the "thread" that runs "noreps.exe" and thus terminates the program that avoids repetitions
    noreps_process.wait()       
    noreps_process = None

    global listener
    if listener is not None:
        listener.stop()
        listener = None
    

status = ctk.StringVar()
status.set("current status: inactive")

startBtn = ctk.CTkButton(window, text="START", command=main, fg_color="Green", hover_color="lightgreen", corner_radius=100)
startBtn.grid(padx=40, pady=20)

startBtn.bind("<Enter>", lambda event: startBtn.configure(text_color="black")) 
startBtn.bind("<Leave>", lambda event: startBtn.configure(text_color="white"))   

text = ctk.CTkLabel(window, textvariable=status)
text.grid(padx=0, pady=0)
text.configure(text_color="Red")

stopBtn = ctk.CTkButton(window, text="STOP", command=stop_listener, fg_color="Gray", hover_color="#FFCCCC", corner_radius=100)
stopBtn.grid(padx=20, pady=20)

stopBtn.bind("<Enter>", lambda event: stopBtn.configure(text_color="black")) 
stopBtn.bind("<Leave>", lambda event: stopBtn.configure(text_color="white"))    

customKeyBtn = ctk.CTkButton(window, text="modify keys", command=modifyKeyWindow)
customKeyBtn.grid(padx=20)

map = ctk.CTkButton(window, text="map", command=lambda: mapKeyboard(), fg_color='transparent', text_color="lightblue", bg_color="transparent", hover_color="black")
map.grid(row = 5, columnspan = 2, pady = 5, padx=20)

window.mainloop()

# you could create an algorithm that every time an app is opened that has never been opened before, it asks if it is an app that does not allow the virtual/gaming 
# keyboard and if the user answers yes, you need a file that stores these things and disables the program when these apps are opened again