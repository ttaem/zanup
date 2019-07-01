import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry



master = tk.Tk()

upper_pane = tk.PanedWindow(master)
#bottom_pane =  tk.PanedWindow(master)
bottom_pane =  tk.LabelFrame(master, text='List of workday')

upper_pane.pack(side=tk.TOP, fill=tk.BOTH)
bottom_pane.pack(side=tk.TOP, fill=tk.BOTH)

calendar = Calendar(upper_pane)
calendar.pack(side=tk.LEFT, fill=tk.BOTH)

delete_button = tk.Button(upper_pane, text='Delete', width=30, command=master.destroy)
done_button = tk.Button(upper_pane, text='Generate', width=30, command=master.destroy)
save_button = tk.Button(upper_pane, text='Save', width=30, command=master.destroy)

delete_button.pack(fill=tk.X)
done_button.pack(fill=tk.X)
save_button.pack(fill=tk.X)

treeview=ttk.Treeview(bottom_pane, 
        columns=["Date", "Week", "Start", "End", "Description"],
        displaycolumns=["Date", "Week", "Start", "End", "Description"])

treeview.column("#0", width=30, anchor="center")
treeview.heading("#0", text="#")

treeview.column("#1", width=100, anchor="center")
treeview.heading("Date", text="Date")

treeview.column("#2", width=50, anchor="center")
treeview.heading("Week", text="Week")

treeview.column("#3", width=50, anchor="center")
treeview.heading("Start", text="Start")

treeview.column("#4", width=50, anchor="center")
treeview.heading("End", text="End")

treeview.column("#5", width=300, anchor="center")
treeview.heading("Description", text="Description")
treeview.pack()


tk.mainloop()



