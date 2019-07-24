from tkinter import *
import tkinter.messagebox

"""
两个list栏，读取所有的群聊，分别为转发群和被转发群，复选框；确定按钮；转发文字设置
"""

class Application(Frame):

    def __init__(self, master=None, groups=None):

        self.groups = groups

        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def createWidgets(self):
        self.enterButton = Button(self, text='确认', command=self.getSelection)
        self.enterButton.pack()

        self.quitButton = Button(self, text='退出', command=self.quit)
        self.quitButton.pack()

        self.megLabel = Label(self, text='')
        self.megLabel.pack()

        self.listenerLabel = Label(self, text='监听群')
        self.listenerLabel.pack(side='left')
        self.listenerScroll = Scrollbar()
        self.listenerScroll.pack(side=LEFT, fill=Y)
        self.listenerLb = Listbox(selectmode=MULTIPLE, yscrollcommand=self.listenerScroll.set, exportselection=FALSE)
        self.listenerLb.pack(side='left')
        self.listenerScroll.config(command=self.listenerLb.yview)

        for item in self.groups:  # 添加监听群数据
            self.listenerLb.insert('end', item)

        self.forwardLabel = Label(self, text='转发群')
        self.forwardLabel.pack(side='right')
        self.forwardScroll = Scrollbar()
        self.forwardScroll.pack(side=RIGHT, fill=Y)
        self.forwardLb = Listbox(selectmode=MULTIPLE, yscrollcommand=self.forwardScroll.set, exportselection=FALSE)
        self.forwardLb.pack(side='right')
        self.forwardScroll.config(command=self.forwardLb.yview)

        for item in self.groups:  # 添加监听群数据
            self.forwardLb.insert('end', item)


    def getSelection(self):
        # 监听群不能为空，转发可以，默认转发到文件传输助手
        listenerGroups = []
        forwardGroups = []


        self.listenerList = self.listenerLb.curselection()
        print("监听群")
        for i, id in enumerate(self.listenerList):
            print(self.listenerLb.get(id))
            listenerGroups.append(self.listenerLb.get(id))

        self.forwardList = self.forwardLb.curselection()
        print("转发群")
        for i, id in enumerate(self.forwardList):
            print(self.forwardLb.get(id))
            forwardGroups.append(self.forwardLb.get(id))


        if listenerGroups == []:
            tkinter.messagebox.showwarning(title='Error', message='请选择需要监听的群')
        else:
            self.megLabel.config(text='正在监听...')





if __name__ == '__main__':
    root = Tk()
    # 设置窗口大小，不可改变
    root.geometry("400x300+500+200")
    root.resizable(0, 0)

    # 监听和转发群，通过微信取
    groups = ['微信群1', '微信群2', '微信群3']

    # 主窗口
    app = Application(root, groups)
    app.master.title('微信群转发设置')
    app.mainloop()