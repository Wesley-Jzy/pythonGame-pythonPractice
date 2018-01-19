__author__ = 'wesley'
#-*- coding:utf-8 -*-
from Tkinter import*
from tkMessageBox import*
import Game
class GameStarter:
    def __init__(self):
        self.root = Tk()
        self.root.title('中二大乱斗!')
        self.root.geometry('600x400')
        self.enterInterface()
        self.root.mainloop()

    def enterInterface(self):
        #建立控件
        welcomeLabel = Label(self.root,text='欢迎来到中二大乱斗!',font=('Times', 30))
        newButton = Button(self.root,text='新建游戏',font=('Times',20))
        loadButton = Button(self.root,text='继续游戏',font=('Times',20))
        helpButton = Button(self.root,text='帮助',font=('Times',20))
        quitButton = Button(self.root,text='退出',font=('Times',20))
        #布局
        welcomeLabel.place(relx=0.5,rely=0.2,anchor='n')
        newButton.place(relx=0.5,rely=0.35,anchor='n')
        loadButton.place(relx=0.5,rely=0.5,anchor='n')
        helpButton.place(relx=0.5,rely=0.65,anchor='n')
        quitButton.place(relx=0.5,rely=0.8,anchor='n')
        #绑定函数
        newButton.bind('<Button-1>',self.New)
        loadButton.bind('<Button-1>',self.Load)
        helpButton.bind('<Button-1>',self.Help)
        quitButton.bind('<Button-1>',self.Quit)

    def New(self,event):
        if askokcancel('新建游戏','之前存档会丢失'):
            g = Game.MainGame(False)
            g.run()

    def Load(self,event):
        g = Game.MainGame('saveData.txt')
        g.run()

    def Help(self,event):
        self.helpWindow = Toplevel()
        self.helpWindow.geometry('400x300')
        self.helpWindow.title('帮助')
        t = Text(self.helpWindow,width=300,height=100,font=('Times',15))
        t.pack()
        f = open('help.txt','r')
        list_f = f.readlines()
        f.close()
        for i in range(len(list_f)):
            s = str(i+1)+'.'+'end'
            t.insert(s,list_f[i])

    def Quit(self,event):
        if askokcancel('退出','确认退出吗?'):
            self.root.destroy()
