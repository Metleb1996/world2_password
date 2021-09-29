import tkinter as tk
import core

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.database_password = ""
        self.edit_mode = False
        self.edit_id = -1
        self.title("W2Password")
        self.geometry("360x480")
        self.resizable(False, False)
        img = tk.PhotoImage(file='./images/icon.png')
        core.cr_table()
        self.tk.call('wm', "iconphoto", self._w, img)
        self.protocol('WM_DELETE_WINDOW', self.exit)
        self.entry_lPass = tk.Entry(bg="#cce1e8", textvariable="password", show='*')
        self.passButton = tk.Button(text="Load", bg="green", fg="black", command=self.login)
        self.listpass = tk.Listbox(height=14)
        self.listpass.bind("<<ListboxSelect>>", self.item_select)
        self.listpass.bind('<Button-3>', self.item_edit)
        self.label_curPass = tk.Label()
        self.copyButton = tk.Button(text="Copy", bg="green", fg="black", command=self.copy_to_clipboard)
        self.entry_sName = tk.Entry()
        self.entry_sPassword = tk.Entry()
        self.okButton = tk.Button(text="Ok", bg="green", fg="black", command=self.add_to_db)
        self.show_childs() #show all child widgets


    def copy_to_clipboard(self):
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(self.label_curPass["text"])
        r.destroy()
        self.label_curPass.configure(text="Copied", fg="green")


    def item_edit(self, event):
        selection = event.widget.curselection()
        if selection:
            service = event.widget.get(selection[0])
            password = core.get_data(service)
            password = core.decrypt(password[0][2][2:-1], self.database_password)
            self.entry_sName.delete(0, tk.END)
            self.entry_sName.insert(0, service)
            self.entry_sPassword.delete(0, tk.END)
            self.entry_sPassword.insert(0, password)
            self.edit_mode = True
            self.edit_id = selection[0]


    def item_select(self, event):
        selection = event.widget.curselection()
        if selection:
            sel_name = event.widget.get(selection[0])
            data = core.get_data(sel_name)
            data = core.decrypt(data[0][2][2:-1], self.database_password)
            self.label_curPass.configure(text=str(data), fg="blue")


    def add_to_db(self):
        new_pass = str(self.entry_sPassword.get()).strip()
        new_service = str(self.entry_sName.get()).strip()
        if  new_pass =="":
            self.label_curPass.configure(text="Enter valid password", fg="red")
        elif new_service == "":
            self.label_curPass.configure(text="Enter valid service name", fg="red")
        else:
            new_pass = str(core.encrypt(new_pass, self.database_password))
            if self.edit_mode:
                core.mod_data(self.edit_id,new_service, new_pass)
                self.edit_mode = False
            else:
                core.add_data(new_service, new_pass)
            self.entry_sPassword.delete(0, tk.END)
            self.entry_sName.delete(0, tk.END)
            self.label_curPass.configure(text="Success", fg="green")



    def login(self):
        if self.database_password == "":
            self.database_password = str(self.entry_lPass.get()).strip()
        if self.database_password == "":
            self.label_curPass.configure(text="Enter valid login password", fg="red")
        else:
            self.entry_lPass.delete(0, tk.END)
            self.label_curPass.configure(text="")
            self.db_list = core.get_all_data()
            self.listpass.delete(0, tk.END)
            if len(self.db_list) > 0:
                for el in self.db_list:
                    self.listpass.insert(int(el[0]), str(el[1]))


    def show_childs(self):
        self.entry_lPass.pack(fill="x", padx=8, pady=6)
        self.passButton.pack(fill="x", padx=2, pady=2)
        self.listpass.pack(fill="x", padx=5, pady=5)
        self.label_curPass.pack(fill="x", padx=2, pady=2)
        self.copyButton.pack(fill="x", padx=2, pady=2)
        self.entry_sName.pack(fill="x", padx=2, pady=2)
        self.entry_sPassword.pack(fill="x", padx=2, pady=2)
        self.okButton.pack(fill="x", padx=2, pady=2)
        

    def exit(self):
        print("The end...")
        exit()

if __name__ == "__main__":
    mw = MainWindow()
    mw.mainloop()