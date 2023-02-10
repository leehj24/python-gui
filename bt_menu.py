import tkinter

window=tkinter.Tk()
window.title("YUN DAE HEE")
window.geometry("640x400+100+100")
window.resizable(False, False)

menubutton=tkinter.Menubutton(window,text="메뉴 메뉴 버튼", relief="raised", direction="right")
menubutton.pack()

hi=tkinter.Menu(menubutton, tearoff=0)
hi.add_command(label="하위메뉴-1")
hi.add_separator()
hi.add_command(label="하위메뉴-2")
hi.add_command(label="하위메뉴-3")

menubutton["menu"]=hi

window.mainloop()