import os
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import subprocess


class App:
    def __init__(self):
        self.vlc_process = None  # subprocess reference
        self.game_running = False  # subprocess reference

        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#AFFCB7')

        # Configure the grid
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # BMO image row
        self.root.grid_rowconfigure(1, weight=1)  # Treeview row
        self.root.grid_rowconfigure(2, weight=0)  # BMO label row

        # Load the image
        img_path = '/home/bmo/code/images/adventure-time-bmo-skating-512x512.png'
        img = Image.open(img_path)

        # Resize the image to fit the column
        img = img.resize((180, 180), Image.ANTIALIAS)
        self.bmo_image = ImageTk.PhotoImage(img)

        # Create a label with the image
        self.bmo_label = tk.Label(
            self.root, image=self.bmo_image, bg='#AFFCB7')
        self.bmo_label.grid(column=0, row=0, sticky="n", padx=(32, 0), pady=48)

        # Create a font object for the OS version label
        self.os_label_font = font.Font(size=10, weight='bold')

        # Create a label for the OS version
        self.os_label = tk.Label(
            self.root, text="BMO-OS v1.1", bg='#AFFCB7', font=self.os_label_font)
        # Placed in new row and aligned to southwest
        self.os_label.grid(column=0, row=2, sticky="sw", padx=(32, 0), pady=16)

        # Create the treeview
        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=69, background='#AFFCB7',
                             fieldbackground='#AFFCB7', borderwidth=0)
        self.style.layout(
            'Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

        # Set the background color of selected items
        self.style.map('Treeview', background=[('selected', '#111912')])

        self.treeview = ttk.Treeview(self.root, columns=(
            'Name',), show='tree', selectmode='browse')
        self.treeview.column('#0', width=self.root.winfo_screenwidth())

        # Create a frame for treeview and scrollbar
        self.treeview_frame = tk.Frame(self.root)
        self.treeview_frame.grid(
            column=1, row=0, rowspan=3, sticky="nsew", padx=32, pady=32)

        # Place Treeview in the grid inside the frame
        self.treeview = ttk.Treeview(self.treeview_frame, columns=(
            'Name',), show='tree', selectmode='browse')
        self.treeview.column('#0', width=self.root.winfo_screenwidth())

        self.treeview.pack(side="left", fill="both", expand=True)

        # Add scrollbar to the treeview frame
        self.scrollbar = ttk.Scrollbar(
            self.treeview_frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        # Create a font object for the treeview items
        self.treeview_font = font.Font(
            size=20, weight="bold")  # Make font bold
        self.treeview.tag_configure('tag_name', font=self.treeview_font)

        video_files = [f for f in os.listdir(
            '/home/bmo/animations/') if f.endswith('.mp4')]

        self.menus = {
            'Main': {'items': ['BMO\'s Pro Skater Game', 'Screensaver', 'Video Player', 'Settings', 'Exit'], 'parent': None},
            'Video Player': {'items': video_files, 'parent': 'Main'},
            'Settings': {'items': ['Setting One', 'Setting Two', 'Setting Three', 'Setting Four', 'Setting Five', 'Setting Six', 'Setting Seven', 'Setting Eight'], 'parent': 'Main'},
        }
        self.current_menu = 'Main'
        self.current_selection = 'BMO\'s Pro Skater Game'

        self.update_menu()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            17, GPIO.FALLING, callback=self.on_up, bouncetime=200)
        GPIO.add_event_detect(
            22, GPIO.FALLING, callback=self.on_down, bouncetime=200)
        GPIO.add_event_detect(
            26, GPIO.FALLING, callback=self.on_select, bouncetime=200)

        # Start the periodic check
        self.root.after(1000, self.check_game_status)
        self.root.mainloop()

        GPIO.cleanup()

    def update_menu(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)
        items = ['Back'] + self.menus[self.current_menu]['items'] if self.current_menu != 'Main' else self.menus[self.current_menu]['items']
        for item in items:
            id = self.treeview.insert('', 'end', text=item, tags='tag_name')
            if item == self.current_selection:
                self.treeview.selection_set(id)
                self.treeview.focus(id)
        if not self.treeview.selection():
            first_id = self.treeview.get_children()[0]
            self.treeview.selection_set(first_id)
            self.treeview.focus(first_id)
            self.current_selection = self.treeview.item(first_id)['text']

    def on_up(self, channel):
        if self.game_running:  # Ignore input if game is running
            return

        cur_item = self.treeview.focus()
        prev_item = self.treeview.prev(cur_item)

        if prev_item:
            self.treeview.selection_set(prev_item)
            self.treeview.focus(prev_item)
            self.current_selection = self.treeview.item(prev_item)['text']

            # If the previous item is the first in the list, set the scrollbar to the top
            if self.treeview.index(prev_item) == 0:
                self.treeview.yview_moveto(0)
            else:
                self.treeview.see(prev_item)

    def on_down(self, channel):
        if self.game_running:  # Ignore input if game is running
            return

        cur_item = self.treeview.focus()
        next_item = self.treeview.next(cur_item)

        if next_item:
            self.treeview.selection_set(next_item)
            self.treeview.focus(next_item)
            self.current_selection = self.treeview.item(next_item)['text']
            self.treeview.see(next_item)

    def on_select(self, channel):
        if self.game_running:  # Ignore input if game is running
            return

        selected = self.treeview.item(self.treeview.focus())['text']
        print('Selected:', selected)

        # If a video is already playing, kill it and reset the process reference
        if self.vlc_process and self.vlc_process.poll() is None:
            self.vlc_process.kill()
            self.vlc_process = None
        elif selected == 'Screensaver':
            self.vlc_process = subprocess.Popen(['vlc', '--fullscreen', '--loop', '--no-video-title-show',
                                                 '/home/bmo/animations/BMO_IdleLoop.mp4'])
        elif selected == 'BMO\'s Pro Skater Game':  # Check if BMO\'s Pro Skater Game is selected
            self.game_running = True  # Set the flag to True
            self.subprocess_game = subprocess.Popen(
                ['python', '/home/bmo/code/BMO-Game.py'])
        elif selected in self.menus:
            self.current_menu = selected
            self.current_selection = 'Back'
        elif selected == 'Back':
            self.current_selection = self.current_menu
            self.current_menu = self.menus[self.current_menu]['parent']
        elif selected == 'Exit':
            self.root.destroy()
        elif self.current_menu == 'Video Player':
            self.vlc_process = subprocess.Popen(['vlc', '--fullscreen', '--play-and-exit', '--no-repeat', '--no-loop',
                                                 '--no-video-title-show', '/home/bmo/animations/{}'.format(selected)])

        self.update_menu()

    def print_dimensions(self):
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        print("Window dimensions: {}x{}".format(window_width, window_height))

    def check_game_status(self):
        if self.game_running and self.subprocess_game.poll() is not None:
            self.game_running = False
        # Schedule the next check
        self.root.after(1000, self.check_game_status)


app = App()
