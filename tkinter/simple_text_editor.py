# http://stackoverflow.com/questions/154245/editing-a-text-buffer
# http://www.catch22.net/tuts/neatpad/
# http://effbot.org/zone/vroom.htm
# http://www.rmi.net/~lutz/about-pp4e.html
import sys
import os
if (sys.version_info[:2] >= (3,0)):
    from tkinter import *
    from tkinter.ttk import *
    #from tkinter.simpledialog import askstring
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox
else:
    from Tkinter import *
    from ttk import *
    #from tkSimpleDialog import askstring
    import tkFileDialog
    import tkMessageBox     

###############################################################################
class TextDocument():
    def __init__(self, filename, maycreatenew=False):
        if maycreatenew or os.path.isfile(filename):
            self.filename = filename
        else:
            raise OSError("Cannot find file {}".format(filename))

    def fetch(self):
        fileh = open(self.filename, 'r')
        text = fileh.read() 
        fileh.close()
        return text

    def save(self, text):
        fileh = open(self.filename, 'w') # , encoding='UTF-8'
        fileh.write(text)
        fileh.close()


###############################################################################
class TextViewFrame(Frame):

    def __init__(self, parent=None, text='', editfile=None, cfg=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack(expand=YES, fill=BOTH)
        #self.modified = property(self.text.edit_modified, self.text.edit_modified)
        #self.modified = False
        self.editfile = editfile
        #self.editfile= StringVar()
        #self.editfile.trace("w", self.onEditfileChange)
        #self.master_title = self.winfo_toplevel().title()

        self.ftypes = [('All files',     '*'),                 # for file open dialog
              ('Text files',   '.txt'),               # customize in subclass
              ('Python files', '.py')]                # or set in each instance
        if cfg:
            self.cfg = cfg
        else:
            self.cfg = dict(borderwidth=0,
                font="{Lucida Sans Typewriter} 12",
                foreground="green",
                background="black",
                insertbackground="white", 
                selectforeground="green", 
                selectbackground="#008000",
                wrap=WORD, 
                width=64,
                undo=True)
        self.makeView()
        self.text.config(**self.cfg)
        if editfile:
            """self.document = TextDocument(editfile)
            self.text.insert('1.0', self.document.fetch())
            self.text.edit_modified(False)
            self.messageDispatch("Editing file {}".format(self.document.filename))"""
            self.onOpen(editfile=editfile)
        else:
            self.document = None
        self.text.focus_set()
        
        ##self.bind("<Control-y>", self.onRedo) 

    def makeView(self):
        vsbar = Scrollbar(self)
        self.text = Text(self, relief=SUNKEN, wrap=WORD)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)
        vsbar['command'] = self.text.yview
        self.text['yscrollcommand'] = vsbar.set
        vsbar.pack(side=RIGHT, fill=Y, before=self.text)   # , expand=YES

    

    def onNew(self, *evt):
        if self.text.edit_modified():
            self.messageDispatch("WARNING Buffer edited: Save or Discard first")
            return
        self.text.delete('1.0', END)
        self.text.edit_modified(False)
        self.text.edit_reset()
        self.editfile = ""
        #self.editfile.set("")

    def onOpen(self, event=None, editfile=None):
        if self.text.edit_modified():
            self.messageDispatch("WARNING Buffer edited: Save or Discard first")
            return
        if not editfile:
            editfile = tkFileDialog.askopenfilename(filetypes=self.ftypes)
        if editfile and os.path.isfile(editfile):
            self.document = TextDocument(editfile)
            self.text.insert('1.0', self.document.fetch())
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.messageDispatch("Editing file {}".format(self.document.filename))
        else:
            self.messageDispatch("WARNING Cannot open file {}".format(editfile))
            

    def onSave(self, *evt):
        if self.document:
            self.document.save( self.text.get('1.0', END) )  # END+'-1c'
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.messageDispatch("INFO Saving file {}".format(self.document.filename))
        else:
            self.onSaveAs()

    def onSaveAs(self):
        editfile = tkFileDialog.asksaveasfilename(filetypes=self.ftypes)
        if editfile:
            self.document = TextDocument(editfile, maycreatenew=True)
            self.onSave()
        else:
            self.messageDispatch("WARNING onSaveAs data not saved".format())

    def messageDispatch(self, message):
        self.parent.messageDispatch(message)

    """def onEditfileChange(self, *event):
        if self.editfile.get():
            new_title = "Editing : " + os.path.basename(self.editfile.get())
        else:
            new_title = self.master_title
        self.winfo_toplevel().title(new_title)"""
    
    #--------------------------------------------------------------------------
    def onUndo(self, event=None):
        try:
            self.text.edit_undo()
        except TclError:
            self.messageDispatch("INFO no edits to undo".format())

    def onRedo(self, event=None):
        try:
            self.text.edit_redo()
        except TclError:
            self.messageDispatch("INFO no edits to redo".format())

    def onCut(self, event=None):
        if not self.text.tag_ranges(SEL):
            self.messageDispatch("WARNING No text selected".format())
        else:
            self.onCopy()
            self.onDelete()

    def onCopy(self, event=None):
        if not self.text.tag_ranges(SEL):
            self.messageDispatch("No text selected".format())
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onPaste(self, event=None):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            self.messageDispatch("Nothing to paste".format())
            return
        self.text.insert(INSERT, text)
        self.text.tag_remove(SEL, '1.0', END)
        self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.text.see(INSERT)                  

    def onDelete(self, event=None):
        if not self.text.tag_ranges(SEL):
            self.messageDispatch("No text selected".format())
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    #--------------------------------------------------------------------------

