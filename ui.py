import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox as msg
from tkinter import filedialog

import datetime
import pandas as pd

import openpyxl as xl
from openpyxl.styles import Border, Side, Alignment

name = "Lee Changkeel"
position = "Senior"
department = "1sil"


def save_df():
    print("save")
    df.to_csv("sample.csv", index=False)


def generate_xl():
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    left_border = Border(left=Side(style='medium'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    right_border = Border(left=Side(style='thin'),
                         right=Side(style='medium'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    bottom_left_border = Border(left=Side(style='medium'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='medium'))
    bottom_right_border = Border(left=Side(style='thin'),
                         right=Side(style='medium'),
                         top=Side(style='thin'),
                         bottom=Side(style='medium'))


    desc_align = Alignment(wrap_text=True, shrink_to_fit=True)

    
    df_count = df.shape[0]
    sheet.insert_rows(7, amount=df_count)
    #sheet["C30"].border=thin_border 
    print("insert " + str(df_count))

    for index, df_row in df.iterrows():
        sheet["B"+str(index+7)] = name
        sheet["C"+str(index+7)] = position
        sheet["D"+str(index+7)] = department
        sheet["E"+str(index+7)] = df_row['date']
        sheet["F"+str(index+7)] = df_row['week']
        sheet["G"+str(index+7)] = df_row['start']
        sheet["H"+str(index+7)] = df_row['end']
        sheet["I"+str(index+7)] = ""
        sheet["J"+str(index+7)] = df_row['rate']
        sheet["K"+str(index+7)] = "=IF(J"+str(index+7)+"=\"A\",15000,IF(J"+str(index+7)+"=\"B\",20000,IF(J"+str(index+7)+"=\"C\",30000,IF(J"+str(index+7)+"=\"D\",40000,''))))"
        sheet["L"+str(index+7)] = df_row['desc']

    for index, df_row in df.iterrows():
        sheet["B"+str(index+7)].border = left_border
        sheet["C"+str(index+7)].border = thin_border
        sheet["D"+str(index+7)].border = thin_border
        sheet["E"+str(index+7)].border = thin_border
        sheet["F"+str(index+7)].border = thin_border
        sheet["G"+str(index+7)].border = thin_border
        sheet["H"+str(index+7)].border = thin_border
        sheet["I"+str(index+7)].border = thin_border
        sheet["J"+str(index+7)].border = thin_border
        sheet["K"+str(index+7)].border = thin_border
        sheet["L"+str(index+7)].border = right_border
        sheet["L"+str(index+7)].alignment = desc_align

        rd = sheet.row_dimensions[index+7]
        rd.height = 30

    sheet["B"+str(index+7)].border = bottom_left_border
    sheet["L"+str(index+7)].border = bottom_right_border

    sheet["K"+str(index+7+1)] = "=SUM(K7:K" + str(index+7) + ")"
    sheet["K"+str(index+7+2)] = "=SUM(K" + str(index+7+1) + ")"
    book.save("result.xlsx")

def insert_row():
    global df

    for index, df_row in df.iterrows():
        print(date_var.get())
        print(df_row['date'])
        if date_var.get() == df_row['date']:
            msg.showerror("New Entry Insertion", "Duplicated Date Detected!!!")
            return

    df = df.append(pd.Series([date_var.get(), week_var.get(), start_var.get()+":00", end_var.get()+":00", rate_var.get(), desc_text.get("1.0", 'end-1c')], index=df.columns), ignore_index=True)
    print(df)
    df = df.sort_values(by="date")
    print(df)
    df = df.reset_index(drop=True)
    print(df)

    for i in treeview.get_children():
        treeview.delete(i)
    for row in df.itertuples(index=True, name='Pandas'):
        treeview.insert('','end', text=row[0], values=row[1:])

    #child_id = treeview.get_children()[-1]
    #treeview.focus(child_id)
    #treeview.selection_set(child_id)
    treeview.yview_moveto(1)

def delete_row():
    global df
    cur = treeview.focus()
    index = treeview.index(cur)
    print(cur)
    print(index)
    print(df)
    df = df.drop(df.index[index])
    print(df)
    df = df.reset_index(drop=True)
    print(df)

    for i in treeview.get_children():
        treeview.delete(i)
    for row in df.itertuples(index=True, name='Pandas'):
        treeview.insert('','end', text=row[0], values=row[1:])



def cal_call(eventObject):
    date = calendar.selection_get()
    print(date)
    print (date.weekday())
    print (date.strftime('%a'))
    print(eventObject)
    date_var.set(date)
    week_var.set(date.strftime('%a'))

def exit_():
    master.quit()
    master.destroy()

def file_open():
    filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("cvs files", "*.csv"), ("all files", "*.*")))
    print(filename)

master = tk.Tk()
master.title("ZanUp")

menu_bar = tk.Menu(master, relief="flat")

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=file_open)
file_menu.add_command(label="Save")
file_menu.add_command(label="Generation")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_)
menu_bar.add_cascade(label="File", menu=file_menu)

