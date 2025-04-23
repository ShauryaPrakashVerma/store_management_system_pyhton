from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1710x910+200+130")
        self.root.title("Shop Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # ------------------------------------------------------------------------------------------------
        # all variables
        self.var_searchby= StringVar()
        self.var_searchtxt= StringVar()

        self.var_sup_invoice= StringVar()
        self.var_name= StringVar()
        self.var_contact= StringVar()

        # search frame
        # options
        # Add combobox for selecting the search column
        lbl_searchby = Label(self.root, text="Search by:", font=("times new roman", 15), bg="white")
        lbl_searchby.place(x=800, y=82)
        combo_searchby = ttk.Combobox(self.root, textvariable=self.var_searchby, values=("invoice", "name", "contact"), font=("times new roman", 12), state="readonly")
        combo_searchby.place(x=895, y=84, width=200, height=22)
        combo_searchby.current(0)  # Set default selection to "invoice"
        
        txt_search= Entry(self.root,textvariable= self.var_searchtxt, font=("times new roman",10),bg="lightyellow").place(x=1115,y=84, width=300, height=22)
        btn_search= Button(self.root, text="Search",command= self.search, font=("times new roman",10),bg="green", fg="white", cursor="hand2").place(x=1430,y=82, width=170, height=23)

        

        # title
        title= Label(self.root, text="Supplier Details", font=("goudy old style",20), bg="#0f4d7d", fg="white").place(x=100, y=10, width=1500, height=50)


        # content
        # row1
        lbl_supplier_invoice= Label(self.root, text="Invoice No.", font=("goudy old style",15), bg="white").place(x=100, y=80)
        txt_supplier_invoice= Entry(self.root, textvariable= self.var_sup_invoice, font=("goudy old style",15), bg="white").place(x=200, y=80, width=350)
 

        # row2
        lbl_name= Label(self.root, text="Name", font=("goudy old style",15), bg="white").place(x=100, y=130)
        txt_name= Entry(self.root, textvariable= self.var_name, font=("goudy old style",15), bg="white").place(x=200, y=130, width=350)


        # row3
        lbl_contact= Label(self.root, text="Contact", font=("goudy old style",15), bg="white").place(x=100, y=180)
        txt_contact= Entry(self.root, textvariable= self.var_contact, font=("goudy old style",15), bg="white").place(x=200, y=180, width=350)
        


        # row4
        lbl_desc= Label(self.root, text="Description", font=("goudy old style",15), bg="white").place(x=100, y=230)
        self.txt_desc= Text(self.root, font=("goudy old style",15), bg="white")
        self.txt_desc.place(x=200, y=230, width=515, height=120)


        # button
        btn_add= Button(self.root, text="Save", command=self.add, font=("times new roman",15),bg="#2196f3", fg="white", cursor="hand2").place(x=200,y=410, width=110, height=23)
        btn_update= Button(self.root, text="Update", command=self.update, font=("times new roman",15),bg="#4caf50", fg="white", cursor="hand2").place(x=325,y=410, width=110, height=23)
        btn_delete= Button(self.root, text="Delete", command=self.delete,font=("times new roman",15),bg="#f44336", fg="white", cursor="hand2").place(x=450,y=410, width=110, height=23)
        btn_clear= Button(self.root, text="Clear", command= self.clear,font=("times new roman",15),bg="#607d8b", fg="white", cursor="hand2").place(x=575,y=410, width=110, height=23)


        # employee details
        emp_frame=Frame(self.root, bd=3, relief= RIDGE)
        emp_frame.place(x=800,y=130, width=800, height=300)

        scrolly= Scrollbar(emp_frame, orient= VERTICAL)
        scrollx= Scrollbar(emp_frame, orient= HORIZONTAL)

        self.supplierTable= ttk.Treeview(emp_frame, columns=("invoice","name","contact","desc"), yscrollcommand=scrolly.set, xscrollcommand= scrollx.set)
        scrollx.pack(side= BOTTOM, fill=X)
        scrolly.pack(side= RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")
        self.supplierTable["show"]="headings"
        
        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

# ------------------------------------------------------------------------------------------------------------------------------------------------#

    def add(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
           if self.var_sup_invoice.get()=="":
               messagebox.showerror("Error","Invoice is required", parent=self.root) 
           else:
               cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
               row=cur.fetchone()
               if row is not None:
                   messagebox.showerror("Error","Invoice no. already assigned, try different", parent= self.root)
               else:
                   cur.execute("Insert into supplier (invoice, name, contact , desc) values(?,?,?,?)",(
                       self.var_sup_invoice.get(),
                       self.var_name.get(),
                       self.var_contact.get(),
                       self.txt_desc.get('1.0',END)
                   ))
                   con.commit()
                   messagebox.showinfo("Success","Supplier added successfully", parent=self.root)
                   self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)

    def show(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
          cur.execute("select * from supplier")
          rows=cur.fetchall()
          self.supplierTable.delete(*self.supplierTable.get_children())
          for row in rows:
             self.supplierTable.insert('',END,values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root) 

    def get_data(self, ev):
      f=self.supplierTable.focus()
      content=(self.supplierTable.item(f))
      row= content['values']
      
      self.var_sup_invoice.set(row[0])
      self.var_name.set(row[1])
      self.var_contact.set(row[2])
      self.txt_desc.delete('1.0',END)
      self.txt_desc.insert(END, row[3])

    def update(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
           if self.var_sup_invoice.get()=="":
               messagebox.showerror("Error","Invoice No. is required", parent=self.root) 
           else:
               cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
               row=cur.fetchone()
               if row is None:
                   messagebox.showerror("Error","Invalid Invoice ID", parent= self.root)
               else:
                   cur.execute("Update supplier set name=?, contact=? , desc=? where invoice=?",(                 
                       self.var_name.get(),
                       self.var_contact.get(),
                       self.txt_desc.get('1.0',END),
                       self.var_sup_invoice.get(),
                   ))
                   con.commit()
                   messagebox.showinfo("Success","Supllier updated successfully", parent=self.root)
                   self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)
            
    def delete(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
               messagebox.showerror("Error","Invoice No. is required", parent=self.root) 
            else:
               cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
               row=cur.fetchone()
               if row is None:
                   messagebox.showerror("Error","Invalid Invoice No.", parent= self.root)
               else:
                   op=messagebox.askyesno("Comfirm","Do you want to delete?",parent=self.root)
                   if op is True:
                       cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                       con.commit()
                       messagebox.showinfo("Delete","Supplier deleted successfully", parent=self.root)
                       self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)

    def clear(self):
      self.var_sup_invoice.set("")
      self.var_name.set("")
      self.var_contact.set("")
      self.txt_desc.delete('1.0',END)
      self.var_searchtxt.set("")
      self.show()

    def search(self):
        con = sqlite3.connect(database="shop management system.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "":
                messagebox.showerror("Error", "Select Search by option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should not be empty", parent=self.root)
            else:
                # Properly format the query with parameterized search
                search_column = self.var_searchby.get()  # Get the column to search by
                search_text = '%' + self.var_searchtxt.get() + '%'  # Prepare the search text with wildcards
                
                query = f"SELECT * FROM supplier WHERE {search_column} LIKE ?"
                cur.execute(query, (search_text,))  # Execute with parameterized input
                rows = cur.fetchall()

                if len(rows) != 0:
                    self.supplierTable.delete(*self.supplierTable.get_children())  # Clear the table
                    for row in rows:
                        self.supplierTable.insert('', END, values=row)  # Insert rows into the table
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__=="__main__":
  root= Tk()
  obj=supplierClass(root)
  root.mainloop()
