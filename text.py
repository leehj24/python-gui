import tkinter

window=tkinter.Tk()
window.title("text")
window.geometry("640x400+100+100")
window.resizable(True, True)

text=tkinter.Text(window)

text.insert(tkinter.CURRENT, "안녕하세요.\n")#필드시작부분 
text.insert(tkinter.END, "???")#텍스트 마지막 문자위치 
text.insert("insert", "반습니다.\n")#삽입커서 위치
text.insert(2.1, "갑")

text.pack()

text.tag_add("강조", "1.0", "5.6")# 태그생성 
#tag_add(tagname, start_index, end_index)
text.tag_config("강조", background="yellow") #범위내에 속성설정
text.tag_remove("강조", "1.1", "1.2") #설정제거, tag_delete/태그삭제

window.mainloop()