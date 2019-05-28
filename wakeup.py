import pandas as pd
import tkinter as tk
import time

__version__ = "v0.0.1"


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack()
        self.frame3 = tk.Frame(self.root)
        self.frame3.pack()

        try:
            self.df = pd.read_csv("log.csv", encoding="gbk")
        except Exception as e:
            self.df = pd.DataFrame([], columns=["date", "event", "category", "status"])

        self.affairs = ["起床", "睡觉", "科研", "读书", "吃饭", "锻炼", "游戏"]
        self.s = tk.StringVar()
        self.s.set("起床")
        for affair in self.affairs:
            self.r = tk.Radiobutton(self.frame3, text=affair, variable=self.s, value=affair, indicatoron=False)
            self.r.configure(width=25)
            self.r.pack()

        self.l1 = tk.Label(self.frame, text="事项描述：")
        self.l1.grid(row=0, column=0, padx=10, pady=10)

        self.e = tk.Entry(self.frame)
        self.e.grid(row=0, column=2, padx=10, pady=10)

        self.bt = tk.Button(self.frame, text="开始", command=lambda: self.write_csv(0))
        self.bt.grid(row=1, column=1, padx=10, pady=5)

        self.bt1 = tk.Button(self.frame, text="结束", command=lambda: self.write_csv(1))
        self.bt1.grid(row=1, column=2, padx=10, pady=5)

        self.s2 = tk.StringVar()
        self.s2.set("")
        self.l2 = tk.Label(self.frame2, textvariable=self.s2)
        self.l2.grid(row=2, column=1)

        self.s3 = tk.StringVar()
        self.l3 = tk.Label(self.frame2, textvariable=self.s3)
        self.loop = True
        self.starttime = 0
        self.root.mainloop()

    def check_time(self):
        if not self.loop:
            return
        self.s3.set(time.strftime("%H:%M:%S", time.gmtime(time.time()-self.starttime)))
        self.l3.grid(row=3, column=1, padx=5, pady=5)
        self.root.after(1000,self.check_time)
        return

    def write_csv(self, status):
        event = self.e.get()
        cat = self.s.get()
        date = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        self.df = self.df.append(pd.DataFrame([[date, event, cat, status]], columns=["date", "event", "category", "status"]))
        self.df.to_csv("log.csv", index=False, encoding="gbk")
        self.s2.set("录入成功！")
        if status == 0:
            self.loop = True
            self.bt.configure(bg="grey")
            self.bt1.configure(bg="#f0f0f0")
            self.starttime = time.time()
            self.check_time()
        else:
            self.bt1.configure(bg="grey")
            self.bt.configure(bg="#f0f0f0")
            self.loop = False
            self.l3.grid_forget()

        self.root.after(2000, lambda: self.s2.set(""))


if __name__ == "__main__":
    app = App()
