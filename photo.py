import tkinter

window=tkinter.Tk()
window.title("photo")
window.geometry("640x400+100+600") #00x00 사이즈 00+00 윈도우 뜰 창 위치
window.resizable(True, True)

image=tkinter.PhotoImage(file="a.png")

label=tkinter.Label(window, image=image)
label.pack()

window.mainloop()