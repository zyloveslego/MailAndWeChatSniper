from tkinter import *

"""
两个list栏，读取所有的群聊，分别为转发群和被转发群，复选框；确定按钮；转发文字设置
"""

class Application(Frame):

    def __init__(self, master=None, listenerGroups=None, forwardGroups=None):

        self.listenerGroups = listenerGroups
        self.forwardGroups = forwardGroups

        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def createWidgets(self):
        self.enterLabel = Button(self, text='确认', command=self.getSelection)
        self.enterLabel.pack()

        self.quitButton = Button(self, text='退出', command=self.quit)
        self.quitButton.pack()

        self.listenerScroll = Scrollbar()
        self.listenerScroll.pack(side=LEFT, fill=Y)
        self.listenerLb = Listbox(selectmode=MULTIPLE, yscrollcommand=self.listenerScroll.set, exportselection=FALSE)
        self.listenerLb.pack(side='left')
        self.listenerScroll.config(command=self.listenerLb.yview)

        for item in self.listenerGroups:  # 添加监听群数据
            self.listenerLb.insert('end', item)


        self.forwardScroll = Scrollbar()
        self.forwardScroll.pack(side=RIGHT, fill=Y)
        self.forwardLb = Listbox(selectmode=MULTIPLE, yscrollcommand=self.forwardScroll.set, exportselection=FALSE)
        self.forwardLb.pack(side='right')
        self.forwardScroll.config(command=self.forwardLb.yview)

        for item in self.forwardGroups:  # 添加监听群数据
            self.forwardLb.insert('end', item)


    def getSelection(self):
        # TODO: 监听群不能为空，转发可以，默认转发到文件传输助手
        self.listenerList = self.listenerLb.curselection()
        print("监听群")
        for i, id in enumerate(self.listenerList):
            print(self.listenerLb.get(id))

        self.forwardList = self.forwardLb.curselection()
        print("转发群")
        for i, id in enumerate(self.forwardList):
            print(self.forwardLb.get(id))



if __name__ == '__main__':
    root = Tk()
    root.geometry("400x300+500+200")
    root.resizable(0, 0)

    listenerGroups = [1, 2, 3]
    forwardGroups = [4, 5, 6]

    app = Application(root, listenerGroups, forwardGroups)
    app.master.title('微信群转发设置')
    app.mainloop()