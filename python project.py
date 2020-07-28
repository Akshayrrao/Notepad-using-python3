from tkinter import Tk, Text, Scrollbar, Menu, messagebox, filedialog, BooleanVar, Checkbutton, Label, Entry, StringVar, Grid, Frame
import os, subprocess, json, string

def mes():
    messagebox.showinfo('Not yet ready :(', 'This is feature is under development')
def copyright():
    messagebox.showinfo('Copyright', 'This Project is done by  https://github/akshayrrao')
def displayabout():
    messagebox.showinfo('About', 'This Project is done by https://github/akshayrrao/ using Python and tkinter for the OOP with Python lab project')

class Editor():
    def __init__(self, root):
        self.root = root        
        self.TITLE = "Python Editor Project"
        self.file_path = None
        self.set_title()
        
        frame = Frame(root)
        self.yscrollbar = Scrollbar(frame, orient="vertical")
        self.editor = Text(frame, yscrollcommand=self.yscrollbar.set)
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.config( wrap = "word", # use word wrapping
               undo = True, # Tk 8.4 
               width = 80 )        
        self.editor.focus()
        self.yscrollbar.pack(side="right", fill="y")
        self.yscrollbar.config(command=self.editor.yview)        
        frame.pack(fill="both", expand=1)

       
        root.protocol("WM_DELETE_WINDOW", self.file_quit) 

       
        self.menubar = Menu(root)
        
        filemenu = Menu(self.menubar, tearoff=0)# tearoff = 0 => can't be seperated from window
        filemenu.add_command(label="New", underline=1, command=self.file_new, accelerator="Ctrl+N")
        filemenu.add_command(label="Open...", underline=1, command=self.file_open, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", underline=1, command=self.file_save, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...", underline=5, command=self.file_save_as, accelerator="Ctrl+Alt+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", underline=2, command=self.file_quit, accelerator="Alt+F4")
        self.menubar.add_cascade(label="File", underline=0, menu=filemenu)
        editMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", underline=0, menu=editMenu)
       
        editMenu.add_command(label="Copy", command=mes)
        editMenu.add_command(label="Paste", command=mes)
        editMenu.add_separator()
        editMenu.add_command(label="Copyright", command=copyright)

        viewMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=viewMenu)
        
        viewMenu.add_command(label="Toolbar", command=mes)
        viewMenu.add_command(label="Status bar", command=mes)
        navigateMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Navigate", underline=0, menu=navigateMenu)
        
        navigateMenu.add_command(label="File", command=mes)
        windowMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", underline=0, menu=windowMenu)
       
        windowMenu.add_command(label="Font Colour", command=mes)
        windowMenu.add_command(label="Font Size", command=mes)
        helpMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", underline=0, menu=helpMenu)
        
        helpMenu.add_command(label="About", command=displayabout)
       
        root.config(menu=self.menubar)
    def save_if_modified(self, event=None):
        if self.editor.edit_modified():
            response = messagebox.askyesnocancel("Save?", "This document has been modified. Do you want to save changes?") #yes = True, no = False, cancel = None
            if response: 
                result = self.file_save()
                if result == "saved": 
                    return True
                else:
                    return None
            else:
                return response #None = cancel/abort, False = no/discard
        else: 
            return True
    
    def file_new(self, event=None):
        result = self.save_if_modified()
        if result != None: 
            self.editor.delete(1.0, "end")
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.file_path = None
            self.set_title()
            

    def file_open(self, event=None, filepath=None):
        result = self.save_if_modified()
        if result != None: 
            if filepath == None:
                filepath = filedialog.askopenfilename()
            if filepath != None  and filepath != '':
                with open(filepath, encoding="utf-8") as f:
                    fileContents = f.read()     
               
                self.editor.delete(1.0, "end")
                self.editor.insert(1.0, fileContents)
                self.editor.edit_modified(False)
                self.file_path = filepath

    def file_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(filepath=self.file_path)
        return result

    def file_save_as(self, event=None, filepath=None):
        if filepath == None:
            filepath = filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))) #defaultextension='.txt'
        try:
            with open(filepath, 'wb') as f:
                text = self.editor.get(1.0, "end-1c")
                f.write(bytes(text, 'UTF-8'))
                self.editor.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return "saved"
        except FileNotFoundError:
            print('FileNotFoundError')
            return "cancelled"

    def file_quit(self, event=None):
        result = self.save_if_modified()
        if result != None:
            self.root.destroy()

    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)
        
    def undo(self, event=None):
        self.editor.edit_undo()
        
    def redo(self, event=None):
        self.editor.edit_redo()   
            

    def main(self, event=None):          
        self.editor.bind("<Control-o>", self.file_open)
        self.editor.bind("<Control-O>", self.file_open)
        self.editor.bind("<Control-S>", self.file_save)
        self.editor.bind("<Control-s>", self.file_save)
        self.editor.bind("<Control-y>", self.redo)
        self.editor.bind("<Control-Y>", self.redo)
        self.editor.bind("<Control-Z>", self.undo)
        self.editor.bind("<Control-z>", self.undo)

        
if __name__ == "__main__":
    root = Tk()
    root.wm_state('zoomed')
    editor = Editor(root)
    editor.main()
    root.mainloop()
