from tkinter import *
from tkinter import ttk


class Board(Canvas):

    def __init__(self, parent):
        Canvas.__init__(self, background="black", highlightthickness=0)         
        self.parent = parent 
        #self.initGame()
        self.pack()
        self.focus_get()


class myCanvasFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        #self.canvas = Canvas(parent, bg="white")
        #self.canvas.pack(side=BOTTOM, fill=BOTH,expand=1)
                
        #parent.title('Nibbles')
        #self.board = Board(self)
        #self.pack()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        canvas = Canvas(self, bg="yellow", bd=10)
        nrows = 1000
        ncols = 50
        wid = 80
        hei = 20
        
        ys = 0
        for ii in range(nrows):
            xs = 0
            for jj in range(ncols):
                canvas.create_rectangle(xs, ys, xs+wid, ys+hei, 
                outline="#fb0", fill="#fff")
                xs = xs + wid
            ys = ys + hei
            
        '''canvas.create_rectangle(30, 10, 120, 80, 
            outline="#fb0", fill="#fb0")
        canvas.create_rectangle(150, 10, 240, 80, 
            outline="#f50", fill="#f50")
        canvas.create_rectangle(270, 10, 370, 80, 
            outline="#05f", fill="#05f")'''            
        #canvas.pack(fill=BOTH, expand=1)
        canvas.grid(sticky=(N,W,E,S))   # column=0, row=0, 
        #canvas.grid_columnconfigure(0, weight=1)
        #canvas.grid_rowconfigure(0, weight=1)
        #self.grid(sticky=(N,W,E,S))

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
        #self.NB.add(ttk.Frame(self.NB), text='Sheet_2')
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
        
        print(master.children)

    def treePopupMenu(self, parent):
        self.TPM = Menu(parent, tearoff=0)
        self.TPM.add_command(label="Add leaf", command=self.onAddLeaf)
        self.TPM.add_command(label="Exit", command=self.onExit)
        parent.bind("<Button-3>", self.showTreePopupMenu)
        
    def showTreePopupMenu(self, evt):
        self.TPM.post(evt.x_root, evt.y_root)
        print(evt, evt.widget)
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
