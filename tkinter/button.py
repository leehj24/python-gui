import tkinter

window=tkinter.Tk()
window.title("연습문제")
window.geometry("640x400+100+100")
window.resizable(False, False)

count=0

def countUP():
    global count
    count +=1
    label.config(text=str(count))

label = tkinter.Label(window, text="0")
label.pack()

button = tkinter.Button(window, overrelief="solid", width=15, command=countUP, repeatdelay=1000, repeatinterval=100)
button.pack()
#overrelief-버튼올렸을때 현상/ soild-검정테두리, 
# flat-사라짐, groove-들어가지는 느낌/살짝 회색, raised, 눌렀을때 들어감, ridge-들어가지는 느낌/흰색
window.mainloop()