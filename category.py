from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1710x910+200+130")
        self.root.title("Shop Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
    
        # variables
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        
        #  title
        lbl_title=Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45", fg="white").pack(side= TOP, fill=X, padx=10, pady=20)
        
        lbl_name=Label(self.root, text="Enter Category Name", font=("goudy old style", 20), bg="white", fg="black").place(x=50, y=100)
        txt_name= Entry(self.root, textvariable= self.var_name, font=("goudy old style", 15), bg="white", fg="black").place(x=50, y=150, width=400)
        
        btn_add= Button(self.root, text="Add", font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2", command=self.add).place(x=480, y=143, width=200)
        btn_delete= Button(self.root, text="Delete", font=("goudy old style", 15), bg="red", fg="white", cursor="hand2", command=self.delete).place(x=700, y=143, width=200)
        
        
        # category details
        
        cat_frame=Frame(self.root, bd=3, relief= RIDGE)
        cat_frame.place(x=1000,y=100, width=700, height=250)
        
        scrolly= Scrollbar(cat_frame, orient= VERTICAL)
        scrollx= Scrollbar(cat_frame, orient= HORIZONTAL)


        self.category_Table = ttk.Treeview(
                    cat_frame, 
                    columns=("cid", "name"), 
                    yscrollcommand=scrolly.set, 
                    xscrollcommand=scrollx.set
                )
        self.category_Table["show"] = "headings"  # Hide the default "#0" column

        scrollx.pack(side= BOTTOM, fill=X)
        scrolly.pack(side= RIGHT, fill=Y)
        scrollx.config(command=self.category_Table.xview)
        scrolly.config(command=self.category_Table.yview)
        self.category_Table.heading("cid",text="C ID")
        self.category_Table.heading("name",text="Name")
    
        
        self.category_Table.column("cid", width=20)
        self.category_Table.column("name", width=100)
        self.category_Table.pack(fill=BOTH, expand=1)
        self.category_Table.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        
        
        # --------------------------------functions--------------------------------
        
    def add(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category name is required", parent=self.root) 
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error","Category already present, try different", parent= self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(
                    self.var_name.get(),
               ))
            con.commit()
            messagebox.showinfo("Success","Category added successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root)
            
    def show(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
          cur.execute("select * from category")
          rows=cur.fetchall()
          self.category_Table.delete(*self.category_Table.get_children())
          for row in rows:
             self.category_Table.insert('',END,values=row)
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root) 

    def get_data(self, ev):
      f=self.category_Table.focus()
      content=(self.category_Table.item(f))
      row= content['values']
      
      self.var_cat_id.set(row[0])
      self.var_name.set(row[1])
    
    def delete(self):
        con= sqlite3.connect(database="shop management system.db")
        cur= con.cursor()
        try:
            if self.var_cat_id.get()=="":
               messagebox.showerror("Error","Please select Category from the list", parent=self.root) 
            else:
               cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
               row=cur.fetchone()
               if row is None:
                   messagebox.showerror("Error","Please try again", parent= self.root)
               else:
                   op=messagebox.askyesno("Comfirm","Do you want to delete?",parent=self.root)
                   if op is True:
                       cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                       con.commit()
                       messagebox.showinfo("Delete","Category deleted successfully", parent=self.root)
                       self.show()
                       self.var_cat_id.set("")
                       self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}", parent= self.root) 
        
if __name__=="__main__":
  root= Tk()
  obj=categoryClass(root)
  root.mainloop()