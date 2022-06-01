import math
import numpy as np
import tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


kRedrawCycle = 1            # msec 再描画間隔
kDrawSec = 0.3              # sec 何秒分表示するか
kDrawSamplingRate = 500     # 点  秒間あたりの表示点数

counter = 0;

class GraphData:
    """ グラフに表示するデータクラス
    """
    def __init__(self):
        self.samplingRate = 1000
        self.counter = 0;
    
    def get_sampling_rate(self):
        """ サンプリングレート返す
        """
        return self.samplingRate
    
    def get_next(self):
        global counter
        """ グラフ表示用のデータを返す
        """
        counter += 1;
        if(counter >= 100):
            counter = 1;
        pi = math.pi
        intList = np.linspace(0, 2*pi, 100)
        y = np.sin(intList)
        intList = [y[counter-1],y[counter]]
        return intList                                      #テストでSin波データを返す

class View:
    """ グラフ表示用のGUI管理クラス
    """
    def __init__(self):        
        self.root = Tk.Tk()
        self.root.wm_title("Real Time Graph")               # Form Title
        
        self.serial = GraphData()
        self.data = []
        self.dataStartTime = 0.0
        
        self.drawSec = kDrawSec                             # Draw plot Sec
        self.drawSamplingRate = kDrawSamplingRate           # Draw Rate
        
        # グラフ設定
        self.figure = Figure(figsize=(6,4), dpi=100)             # Graph Size
        self.figureGraph = self.figure.add_subplot(111)                    # Draw Figure Graph
        self.figureGraph.set_title('Test Real Time Plot', size=12)    # Graph Title
        self.figureGraph.set_xlabel('Time[s]')                        # X Axis Label
        self.figureGraph.set_ylabel('data[℃]')                       # Y Axis Label

        self.plot_data = self.figureGraph.plot(
                self.data,
                linewidth=0.5,
                color=(1, 0, 0),
                )[0]
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)       # Tkinter Use Matplotlib
        self.canvas.draw()                                              # Draw Figure
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1) # Draw Figure Position            
        
        self.button = Tk.Button(master=self.root, text='Close', command=self.close_button_click)    # Create Button
        self.button.pack(side=Tk.BOTTOM)                    # Button Pack
        
        self.reDrawTimerCallBack()                              # Call Interval Timer

        self.root.mainloop()                                                                        
    
    def reDrawTimerCallBack(self):
        """ 定期タイマーコールイベント
        """
        self.add_draw_data(self.serial.get_next())              # Call Get Plot Data
        self.draw_plot()                                        # Call Plot Graph Function
        self.root.after(kRedrawCycle, self.reDrawTimerCallBack) # Start Interval Timer
    
    def add_draw_data(self, data):
        """ 描画対象のデータを追加
            @param data データ配列
        """
        samplingRate = self.serial.get_sampling_rate()
        samplingSec = 1. / samplingRate
        
        drawSamplingRate = self.drawSamplingRate
        drawSamplingSec = 1. / drawSamplingRate
        
        newData = []
        time = 0.0
        
        for s in data:
            time += samplingSec
            
            # Add Elapsed Sampling Rate 
            if time >= drawSamplingSec:
                time -= drawSamplingSec
                newData.append(s)

        self.data += newData                                        # Add New Data
        remainFrameLength = int(self.drawSec * drawSamplingRate)    # All Draw Data Count
        
        self.dataStartTime += max((len(self.data) - remainFrameLength), 0) / float(drawSamplingRate)  # X Axis Scale Scroll
        
        self.data = self.data[-remainFrameLength:]      # First Delete
        
    def draw_plot(self):
        """ グラフデータプロット
        """
        num_draw_frame = int(self.drawSec * self.drawSamplingRate)   
        draw_sampling_rate = self.drawSamplingRate      # Sampling Rate
        
        xMin = self.dataStartTime                       # X Axis Min
        xMax = xMin + self.drawSec                      # X Axis Max
        
        yMin = -1.5                                     # Y Axis Min
        yMax = 1.5                                      # Y Axis Max
        
        self.figureGraph.set_xbound(lower=xMin, upper=xMax)       # Set X Axis Min,Max
        self.figureGraph.set_ybound(lower=yMin, upper=yMax)       # Set Y Axis Min,Max
        
        self.figureGraph.grid(True, color='gray')                 # Grid Color
        
        xaxis = [float(con) / self.drawSamplingRate + self.dataStartTime for con in range(len(self.data))]  # Calc X Plot
        self.plot_data.set_xdata(xaxis)                 # X plot
        self.plot_data.set_ydata(np.array(self.data))   # Y plot
        self.canvas.draw()                              # Canvas Draw
        
    def close_button_click(self):
        self.root.destroy()                             # Form Destory -> Close 

if __name__ == '__main__':
    v = View()