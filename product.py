from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1710x910+200+130")
        self.root.title("Shop Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # ----------------------------------------------------------------------------------------------------------#
        
        # variables
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        
        self.var_pid=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_quantity=StringVar()
        self.var_status=StringVar()
        
        self.var_searchby= StringVar()
        self.var_searchtxt= StringVar()

        self.var_emp_id= StringVar()
        self.var_gender= StringVar()
        self.var_contact= StringVar()
        self.var_name= StringVar()
        self.var_dob= StringVar()
        self.var_doj= StringVar()
        self.var_email= StringVar()
        self.var_pass= StringVar()
        self.var_utype= StringVar()
        self.var_salary= StringVar()
        
        
        product_Frame=Frame(self.root, bd=2, relief= RIDGE, bg="white")
        product_Frame.place(x=10,y=10,width=650, height=680)
        
        # title
        title= Label(product_Frame, text="Product Details", font=("goudy old style",18), bg="#0f4d7d", fg="white").pack(side= TOP, fill=X)
        
        lbl_category= Label(product_Frame, text="Category", font=("goudy old style",16), bg="white").place(x=30, y=60)
        lbl_supplier= Label(product_Frame, text="Supplier", font=("goudy old style",16), bg="white").place(x=30, y=110)
        lbl_name= Label(product_Frame, text="Name", font=("goudy old style",16), bg="white").place(x=30, y=160)
        lbl_price= Label(product_Frame, text="Price", font=("goudy old style",16), bg="white").place(x=30, y=210)
        lbl_quantity= Label(product_Frame, text="Quantity", font=("goudy old style",16), bg="white").place(x=30, y=260)
        lbl_status= Label(product_Frame, text="Status", font=("goudy old style",16), bg="white").place(x=30, y=310)
        
        
        
        
        # column 2
        cmb_cat= ttk.Combobox(product_Frame, textvariable=self.var_cat, values= self.cat_list, state='readonly', justify=CENTER, font=("times new roman",10))
        cmb_cat.place(x=170,y=65,width=400, height=22)
        cmb_cat.current(0)
        
        cmb_sup= ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=("times new roman",10))
        cmb_sup.place(x=170,y=115,width=400, height=22)
        cmb_sup.current(0)
        
        txt_name= Entry(product_Frame, textvariable= self.var_name, font=("times new roman",15)).place(x=170,y=165, width=400, height=22)
        txt_price= Entry(product_Frame, textvariable= self.var_price, font=("times new roman",15)).place(x=170,y=215, width=400, height=22)
        txt_quantity= Entry(product_Frame, textvariable= self.var_quantity, font=("times new roman",15)).place(x=170,y=265, width=400, height=22)
        
        cmb_status= ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active","Inactive"), state='readonly', justify=CENTER, font=("times new roman",10))
        cmb_status.place(x=170,y=315,width=400, height=22)
        cmb_status.current(0)
        
        
        # button
        btn_add= Button(product_Frame, text="Save", command= self.add, font=("times new roman",15),bg="#2196f3", fg="white", cursor="hand2").place(x=30,y=400, width=110, height=23)
        btn_update= Button(product_Frame, text="Update", command= self.update, font=("times new roman",15),bg="#4caf50", fg="white", cursor="hand2").place(x=170,y=400, width=110, height=23)
        btn_delete= Button(product_Frame, text="Delete", command= self.delete, font=("times new roman",15),bg="#f44336", fg="white", cursor="hand2").place(x=310,y=400, width=110, height=23)
        btn_clear= Button(product_Frame, text="Clear", command= self.clear, font=("times new roman",15),bg="#607d8b", fg="white", cursor="hand2").place(x=450,y=400, width=110, height=23)



        # search frame
        SearchFrame= LabelFrame(self.root,text="Search Products",bg="white",font=("times new roman",12), bd=2, relief= RIDGE)
        SearchFrame.place(x=970,y=20, width=700, height=70)

        # options
        cmb_search= ttk.Combobox(SearchFrame, textvariable=self.var_searchby, values=("Select","Category","Supplier","Name"), state='readonly', justify=CENTER, font=("times new roman",10))
        cmb_search.place(x=10,y=10,width=200)
        cmb_search.current(0)


        txt_search= Entry(SearchFrame,textvariable= self.var_searchtxt, font=("times new roman",10),bg="lightyellow").place(x=220,y=10, width=280, height=22)
        btn_search= Button(SearchFrame, command=self.search, text="Search",font=("times new roman",10),bg="green", fg="white", cursor="hand2").place(x=510,y=10, width=170, height=23)
        
        
        # Product details
        p_frame=Frame(self.root, bd=3, relief= RIDGE)
        p_frame.place(x=970,y=100, width=700, height=590)

        scrolly= Scrollbar(p_frame, orient= VERTICAL)
        scrollx= Scrollbar(p_frame, orient= HORIZONTAL)

        self.product_table= ttk.Treeview(p_frame, columns=("pid","Category","Supplier","Name",'price',"qty","status"), yscrollcommand=scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side= BOTTOM, fill=X)
        scrolly.pack(side= RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid",text="Product Id")
        self.product_table.heading("Category",text="Category")
        self.product_table.heading("Supplier",text="Supplier")
        self.product_table.heading("Name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Qty")
        self.product_table.heading("status",text="Status")
        self.product_table["show"]="headings"
        
        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("Name", width=100)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("status", width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try: 
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            
            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)
        
    def add(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=='Select' or self.var_name.get()=='':
                messagebox.showerror("Error","All fields are required", parent=self.root) 
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","Product already present, try different", parent= self.root)
                else:
                    cur.execute("Insert into product (Category, Supplier , Name, price, qty , status) values(?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_quantity.get(),
                        self.var_status.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)

    def show(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root) 

    def get_data(self, ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row= content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_quantity.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please selct product from list", parent=self.root) 
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row is None:
                    messagebox.showerror("Error","Invalid Product ID", parent= self.root)
                else:
                    cur.execute("Update product set Category=?, Supplier=? , Name=?, price=?, qty=? , status=? where pid=?",(                                                                                                       
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_quantity.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)
            
    def delete(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select product from the list", parent=self.root) 
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row is None:
                    messagebox.showerror("Error","Invalid Product ID", parent= self.root)
                else:
                    op=messagebox.askyesno("Comfirm","Do you want to delete?",parent=self.root)
                    if op is True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee deleted successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_quantity.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
    
    # def search(self):
    #     con= sqlite3.connect(database="shop management system.db")
    #     cur= con.cursor()
    #     try:
    #         if self.var_searchby.get()=="Select":
    #             messagebox.showerror("Error","Select Search by option", parent= self.root)
    #         elif self.var_searchtxt.get()=="":
    #             messagebox.showerror("Error","Select input should be required", parent= self.root)
    #         else: 
    #             cur.execute("select * from product where "+self.var_searchby.get()+"LIKE '%"+self.var_searchtxt.get()+"%'")
    #             rows=cur.fetchall()
    #             if len(rows) is not 0:
    #                 self.product_table.delete(*self.product_table.get_children())
    #                 for row in rows:
    #                     self.product_table.insert('',END,values=row)
    #             else:
    #                 messagebox.showerror("Error","No record found!!!", parent= self.root)
    #     except Exception as ex:
    #         messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)
            
    def search(self):
        con = sqlite3.connect(database="shop management system.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search by option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should not be empty", parent=self.root)
            else:
                # Properly format the query with parameterized search
                search_column = self.var_searchby.get()  # Get the column to search by
                search_text = '%' + self.var_searchtxt.get() + '%'  # Prepare the search text with wildcards
                
                query = f"SELECT * FROM product WHERE {search_column} LIKE ?"
                cur.execute(query, (search_text,))  # Execute with parameterized input
                rows = cur.fetchall()

                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())  # Clear the table
                    for row in rows:
                        self.product_table.insert('', END, values=row)  # Insert rows into the table
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

            
if __name__=="__main__":
  root= Tk()
  obj=productClass(root)
  root.mainloop()