from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time
class SMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1980x1080+0+0")
        self.root.title("Shop Management System")
        self.root.config(bg="white")

        # title
        self.icon_title= PhotoImage(file= "images/logo1.png")
        title= Label(self.root, text="Shop Management System", image=self.icon_title, compound= LEFT ,font=("times new roman", 40, "bold"), bg="seagreen", fg="white",anchor="w",padx=20).place(x=0, y=0, relwidth=1, height=70)

        # button
        btn_logout= Button(self.root, text="Logout", font=("Times new roman", 15,"bold"),bg="skyblue",width=10, cursor="hand2").place(x=1720, y=15)

        # clock
        self.lbl_clock= Label(self.root, text=" Welcome to Shop Management System \t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS",font=("times new roman", 10), bg="lightgreen", fg="black")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # left menu
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo= self.MenuLogo.resize((200,200))
        self.MenuLogo= ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu= Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=100, width=200, height=939)

        lbl_menuLogo= Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        self.icon_side= PhotoImage(file= "images/side.png")
        lbl_menu= Label(LeftMenu, text="MENU", font=("Times new roman", 15),bg="skyblue").pack(side=TOP, fill=X)
        btn_employee= Button(LeftMenu, text="Employee", image=self.icon_side, compound= LEFT, anchor="w", padx=10,font=("Times new roman", 15),bg="green",border=2, cursor="hand2",command= self.employee).pack(side=TOP, fill=X)
        btn_supplier= Button(LeftMenu, text="Supplier", image=self.icon_side, compound= LEFT, anchor="w", padx=10,font=("Times new roman", 15),bg="green",border=2, cursor="hand2", command= self.supplier).pack(side=TOP, fill=X)
        btn_category= Button(LeftMenu, text="Category", image=self.icon_side, compound= LEFT, anchor="w", padx=10,font=("Times new roman", 15),bg="green",border=2, cursor="hand2", command= self.category).pack(side=TOP, fill=X)
        btn_product= Button(LeftMenu, text="Product", image=self.icon_side, compound= LEFT, anchor="w", padx=10,font=("Times new roman", 15),bg="green",border=2, cursor="hand2", command=self.product).pack(side=TOP, fill=X)
        btn_sales= Button(LeftMenu, text="Sales", image=self.icon_side, compound= LEFT, anchor="w", padx=10,font=("Times new roman", 15),bg="green",border=2, cursor="hand2", command=self.sales).pack(side=TOP, fill=X)
        btn_exit= Button(LeftMenu, text="Exit", image=self.icon_side, compound= LEFT, anchor="w", padx=10,font=("Times new roman", 15),bg="green",border=2, cursor="hand2").pack(side=TOP, fill=X)
        
        # content
        self.lbl_employee = Label(self.root, text="Total Employee\n [0]", fg="white", bg="seagreen", bd=5, relief=RIDGE , font=("times new roman",20,"bold"))
        self.lbl_employee.place(x=230,y= 170, height=200, width=306)

        self.lbl_supplier = Label(self.root, text="Total Suppliers\n [0]", fg="white", bg="seagreen", bd=5, relief=RIDGE , font=("times new roman",20,"bold"))
        self.lbl_supplier.place(x=566,y= 170, height=200, width=306)

        self.lbl_category = Label(self.root, text="Total Category\n [0]", fg="white", bg="seagreen", bd=5, relief=RIDGE , font=("times new roman",20,"bold"))
        self.lbl_category.place(x=902,y= 170, height=200, width=306)

        self.lbl_product = Label(self.root, text="Total Products\n [0]", fg="white", bg="seagreen", bd=5, relief=RIDGE , font=("times new roman",20,"bold"))
        self.lbl_product.place(x=1238,y= 170, height=200, width=306)

        self.lbl_sales = Label(self.root, text="Total Sales\n [0]", fg="white", bg="seagreen", bd=5, relief=RIDGE , font=("times new roman",20,"bold"))
        self.lbl_sales.place(x=1574,y= 170, height=200, width=306)

        # footer
        lbl_footer= Label(self.root, text="SHOP MANAGEMENT SYSTEM | Developed by CS-AIML-B-11",font=("times new roman", 10), bg="lightgreen", fg="black").pack(side=BOTTOM, fill=X)
        self.update_content()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def employee(self):
       self.new_win= Toplevel(self.root)
       self.new_obj= employeeClass(self.new_win)
       
    def supplier(self):
       self.new_win= Toplevel(self.root)
       self.new_obj= supplierClass(self.new_win)
       
    def category(self):
       self.new_win= Toplevel(self.root)
       self.new_obj= categoryClass(self.new_win)
       
    def product(self):
       self.new_win= Toplevel(self.root)
       self.new_obj= productClass(self.new_win)
       
    def sales(self):
       self.new_win= Toplevel(self.root)
       self.new_obj= salesClass(self.new_win)

    def update_content(self):
       con = sqlite3.connect(database="shop management system.db")
       cur = con.cursor()
       try:
          cur.execute("select * from product")
          product=cur.fetchall()
          self.lbl_product.config(text=f"Total Products\n[ {str(len(product))} ]")
          
          cur.execute("select * from supplier")
          supplier=cur.fetchall()
          self.lbl_supplier.config(text=f"Total Suppliers\n[ {str(len(supplier))} ]")
          
          cur.execute("select * from category")
          category=cur.fetchall()
          self.lbl_category.config(text=f"Total Categories\n[ {str(len(category))} ]")
          
          cur.execute("select * from employee")
          employee=cur.fetchall()
          self.lbl_employee.config(text=f"Total Employees\n[ {str(len(employee))} ]")
          
          bill=len(os.listdir('bill'))
          self.lbl_sales.config(text=f'Total Sales\n[{str(bill)}]')
          
          time_=time.strftime("%I:%M:%S")
          date_=time.strftime("%d-%m-%Y")
          self.lbl_clock.config(text=f" Welcome to Shop Management System \t\t Date: {str(date_)}\t\t Time: {str(time_)}")
          self.lbl_clock.after(200,self.update_content)
          
       except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)
          

           
       
if __name__=="__main__":
  root= Tk()
  obj=SMS(root)
  root.mainloop()