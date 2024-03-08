import random

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

        # images - frames
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

        # first animation to display
        self.state = 2
        self.img = tk.PhotoImage(file='assets/brown_cat/idle1.png')
        self.frame_index = 0
        self.animation_num = 0
        self.animation_max = 5      # run the animation 5 times

        # animation's position
        self.x = int(screen_width * 0.8)
        self.y = work_height - 64

        # set focus-highlight to black when the window does not have focus
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

        self.label.bind("<ButtonPress-1>", self.drag_window)
        self.label.bind("<ButtonRelease-1>", self.drop_window)
        self.label.bind("<B1-Motion>", self.on_move_window)

        self.blocked_state = False

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()



    def animate(self, array):
        """
        Change the frames of an animation
        :param array: the list of frames
        """
        self.window.after(250)
        self.frame_index = (self.frame_index + 1) % len(array)
        self.img = array[self.frame_index]
        if self.frame_index == len(array) - 1:
            self.animation_num += 1
        self.event()

    def move(self):
        """
        Move the buddy left and right
        """
        # collision with the right part of the screen
        if self.state == 0:
            if self.x < screen_width - 80:
                self.x += 5
            if self.x >= screen_width - 80:
                self.state = 1
                self.frame_index = 0
        # collision with the left part of the screen
        elif self.state == 1:
            if self.x > 10:
                self.x -= 5
            if self.x <= 10:
                self.state = 0
                self.frame_index = 0

    def event(self):
        """
        The buddy gets a new action to do
        """
        if self.animation_num == self.animation_max:
            if self.state == 0:
                self.state = random.choices([0, 2], weights=[5, 3])[0]
            elif self.state == 1:
                self.state = random.choices([1, 2], weights=[5, 3])[0]
            elif self.state == 2:
                self.state = random.choices([0, 1, 2, 3], weights=[2, 2, 2, 1])[0]
            elif self.state == 3:
                self.state = 4
            elif self.state == 4:
                self.state = random.choices([0, 1, 2, 4], weights=[1, 1, 2, 1])[0]

            # reset the animation_num and set the duration of the new state (animation_max)
            self.animation_num = 0
            if self.state in [0, 1]:
                self.animation_max = random.randint(7, 15)
            elif self.state == 2:
                self.animation_max = random.randint(6, 10)
            elif self.state == 3:
                self.animation_max = 0
            elif self.state == 4:
                self.animation_max = random.choice([5, 10, 15, 20])

    def update(self):
        if self.blocked_state is False:
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
            elif self.state == 4:
                self.animate(self.zzz)

            # create a window of size 72x64 pixels
            # self.window.geometry('72x64+' + str(self.x) + '+' + str(self.y))
            self.window.geometry("+%s+%s" % (self.x, self.y))

            # add the image to our label
            self.label.configure(image=self.img)
            # give window to geometry manager (so it will appear)
            self.label.pack()

            self.window.after(1, self.update)

    def drag_window(self, event):
        self.blocked_state = True
        self.x = event.x
        self.y = event.y

    def drop_window(self, event):
        self.blocked_state = False
        x = event.x_root - self.x
        y = event.y_root - self.y

        # Ensure window does not go out of screen bounds
        if x < 0:
            x = 0
        elif x > screen_width - self.window.winfo_width():
            x = screen_width - self.window.winfo_width()
        if y < 0:
            y = 0
        elif y > work_height - self.window.winfo_height():
            y = work_height - self.window.winfo_height()

        self.window.geometry("+%s+%s" % (x, y))
        self.x = x
        self.y = y
        self.update()



    def on_move_window(self, event):
        x = (event.x_root - self.x - self.window.winfo_rootx() + self.window.winfo_rootx())
        y = (event.y_root - self.y - self.window.winfo_rooty() + self.window.winfo_rooty())

        # Ensure window does not go out of screen bounds
        if x < 0:
            x = 0
        elif x > screen_width - self.window.winfo_width():
            x = screen_width - self.window.winfo_width()
        if y < 0:
            y = 0
        elif y > work_height - self.window.winfo_height():
            y = work_height - self.window.winfo_height()

        self.window.geometry("+%s+%s" % (x, y))


# TODO: add gravity
buddy = Buddy()
