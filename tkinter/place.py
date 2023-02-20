import tkinter

window=tkinter.Tk()
window.title("place")
window.geometry("640x600+100+100")
window.resizable(False, False)

b1=tkinter.Button(window, text="(50, 50)")
b2=tkinter.Button(window, text="(50, 100)")
b3=tkinter.Button(window, text="(100, 150)")
b4=tkinter.Button(window, text="(0, 200)")
b5=tkinter.Button(window, text="(0, 300)")
b6=tkinter.Button(window, text="(0, 300)")
b7=tkinter.Button(window, text="(0, 250)")
b8=tkinter.Button(window, text="(0, 150)")

b1.place(x=50, y=50) 
b2.place(x=50, y=100, width=50, height=50)
b3.place(x=100, y=150, bordermode="inside")
#bordermode - INSIDE (기본값) 다른 옵션이 부모의 내부를 참조한다는 것을 나타냅니다 
# (부모의 테두리를 무시); 그렇지 않으면 외부
b4.place(x=0, y=200, relwidth=0.5) #relwidth, relheight 위젯 너비, 높이 비율
b5.place(x=0, y=300, relx=0.5) #relx,rely 좌표 배치 비율
b6.place(x=0, y=300, relx=0.5, anchor="s")

b7.place(x=0, y=250, relheight=0.5)
b8.place(x=0, y=150)

window.mainloop()