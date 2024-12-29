import tkinter as tk
from tkinter import  messagebox
from tkinter import  ttk
import tkinter.font as tkFont
import database as db
import subprocess
import datetime as dt

DAY_SUMARY = 0
DAY_INCOME = 0
SUMARY = 0
INCOME = 0
LINES = 0
BILL_TEXT = []
LOG_FILE_TEXT = []
BILL_TEXT.append("************Կտրոն************\n")
date_day = dt.datetime.now()
d_day = date_day.strftime("%d.%m.%y")
LOG_FILE = "LOG_"+d_day+"_.txt"

font_printer = {
    "height": 11,
}

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def on_close():
    response=messagebox.askyesno("Հարցում ","Ցանկանո՞ւմ եք Փակել ծրագիրը ")
    if response:
	    window.destroy()

# def save_log():
# 	myfile = open(LOG_FILE,"a")
# 	myfile.write(DAY_INCOME)
# 	myfile.close()


window = tk.Tk()
window.protocol('WM_DELETE_WINDOW',on_close)
img = tk.PhotoImage("logo.ico")
#window.iconphoto(True,img)
window.tk.call('wm', 'iconphoto', window._w, img)

# define font size for listbox and combobox
bigfont = tkFont.Font(family="Arial LatArm",size=16)
window.option_add("*TCombobox*Listbox*Font", bigfont)
window.call('encoding', 'system', 'utf-8')
window.title("MyMarket")
#window.geometry("800x500+500+100")  
#window.attributes('-fullscreen', True)
window.resizable(False, False)
width= window.winfo_screenwidth()               
height= window.winfo_screenheight()               
window.geometry("%dx%d-1+0" %(width, height-50))

login_type = ["Ղեկավար","Վաճառող"]

password = {"Ղեկավար": 4321, "Վաճառող": 1234}

login_f = tk.Frame(window)
admin_f = tk.Frame(window)
user_f = tk.Frame(window)
login_f.pack(padx=50, pady=50)

frames = {"Ղեկավար": admin_f, "Վաճառող": user_f,"Մուտք": login_f}
frame_state = "Մուտք"

def callback(product_entres_obj):
	if product_entres_obj[0].get() != '':
		output = db.search_product(product_entres_obj)
		if output:
			#print(output)
			for l in range(1,len(product_entres_obj)):
				product_entres_obj[l].delete(0,tk.END)
				product_entres_obj[l].insert(0,output[0][l])
			if product_entres_obj[4].get()=='-':
				product_entres_obj[5].delete(0,tk.END)
			else:
				product_entres_obj[4].delete(0,tk.END)
		else:
			pass
			#messagebox.showerror("Փնտրման սխալ", "Product not found. ")

#widget clear event 
def clear_event(event):
	global SUMARY, LINES, BILL_TEXT, LOG_FILE_TEXT, INCOME
	SUMARY = 0
	INCOME = 0
	LINES = 0
	BILL_TEXT = []
	LOG_FILE_TEXT = []
	BILL_TEXT.append("************Կտրոն************\n")
	bill_list.delete(0,tk.END)
	general_l.config(text="Ընդամենը: ")
	general_l_user.config(text="Ընդամենը: ")
	bill_list_user.delete(0,tk.END)
	for  t in product_entres_obj:
		t.delete(0,tk.END)
	for  t in product_entres_obj_user:
		t.delete(0,tk.END)
	password_entry.delete(0, tk.END)

def cheak_entery():
	if frame_state == "Ղեկավար":
		for i in product_entres_obj:
			if i.get() == '':
				return 0
			else : return 1
	elif frame_state == "Վաճառող":
		for i in product_entres_obj_user:
			if i.get() == '':
				return 0
			else : return 1		
	else: pass

def bill_fill(product_entres_obj,product_entres,bill_list_par):
	bill_list.delete(0,tk.END)
	output = db.search_product(product_entres_obj)
	if output:
		k = 0
		for l in output[0] if frame_state == "Ղեկավար" else output[0][:-1]:
			bill_list_par.insert(tk.END, f"{product_entres[k]}|{l}")
			k+=1
	else:
		messagebox.showerror("Փնտրման սխալ", "Ապրանք չի գտնվել: ")