###############################################################################
mymenuList = [ 
        ( "cascade", { "label":"File", "underline":0},
            [ ( "command", { "label":"New", "underline":0, "accelerator":"Ctrl-n"}, "self.textFr.onNew" ),
              ( "command", { "label":"Open", "underline":0, "accelerator":"Ctrl-o"}, "self.textFr.onOpen" ),
              ( "command", { "label":"Save", "underline":0, "accelerator":"Ctrl-s"}, "self.textFr.onSave" ),
              ( "command", { "label":"Save as...", "underline":1}, "self.textFr.onSaveAs" ),
              ("separator", {}, None),
              ( "command", { "label":"Quit", "underline":0, "accelerator":"Ctrl-q"}, "self.onQuit") 
            ]
        ),
        ( "cascade", { "label":"Edit", "underline":0},
            [ ( "command", { "label":"Undo", "underline":0, "accelerator":"Ctrl-z"}, "self.textFr.onUndo" ),
              ( "command", { "label":"Redo", "underline":0, "accelerator":"Ctrl-y"}, "self.textFr.onRedo" ),
              ("separator", {}, None),
              ( "command", { "label":"Cut", "underline":2, "accelerator":"Ctrl-x"}, "self.textFr.onCut" ),
              ( "command", { "label":"Copy", "underline":0, "accelerator":"Ctrl-c"}, "self.textFr.onCopy" ),
              ( "command", { "label":"Paste", "underline":0, "accelerator":"Ctrl-v"}, "self.textFr.onPaste" ),
              ("separator", {}, None),
              ( "cascade", { "label":"TestSubMenu", "underline":6},
                   [ ( "command", { "label":"SubMenuNew"}, "lambda: 0" ),
                     ( "command", { "label":"SubMenuExit", "underline":8}, "lambda: 0" ) 
                   ] 
              ),
              ("separator", {}, None),
              ("command", { "label":"Paste again",  "accelerator":"Ctrl+V"}, "lambda: 0") 
            ] 
        ),
        ( "cascade", { "label":"View", "underline":0},
            [ ( "command", { "label":"Hide/Show:", "state":"disabled"}, "lambda: 0" ),
              ("separator", {}, None),
              ( "command", { "label":"Menu",  "accelerator":"Ctrl-Shift-m"}, "self.toggleMenu" ),
              ( "command", { "label":"Statusbar",  "accelerator":"Ctrl-Shift-s"}, "self.toggleStatusbar" )
              
            ] 
        )
        ]

mymenuList2 = [ 
        ( "cascade", { "label":"File", "underline":0},
            [ ( "command", {"label":"New", "underline":0, "accelerator":"Ctrl-n"}, "self.textFr.onNew" ),
              ("separator", {}, None),
              ( "command", {"label":"Open", "underline":0, "accelerator":"Ctrl-o"}, "self.textFr.onOpen" ),
            ]
        )
        ]