setting_menu = tk.Menu(menu_bar, tearoff=0)
setting_menu.add_command(label="Preference")
menu_bar.add_cascade(label="Setting", menu=setting_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help")
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)

master.config(menu=menu_bar)

upper_pane = tk.PanedWindow(master)
#bottom_pane =  tk.PanedWindow(master)
bottom_pane =  tk.LabelFrame(master, text='List of workday')
insert_pane = tk.LabelFrame(upper_pane, text='New Entry')

upper_pane.pack(side=tk.TOP, fill=tk.BOTH)
bottom_pane.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

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
date_var.set(calendar.selection_get())
date_label = tk.Label(insert_pane, textvariable=date_var)
date_label.grid(row=0, column=0, sticky='W', padx=10)

week_var = tk.StringVar(insert_pane)
week_var.set(calendar.selection_get().strftime('%a'))
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
delete_button = tk.Button(upper_pane, text='Delete', width=30, command=delete_row)
done_button = tk.Button(upper_pane, text='Generate', width=30, command=generate_xl)
save_button = tk.Button(upper_pane, text='Save', width=30, command=save_df)

insert_button.pack(fill=tk.X)
delete_button.pack(fill=tk.X)
done_button.pack(fill=tk.X)
save_button.pack(fill=tk.X)

treeview=ttk.Treeview(bottom_pane, 
        columns=["Date", "Week", "Start", "End", "Rate", "Description"],
        displaycolumns=["Date", "Week", "Start", "End", "Rate", "Description"])

treeview.column("#0", width=50, minwidth=50, stretch=False, anchor="w")
treeview.heading("#0", text="#")

treeview.column("#1", width=100, minwidth=100, stretch=False, anchor="center")
treeview.heading("Date", text="Date")

treeview.column("#2", width=50, minwidth=50, stretch=False, anchor="center")
treeview.heading("Week", text="Week")

treeview.column("#3", width=50, minwidth=50, stretch=False, anchor="center")
treeview.heading("Start", text="Start")

treeview.column("#4", width=50, minwidth=50, stretch=False, anchor="center")
treeview.heading("End", text="End")

treeview.column("#5", width=50, minwidth=50, stretch=False, anchor="center")
treeview.heading("Rate", text="Rate")

treeview.column("#6", width=300, anchor="w")
treeview.heading("Description", text="Description")
treeview.pack(side='left', fill=tk.BOTH, expand=tk.YES)

ttk.Style().configure('Treeview',rowheight=30)

df = pd.read_csv("sample.csv")
for row in df.itertuples(index=True, name='Pandas'):
    treeview.insert('','end', text=row[0], values=row[1:])

#treeview.insert('','end', text='1', values=('2019-7-02', 'Sun', '09:00', '22:00', 'hahaha'))

vsb = ttk.Scrollbar(bottom_pane, orient="vertical", command=treeview.yview)
#vsb.pack(side='right', fill='y')
vsb.pack(side='right', fill=tk.BOTH)
treeview.configure(yscrollcommand=vsb.set)


filename = "sample.xlsx"
book = xl.load_workbook(filename)
sheet = book.worksheets[0]

tk.mainloop()