def update_product(product_entres_obj):
	bar_c = product_entres_obj[0].get()
	product_e = tuple(product_entres_obj[i].get() for i in range(1,len(product_entres_obj)))
	product_e = product_e +(bar_c,)
	db.update_product_db(product_e)
	for  t in product_entres_obj: t.delete(0,tk.END)

def sell_calculation(product_entres_obj,product_entres,bill_list_par,general_l_par):
	global SUMARY, BILL_TEXT, LOG_FILE_TEXT, LINES, INCOME
	if SUMARY == 0: 
		bill_list.delete(0,tk.END)
		bill_list_user.delete(0,tk.END)
	req = list(val.get() for val in product_entres_obj)
	dic1 = dict(zip(product_entres, req))
	search = list(db.search_product(product_entres_obj)[0])
	dic2 = dict(zip(product_entres, search))
	if dic1['քաշը :'] == '-':
		if is_number(dic1['քանակը :']) and is_number(dic2['քանակը :']) and is_number(dic1['գինը :']):
			if float(dic2['քանակը :']) >= float(dic1['քանակը :']):
				val = float(dic2['քանակը :']) - float(dic1['քանակը :'])
				temp = float(dic1['գինը :']) * float(dic1['քանակը :'])
				temp_p = (float(dic1['գինը :'])-float(dic1['ինքնարժեք :']))* float(dic1['քանակը :'])
				SUMARY += temp
				INCOME += temp_p
				line = f"{dic1['անունը :']}   {dic1['քանակը :']} հատ  {temp} դր"
				line2 = f"{dic1['անունը :']}   {dic1['քանակը :']} հատ  {temp} դր  եկամուտ {temp_p} դր\n"
				BILL_TEXT.append(line+"\n")
				LOG_FILE_TEXT.append(line2)
				bill_list_par.insert(tk.END, line)
				db.update_product_after_sell(dic2['կոդը :'],dic2['քաշը :'],val)
			else: 
				messagebox.showerror("Փնտրման սխալ", "Ապրանքը վերջացել է: ")
				
		else:
			messagebox.showerror("Փնտրման սխալ", "Դաշտը լրացրեք թվով: ")
	else:
		if is_number(dic1['քաշը :']) and is_number(dic2['քաշը :']) and is_number(dic1['գինը :']):
			if float(dic2['քաշը :']) >= float(dic1['քաշը :']):
				val = float(dic2['քաշը :']) - float(dic1['քաշը :'])
				temp = float(dic1['գինը :']) * float(dic1['քաշը :'])
				temp_p = (float(dic1['գինը :']) - float(dic1['ինքնարժեք :']))* float(dic1['քաշը :'])
				SUMARY += temp
				INCOME += temp_p
				line = f"{dic1['անունը :']}   {dic1['քաշը :']} կգ  {temp} դր"
				line2 = f"{dic1['անունը :']}   {dic1['քանակը :']} հատ  {temp} դր  եկամուտ {temp_p} դր\n"
				BILL_TEXT.append(line+"\n")
				LOG_FILE_TEXT.append(line2)
				bill_list_par.insert(tk.END, line)
				db.update_product_after_sell(dic2['կոդը :'],val,dic2['քանակը :'])
			else:
				messagebox.showerror("Փնտրման սխալ", "Ապրանքը վերջացել է: ")
		else:
			messagebox.showerror("Փնտրման սխալ", "Դաշտը լրացրեք թվով: ")
	for  t in product_entres_obj: t.delete(0,tk.END)
	general_l_par.config(text = "Ընդամենը: " + str(SUMARY))
	
def pay_print():
	global BILL_TEXT, SUMARY,DAY_SUMARY, LOG_FILE, LOG_FILE_TEXT, DAY_INCOME
	BILL_TEXT.append("______________________\n")
	BILL_TEXT.append(f"Ընդամենը: {str(SUMARY)}\n")
	date = dt.datetime.now()
	d = date.strftime("\n*******%d.%m.%y %H:%M*******\n")
	BILL_TEXT.append(d)
	BILL_TEXT.append("******Շնորհակալություն💓******")
	txt =''
	for i in BILL_TEXT:
		txt +=i
	print(txt)
	with open("print.txt","w") as p:
		res = p.writelines(txt)
	subprocess.Popen('lpr print.txt', shell=True)
	DAY_SUMARY += SUMARY
	DAY_INCOME += INCOME
	LOG_FILE_TEXT.append("Ընդհանուր "+str(SUMARY)+" եկամուտ "+str(INCOME) + " " + d+"\n")
	myfile = open(LOG_FILE,"a")
	myfile.writelines(LOG_FILE_TEXT)
	myfile.close()
	window.event_generate("<<clear>>")
	pass