###############################################################################
class StatusBarFrame(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(fill=X)   # expand=YES, 
        self.sizegrip = Sizegrip(self)
        self.sizegrip.pack(side=RIGHT, anchor=E)
        self.messagetext = StringVar()   # will vanish when variable goes out of scope, so make it an instance attribute
        self.message = Label(self, relief=SUNKEN, textvariable=self.messagetext, anchor=W)  # 
        self.message.pack(fill=X, side=LEFT, expand=YES)   # , expand=YES
        self.messagetext.set('Starting basic text editor....')
        
    def clear(self):
        self.messagetext.set('')
        

    """def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()"""
################################################################################


class TheApp(Frame):
  
    def __init__(self, master, name, editfile=None):
        Frame.__init__(self, master, name=name)
        self.pack(fill=BOTH, expand=YES)
        self.master.title("The App")
        self.mymenuList = mymenuList
        self.statusbar = None

        #self.statusbar = StatusBarFrame(master)
        self.textFr = TextViewFrame(self, editfile=editfile)

        # deferring packing to avoid _tkinter.TclError: can't pack .app.3071179276 inside .
        self.textFr.pack(fill=BOTH, expand=YES)
        #self.statusbar.pack(side=BOTTOM, fill=X, before=self.textFr)
        self.toggleStatusbar()




        self.toggleMenu()

        
        self.bind_all("<Control-q>", self.onQuit)
        self.bind_all("<Control-M>", self.toggleMenu)
        self.bind_all("<Control-S>", self.toggleStatusbar)
        self.bind_all("<Control-n>", self.textFr.onNew)
        self.bind_all("<Control-o>", self.textFr.onOpen)
        self.bind_all("<Control-s>", self.textFr.onSave)
        # undo and redo have built-in keyboard bindings, changing them is not easy
        # two ways to map Ctrl-y to undo: bind_class, or delete interferring virtual event
        #self.master.bind_class("Text","<Control-y>", self.textFr.onRedo)
        self.bind_all("<Control-y>", self.textFr.onRedo)
        self.master.event_delete("<<Paste>>")  # also need to kill built-in virtual event bound to Ctrl-y
        # need to suppress <<Redo>> virtual event on Windows due to Ctrl-y binding, otherwise get double redos
        if sys.platform=="win32":
            self.master.event_delete("<<Redo>>")
        self.bind_all("<Control-x>", self.textFr.onCut)
        self.bind_all("<Control-p>", self.textFr.onCopy)
        self.bind_all("<Control-v>", self.textFr.onPaste)


    def toggleMenu(self, *evt):
        if hasattr(self, "menubar"):
            self.menubar.destroy()
            del self.menubar
            self.messageDispatch("To restore the menubar press Ctrl-Shift-m".format())
        else:
            self.menubar = Menu(self, name="menubar")
            self.list2menu(self.mymenuList, menutop=self.menubar)
            self.master.config(menu=self.menubar)

    def toggleStatusbar(self, *evt):
        if getattr(self, "statusbar"):
            self.statusbar.destroy()
            self.statusbar = None
        else:
            self.statusbar = StatusBarFrame(self.master)
            self.statusbar.pack(side=BOTTOM, fill=X, before=self.textFr)

    def onQuit(self, *evt):
        if self.textFr.text.edit_modified():
            proceed = tkMessageBox.askokcancel("WARNING!", "Document not " + 
            "saved.\nDo you want to quit without saving?", 
            icon=tkMessageBox.WARNING, default=tkMessageBox.CANCEL)
        else:
            proceed = True
        if proceed:
            self.quit()

    def messageDispatch(self, message):
        if self.statusbar:
            self.statusbar.messagetext.set(message)
            self.master.after(5000, self.statusbar.clear)
        print(message)
   
    def list2menu(self, menuList, menutop, menu=None):
        """Recursive function that generates a menu from a list of tuples"""
        for mitem in menuList:
            if mitem[0]=="cascade":
                menupage = Menu(menutop, tearoff=FALSE, name=mitem[1]["label"].lower() )
                menutop.add("cascade", mitem[1], menu=menupage)
                self.list2menu(mitem[-1], menutop=menupage, menu=menupage)
            else:
                menu.add( mitem[0], mitem[1], 
                         command=( mitem[-1] and eval(mitem[-1]) ))



def main():
    root = Tk()
    #print("System: ", root.tk.call('tk', 'windowingsystem') )
    style = Style()
    style.theme_use('clam')
    app = TheApp(root, name="app", 
                 editfile=sys.argv[1] if len(sys.argv) > 1 else None)
    app.mainloop()     


if __name__ == "__main__":
    main()
