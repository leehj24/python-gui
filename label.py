import tkinter

window=tkinter.Tk()
window.title("연습문제")
window.geometry("640x400+100+100")
window.resizable(False, False)

label=tkinter.Label(window, text="파이썬", width=10, height=5, fg="red", relief="solid") #테두리 
label.pack()

window.mainloop()