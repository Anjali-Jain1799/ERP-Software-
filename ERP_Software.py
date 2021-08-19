from tkinter import *
import mysql.connector
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

# creating an object of tkinter
loginform = Tk()  # Tkinter app for loginpage
USERNAME = StringVar()
PASSWORD = StringVar()

name = ""
dept = ""

loginform.title("Login Page")
loginform.minsize(width=400, height=400)  # Size of application window
loginform.geometry("600x500")
mydb = mysql.connector.connect(host="localhost", user="root", password="sona2158",
                               auth_plugin="mysql_native_password", database="admin")
mycursor = mydb.cursor()


# Class for all the department homepage
class Department:
    def __init__(self, dept_name, table_name, options, col_name):
        global Option0, Option1, Option2, SEARCH
        self.dept_name = dept_name
        self.table_name = table_name
        self.options = options
        self.col_name = col_name
        Option0 = StringVar()
        Option1 = StringVar()
        Option2 = StringVar()
        SEARCH = StringVar()

    def homepage(self):
        global viewform
        viewform = Tk()
        viewform.minsize(width=600, height=400)  # Size of application window
        viewform.geometry("800x700")
        self.ViewForm()

    def ViewForm(self):
        global tree
        viewform.title(self.dept_name)
        TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(viewform, width=100)
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(viewform, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text=self.dept_name, font=('arial', 18), width=600)
        lbl_text.pack(fill=X)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
        lbl_txtsearch.pack(side=TOP, anchor=W)
        sea = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
        sea.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search)
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_search = Button(LeftViewForm, text="Add", command=self.Add)
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Reset", command=self.Reset)
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete)
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Update", command=self.Update)
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Exit", command=self.Exit)
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
        tree = ttk.Treeview(MidViewForm, columns=(self.options[0], self.options[1], self.options[2], self.options[3]),
                            selectmode="extended", height=100, yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading(self.options[0], text=self.options[0], anchor=W)
        tree.heading(self.options[1], text=self.options[1], anchor=W)
        tree.heading(self.options[2], text=self.options[2], anchor=W)
        tree.heading(self.options[3], text=self.options[3], anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=0)
        tree.column('#2', stretch=NO, minwidth=0, width=200)
        tree.column('#3', stretch=NO, minwidth=0, width=120)
        tree.column('#4', stretch=NO, minwidth=0, width=120)
        tree.pack()
        self.DisplayData()

    def Exit(self):
        result = tkMessageBox.askquestion(self.dept_name, 'Are you sure you want to exit?', icon="warning")
        if result == 'yes':
            loginform.deiconify()
            viewform.destroy()

    def DisplayData(self):
        # Database()
        sql = "SELECT * FROM " + self.table_name
        mycursor.execute(sql)
        fetch = mycursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        # mycursor.close()

    def Search(self):
        print(str(SEARCH.get()))
        if SEARCH.get() != "":
            tree.delete(*tree.get_children())
            sql = "SELECT * FROM " + self.table_name + " WHERE " + self.col_name[1] + " LIKE %s"
            mycursor.execute(sql, ('%' + str(SEARCH.get()) + '%',))
            fetch = mycursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            # mycursor.close()

    def Reset(self):
        tree.delete(*tree.get_children())
        self.DisplayData()
        SEARCH.set("")

    def Delete(self):
        if not tree.selection():
            print("ERROR")
        else:
            result = tkMessageBox.askquestion(self.dept_name, 'Are you sure you want to delete this record?',
                                              icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selectitem = contents['values']
                tree.delete(curItem)
                # Database()
                print(selectitem[0])
                sql = "DELETE FROM " + self.table_name + " WHERE " + self.col_name[0] + " = %d"
                mycursor.execute(sql % selectitem[0])
                mydb.commit()
                # mycursor.close()

    def Add(self):
        global addnewform
        addnewform = Toplevel()
        addnewform.title("ERP System/" + self.dept_name + "/Add new")
        addnewform.minsize(width=600, height=400)  # Size of application window
        addnewform.geometry("800x700")
        TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
        TopAddNew.pack(side=TOP, pady=20)
        lbl_text = Label(TopAddNew, text="Add New", font=('arial', 18), width=600)
        lbl_text.pack(fill=X)
        MidAddNew = Frame(addnewform, width=600)
        MidAddNew.pack(side=TOP, pady=50)
        lbl_productname = Label(MidAddNew, text=self.options[1] + ":", font=('arial', 25), bd=10)
        lbl_productname.grid(row=0, sticky=W)
        lbl_qty = Label(MidAddNew, text=self.options[2] + ":", font=('arial', 25), bd=10)
        lbl_qty.grid(row=1, sticky=W)
        lbl_price = Label(MidAddNew, text=self.options[3] + ":", font=('arial', 25), bd=10)
        lbl_price.grid(row=2, sticky=W)
        opt0 = Entry(MidAddNew, textvariable=Option0, font=('arial', 25), width=15)
        opt0.grid(row=0, column=1)
        opt1 = Entry(MidAddNew, textvariable=Option1, font=('arial', 25), width=15)
        opt1.grid(row=1, column=1)
        opt2 = Entry(MidAddNew, textvariable=Option2, font=('arial', 25), width=15)
        opt2.grid(row=2, column=1)
        btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=self.AddNew)
        btn_add.grid(row=3, columnspan=2, pady=20)

    def AddNew(self):
        print("Executed")
        sql = "SELECT MAX(" + self.col_name[0] + ") FROM " + self.table_name
        mycursor.execute(sql)
        fetch = mycursor.fetchone()
        if fetch[0] is None:
            id = 1
        else:
            id = fetch[0] + 1
        # print("INSERT INTO "+self.table_name+" ("+self.col_name[0]+", "+self.col_name[1]+", "+self.col_name[2]+", "+self.col_name[3]+")")
        sql = "INSERT INTO " + self.table_name + " (" + self.col_name[0] + ", " + self.col_name[1] + ", " + self.col_name[2] + ", " + self.col_name[3] + ") VALUES(%s, %s, %s, %s)"
        val = (id, str(Option0.get()), str(Option1.get()), str(Option2.get()))
        mycursor.execute(sql, val)
        mydb.commit()
        Option0.set("")
        Option1.set("")
        Option2.set("")

    def Update(self):
        global selecteditem
        if not tree.selection():
            print("ERROR")
        else:
            result = tkMessageBox.askquestion(self.dept_name, 'Are you sure you want to update this record?',
                                              icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                self.Updateform()

    def Updateform(self):
        global updatenewform
        updatenewform = Toplevel()
        updatenewform.title(self.dept_name + "/Update " + selecteditem[1])
        updatenewform.minsize(width=600, height=400)  # Size of application window
        updatenewform.geometry("800x700")
        TopAddNew = Frame(updatenewform, width=600, height=100, bd=1, relief=SOLID)
        TopAddNew.pack(side=TOP, pady=20)
        lbl_text = Label(TopAddNew, text="Update " + selecteditem[1], font=('arial', 18), width=600)
        lbl_text.pack(fill=X)
        MidAddNew = Frame(updatenewform, width=600)
        MidAddNew.pack(side=TOP, pady=50)
        lbl_productname = Label(MidAddNew, text=self.options[1] + ":", font=('arial', 25), bd=10)
        lbl_productname.grid(row=0, sticky=W)
        lbl_qty = Label(MidAddNew, text=self.options[2] + ":", font=('arial', 25), bd=10)
        lbl_qty.grid(row=1, sticky=W)
        lbl_price = Label(MidAddNew, text=self.options[3] + ":", font=('arial', 25), bd=10)
        lbl_price.grid(row=2, sticky=W)
        productname = Entry(MidAddNew, textvariable=Option0, font=('arial', 25), width=15)
        productname.grid(row=0, column=1)
        productqty = Entry(MidAddNew, textvariable=Option1, font=('arial', 25), width=15)
        productqty.grid(row=1, column=1)
        productprice = Entry(MidAddNew, textvariable=Option2, font=('arial', 25), width=15)
        productprice.grid(row=2, column=1)
        btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=self.UpdateNew)
        btn_add.grid(row=3, columnspan=2, pady=20)

    def UpdateNew(self):

        sql = "UPDATE " + self.table_name + " SET " + self.col_name[1] + " = %s, " + self.col_name[2] + " = %s, " + \
              self.col_name[3] + " = %s WHERE " + self.col_name[0] + " = %s"
        val = (str(Option0.get()), str(Option1.get()), str(Option2.get()), str(selecteditem[0]))
        mycursor.execute(sql, val)
        mydb.commit()
        Option0.set("")
        Option1.set("")
        Option2.set("")


def home():  # After successful login
    loginform.withdraw()
    global page
    if (dept == "inventory"):
        page = Department("Inventory", "inventory", ["Product_ID", "Product Name", "Product_Price", "Product_Qty"],
                          ["idinventory", "pname", "price", "qty"])
        page.homepage()

    elif (dept == "HR"):
        page = Department("Human Resources", "admin_list", ["Admin_ID", "Username", "Password", "Department"],
                          ["id_admin", "username", "password", "department"])
        page.homepage()

    elif (dept == "marketing"):
        page = Department("Marketing", "clients", ["Client_ID", "Client Name", "Contact", "Order"],
                          ["idclient", "cname", "contact", "order"])
        page.homepage()
    else:
        exit()


def Login(event=None):
    global dept
    mydb = mysql.connector.connect(host="localhost", user="root", password="sona2158",
                                   auth_plugin="mysql_native_password", database="admin")
    mycursor = mydb.cursor()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")  # Warning
    else:
        print(USERNAME.get(), PASSWORD.get())
        mycursor.execute("SELECT * FROM `admin_list` WHERE `username` = %s AND `password` = %s",
                         (USERNAME.get(), PASSWORD.get()))  # use %s not?
        if mycursor.fetchone() is not None:
            mycursor.execute("SELECT * FROM `admin_list` WHERE `username` = %s AND `password` = %s",
                             (USERNAME.get(), PASSWORD.get()))
            data = mycursor.fetchone()
            dept = data[3]
            USERNAME.set("")
            PASSWORD.set("")

            lbl_result.config(text="")
            home()  # Successful login

        else:
            lbl_result.config(text="Invalid username or password", fg="red")  # Warning
            USERNAME.set("")
            PASSWORD.set("")
    mycursor.close()


global lbl_result
TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
TopLoginForm.pack(side=TOP, pady=20)
lbl_text = Label(TopLoginForm, text="Login", font=('arial', 18), width=600)
lbl_text.pack(fill=X)
MidLoginForm = Frame(loginform, width=600)
MidLoginForm.pack(side=TOP, pady=50)  # pady is space here
lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 25), bd=18)
lbl_username.grid(row=0)
lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 25), bd=18)
lbl_password.grid(row=1)
lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
lbl_result.grid(row=3, columnspan=2)  # invalid username and pass msg0
username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
username.grid(row=0, column=1)
password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
password.grid(row=1, column=1)
btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=30, command=Login)
btn_login.grid(row=2, columnspan=2, pady=20)
btn_login.bind('<Return>', Login)

loginform.mainloop()
