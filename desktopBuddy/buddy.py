import random
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

        self.walking_left = [tk.PhotoImage(file='assets/brown_cat/walkingleft1.png'),
                             tk.PhotoImage(file='assets/brown_cat/walkingleft2.png'),
                             tk.PhotoImage(file='assets/brown_cat/walkingleft3.png'),
                             tk.PhotoImage(file='assets/brown_cat/walkingleft4.png')]

        self.walking_right = [tk.PhotoImage(file='assets/brown_cat/walkingright1.png'),
                              tk.PhotoImage(file='assets/brown_cat/walkingright2.png'),
                              tk.PhotoImage(file='assets/brown_cat/walkingright3.png'),
                              tk.PhotoImage(file='assets/brown_cat/walkingright4.png')]

        self.sleeping = [tk.PhotoImage(file='assets/brown_cat/sleeping1.png'),
                         tk.PhotoImage(file='assets/brown_cat/sleeping2.png'),
                         tk.PhotoImage(file='assets/brown_cat/sleeping3.png'),
                         tk.PhotoImage(file='assets/brown_cat/sleeping4.png'),
                         tk.PhotoImage(file='assets/brown_cat/sleeping5.png'),
                         tk.PhotoImage(file='assets/brown_cat/sleeping6.png')]

        self.zzz = [tk.PhotoImage(file='assets/brown_cat/zzz1.png'), tk.PhotoImage(file='assets/brown_cat/zzz2.png'),
                    tk.PhotoImage(file='assets/brown_cat/zzz3.png'), tk.PhotoImage(file='assets/brown_cat/zzz4.png')]

        self.img = tk.PhotoImage(file='assets/brown_cat/idle1.png')
        self.frame_index = 0

        self.state = 0
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
        self.window.after(1, self.update)
        self.window.mainloop()

    def animate(self, array):
        if time.time() > self.timestamp + 0.3:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % len(array)
            self.img = array[self.frame_index]


    def move(self):
        if self.state == 0:
            if self.x < screen_width - 80:
                self.x += 1
            if self.x >= screen_width - 80:
                self.state = 1
                self.frame_index = 0
        elif self.state == 1:
            if self.x > 10:
                self.x -= 1
            if self.x <= 10:
                self.state = 0
                self.frame_index = 0

    def event(self):
        change_state = int(time.time()) % 70
        state_prev = self.state
        if change_state < 7:
            # stay
            self.state = 2
        elif change_state < 17:
            # go right
            if self.state not in [0, 1]:
                self.state = 0
        elif change_state < 27:
            # sleep
            if self.state not in [3, 4]:
                self.state = 3
        elif change_state < 32:
            # stay
            self.state = 2
        elif change_state < 47:
            # go
            if self.state not in [0, 1]:
                self.state = 1
        elif change_state < 53:
            # stay
            self.state = 2
        elif change_state <= 70:
            # go
            if self.state not in [0, 1]:  # avoid move function contradiction
                self.state = 1

        if state_prev != self.state:
            self.frame_index = 0

    def update(self):
        self.event()

        if self.state == 0:
            self.animate(self.walking_right)
            self.move()
        elif self.state == 1:
            self.animate(self.walking_left)
            self.move()
        elif self.state == 2:
            self.animate(self.idle)
        elif self.state == 3:
            self.animate(self.sleeping)
            if self.frame_index == 5:
                self.state = 4
        elif self.state == 4:
            self.animate(self.zzz)


        # create a window of size 72x64 pixels
        self.window.geometry('72x64+' + str(self.x) + '+' + str(self.y))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        self.window.after(15, self.update)


buddy = Buddy()
