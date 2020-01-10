"""
https://github.com/dmnfarrell/tkintertable
"""
from tkinter import *
from tkinter import ttk
from tkintertable.Tables import TableCanvas


class myCanvasFrame(ttk.Frame):   # ttk.Frame
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        table = TableCanvas(self)
        table.createTableFrame()


class MainApp(object):
    def __init__(self, master, title=None, add_Sizegrip=True):
        #frame = ttk.Frame(master)
        #self.master = master
        
        self.height = 500
        self.width = 700
        master.geometry('%dx%d+300+300' % (self.width, self.height))
        ##self.master.minsize(width, height)
        master.title(title)

        # add Panedwindow
        self.PW = ttk.Panedwindow(master, orient=HORIZONTAL)
        self.PW.f1 = ttk.Frame(self.PW, borderwidth=1, relief="sunken",
                     width=150)
        self.PW.f2 = ttk.Frame(self.PW); # second pane    
        self.PW.add(self.PW.f1)
        self.PW.add(self.PW.f2)
        self.PW.grid(column=0, row=0, sticky=(N,W,E,S))
        
        # add Notebook
        self.NB = ttk.Notebook(self.PW.f2)
        self.NB.add(myCanvasFrame(self.NB), text='Sheet_1')
        self.NB.add(myCanvasFrame(self.NB), text='Sheet_2')
        self.NB.add(myCanvasFrame(self.NB), text='Sheet_3')
        self.NB.add(myCanvasFrame(self.NB), text='Sheet_4')
        self.NB.add(myCanvasFrame(self.NB), text='Sheet_5')
        ##self.NB.add(ttk.Frame(self.NB), text='Sheet_2')
        self.NB.grid(column=0, row=0, sticky=(N,W,E,S))
        self.NB.master.grid_columnconfigure(0, weight=1)
        self.NB.master.grid_rowconfigure(0, weight=1)
        
        # add Treeview
        self.TV = ttk.Treeview(self.PW.f1)
        self.TV.insert('', 'end', 'BLC', text='Base cases')
        self.TV.grid(column=0, row=0, sticky='nsew')
        self.TV.master.grid_columnconfigure(0, weight=1)
        self.TV.master.grid_rowconfigure(0, weight=1)
        self.TVleafref = 0
        
        # tree pop-up
        self.treePopupMenu(self.TV)
                
        if add_Sizegrip:
            ttk.Sizegrip(master).grid(column=0, row=1, sticky=(S,E))

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        #print master.children

    def treePopupMenu(self, parent):
        self.TPM = Menu(parent, tearoff=0)
        self.TPM.add_command(label="Add leaf", command=self.onAddLeaf)
        self.TPM.add_command(label="Exit", command=self.onExit)
        parent.bind("<Button-3>", self.showTreePopupMenu)
        
    def showTreePopupMenu(self, evt):
        self.TPM.post(evt.x_root, evt.y_root)
        #print evt, evt.widget
        #print dir(evt.widget)

    def onAddLeaf(self):
        item = self.TV.selection()[0]
        self.TV.insert(item, 'end', 'LC_'+str(self.TVleafref), 
          text='Load case '+str(self.TVleafref))
        self.TVleafref += 1
        #self.NB.add(ttk.Frame(self.NB), text='dummy name')       

    def onAddSheet(self):
        self.NB.add(ttk.Frame(self.NB), text='dummy name')    

    def onExit(self):
        self.quit()  # self needs to be a frame

def main():
    root = Tk()
    style = ttk.Style()
    app = MainApp(root, 'Test Application')
    root.mainloop()

if __name__ == "__main__":
    main()
