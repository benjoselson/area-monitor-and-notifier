import os
import tkinter as tk
from filefuncs import empty_smsnums, read_smsnums, write_smsnums
import sys

class EnvVarGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Environment Variables')
        self.master.geometry('400x320')

        self.missing_vars = self.check_env_vars()
        self.missing_vars = False
        if self.missing_vars:
            self.create_widgets()
        else:
            print("env var already exist")
            self.master.destroy()
            self.start_number_gui()

    def check_env_vars(self):
        env_vars = ['TwilioAccountSID', 'TwilioAuthToken', 'TwilioPhoneNumber']
        missing_vars = []
        for var in env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        return missing_vars

    def submit(self):
        if all(entry.get() for entry in self.entries):
            for var, entry in zip(self.missing_vars, self.entries):
                os.environ[var] = entry.get()
                if sys.platform == "win32":
                    os.system(f'setx {var} "{entry.get()}"')
                else:
                    with open(os.path.expanduser("~/.bash_profile"), "a") as f:
                        f.write(f"\nexport {var}={entry.get()}\n")
            print("env variables updated")
            self.master.destroy()
            self.start_number_gui()

    def create_widgets(self):
        self.labels = []
        self.entries = []
        for var in self.missing_vars:
            label = tk.Label(self.master, text=var)
            label.pack(padx=10, pady=10)
            self.labels.append(label)

            entry = tk.Entry(self.master)
            entry.pack(padx=10, pady=10)
            self.entries.append(entry)

        button_frame = tk.Frame(self.master)
        button_frame.pack()

        quit_button = tk.Button(button_frame, text='Quit', command=sys.exit)
        quit_button.pack(side=tk.LEFT, padx=5, pady=5)

        submit_button = tk.Button(button_frame, text='Submit', command=self.submit)
        submit_button.pack(side=tk.LEFT, padx=5, pady=5)

    def start_number_gui(self):
        root = tk.Tk()
        gui = PhoneNumGui(root)
        root.mainloop()


class PhoneNumGui:
    def __init__(self, master):
        self.master = master
        self.entry_list = []
        self.label = tk.Label(self.master,
                              text="Enter all recipient phone numbers. Make sure to include the area code.",
                              font=("TkDefaultFont", 12))
        self.label.pack(padx=10, pady=10)
        vcmd = (self.master.register(self.validate), '%P')
        self.entry = tk.Entry(self.master,
                              validate="key",
                              validatecommand=vcmd,
                              font=("TkDefaultFont", 12))
        self.entry.pack(padx=10, pady=10)
        self.message_label = tk.Label(self.master, text="", font=("TkDefaultFont", 12))
        self.message_label.pack(padx=10, pady=10)
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(padx=10, pady=10)
        self.quit_button = tk.Button(self.button_frame,
                                     text="Quit",
                                     command=sys.exit,
                                     font=("TkDefaultFont", 12))
        self.quit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.remove_button = tk.Button(self.button_frame,
                                       text="Remove Entry",
                                       command=self.remove_entry,
                                       font=("TkDefaultFont", 12))
        self.remove_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_button = tk.Button(self.button_frame,
                                    text="Add Entry",
                                    command=self.add_entry,
                                    font=("TkDefaultFont", 12))
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.next_button = tk.Button(self.button_frame,
                                     text="Next",
                                     command=self.next_page,
                                     font=("TkDefaultFont", 12))
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

    def add_entry(self):
        vcmd = (self.master.register(self.validate), '%P')
        new_entry = tk.Entry(self.master,
                             validate="key",
                             validatecommand=vcmd,
                             font=("TkDefaultFont", 12))
        self.entry_list.append(new_entry)
        self.button_frame.pack_forget()
        new_entry.pack(padx=10, pady=10)
        self.button_frame.pack(padx=10, pady=10)

    def remove_entry(self):
        if len(self.entry_list) > 0:
            last_entry = self.entry_list.pop()
            last_entry.destroy()
            self.button_frame.pack_forget()
            self.button_frame.pack(padx=10, pady=10)

    def next_page(self):
        all_valid = True
        phone_numbers = []
        for entry in self.entry_list + [self.entry]:
            text = entry.get()
            if len(text) > 0 and len(text) < 10:
                all_valid = False
                break
            elif len(text) == 10:
                phone_numbers.append(text)
        if not all_valid:
            self.message_label.config(text="Please use a 10 digit phone number (include the area code).", fg="red")
        else:
            self.message_label.config(text="")
            written_numbers = ['+1' + number for number in phone_numbers]
            empty_smsnums()
            write_smsnums(content=written_numbers)
            # print(phone_numbers)
            read_smsnums()
            self.master.destroy()

    def validate(self, new_text):
        if not new_text:
            return True
        if len(new_text) > 10:
            return False
        try:
            int(new_text)
            return True
        except ValueError:
            return False


def main_gui():
    root = tk.Tk()
    gui = EnvVarGUI(root)
    root.mainloop()