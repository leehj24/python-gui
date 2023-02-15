import tkinter as tk
from tkinter import ttk

# https://blog.naver.com/heennavi1004/222027822125

class MyWidgets(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.count =0

        self.widget = tk.LabelFrame(self, text ="Label Frame")
        self.notebook = ttk.Notebook(self.widget, width=200, height=300)
        self.notebook.pack()

        self.frame1= tk.Frame(self.notebook)
        self.notebook.add(self.frame1, text="페이지 1")

        self.label1 =tk.Label(self.frame1, text="레이블 1")
        self.label1.pack()

        self.frame2= tk.Frame(self.notebook)
        self.notebook.add(self.frame2, text="페이지 2")

        self.label2 =tk.Label(self.frame2, text="레이블 2")
        self.label2.pack()

        self.frame3= tk.Frame(self.notebook)
        self.notebook.add(self.frame3, text="페이지 3")

        self.label3 =tk.Label(self.frame3, text="레이블 3")
        self.label3.pack()

        self.button1 = tk.Button(self.widget, text="add Page", command=self.add_cmd)
        self.button1.pack()
        self.button2 = tk.Button(self.widget, text="insert Page", command=self.ins_cmd)
        self.button2.pack()
        self.button3 = tk.Button(self.widget, text="delete Page", command=self.del_cmd)
        self.button3.pack()
        self.button4 = tk.Button(self.widget, text="hide Page", command=self.hide_cmd)
        self.button4.pack()
        self.button4 = tk.Button(self.widget, text="restore Page", command=self.restore_cmd)
        self.button4.pack()
        
        self.widget.grid(row=0, column=1, sticky=(tk.W + tk.E))
        

    def add_cmd(self):
        self.frame_a = tk.Frame(self)
        self.label_a = tk.Label(self.frame_a, text="added label")
        self.label_a.pack()
        self.notebook.add(self.frame_a, text="frame added")

    def ins_cmd(self):
        self.frame_i = tk.Frame(self)
        self.label_i = tk.Label(self.frame_i, text="inserted label")
        self.label_i.pack()
        self.notebook.insert( 1, self.frame_i,text="frame inserted")

    def del_cmd(self):
        self.notebook.forget(1)
        
    def hide_cmd(self): #감추기
        self.notebook.hide(1)
        
        
    def restore_cmd(self):#감춘탭 다시 회복 
        self.notebook.add(self.frame2)
        
    def index_cmd(self):
        idx = self.notebook.index(self.frame2)
        print(idx)

class MainApp(tk.Tk):
    """Application root window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hello World!")
        self.resizable(width=True, height=True)

        self.widgetform = MyWidgets(self)
        self.widgetform.grid(row=3, padx=10, sticky=(tk.W + tk.E))

        self.geometry("640x480+200+200")
        

    
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()