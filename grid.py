import tkinter

window=tkinter.Tk()
window.title("grid")
window.geometry("640x400+100+100")
window.resizable(False, False)

b1=tkinter.Button(window, text="(0, 0)")
b2=tkinter.Button(window, text="(0, 1)", width=20)
b3=tkinter.Button(window, text="(0, 2)")

b4=tkinter.Button(window, text="(1, 0)")
b5=tkinter.Button(window, text="(1, 1)")
b6=tkinter.Button(window, text="(1, 3)")

b7=tkinter.Button(window, text="(2, 1)")
b8=tkinter.Button(window, text="(2, 2)")
b9=tkinter.Button(window, text="(2, 4)")

b1.grid(row=0, column=0, ipadx="100") #ipadx, ipady, 위젯에 대한 x,y방향 내부 패딩
b2.grid(row=0, column=1)
b3.grid(row=0, column=2, pady="10") # padx, pady, 위젯에 대한 x,y방향 외부 패빙 

b4.grid(row=1, column=0, rowspan=2) #rowspan 행위치 조정
b5.grid(row=1, column=1, columnspan=3) #columspan duf위치 조정
b6.grid(row=1, column=3)

b7.grid(row=2, column=1, sticky="nw") #sticky 할당된 공간내에 위치 조정
b8.grid(row=2, column=2)
b9.grid(row=2, column=99)

window.mainloop()