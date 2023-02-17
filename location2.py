import logging
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt #pip install -U matplotlib
import os

root=tkinter.Tk()
root.title("photo")
root.geometry("640x640+400+100") #00x00 사이즈 00+00 윈도우 뜰 창 위치
root.resizable(True, True)

def createNewWindow(): #버튼 누룰시 새로운 윈도우
    #global new
    #new= tkinter.Toplevel()
    new = tkinter.Toplevel(root)
    new.geometry("640x640+600+100")
    canvas = tkinter.Canvas(new, background="white") 
    canvas.pack() #canvas 위치
    images=tkinter.PhotoImage(file="images.png")
    canvas.create_image(150, 150, image=images)
    
buttonw = tkinter.Button(root, text="new window",command=createNewWindow)
buttonw.place(x=250, y=10)

def start():
  images=tkinter.PhotoImage(file="images.png")
  label=tkinter.Label(root, image=images, width=335,height=350, relief= "solid")
  label.place(x=str(x1_entry.get()), y=str(y1_entry.get())) #canvas 위치 
  #시작버튼 누르면 x,y값에 따라 사진 넣고 싶은데 모르겠음
  
def stop():
  canvas = tkinter.Canvas(root, width=300, height=300, background="white") #canvas 넓이
  canvas.place(x=340, y=0) #canvas 위치
  images=tkinter.PhotoImage(file="images.png")
  canvas.create_image(150, 150, image=images)

b1=tkinter.Button(root, text="start", command=start)
b2=tkinter.Button(root, text="stop", command=stop)
b1.place(x=200, y=10) 
b2.place(x=200, y=35)

def result(n):
    lab.config(text="x,y="+ x1_entry.get()+ ","+ y1_entry.get())
    
x1_label = tkinter.Label(root, text="x값")
x1_label.place(x=10, y=10)


x1_entry = tkinter.Entry(root)
x1_entry.place(x=10, y=35)

y1_label = tkinter.Label(root, text="y값")
y1_label.place(x=10, y=60)

y1_entry = tkinter.Entry(root)
y1_entry.place(x=10, y=85)
y1_entry.bind("<Return>", result)

lab=tkinter.Label(root, text="x , y값")
lab.place(x=10, y=110)

file_frame = tkinter.Frame(root) 
file_frame.place(x=0, y=140) #폴더선택 위치

def folder_select():

	dir_path = filedialog.askdirectory(initialdir="/",\
					title = "폴더를 선택 해 주세요")
	#folder 변수에 선택 폴더 경로 넣기

	if dir_path == '':
		messagebox.showwarning("경고", "폴더를 선택 하세요")    #폴더 선택 안했을 때 메세지 출력
	else:
		res = os.listdir(dir_path) # 폴더에 있는 파일 리스트 넣기


btn_active_dir = tkinter.Button(file_frame, text ="폴더 선택", width = 12, command=folder_select)
btn_active_dir.pack( padx = 5, pady= 5)

#https://rootiel.tistory.com/32
#https://flyingkiwi.tistory.com/27
#그래프 만들기
"""df = pd.read_csv("excel.csv")
df = df[["numEmps", "raisedAmt"]]

figure2= plt.Figure(figsize=(5,4))
plt.rcParams.update({'font.size': 22})
ax = df.set_index('numEmps')['craisedAmt'].plot(kind='line', marker='d')
ax.set_ylabel("raisedAmt")
ax.set_xlabel("numEmps")
plt.show()"""

#00~00줄 로그창 띠우고 싶은데 시도중#
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

root.mainloop()