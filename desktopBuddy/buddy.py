import time
import tkinter as tk
from win32api import GetMonitorInfo, MonitorFromPoint

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get('Work')
screen_width = work_area[2]
work_height = work_area[3]

class Buddy:
    def __init__(self):
        # create a window
        self.window = tk.Tk()

        # placeholder image
        self.idle = [tk.PhotoImage(file='assets/brown_cat/idle1.png'), tk.PhotoImage(file='assets/brown_cat/idle2.png'),
                     tk.PhotoImage(file='assets/brown_cat/idle3.png'), tk.PhotoImage(file='assets/brown_cat/idle4.png')]

        self.img = tk.PhotoImage(file='assets/brown_cat/idle1.png')
        self.frame_index = 0

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        self.x = int(screen_width * 0.8)
        self.y = work_height - 64

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)
        # make window draw over all others
        self.window.attributes('-topmost', True)
        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')
        # create a window of size 72x64 pixels
        self.window.geometry('72x64+' + str(self.x) + '+' + str(self.y))
        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

    def update(self):
        if time.time() > self.timestamp + 0.45:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 4
            self.img = self.idle[self.frame_index]

        # create a window of size 72x64 pixels
        self.window.geometry('72x64+' + str(self.x) + '+' + str(self.y))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        self.window.after(10, self.update)


buddy = Buddy()
