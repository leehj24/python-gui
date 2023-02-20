import tkinter

window=tkinter.Tk()
window.title("frame")
window.geometry("640x400+100+100")
window.resizable(False, False)

frame1=tkinter.Frame(window, relief="solid", bd=2)
frame1.pack(side="left", fill="x",expand=True)
#fill=x 창의 너비, fill=y 창의 높이, fill=both 창 모두채우기

frame2=tkinter.Frame(window, relief="solid", bd=5)
frame2.pack(side="right", fill="both", expand=False)
#expand = 요구되지 않은공간 사용하기

frame3=tkinter.Frame(window, relief="solid", bd=1)
frame3.pack(side="right", fill="y", expand=False)
#expand = 요구되지 않은공간 사용하기

button1=tkinter.Button(frame1, text="프레임1")
button1.pack(side="right")

button2=tkinter.Button(frame2, text="프레임2")
button2.pack(side="top")

button3=tkinter.Button(frame3, text="프레임3")
button3.pack(side="left")

window.mainloop()