import tkinter
import tkinter.ttk

window=tkinter.Tk()
window.title("progress")
window.geometry("640x400+100+100")
window.resizable(False, False)

progressbar=tkinter.ttk.Progressbar(window, maximum=100, mode="determinate")
#derterminate 채워짐, inerterminate 바 너비 만큼만 움직임
progressbar.pack()

progressbar.start(50)

window.mainloop()