import tkinter
import tkinter.font

window=tkinter.Tk()
window.title("front")
window.geometry("640x400+100+100")
window.resizable(True, True)

font=tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", overstrike="True")
#family 글꼴, slant 기울림 weight 진하게 unerline 밑줄, overstrike취소선
label=tkinter.Label(window, text="파이썬 3.6", font=font)
label.pack()

window.mainloop()