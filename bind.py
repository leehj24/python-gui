import tkinter

window=tkinter.Tk()
window.title("bind")
window.geometry("640x400+100+100")
window.resizable(True, True)

width=1

def drawing(event):
    if width>0:
        x1=event.x-1
        y1=event.y-1
        x2=event.x+1
        y2=event.y+1
        canvas.create_oval(x1, y1, x2, y2, fill="blue", width=width ,outline="yellow")

def scroll(event):
    global width
    if event.delta==120:
        width+=1
    if event.delta==-120:
        width-=1
    label.config(text=str(width))

canvas=tkinter.Canvas(window, relief="solid", bd=2)
canvas.pack(expand=True, fill="both")
canvas.bind("<Motion>", drawing) #Motion 마우스가 움직일때
#b1-motion 왼쪽 버튼 누리면서 움직일때
#b2-motion 휠누르면서 움직일때 
#b3-motion 오른쪽 버튼 누리면서 움직일때
canvas.bind("<MouseWheel>", scroll)
#button-1 왼쪽 button-2휠 button-3 오른쪽 누를때
#button-4 스크롤 업, button-5 스크롤 다운, mousewhell 휠이동
label=tkinter.Label(window, text=str(width))
label.pack()

window.mainloop()