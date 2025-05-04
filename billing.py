from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1980x1080+0+0")
        self.root.title("Shop Management System")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        
        # title
        self.icon_title= PhotoImage(file= "images/logo1.png")
        title= Label(self.root, text="Shop Management System", image=self.icon_title, compound= LEFT ,font=("times new roman", 40, "bold"), bg="seagreen", fg="white",anchor="w",padx=20).place(x=0, y=0, relwidth=1, height=70)

        # button
        btn_logout= Button(self.root, text="Logout", font=("Times new roman", 15,"bold"),bg="skyblue",width=10, cursor="hand2").place(x=1720, y=15)

        # clock
        self.lbl_clock= Label(self.root, text=" Welcome to Shop Management System \t\t Date: DD-MM-YYYY \t\t Time: HH:MM:SS",font=("times new roman", 10), bg="lightgreen", fg="black")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        
        
    # --------Product frame---------\\
        # variables
        self.var_search=StringVar()

        ProductFrame1= Frame(self.root, bd=4, bg="white", relief=RIDGE)
        ProductFrame1.place(x=0, y=106, width=640, height=920)
        
        pTitle=Label(ProductFrame1, text="All Products", font=("goudy old style",20), bg="#262626", fg="white").pack(side= TOP, fill=X)
        
        
        # --------------------Product search frame------------------------
        ProductFrame2= Frame(ProductFrame1, bd=4, bg="white", relief=RIDGE)
        ProductFrame2.place(x=2, y=40, width=630, height=120)
        
        lbl_search=Label(ProductFrame2, text="Search Products | By Name ", font=("times new roman", 15, "bold"), bg="white", fg="green").place(x=2,y=5) 
        lbl_search=Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15), bg="white", fg="green").place(x=135,y=50,width=350, height=22)
        
        btn_search= Button(ProductFrame2, text="Search", font=("goudy old style",15), bg="#2196f3",fg="white", cursor="hand2", command=self.search).place(x=500,y=49, width=100, height=25)
        btn_show_all= Button(ProductFrame2, text="Show All", font=("goudy old style",15), bg="#083531",fg="white", cursor="hand2", command=self.show).place(x=500,y=19, width=100, height=25)
        
        # -------------------Product details frame------
        ProductFrame3=Frame(ProductFrame1, bd=3, relief= RIDGE)
        ProductFrame3.place(x=4,y=165, width=630, height=720)

        scrolly= Scrollbar(ProductFrame3, orient= VERTICAL)
        scrollx= Scrollbar(ProductFrame3, orient= HORIZONTAL)

        self.product_Table= ttk.Treeview(ProductFrame3, columns=("pid","name","price","qty","status"), yscrollcommand=scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side= BOTTOM, fill=X)
        scrolly.pack(side= RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="P ID ")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Qty")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        
        self.product_Table.column("pid", width=90)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=100)
        self.product_Table.column("status", width=100)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        # self.show()
        
        lbl_note= Label(ProductFrame1, text="Note: 'Enter 0 qty. to remove product from the Cart'", font=("goudy old style",15), bg="white", fg="red").pack(side=BOTTOM, fill=X)


    #-------------------------------Customer frame-----------------------------------------------------------------#

        #  variables
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        
        CustomerFrame= Frame(self.root, bd=4, bg="white", relief=RIDGE)
        CustomerFrame.place(x=645, y=106, width=640, height=90)
        
        cTitle=Label(CustomerFrame, text="Customer Details", font=("goudy old style",15), bg="lightgrey").pack(side= TOP, fill=X)
        
        lbl_name=Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13), bg="white", fg="green").place(x=80,y=37,width=190, height=22)
        
        lbl_contact=Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=300,y=35)
        txt_contact=Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13), bg="white", fg="green").place(x=410,y=37,width=190, height=22)
        
        
        # ------------cal cart frame---------
        Cal_Cart_Frame= Frame(self.root, bd=2, bg="white", relief=RIDGE)
        Cal_Cart_Frame.place(x=645, y=200, width=640, height=670)
        
        # ----------calculator frame------
        self.var_cal_input= StringVar()
        Cal_Frame= Frame(Cal_Cart_Frame, bd=5, bg="white", relief=RIDGE)
        Cal_Frame.place(x=5, y=5, width=318, height=659)
        
        txt_cal_input=Entry(Cal_Frame, textvariable= self.var_cal_input, font=("arial",15,"bold"), width=26, bd=10,relief=GROOVE, state="readonly", justify=RIGHT)
        txt_cal_input.grid(row=0, columnspan=4, pady=30)
        
        btn_c=Button(Cal_Frame, text='C', font=("arial", 15, "bold"), command=self.clear_cal, bd=5,width=5, pady=20, cursor="hand2").grid( row=1, column=3)
        
        btn_7=Button(Cal_Frame, text='7', font=("arial", 15, "bold"), command=lambda:self.get_input(7), bd=5,width=5, pady=20, cursor="hand2").grid( row=2, column=0)
        btn_8=Button(Cal_Frame, text='8', font=("arial", 15, "bold"),command=lambda:self.get_input(8), bd=5,width=5, pady=20, cursor="hand2").grid( row=2, column=1)
        btn_9=Button(Cal_Frame, text='9', font=("arial", 15, "bold"),command=lambda:self.get_input(9), bd=5,width=5, pady=20, cursor="hand2").grid( row=2, column=2)
        btn_sum=Button(Cal_Frame, text='+', font=("arial", 15, "bold"),command=lambda:self.get_input('+'), bd=5,width=5, pady=20, cursor="hand2").grid( row=2, column=3)
        
        btn_4=Button(Cal_Frame, text='4', font=("arial", 15, "bold"),command=lambda:self.get_input(4), bd=5,width=5, pady=20, cursor="hand2").grid( row=3, column=0)
        btn_5=Button(Cal_Frame, text='5', font=("arial", 15, "bold"),command=lambda:self.get_input(5), bd=5,width=5, pady=20, cursor="hand2").grid( row=3, column=1)
        btn_6=Button(Cal_Frame, text='6', font=("arial", 15, "bold"),command=lambda:self.get_input(6), bd=5,width=5, pady=20, cursor="hand2").grid( row=3, column=2)
        btn_subtract=Button(Cal_Frame, text='-', font=("arial", 15, "bold"),command=lambda:self.get_input('-'), bd=5,width=5, pady=20, cursor="hand2").grid( row=3, column=3)
        
        btn_1=Button(Cal_Frame, text='1', font=("arial", 15, "bold"),command=lambda:self.get_input(1), bd=5,width=5, pady=20, cursor="hand2").grid( row=4, column=0)
        btn_2=Button(Cal_Frame, text='2', font=("arial", 15, "bold"),command=lambda:self.get_input(2), bd=5,width=5, pady=20, cursor="hand2").grid( row=4, column=1)
        btn_3=Button(Cal_Frame, text='3', font=("arial", 15, "bold"),command=lambda:self.get_input(3), bd=5,width=5, pady=20, cursor="hand2").grid( row=4, column=2)
        btn_mul=Button(Cal_Frame, text='*', font=("arial", 15, "bold"),command=lambda:self.get_input('*'), bd=5,width=5, pady=20, cursor="hand2").grid( row=4, column=3)
        
        btn_0=Button(Cal_Frame, text='0', font=("arial", 15, "bold"),command=lambda:self.get_input(0), bd=5, width=5, pady=20, cursor="hand2").grid( row=5, column=0)
        btn_div=Button(Cal_Frame, text='/', font=("arial", 15, "bold"),command=lambda:self.get_input('/'), bd=5,width=5, pady=20, cursor="hand2").grid( row=5, column=3)
        
        btn_eq=Button(Cal_Frame, text='=', font=("arial", 15, "bold"),command=self.perform_cal, bd=5,width=24, pady=20, cursor="hand2").grid( row=6, column=0, columnspan=4)
        
        
        # ---------cart frame---------
        cart_Frame=Frame(Cal_Cart_Frame, bd=3, relief= RIDGE)
        cart_Frame.place(x=322,y=5, width=318, height=659)
        self.cartTitle=Label(cart_Frame, text="Cart\nTotal Products: [0]", font=("goudy old style",15), bg="lightgrey")
        self.cartTitle.pack(side= TOP, fill=X)

        scrolly= Scrollbar(cart_Frame, orient= VERTICAL)
        scrollx= Scrollbar(cart_Frame, orient= HORIZONTAL)

        self.CartTable= ttk.Treeview(cart_Frame, columns=("pid","name","price","qty"), yscrollcommand=scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side= BOTTOM, fill=X)
        scrolly.pack(side= RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid",text="P ID ")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Qty")
        self.CartTable["show"]="headings"
        
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=60)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        # ---Add cart widgets frame--------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        
        Add_CartWidgetsFrame= Frame(self.root, bd=2, bg="white", relief=RIDGE)
        Add_CartWidgetsFrame.place(x=645, y=873, width=640, height=153)
        
        lbl_p_name= Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman",15), bg="white").place(x=5,y=5)
        txt_p_name= Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman",15), bg="white", state="readonly").place(x=5,y=35, width=190, height=22)
        
        lbl_p_price= Label(Add_CartWidgetsFrame, text="Price per qty", font=("times new roman",15), bg="white").place(x=220,y=5)
        txt_p_price= Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman",15), bg="white", state="readonly").place(x=220,y=35, width=190, height=22)
        
        lbl_p_qty= Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman",15), bg="white").place(x=430,y=5)
        txt_p_qty= Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman",15), bg="white").place(x=430,y=35, width=190, height=22)
        
        self.lbl_instock= Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman",15), bg="white")
        self.lbl_instock.place(x=5,y=80)
        
        btn_clear_cart= Button(Add_CartWidgetsFrame, text="Clear", font=("times new roman",15), bg="lightgrey", cursor="hand2", command= self.clear_cart).place(x=220,y=80, width=190, height=30)
        btn_add_cart= Button(Add_CartWidgetsFrame, text="Add | Update Cart", font=("times new roman",15), bg="orange", cursor="hand2", command=self.add_update_cart).place(x=430,y=80, width=190, height=30)
        
        
        
        # ----------------------------Billing area------------------------------------
        billFrame=Frame(self.root, bd=2, relief= RIDGE, bg="white")
        billFrame.place(x=1286, y=106, width=631, height=740)
        
        BTitle=Label(billFrame, text="Customer Bill Area", font=("goudy old style",20), bg="#262626", fg="white").pack(side= TOP, fill=X)
        
        scrolly=Scrollbar(billFrame, orient= VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        
        self.txt_bill_area=Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command= self.txt_bill_area)
        
        # ----------------------------Billing Buttons------------------------------------
        billMenuFrame=Frame(self.root, bd=2, relief= RIDGE, bg="white")
        billMenuFrame.place(x=1286, y=845, width=631, height=181)
        
        self.lbl_amt= Label(billMenuFrame, text="Bill Amount \n[0]", font=("times new roman",15), bg="#3f51b5", fg="white")
        self.lbl_amt.place(x=5, y=5, width=205, height=80)
        
        self.lbl_discount= Label(billMenuFrame, text="Discount \n[5%]", font=("times new roman",15), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=215, y=5, width=205, height=80)
        
        self.lbl_net_pay= Label(billMenuFrame, text="Net Amount \n[0]", font=("times new roman",15), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=425, y=5, width=200, height=80)
        
        
        
        btn_print= Button(billMenuFrame, text="Print", font=("times new roman",15), bg="lightgreen", fg="white", cursor="hand2", command=self.print_bill)
        btn_print.place(x=5, y=90, width=205, height=80)
        
        btn_clear_all= Button(billMenuFrame, text="Clear all", font=("times new roman",15), bg="grey", fg="white", cursor="hand2", command= self.clear_all)
        btn_clear_all.place(x=215, y=90, width=205, height=80)
        
        btn_generate= Button(billMenuFrame, text="Generate / Save Bill", font=("times new roman",15), bg="#009688", fg="white", cursor="hand2", command=self.generate_bill)
        btn_generate.place(x=425, y=90, width=200, height=80)
        
        
        self.show()
        self.update_date_time()
        
    #-----------------------------------------------All functions-----------------------------------------------------
    def get_input(self, num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    def clear_cal(self):
        self.var_cal_input.set('')
        
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))       
        
    
    def show(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            cur.execute("select pid, name, price, qty, status from product WHERE status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)  
            
            
    def search(self):
        con = sqlite3.connect(database="shop management system.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should not be empty", parent=self.root)
            else:
                cur.execute ("SELECT pid, name, price, qty, status FROM product WHERE name LIKE '%"+ self.var_search.get()+"%' and status='Active")
                rows = cur.fetchall()
                if len(rows) !=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No matching product found.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def get_data(self, ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row= content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")
        
    def get_data_cart(self, ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row= content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
        
    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "Quantity is required", parent=self.root)
        elif (int(self.var_qty.get()) > int(self.var_stock.get())):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)
        
        else:
            # price_cal = int(int(self.var_qty.get()) * float(self.var_price.get()))  # Calculate price based on quantity
            # price_cal = float(price_cal)
            price_cal= self.var_price.get()
            # Create cart data with pid, name, calculated price, quantity
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            
            # Update or add to cart
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:  # Check if the product is already in the cart
                    present = 'yes'
                    break
                index_ += 1
            
            if present == 'yes':
                op = messagebox.askyesno('Confirm', "Product already present. Do you want to update/remove from the Cart?", parent=self.root)
                if op:
                    if self.var_qty.get() == "0":  # If quantity is 0, remove the product from the cart
                        self.cart_list.pop(index_)
                    else:
                        # Update the cart list at the specific index
                        # self.cart_list[index_][2] = price_cal  # Update price
                        self.cart_list[index_][3] = self.var_qty.get()  # Update quantity
            else:
                # Add the new product to the cart list if it's not already there
                self.cart_list.append(cart_data)
            # Update the cart display after any changes
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amt=self.bill_amt+ (float(row[2])* int(row[3]))
        
        self.discount= (self.bill_amt*5)/100   
        self.net_pay= self.bill_amt-self.discount
        self.lbl_amt.config(text=f"Bill Amount\n {str(self.bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n {str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart\nTotal Products: [{str(len(self.cart_list))}]")
        
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)  
         
    def generate_bill(self):
        if self.var_cname.get()== '' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer datails are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please add product to the cart")
        else:
            # ---------------Bill Top-----------------
            self.bill_top()
            # ---------------Bill Middle--------------
            self.bill_middle()
            # ---------------Bill Bottom--------------
            self.bill_bottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt',"w")
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved','Bill has been Generated/Saved',parent=self.root)
            self.chk_print=1
            
        
    def bill_top(self):
        self.invoice= int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\t\t\t SHOP MANGEMENT
\t\t      Phone NO. 798554****, Lucknow-226022
{str("-"*74)}
 Customer Name: {self.var_cname.get()}
 Ph. No. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\t\t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("-"*74)}
 Product Name\t\t\t\t\tQty.\t\tPrice
{str("-"*74)}
        '''
        self.txt_bill_area.delete("1.0",END)
        self.txt_bill_area.insert("1.0",bill_top_temp)
    
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("-"*74)}
 Bill Amount\t\t\t\t\t\t\tRs.{self.bill_amt}
 Discount\t\t\t\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\t\t\t\tRs.{self.net_pay}
{str("-"*74)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)
        
        
    def bill_middle(self):
        con = sqlite3.connect(database="shop management system.db")
        cur = con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'   
                price=float(int(row[2])*int(row[3]))
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t\t\t"+row[3]+"\t\tRs."+price)
                #-------------------Update qty in product table-------------------
                cur.execute('Update product set qty=?, status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
                messagebox.showerror("Error",f"Error")
    
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')
        
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart\nTotal Products: [0]")
        self.var_search.set('')
        self.chk_print=0
        self.clear_cart()
        self.show()
        self.show_cart()
    
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f" Welcome to Shop Management System \t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)
    
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while the bill is printing",parent=self.root)
            new_file= tempfile.mktemp('.txt')
            open(new_file,"w").write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror("Print","Please generate bill to print the reciept", parent=self.root)
            
            
            
if __name__=="__main__":
  root= Tk()
  obj=BillClass(root)
  root.mainloop()
