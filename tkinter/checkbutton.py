import tkinter

window=tkinter.Tk()
window.title("checkbutton")
window.geometry("640x480+100+100")
window.resizable(False, False)

def flash():
    checkbutton1.flash()

CheckVariety_1=tkinter.IntVar()
CheckVariety_2=tkinter.IntVar()
CheckVariety_3=tkinter.IntVar()

checkbutton1=tkinter.Checkbutton(window, text="O", variable=CheckVariety_1, activebackground="blue")
checkbutton2=tkinter.Checkbutton(window, text="△", variable=CheckVariety_2)
checkbutton3=tkinter.Checkbutton(window, text="X", variable=CheckVariety_3, command=flash) 
# select()-체크상태, deselect()해제상태, toggle()체크일경우 해제/해제일경우 체크, 
# invoke()클릭했을때와 동일한 샐행, flash()배경색상과 깜박임

checkbutton1.pack()
checkbutton2.pack()
checkbutton3.pack()

window.mainloop()