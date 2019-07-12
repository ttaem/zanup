import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox as msg
from tkinter import filedialog
#import TkUtil
#import TkUtil.Dialog

import datetime
from datetime import date
import pandas as pd

import openpyxl as xl
from openpyxl.styles import Border, Side, Alignment

from pathlib import Path
import configparser


g_config = configparser.ConfigParser()

g_month = 1
g_department = "1sil"
g_name = "cklee"
global df


def ok_pref(pref_win):
    print("save...")
    g_config['FILE']['GenerationFilePath'] = gen_var.get()
    g_config['FILE']['SaveFilePath'] = save_var.get()
    g_config['USER']['Name'] = name_var.get()
    g_config['USER']['Position'] = pos_var.get()
    g_config['USER']['Department'] = depart_var.get()
    g_config['ETC']['Language'] = lang_var.get()
    with open('config.ini', 'w') as configfile:
        g_config.write(configfile)


    pref_win.destroy()

def cancel_pref(pref_win):
    pref_win.destroy()
    print("cancel...")

def create_pref_window():
    pref_win = tk.Toplevel(master)
    pref_win.title("Preference")
    pref_win.transient(master)
    pref_win.grab_set()

    file_info_pane = tk.LabelFrame(pref_win, text="File Info")
    user_info_pane = tk.LabelFrame(pref_win, text="User Info")
    etc_info_pane = tk.LabelFrame(pref_win, text="Etc Info")

    file_info_pane.pack(side=tk.TOP, fill=tk.X)
    user_info_pane.pack(side=tk.TOP, fill=tk.X)
    etc_info_pane.pack(side=tk.TOP, fill=tk.X)

    global gen_var, save_var, name_var, pos_var, depart_var, lang_var

    gen_var = tk.StringVar(file_info_pane)
    gen_var.set(g_config['FILE']['GenerationFilePath'])
    gen_label = tk.Label(file_info_pane, text="Generation File Path:")
    gen_label.grid(column=0, row=0, sticky='W')
    gen_entry = tk.Entry(file_info_pane, textvariable=gen_var)
    gen_entry.grid(column=0, row=1, sticky='WE')
    gen_button = tk.Button(file_info_pane, text="Change", command=lambda: directory_select(gen_var))
    gen_button.grid(column=1, row=1, sticky='WE')
    gen_separator = ttk.Separator(file_info_pane, orient='horizontal')
    gen_separator.grid(row=2,columnspan=2, stick='WE')
    file_info_pane.grid_columnconfigure(0, weight=1)

    save_var = tk.StringVar(file_info_pane)
    save_var.set(g_config['FILE']['SaveFilePath'])
    save_label = tk.Label(file_info_pane, text="Save File Path:")
    save_label.grid(column=0, row=3, sticky='W')
    save_entry = tk.Entry(file_info_pane, textvariable=save_var)
    save_entry .grid(column=0, row=4, sticky='WE')
    save_button = tk.Button(file_info_pane, text="Change", command=lambda: directory_select(save_var))
    save_button.grid(column=1, row=4, sticky='E')

    name_var = tk.StringVar(user_info_pane)
    name_var.set(g_config['USER']['Name'])
    name_label = tk.Label(user_info_pane, text="Name:")
    name_label.grid(column=0, row=0, sticky='WE')
    name_entry = tk.Entry(user_info_pane, textvariable=name_var)
    name_entry.grid(column=1, row=0, sticky='WE')

    pos_var = tk.StringVar(user_info_pane)
    pos_var.set(g_config['USER']['Position'])
    pos_label = tk.Label(user_info_pane, text="Position:")
    pos_label.grid(column=0, row=1, sticky='WE')
    pos_entry = tk.Entry(user_info_pane, textvariable=pos_var)
    pos_entry.grid(column=1, row=1, sticky='WE')

    depart_var = tk.StringVar(user_info_pane)
    depart_var.set(g_config['USER']['Department'])
    depart_label = tk.Label(user_info_pane, text="Department:")
    depart_label.grid(column=0, row=2, sticky='WE')
    depart_entry = tk.Entry(user_info_pane, textvariable=depart_var)
    depart_entry.grid(column=1, row=2, sticky='WE')

    user_info_pane.grid_columnconfigure(1, weight=1)

    lang_var = tk.StringVar(etc_info_pane)
    lang_var.set(g_config['ETC']['Language'])
    lang_label = tk.Label(etc_info_pane, text="Language:")
    lang_label.grid(column=0, row=0, sticky='WE')
    lang_choices = {'ko_KR', 'C'}
    lang_choices = sorted(lang_choices)
    lang_pop = tk.OptionMenu(etc_info_pane, lang_var, *lang_choices)
    lang_pop.grid(column=1, row=0, sticky='WE')


    ok_button = tk.Button(pref_win, text="OK", command=lambda: ok_pref(pref_win))
    cancel_button = tk.Button(pref_win, text="Cancel", command=lambda: cancel_pref(pref_win))
    ok_button.pack(side=tk.TOP, fill=tk.X)
    cancel_button.pack(side=tk.TOP, fill=tk.X)

