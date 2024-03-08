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

        # Load images
        self.load_images()

        # Set initial state
        self.set_initial_state()

        self.configure_window()

        self.label.bind("<ButtonPress-1>", self.drag_window)
        self.label.bind("<ButtonRelease-1>", self.drop_window)
        self.label.bind("<B1-Motion>", self.on_move_window)

        self.run_animation()

    def load_images(self):
        """Load images for animations"""
        self.idle = [tk.PhotoImage(file=f'assets/brown_cat/idle{i}.png') for i in range(1, 5)]
        self.walking_left = [tk.PhotoImage(file=f'assets/brown_cat/walkingleft{i}.png') for i in range(1, 5)]
        self.walking_right = [tk.PhotoImage(file=f'assets/brown_cat/walkingright{i}.png') for i in range(1, 5)]
        self.sleeping = [tk.PhotoImage(file=f'assets/brown_cat/sleeping{i}.png') for i in range(1, 7)]
        self.zzz = [tk.PhotoImage(file=f'assets/brown_cat/zzz{i}.png') for i in range(1, 5)]

    def set_initial_state(self):
        """Initialize animation state variables"""
        # Set initial animation state
        self.state = 2
        self.img = self.idle[0]

        # Control the animation change
        self.animation_num = 0
        self.animation_max = 5  # run the animation 5 times
        self.frame_index = 0

        # animation's position
        self.x = int(screen_width * 0.8)
        self.y = work_height - 64

        # decide if the object can be animated or not (not if the window is dragged)
        self.blocked_state = False

    def configure_window(self):
        """Configure window properties"""
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
        # give window to geometry manager (so it will appear)
        self.label.pack()
        # Update window size and position
        self.update_window_geometry()

    def update_window_geometry(self):
        """Update window size and position"""
        self.window.geometry('72x64+' + str(self.x) + '+' + str(self.y))

    def run_animation(self):
        """Start animation loop"""
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
        self.handle_event()

    def move(self):
        """Move the buddy left and right"""
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

    def handle_event(self):
        """Determine the next action for the buddy"""
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
        """Update the animation and window position"""
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

            self.window.geometry("+%s+%s" % (self.x, self.y))
            self.label.configure(image=self.img)
            self.label.pack()
            self.window.after(1, self.update)

    def drag_window(self, event):
        """Handle dragging the window"""
        self.blocked_state = True
        self.x = event.x
        self.y = event.y

    def drop_window(self, event):
        """Handle dropping the window after dragging"""
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
        """Handle moving the window"""
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
if __name__ == "__main__":
    app = Buddy()