window.bind("<<change_frame>>",clear_event)
window.bind("<<clear>>",clear_event)
window.bind("<<login_error>>",clear_event)

def password_cheaker():
	log = login_entry.get()
	try:
	   pas = int(password_entry.get())
	   if log in password and int(pas) == password[log]:
		   change_frame(log)
	   else:
		   messagebox.showerror("Մուտքի սխալ ", "Մուտքը արգելված է! \n Գաղտնաբառը սխալ է:")
		   window.event_generate("<<login_error>>")
	except ValueError:
	   messagebox.showerror("Արժեքի սխալ ", "Արժեքը թիվ չէ!")
	   window.event_generate("<<login_error>>")

def change_frame(login):
	global frame_state
	frames[frame_state].forget()
	window.event_generate("<<change_frame>>")
	frames[login].pack(padx=40,pady=40)
	frame_state = login
	#messagebox.showinfo("info", frame_state)

def enter_key_pressed(event):
	password_cheaker()

def error_print():
	messagebox.showerror("Արժեքի սխալ", "Դաշտերը լրացրեք: ")

# login frame content
login_entry = ttk.Combobox(login_f, width=50, values=login_type,font =bigfont, state="readonly")
login_entry.current(1)
login_entry.pack(padx= 5, pady=5)
password_entry = tk.Entry(login_f, show="*",width=50, border=1, borderwidth=2, bg="turquoise", font =bigfont)
password_entry.pack(padx= 5, pady=5)
password_entry.bind("<Return>",enter_key_pressed)
login_b = tk.Button(login_f,bg="turquoise" ,text="Մուտք",command= password_cheaker, height= 2,width=6, font =bigfont)
login_b.pack()

#product name entry content
product_entres =["կոդը :","անունը :","տեսակը :","գինը :", "քաշը :","քանակը :","ինքնարժեք :"]
product_frame_obj = []
product_label_obj = []
product_entres_obj = []

for i in product_entres:
	frame= tk.Frame(admin_f)
	frame.pack(fill=tk.X)
	product_frame_obj.append(frame)
	label = tk.Label(frame,text=i,font =bigfont)
	label.pack(side=tk.LEFT, padx=5, pady=5)
	product_label_obj.append(label)
	entry = tk.Entry(frame,width=30,border=1,borderwidth=2, bg="turquoise", font =bigfont)
	entry.pack(fill= tk.X, padx=5, expand=True)
	product_entres_obj.append(entry)

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv:callback(product_entres_obj))
product_entres_obj[0].config(textvariable=sv)


#apply buttons 
btn_frame = tk.Frame(admin_f)
btn_frame.pack()
back_b = tk.Button(btn_frame,text = "Հետ", bg = "turquoise", command=lambda: change_frame("Մուտք"),font =bigfont)
back_b.pack(side=tk.LEFT,padx= 5, pady=5)
apply_b = tk.Button(btn_frame,text = "Ավելացնել", bg = "turquoise",  font =bigfont,command=lambda: db.insert_product(product_entres_obj))
apply_b.pack(side=tk.LEFT,padx= 5, pady=5)
update_b = tk.Button(btn_frame,text = "Թարմացնել", bg = "turquoise",  font =bigfont,command=lambda: update_product(product_entres_obj))
update_b.pack(side=tk.LEFT,padx= 5, pady=5)
search_b = tk.Button(btn_frame,text = "Փնտրել", bg = "turquoise",  font =bigfont,command=lambda: bill_fill(product_entres_obj,product_entres,bill_list))
search_b.pack(side=tk.LEFT,padx= 5, pady=5)
delete_b = tk.Button(btn_frame,text = "Ջնջել", bg = "turquoise",  font =bigfont,command=lambda: db.delete_product(product_entres_obj))
delete_b.pack(side=tk.LEFT,padx= 5, pady=5)
sell_b = tk.Button(btn_frame,text = "Վաճառք", bg = "turquoise",  font =bigfont,command= lambda:sell_calculation(product_entres_obj,product_entres,bill_list,general_l) if cheak_entery() else error_print())
sell_b.pack(side=tk.LEFT,padx= 5, pady=5)
pay_b = tk.Button(btn_frame,text = "Վճարել", bg = "turquoise",  font =bigfont,command= pay_print)
pay_b.pack(side=tk.LEFT,padx= 5, pady=5)

