import tkinter as tk
from src.client import Game
from src.client import Server


class Application:
    def __init__(self):
        self.master = tk.Tk()

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.server_address = tk.StringVar()

        self.username_entry = None
        self.password_entry = None
        self.server_address_entry = None

        self.master.title('SimpleMultiplayerGame')
        self.master.config(width=640, height=480)

        self.create_view()

        self.master.mainloop()

    def create_view(self):
        entries_frame = tk.Frame(self.master)
        entries_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        entries_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        username_frame = tk.Frame(entries_frame)
        username_frame.pack()

        username_label = tk.Label(username_frame, text='USERNAME: ')
        username_label.pack(side=tk.LEFT)

        self.username_entry = tk.Entry(username_frame, textvariable=self.username)
        self.username_entry.pack()
        
        server_address_frame = tk.Frame(entries_frame)
        server_address_frame.pack()

        server_address_label = tk.Label(server_address_frame, text='      SERVER: ')
        server_address_label.pack(side=tk.LEFT)

        self.server_address_entry = tk.Entry(server_address_frame, textvariable=self.server_address)
        self.server_address_entry.pack()

        connect_button = tk.Button(entries_frame, text='CONNECT', command=self.connect_button_clicked)
        connect_button.pack()

    def connect_button_clicked(self):
        if self.username.get() == '':
            self.username_entry.config(highlightbackground='red')
        elif self.server_address.get() == '':
            self.server_address_entry.config(highlightbackground='red')
        else:
            self.master.destroy()

            # msg = tk.Message( text='OK', width=30)
            # msg.config(font=('times', 16))
            # msg.pack()
            # tk.mainloop()

            game = Game.Game(self.username.get(), self.server_address.get())
            game.start()


if __name__ == '__main__':
    app = Application()
