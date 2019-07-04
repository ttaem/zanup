import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry

import datetime
import pandas as pd


def insert_row():
    global df
    df = df.append(pd.Series([date_var.get(), week_var.get(), start_var.get(), end_var.get(), rate_var.get(), desc_text.get("1.0", tk.END)], index=df.columns), ignore_index=True)
    print(df)



def cal_call(eventObject):
    date = calendar.selection_get()
    print(date)
    print (date.weekday())
    print (date.strftime('%a'))
    print(eventObject)
    date_var.set(date)
    week_var.set(date.strftime('%a'))

master = tk.Tk()

upper_pane = tk.PanedWindow(master)
#bottom_pane =  tk.PanedWindow(master)
bottom_pane =  tk.LabelFrame(master, text='List of workday')
insert_pane = tk.LabelFrame(upper_pane, text='New Entry')

upper_pane.pack(side=tk.TOP, fill=tk.BOTH)
bottom_pane.pack(side=tk.TOP, fill=tk.BOTH)

calendar = Calendar(upper_pane, font="Arial 14", firstweekday='sunday')
calendar.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
calendar.bind("<<CalendarSelected>>", cal_call)

insert_pane.pack(fill=tk.X)
insert_pane.grid_rowconfigure(0, weight=1)
insert_pane.grid_rowconfigure(1, weight=1)
insert_pane.grid_columnconfigure(0, weight=1)
insert_pane.grid_columnconfigure(1, weight=1)
insert_pane.grid_columnconfigure(2, weight=1)
insert_pane.grid_columnconfigure(3, weight=1)
insert_pane.grid_columnconfigure(4, weight=1)

date_var = tk.StringVar(insert_pane)
date_var.set("Select from calendar")
date_label = tk.Label(insert_pane, textvariable=date_var)
date_label.grid(row=0, column=0, sticky='W', padx=10)

week_var = tk.StringVar(insert_pane)
#week_var.set("2019-07-03")
week_label = tk.Label(insert_pane, textvariable=week_var)
week_label.grid(row=0, column=1, sticky='W')
#start_label = tk.Label(insert_pane, text="09:00")
#start_label.grid(row=0, column=1)
start_var = tk.StringVar(insert_pane)
start_var.set('09')
start_choices = {'07', '08', '09', '10', '11'}
start_pop = tk.OptionMenu(insert_pane, start_var, *start_choices)
start_pop.grid(row=0, column=2, stick='W')

during_label = tk.Label(insert_pane, text="~")
during_label.grid(row=0, column=3)

end_var = tk.StringVar(insert_pane)
end_var.set('21')
end_choices = {'21', '22', '23', '24'}
end_pop = tk.OptionMenu(insert_pane, end_var, *end_choices)
end_pop.grid(row=0, column=4)

#end_label = tk.Label(insert_pane, text="22:00")
#end_label.grid(row=0, column=2)
rate_var = tk.StringVar(insert_pane)
rate_var.set('A')
rate_label = tk.Label(insert_pane, textvariable=rate_var)
#level_label.grid(row=0, column=3, sticky="E")
rate_label.grid(row=0, column=5, padx=10)
desc_var = tk.StringVar(insert_pane)
desc_text = tk.Text(insert_pane, height=2, width=50)
desc_text.grid(row=1, columnspan=6, sticky='WE')


insert_button = tk.Button(upper_pane, text='Insert', width=30, command=insert_row)
delete_button = tk.Button(upper_pane, text='Delete', width=30, command=master.destroy)
done_button = tk.Button(upper_pane, text='Generate', width=30, command=master.destroy)
save_button = tk.Button(upper_pane, text='Save', width=30, command=master.destroy)

insert_button.pack(fill=tk.X)
delete_button.pack(fill=tk.X)
done_button.pack(fill=tk.X)
save_button.pack(fill=tk.X)

treeview=ttk.Treeview(bottom_pane, 
        columns=["Date", "Week", "Start", "End", "Rate", "Description"],
        displaycolumns=["Date", "Week", "Start", "End", "Rate", "Description"])

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

treeview.column("#5", width=30, anchor="center")
treeview.heading("Rate", text="Rate")

treeview.column("#6", width=300, anchor="center")
treeview.heading("Description", text="Description")
treeview.pack(fill=tk.BOTH)

df = pd.read_csv("sample.csv")
for row in df.itertuples(index=True, name='Pandas'):
    treeview.insert('','end', text=row[0], values=row[1:])

#treeview.insert('','end', text='1', values=('2019-7-02', 'Sun', '09:00', '22:00', 'hahaha'))

tk.mainloop()



