import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class File:

    def __init__(self, path=''):
        self.path = path
        self.pgn_list = []
        self.pgn_set = set()
        self.str_list = []

    def __str__(self):
        return 'Cl2000 Log File'


def get_path():
    data_log.path = filedialog.askopenfilename(filetypes=(("txt", "*.txt"), ("all files", "*.*")))
    file_path_label.config(text=data_log.path)
    get_content()


def get_content():
    # Read Content From File
    try:
        f = open(data_log.path, 'r')
        all_content = f.readlines()
        f.close()
    except PermissionError:
        messagebox.showerror('Error', 'No file selected!')
        raise Exception('No file selected!')

    pgn_list = []
    for line in all_content:
        if line[0] == '2':
            pgn_list.append(line.rstrip())

    pgn_set = set()
    for num in pgn_list:
        pgn = num[15:23]
        if pgn[-1] == ';':
            pgn_set.add(pgn[1:5])
        else:
            pgn_set.add(pgn[2:6])

    hex_set = []
    dec_set = []
    for num in pgn_set:
        x = int(num, 16)
        dec_set.append(x)
        hex_set.append(num)

    hex_set.sort()
    dec_set.sort()

    str_list = ''
    for index in range(1, len(dec_set)):
        # print('{' + str(dec_set[index]) + ',kvFalse}/* Placeholder */')
        str_list += '{' + str(dec_set[index]) + ',kvFalse}/* Placeholder */\n'

    data_log.str_list = str_list
    output_text.insert('end', str_list)


def save_to_file():
    file = filedialog.asksaveasfilename(defaultextension='.txt',
                                        filetypes=(("txt", "*.txt"), ("all files", "*.*")))
    with open(file, "w") as f:
        for index in data_log.str_list:
            f.write(index)


# Set data_log as File class
data_log = File()

# Tkinter Window Setup
window = Tk()

current_dir = os.getcwd()
# Set window properties
window.title('CL2000 Log Unloader')
window.geometry("500x700")
window.iconbitmap(current_dir + '/images/favicon.png')


# Configure Grid
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=1)


# Create Labels for browsing Files and Displaying File Path
label_file_explorer = Label(window, text="Decode CL2000 Log Files", width=50, height=2)
label_file_explorer.grid(column=0, row=0, columnspan=3)

path_label = Label(window, text='File Path:')
path_label.grid(column=0, row=1, sticky=E)

file_path_label = Label(window, text=data_log.path, background='white', width=52, borderwidth=1, relief='sunken')
file_path_label.grid(column=1, row=1, pady=2, ipady=3)


# Setup Buttons
# Browse Button
button_explore = Button(window, text="Browse", command=get_path)
button_explore.grid(column=2, row=1, pady=2, padx=10, sticky=W)

# Output box for converter PGNs
output_text = Text(window, width=45, height=35)
output_text.grid(column=1, row=2)

# Save Button
button_save_list = Button(window, text="Save", command=save_to_file)
button_save_list.grid(column=1, row=5, sticky=W, pady=5, padx=5, ipady=5, ipadx=15)

# Exit Button
button_exit = Button(window, text="Exit", command=window.destroy)
button_exit.grid(column=1, row=5, sticky=E, pady=5, padx=5, ipady=5, ipadx=15)

# Let the window wait for any events
window.mainloop()

# TODO: Add Names of PGNs instead of Placeholder
