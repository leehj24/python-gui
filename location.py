import logging
import tkinter
import threading

window=tkinter.Tk()
window.title("photo")
window.geometry("640x640+300+100") #00x00 사이즈 00+00 윈도우 뜰 창 위치
window.resizable(True, True)

canvas = tkinter.Canvas(window, width=300, height=300, background="white") #canvas 넓이
canvas.place(x=340, y=0) #canvas 위치
image=tkinter.PhotoImage(file="images.png")
canvas.create_image(150, 150, image=image) #canvas에 있는 사진 위치

b1=tkinter.Button(window, text="start")
b2=tkinter.Button(window, text="stop")
b1.place(x=200, y=10) 
b2.place(x=200, y=35)

def result(n):
    lab.config(text="x,y="+ str(eval(x1_entry.get()))+ ","+ str(eval(y1_entry.get())))
    
x1_label = tkinter.Label(window, text="x값")
x1_label.place(x=10, y=10)


x1_entry = tkinter.Entry(window)
x1_entry.place(x=10, y=35)

y1_label = tkinter.Label(window, text="y값")
y1_label.place(x=10, y=60)

y1_entry = tkinter.Entry(window)
y1_entry.place(x=10, y=85)
y1_entry.bind("<Return>", result)

lab=tkinter.Label(window, text="x , y값")
lab.place(x=10, y=110)

class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tkinter.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tkinter.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


# Sample usage
if __name__ == '__main__':
    # Create the GUI
    root = tkinter.Tk()
    
    from tkinter import scrolledtext
    st = scrolledtext.ScrolledText(root, state='disabled')
    st.configure(font='TkFixedFont')
    st.pack()

    # Create textLogger
    text_handler = TextHandler(st)

    # Add the handler to logger
    logger = logging.getLogger()
    logger.addHandler(text_handler)

    # Log some messages
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

window.mainloop()