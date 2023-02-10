import tkinter

window=tkinter.Tk()
window.title("massage")
window.geometry("640x400+100+100")
window.resizable(False, False)

message=tkinter.Message(window, text="메세지입니다.", width=100, relief="solid", bg="red")
message.pack()

window.mainloop()