def read_config():
    my_file = Path("./config.ini")
    if my_file.is_file():
        print("config file already exist")
        g_config.read("./config.ini")
    else:
        print("config file not exist")
        #config = configparser.ConfigParser()
        g_config['FILE'] = {'GenerationFilePath': './',
                             'SaveFilePath': './'}
        g_config['USER'] = {'Name': 'Hong gildong',
                             'Position': 'bastard',
                             'Department': 'Korea'}
        g_config['ETC'] = {'Language': 'C'}
        with open('config.ini', 'w') as configfile:
            g_config.write(configfile)

def read_csv(month):
    global df
    filename_f = '{month}M_zanup_{department}_{name}.csv'
    filename = filename_f.format(month=month, department=g_config['USER']['Department'], name=g_config['USER']['Name'])
    print(filename)
    my_file = Path(g_config['FILE']['SaveFilePath'] + filename)
    if my_file.is_file():
        df = pd.read_csv(my_file)
    else:
        df = pd.DataFrame(columns=['date', 'week', 'start', 'end', 'rate', 'desc'])




def save_df():
    print("save")
    filename_f = '{month}M_zanup_{department}_{name}.csv'
    filename = filename_f.format(month=g_month, department=g_config['USER']['Department'], name=g_config['USER']['Name'])
    print(filename)
    df.to_csv(filename, index=False)


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
    if df_count == 0:
        return
    sheet.insert_rows(7, amount=df_count)
    #sheet["C30"].border=thin_border 
    print("insert " + str(df_count))

    for index, df_row in df.iterrows():
        sheet["B"+str(index+7)] = g_config['USER']['Name']
        sheet["C"+str(index+7)] = g_config['USER']['Position']
        sheet["D"+str(index+7)] = g_config['USER']['Department']
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

    filename_f = '{month}M_zanup_{department}_{name}.xlsx'
    filename = filename_f.format(month=g_month, department=g_config['USER']['Department'], name=g_config['USER']['Name'])
    print(filename)

    book.save(filename)


def insert_row():
    global df

    if len(desc_text.get("1.0", 'end-1c')) == 0:
        msg.showerror("New Entry Insertion", "Please, Insert description!!!")
        return

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
    if cur is None:
        print("None just return")
    index = treeview.index(cur)
    print("cur:")
    print(cur)
    print("index:" + str(index))
    print(df)
    df_count = df.shape[0]
    if (df_count == 0):
        print("DF size is 0, just return")
        return
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

def directory_select(var):
    path = filedialog.askdirectory()
    print(path)
    var.set(path)


read_config()
today = date.today()
g_month = int(today.strftime('%m'))
print(g_month)

read_csv(g_month)

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
setting_menu.add_command(label="Preference", command=create_pref_window)
menu_bar.add_cascade(label="Setting", menu=setting_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help")
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help", menu=help_menu)

master.config(menu=menu_bar)

upper_pane = tk.PanedWindow(master)
#bottom_pane =  tk.PanedWindow(master)
bottom_pane =  tk.LabelFrame(master, text="Work List", font="Arial 20")
bottom_pane.configure(text="List of " + str(g_month)) 
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
start_choices = {'07', '08', '09', '10', '11', '12'}
start_choices = sorted(start_choices)
start_pop = tk.OptionMenu(insert_pane, start_var, *start_choices)
start_pop.grid(row=0, column=2, stick='W')

during_label = tk.Label(insert_pane, text="~")
during_label.grid(row=0, column=3)

end_var = tk.StringVar(insert_pane)
end_var.set('21')
end_choices = {'16','17','18','19','20','21','22','23','24'}
end_choices = sorted(end_choices)
end_pop = tk.OptionMenu(insert_pane, end_var, *end_choices)
end_pop.grid(row=0, column=4)

#end_label = tk.Label(insert_pane, text="22:00")
#end_label.grid(row=0, column=2)
rate_var = tk.StringVar(insert_pane)
rate_var.set('A')
rate_choices = {'A','B','C','D'}
rate_choices = sorted(rate_choices)
rate_pop  = tk.OptionMenu(insert_pane, rate_var, *rate_choices)
#level_label.grid(row=0, column=3, sticky="E")
rate_pop.grid(row=0, column=5, padx=10)
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

csv_file = Path("./config.ini")

#df = pd.read_csv("sample.csv")
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

read_config()

tk.mainloop()



