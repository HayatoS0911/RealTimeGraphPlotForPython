import math
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from collections import deque
import random
import numpy as np

kAxisLength = 100

counter = 0;
ouputCounter = 0;

class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.running = False
        self.ani = None

        mainFrame = tk.Frame(self,width = 610,height = 400,bg = "lightcyan",relief = tk.FLAT)
        mainFrame.pack()

        settingFrame = tk.LabelFrame(mainFrame,text = "設定",width = 290,height = 100,bg="white")
        settingFrame.place(x = 5,y = 5)

        lbl = tk.Label(settingFrame, font=("Arial", 12),text="描画点数:",bg = "white")
        lbl.place(x = 5,y = 5)

        self.points_ent = tk.Entry(settingFrame, width = 5,font=("Arial", 12))
        self.points_ent.insert(0, '500')
        self.points_ent.place(x = 130,y = 5)

        lbl = tk.Label(settingFrame, font=("Arial", 12), text="送信間隔(ms):",bg = "white")
        lbl.place(x = 5,y = 40)
        self.interval = tk.Entry(settingFrame, font=("Arial", 12),width = 5)
        self.interval.insert(0, '30')
        self.interval.place(x = 130,y = 40)

        self.btn = tk.Button(settingFrame,font=("Arial", 16), text='開始', command=self.on_click)
        self.btn.place(x = 200,y = 10)
        outputFrame = tk.LabelFrame(mainFrame,text = "出力",width = 290,height = 100,bg="white")
        outputFrame.place(x = 300,y = 5)

        lbl = tk.Label(outputFrame, font=("Arial", 12),text="出力点数:",bg = "white")
        lbl.place(x = 5,y = 5)
        self.outPoints_ent = tk.Entry(outputFrame, width = 5,font=("Arial", 12))
        self.outPoints_ent.insert(0, '0')
        self.outPoints_ent.place(x = 130,y = 5)

        lbl = tk.Label(outputFrame, font=("Arial", 12), text="出力値:",bg = "white")
        lbl.place(x = 5,y = 40)
        self.outputValueEnt = tk.Entry(outputFrame, font=("Arial", 12),width = 12)
        self.outputValueEnt.insert(0, '')
        self.outputValueEnt.place(x = 130,y = 40)

        graphFrame = tk.Frame(mainFrame,bg = "white")
        graphFrame.place(x = 5,y = 110)

        self.figure = plt.Figure(figsize  = (6, 3))
        self.figureGraph = self.figure.add_subplot(111)
        self.figureGraph.set_title('Test Real Time Plot',size=12)        # Graph Title
        self.figureGraph.set_xlabel('Time[s]')                           # X Axis Label
        self.figureGraph.set_ylabel('data[℃]')                          # Y Axis Label
        self.figureGraph.grid(which = "major", axis = "both", color = "skyblue", alpha = 0.8,
        linestyle = "-", linewidth = 1)
        self.figureGraph.set_ylim(-10, 10)
        self.figureGraph.set_xlim(0, 5)
        self.figure.subplots_adjust(left=0.11, right=0.95, bottom=0.21, top=0.89)
        self.line, = self.figureGraph.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.figure,graphFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def on_click(self):
        global counter,ouputCounter

        if self.ani is None:
            return self.start()
        if self.running:
            self.ani.event_source.stop()
            self.btn.config(text='開始')
        else:
            self.ani.event_source.start()
            self.btn.config(text='停止')
        self.running = not self.running

    def start(self):
        self.xdata = deque([], maxlen=kAxisLength)
        self.ydata = deque([], maxlen=kAxisLength)
        self.points = int(self.points_ent.get())+1
        self.ani = animation.FuncAnimation(
            self.figure,
            self.update_graph,
            frames=self.points,
            interval=int(self.interval.get()),
            repeat=False)
        self.running = True
        self.btn.config(text='停止')
        self.ani._start()

    def update_graph(self, i):
        if i == 0:
            return;

        global counter,ouputCounter

        counter += 1;
        ouputCounter += 1;
        self.outPoints_ent.delete(0, tk.END)
        self.outPoints_ent.insert(0, str(ouputCounter))

        if(counter >= 100):
            counter = 1;
        pi = math.pi
        intList = np.linspace(0, 2*pi, 100)
        y = np.sin(intList)

        self.outputValueEnt.delete(0, tk.END)
        self.outputValueEnt.insert(0, str(round(y[counter],5)))

        self.xdata.append(i * (int(self.interval.get()) / 1000.0))
        self.ydata.append(round(y[counter],5))
        self.line.set_data(self.xdata, self.ydata)
        
        self.figureGraph.set_ylim(min(self.ydata) - 0.1, max(self.ydata) + 0.1)
        self.figureGraph.set_xlim(min(self.xdata), max(self.xdata) + 0.01)

        if i >= self.points - 1:
            self.btn.config(text='Start')
            self.running = False
            self.ani = None

            counter = 0;
            ouputCounter = 0;
        return self.line,

def main():
    root = tk.Tk()
    root.geometry("610x400")
    app = App(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