#cheak (bill) design implementation
bill_frame = tk.Frame(admin_f)
bill_frame.pack()
clear_b = tk.Button(bill_frame,text = "Մաքրել", bg = "turquoise",  font =bigfont,command=lambda : window.event_generate("<<clear>>"))
clear_b.pack( padx= 5, pady=5)
general_l = tk.Label(bill_frame,text="Ընդամենը: ",font =bigfont)
general_l.pack()
scrollbar = tk.Scrollbar(bill_frame)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
bill_list = tk.Listbox(bill_frame, font=bigfont,yscrollcommand=scrollbar.set,width=50,height=16, justify="center")
bill_list.pack()
scrollbar.config(command=bill_list.yview)

#user frame content
product_frame_obj_user = []
product_label_obj_user = []
product_entres_obj_user = []

for i in product_entres:
	frame= tk.Frame(user_f)
	frame.pack(fill=tk.X)
	product_frame_obj_user.append(frame)
	label = tk.Label(frame,text=i,font =bigfont)
	label.pack(side=tk.LEFT, padx=5, pady=5)
	product_label_obj_user.append(label)
	entry = tk.Entry(frame, width=30, border=1,borderwidth=2, bg="turquoise", font =bigfont)
	entry.pack(fill= tk.X, padx=5, expand=True)
	product_entres_obj_user.append(entry)

product_label_obj_user[6].forget()
product_entres_obj_user[6].forget()

svu = tk.StringVar()
svu.trace("w", lambda name, index, mode, svu=svu:callback(product_entres_obj_user))
product_entres_obj_user[0].config(textvariable=svu)

# user buttons
btn_frame_user = tk.Frame(user_f)
btn_frame_user.pack()
back_b_user = tk.Button(btn_frame_user,text = "Հետ", bg = "turquoise",font =bigfont, command=lambda:change_frame("Մուտք"))
back_b_user.pack(side=tk.LEFT,padx= 5, pady=5)
search_b_user = tk.Button(btn_frame_user,text = "Փնտրել", bg = "turquoise",  font =bigfont,command=lambda: bill_fill(product_entres_obj_user,product_entres,bill_list_user))
search_b_user.pack(side=tk.LEFT,padx= 5, pady=5)
sell_b_user = tk.Button(btn_frame_user,text = "Վաճառք", bg = "turquoise",  font =bigfont,command= lambda:sell_calculation(product_entres_obj_user,product_entres,bill_list_user,general_l_user) if cheak_entery() else error_print())
sell_b_user.pack(side=tk.LEFT,padx= 5, pady=5)
pay_b_user= tk.Button(btn_frame_user,text = "Վճարել", bg = "turquoise",  font =bigfont,command= pay_print)
pay_b_user.pack(side=tk.LEFT,padx= 5, pady=5)

#bill list show user
bill_frame_user = tk.Frame(user_f)
bill_frame_user.pack()
clear_b_user = tk.Button(bill_frame_user,text = "Մաքրել", bg = "turquoise",  font =bigfont,command=lambda : window.event_generate("<<clear>>"))
clear_b_user.pack( padx= 5, pady=5)
general_l_user = tk.Label(bill_frame_user,text="Ընդամենը: ",font =bigfont)
general_l_user.pack(padx= 5, pady=5)
scrollbar_user = tk.Scrollbar(bill_frame_user)
scrollbar_user.pack(side=tk.RIGHT,fill=tk.Y)
bill_list_user = tk.Listbox(bill_frame_user, font=bigfont,yscrollcommand=scrollbar.set,width=50,height=16, justify="center")
bill_list_user.pack()
scrollbar_user.config(command=bill_list.yview)

window.mainloop()
