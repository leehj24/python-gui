from tkinter import *
import datetime
 
class GUIT():
    def __init__(self):
        self.tkhandler = Tk()
        self.tkhandler.geometry('800x760')
        self.tkhandler.title('자동화프로그램')
 
 
 
        ###################공간띄우기##########################
        self.label_title = Label(self.tkhandler, text='')
        self.label_title.grid(row=0, column=0, sticky="w")
        ######################################################
 
        # 텍스트박스에 스크롤 연결
        self.scroll = Scrollbar(self.tkhandler, orient='vertical')
        self.lbox = Listbox(self.tkhandler, yscrollcommand=self.scroll.set, width=116)
        self.scroll.config(command=self.lbox.yview)
        self.lbox.grid(row=0, column=0, columnspan=5, sticky="s")
 
        # 1 시작시 보이는 메세지 'append_log'
        self.append_log('프로그램을 시작했습니다.')
 
    def append_log(self, msg):
        global now
        self.now = str(datetime.datetime.now())[0:-7]
        self.lbox.insert(END, "[{}] {}".format(self.now, msg))
        self.lbox.update()
        self.lbox.see(END)
 
    def run(self):
        self.tkhandler.mainloop()
 
 
g = GUIT()
g.run()