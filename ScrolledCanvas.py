from tkinter import * 

class ScrolledCanvas(Frame):
    def __init__(self, parent=None, color='brown'):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)                  
        canv = Canvas(self, relief=SUNKEN)
        canv.config(width=850, height=650)                
        canv.config(scrollregion=(0,0,300, 2500))         
        canv.config(highlightthickness=0)                 

        sbar = Scrollbar(self)
        sbar.config(command=canv.yview)                   
        canv.config(yscrollcommand=sbar.set)              
        sbar.pack(side=RIGHT, fill=Y)                     
        canv.pack(side=LEFT, expand=YES, fill=BOTH)       
        canv.bind('<Double-1>', self.onDoubleClick)       # set event handler
        self.canvas = canv
        self.canvas.create_text(50,50,text="test",fill='red')

    def onDoubleClick(self, event):                  
        print(event.x, event.y)
        print(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def delete(self):
        self.canvas.delete(ALL)




if __name__ == '__main__': ScrolledCanvas().mainloop()