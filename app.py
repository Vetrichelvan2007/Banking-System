import os
import oracledb
from customtkinter import *
from CTkTable import CTkTable
import tkinter as tk
from tkinter import ttk
from PIL import Image
import time
import datetime as dt

main = CTk()
main.title("Banking System")
main.config(bg="#222224")
main.geometry("890x500")
main.resizable(False,False)
 
def connect_db():
    try:
        return oracledb.connect(user="system", password="vetri", dsn="localhost:1521/XEPDB1")
    except Exception as e:
        print("Error:", e)
        return None

def login_frame():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "bg1.jpg")

    loginframe=CTkFrame(main,fg_color="white",width=800,height=600)
    loginframe.pack()

    bg_img = CTkImage(dark_image=Image.open(img_path), size=(500, 500))
    bg_lab = CTkLabel(loginframe, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    frame1 = CTkFrame(loginframe, fg_color="#D9D9D9", bg_color="white",height=350, width=300, corner_radius=20)
    frame1.grid(row=0, column=1, padx=40)


    title = CTkLabel(frame1, text="Welcome Back! \nLogin to Account",text_color="black", font=("", 35, "bold"))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    result_label = CTkLabel(frame1, text="",font=("Arial", 18, "bold"),text_color="black")
    result_label.grid(row=5, column=0, pady=10)

    def login():

        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role=combobox.get()

        if not username or not password or not role:
            result_label.configure(text="Please fill all details", text_color="red")
            return
        
        roles=["customer","employee","manager"]
        if role not in roles:
            result_label.configure(text="Invalid role", text_color="red")
            return

        try:
            connection = connect_db()
            cursor = connection.cursor()

            query = """SELECT user_id, username, role, employee_id, customer_id FROM users WHERE username = :1 AND password = :2 and role = :3"""
            cursor.execute(query, (username, password,role))
            row = cursor.fetchone()

            print("Entered:", username, password)
            print("DB Row:", row)

            if row:
                if row[2].lower()=="customer": 
                    loginframe.pack_forget()
                    customer_frame()
                    global globalcustomerid 
                    globalcustomerid = row[4]
                    print(globalcustomerid)
                if row[2].lower()=="manager": 
                    loginframe.pack_forget()
                    manager_frame()
                if row[2].lower()=="employee":
                    cursor.execute("select job_role from employee where employee_id=:1",(row[3],))
                    rows=cursor.fetchone()
                    print(rows)
                    if rows and rows[0].lower()=="teller":
                        loginframe.pack_forget()
                        teller_frame()
                    elif rows and rows[0].lower()=="loan officer":
                        loginframe.pack_forget()
                        loanofficer_frame()
                if row[2].lower()=="manager":
                    loginframe.pack_forget()
                    # manager_frame()
            else:
                result_label.configure(text="Login Failed", text_color="red")

        except Exception as e:
            result_label.configure(text="Error in connection", text_color="yellow")
            print("Error:", e)

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
                
    username_entry = CTkEntry(frame1, text_color="white",placeholder_text="Username", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
    username_entry.grid(row=1, column=0, sticky="nwe", padx=30)

    password_entry = CTkEntry(frame1, text_color="white",placeholder_text="Password", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45, show="*")
    password_entry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)
    
    combobox = CTkComboBox(frame1, values=["customer", "employee", "manager"],text_color="white",button_color="blue", fg_color="black",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
    combobox.grid(row=3, column=0, sticky="nwe", padx=30, pady=20)
    combobox.set("Enter Your Role")

    def cca():
        loginframe.pack_forget()
        create_customer_account()
    def cea():
        loginframe.pack_forget()
        create_employee_account()

    menu = tk.Menu(main,fg="blue",bg="black", tearoff=0)
    menu.add_command(label="Customer", command=cca)
    menu.add_command(label="Employee", command=cea)
    menu.add_command(label="Manager")

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)
    createacc = CTkButton(frame1, text="Create Account!",text_color="#0085FF", cursor="hand2", font=("", 15),fg_color="#D9D9D9")
    createacc.grid(row=4, column=0, sticky="w", pady=20, padx=40)
    createacc.bind("<Button-1>", show_menu)

    loginbtn = CTkButton(frame1, text="Login", font=("", 15, "bold"),height=40, width=60, fg_color="blue",cursor="hand2", corner_radius=15,command=login)
    loginbtn.grid(row=4, column=0, sticky="ne", pady=20, padx=35)

def teller_frame():
    main.title("Teller Frame")
    frame=CTkFrame(main,width=890,height=500,fg_color="#19191a")
    frame.pack(fill="both",expand=True)

    current_content = None  

    def show_content(new_frame):
        nonlocal current_content
        if current_content is not None:
            current_content.place_forget()   
        current_content = new_frame
        current_content.place(x=100, y=45) 

    def menu():
        frame2=CTkFrame(frame,width=250,height=500,fg_color="#222224",corner_radius=20)
        frame2.place(x=0,y=0)


        def back():
            frame2.place_forget()
        backbtn=CTkButton(frame2,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back).place(x=0,y=0)
        
        def deposit():
            frame2.place_forget()
            frame3=CTkFrame(frame,width=720,height=420,fg_color="#222224",corner_radius=20)
            

            CTkLabel(frame3,text="Customer Id : ",text_color="white",font=("",22,"bold")).place(x=20,y=35)
            CTkLabel(frame3,text="Account Id : ",text_color="white",font=("",22,"bold")).place(x=20,y=95)
            CTkLabel(frame3,text="Account Type : ",text_color="white",font=("",22,"bold")).place(x=20,y=155)
            CTkLabel(frame3,text="Amount : ",text_color="white",font=("",22,"bold")).place(x=20,y=215)

            cust_id_entry=CTkEntry(frame3,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Customer Id ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            cust_id_entry.place(x=190,y=30)

            acc_id_entry=CTkEntry(frame3,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Account Id ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            acc_id_entry.place(x=190,y=90)

            acc_type_entry=CTkComboBox(frame3,values=["Savings","Current"],fg_color="black",text_color="white",font=("",20,"bold"),width=300,height=45,corner_radius=20,button_color="blue")
            acc_type_entry.place(x=190,y=150)
            acc_type_entry.set("Select Account Type")

            amount_entry=CTkEntry(frame3,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Amount ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            amount_entry.place(x=190,y=210)

            result_label=CTkLabel(frame3,text="Enter The Details to deposit",text_color="white",font=("",20,"bold"),bg_color="#222224")
            result_label.place(x=20,y=370)


            def deposit_amount():

                cust_id=cust_id_entry.get().strip()
                acc_id=acc_id_entry.get().strip()
                acc_type=acc_type_entry.get()
                amount=amount_entry.get().strip()

                if not all([cust_id,acc_id,acc_type,amount]):
                    result_label.configure(text="All fields are required", text_color="red")
                    return
                try:
                    acc_id = int(acc_id)
                    cust_id = int(cust_id)
                    amount = float(amount)
                except ValueError:
                    result_label.configure(text="Invalid Accountid or CustomerID or Amount", text_color="red")
                    return

                try:
                    connection = connect_db()
                    cursor = connection.cursor()
                    query = "UPDATE account SET balance = balance + :1 WHERE account_id = :2 AND customer_id = :3 AND account_type = :4"
                    cursor.execute(query, (amount, acc_id, cust_id,acc_type))
                    connection.commit()

                    if cursor.rowcount > 0:
                        result_label.configure(text="Deposit successful",text_color="lightgreen")
                        query="""insert into transactions(txn_id, account_id, txn_type, amount, description)
                                VALUES (txn_seq.NEXTVAL, :1, :2, :3,NVL(:4, 'N/A'))"""
                        cursor.execute(query,(acc_id,"DEPOSIT",amount,"Bank Deposit"))
                        connection.commit()

                        acc_id_entry.delete(0,"end")
                        cust_id_entry.delete(0,"end")
                        amount_entry.delete(0,"end")
                        acc_type_entry.set("Select Account Type")
                            
                    else:
                        result_label.configure(text="No matching account", text_color="red")
                        acc_id_entry.delete(0,"end")
                        cust_id_entry.delete(0,"end")
                        amount_entry.delete(0,"end")
                        acc_type_entry.set("Select Account Type")

                except Exception as e:
                    result_label.configure(text="Error connecting to DB", text_color="yellow")
                    acc_id_entry.delete(0,"end")
                    cust_id_entry.delete(0,"end")
                    amount_entry.delete(0,"end")
                    acc_type_entry.set("Select Account Type")
                    print("Error:", e)

                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()
            def clear():
                cust_id_entry.delete(0,tk.END)
                acc_id_entry.delete(0,tk.END)
                acc_type_entry.set("Select Account Type")
                amount_entry.delete(0,tk.END)


            CTkButton(frame3,text="Clear",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=clear).place(x=50,y=300)
            CTkButton(frame3,text="Deposite",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=deposit_amount).place(x=400,y=300)
            show_content(frame3)
        CTkButton(frame2,text="💰 Deposit",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=deposit).place(x=40,y=40)

        def withdraw():
            frame2.place_forget()
            frame4=CTkFrame(frame,width=720,height=420,fg_color="#222224",corner_radius=20)
            

            CTkLabel(frame4,text="Customer Id : ",text_color="white",font=("",22,"bold")).place(x=20,y=35)
            CTkLabel(frame4,text="Account Id : ",text_color="white",font=("",22,"bold")).place(x=20,y=95)
            CTkLabel(frame4,text="Account Type : ",text_color="white",font=("",22,"bold")).place(x=20,y=155)
            CTkLabel(frame4,text="Amount : ",text_color="white",font=("",22,"bold")).place(x=20,y=215)

            cust_id_entry=CTkEntry(frame4,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Customer Id ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            cust_id_entry.place(x=190,y=30)

            acc_id_entry=CTkEntry(frame4,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Account Id ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            acc_id_entry.place(x=190,y=90)

            acc_type_entry=CTkComboBox(frame4,values=["Savings","Current"],fg_color="black",text_color="white",font=("",20,"bold"),width=300,height=45,corner_radius=20,button_color="blue")
            acc_type_entry.place(x=190,y=150)
            acc_type_entry.set("Select Account Type")

            amount_entry=CTkEntry(frame4,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Amount ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            amount_entry.place(x=190,y=210)

            result_label=CTkLabel(frame4,text="Enter The Details to Withdraw",text_color="white",font=("",20,"bold"),bg_color="#222224")
            result_label.place(x=20,y=370)


            def withdraw_amount():

                cust_id=cust_id_entry.get().strip()
                acc_id=acc_id_entry.get().strip()
                acc_type=acc_type_entry.get()
                amount=amount_entry.get().strip()

                if not all([cust_id,acc_id,acc_type,amount]):
                    result_label.configure(text="All fields are required", text_color="red")
                    return
                try:
                    acc_id = int(acc_id)
                    cust_id = int(cust_id)
                    amount = float(amount)
                except ValueError:
                    result_label.configure(text="Invalid Accountid or CustomerID or Amount", text_color="red")
                    return

                try:
                    connection = connect_db()
                    cursor = connection.cursor()
                    query="select balance from account where account_id=:1 and customer_id=:2 and account_type=:3"
                    cursor.execute(query,(acc_id,cust_id,acc_type,))
                    row=cursor.fetchone()
                    print("Entered:",acc_id,cust_id,row)
                    if row :
                        if row[0]>=amount:
                            query2= "update account set balance=balance-:1 where account_id=:2 and customer_id=:3"
                            cursor.execute(query2,(amount,acc_id,cust_id,))
                            query3="select balance from account where account_id=:1 and customer_id=:2"
                            cursor.execute(query3,(acc_id,cust_id,))
                            row=cursor.fetchone()
                            result_label.configure(text="Balance after withdraw: "+str(row[0]),text_color="lightgreen")

                            query="""insert into transactions(txn_id, account_id, txn_type, amount, description)
                                VALUES (txn_seq.NEXTVAL, :1, :2, :3,NVL(:4, 'N/A'))"""
                            cursor.execute(query,(acc_id,"Debited",amount,"Bank Withdraw"))
                            connection.commit()

                            acc_id_entry.delete(0,"end")
                            cust_id_entry.delete(0,"end")
                            acc_type_entry.set("Select Account Type")
                            amount_entry.delete(0,"end")
                            connection.commit()

                        else:
                            result_label.configure(text="Insufficient balance",text_color="red")
                            amount_entry.delete(0,"end")
                    else:
                        result_label.configure(text="No matching account",text_color ="red")
                        acc_id_entry.delete(0,"end")
                        cust_id_entry.delete(0,"end")
                        acc_type_entry.set("Select Account Type")
                        amount_entry.delete(0,"end")
                except Exception as e:
                    result_label.configure(text="Error connecting to DB", text_color="yellow")
                    print("Error:", e)

                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()
            def clear():
                cust_id_entry.delete(0,tk.END)
                acc_id_entry.delete(0,tk.END)
                acc_type_entry.set("Select Account Type")
                amount_entry.delete(0,tk.END)


            CTkButton(frame4,text="Clear",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=clear).place(x=50,y=300)
            CTkButton(frame4,text="Withdraw",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=withdraw_amount).place(x=400,y=300)
            show_content(frame4)
        CTkButton(frame2,text="💵 Withdraw",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=withdraw).place(x=40,y=100)

        def account_details():
            
            frame2.place_forget()
            frame5=CTkFrame(frame,width=720,height=420,fg_color="#222224",corner_radius=20)
            

            CTkLabel(frame5,text="Customer Id : ",text_color="white",font=("",22,"bold")).place(x=20,y=35)
            CTkLabel(frame5,text="Account Id : ",text_color="white",font=("",22,"bold")).place(x=20,y=95)
            CTkLabel(frame5,text="Account Type : ",text_color="white",font=("",22,"bold")).place(x=20,y=155)
           
            cust_id_entry=CTkEntry(frame5,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Customer Id ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            cust_id_entry.place(x=190,y=30)

            acc_id_entry=CTkEntry(frame5,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Account Id ",placeholder_text_color="white",width=300,height=45,corner_radius=20)
            acc_id_entry.place(x=190,y=90)

            acc_type_entry=CTkComboBox(frame5,values=["Savings","Current"],fg_color="black",text_color="white",font=("",20,"bold"),width=300,height=45,corner_radius=20,button_color="blue")
            acc_type_entry.place(x=190,y=150)
            acc_type_entry.set("Select Account Type")

            result_label=CTkLabel(frame5,text="Enter The Details To See Customer Info",text_color="white",font=("",20,"bold"),bg_color="#222224")
            result_label.place(x=20,y=370)

            def display_details():
                cust_id=cust_id_entry.get().strip()
                acc_id=acc_id_entry.get().strip()
                acc_type=acc_type_entry.get()

                if not all([cust_id,acc_id,acc_type]):
                    result_label.configure(text="Fill All The Details",text_color="red")
                    return
                try:
                    cust_id=int(cust_id)
                    acc_id=int(acc_id)
                except ValueError:
                    result_label.configure(text="Invalid Customer Id or Account Id",text_color="red")
                    return
                
                if acc_type not in ["Savings","Current"]:
                    result_label.configure(text="Invalid Account Type",text_color="red")
                    return
                
                try:
                    connection = connect_db()
                    cursor = connection.cursor()

                    cursor.execute("select * FROM account where customer_id=:1 and account_id=:2 and account_type=:3",(cust_id, acc_id, acc_type,))
                    account_info = cursor.fetchone()

                    if account_info:
                        cursor.execute("SELECT * FROM customer WHERE customer_id=:1", (cust_id,))
                        customer_info = cursor.fetchone()
                        frame5.place_forget()
                        detailsframe = CTkScrollableFrame(frame, width=700, height=350, fg_color="#222224", corner_radius=20)
                        
                        CTkLabel(detailsframe, text="Customer Details :", text_color="white",font=("", 26, "bold")).pack(anchor="w", pady=10, padx=20)

                        CTkLabel(detailsframe, text=f"Customer Id : {customer_info[0]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Customer Name : {customer_info[1]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Date Of Birth : {customer_info[2]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Gender : {customer_info[6]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Address : {customer_info[3]}",text_color="white", font=("", 22, "bold"), wraplength=600).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Phone : {customer_info[4]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Email : {customer_info[5]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text="Account Details :", text_color="white",font=("", 26, "bold")).pack(anchor="w", pady=10, padx=20)

                        CTkLabel(detailsframe, text=f"Customer Id : {account_info[1]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Account Id : {account_info[0]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Account Type : {account_info[2]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Balance : {account_info[3]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Opened Date : {account_info[4]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)

                        CTkLabel(detailsframe, text=f"Status : {account_info[5]}",text_color="white", font=("", 22, "bold")).pack(anchor="w", pady=10, padx=40)
                        def transaction():
                            detailsframe.place_forget()
                            columns = ["Account Id", "Transaction Type", "Amount", "Transaction Date", "Description"]
                            data = [columns]

                            try:
                                connection = connect_db()
                                cursor = connection.cursor()
                                query = """SELECT account_id, txn_type, amount, txn_date, description FROM transactions WHERE account_id=:1 order by txn_date desc"""
                                cursor.execute(query, (acc_id,))
                                rows = cursor.fetchall()

                                if rows:
                                    for row in rows:
                                        data.append(list(row))
                                else:
                                    data.append(["-", "No Data", "-", "-", "-"])
                            except Exception as e:
                                print("DB Error:", e)

                            transactionframe=CTkFrame(main,width=890, height=500,fg_color="#222224",corner_radius=20)
                            transactionframe.place(x=0,y=0)
                            
                            thframe = CTkScrollableFrame(transactionframe, width=870, height=350, fg_color="#222224", corner_radius=0)
                            thframe.place(x=0, y=20)
                            table = CTkTable(thframe,row=len(data),column=len(columns),values=data,colors=["#222224", "#2c2c2c"],header_color="#0f4bf2",hover_color="#444",font=("Arial", 13),text_color="white",corner_radius=15)
                            table.pack(fill="both", expand=True, padx=20, pady=10)

                            def back():
                                transactionframe.place_forget()
                                show_content(detailsframe)
                            
                            # show_content(transactionframe)
                            backbtn=CTkButton(transactionframe,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back).place(x=0,y=0)
                        
                        def back():
                                detailsframe.place_forget()
                                cust_id_entry.delete(0,"end")
                                acc_id_entry.delete(0,"end")
                                acc_type_entry.set("Select Account Type")
                                result_label.configure(text="")
                                show_content(frame5)

                        CTkButton(detailsframe,text="⬅ Back",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=back).place(x=50,y=742)
                        CTkButton(detailsframe,text="Transactions Histroy",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=transaction).pack(anchor="e", pady=10, padx=20)
                        show_content(detailsframe)
                    else:
                        result_label.configure(text="No Matching Account Found", text_color="red")

                except Exception as e:
                    print("Error:", e)
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()
                            
    
            def clear():
                cust_id_entry.delete(0,tk.END)
                acc_id_entry.delete(0,tk.END)
                acc_type_entry.set("Select Account Type")

            CTkButton(frame5,text="Clear",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=clear).place(x=50,y=300)
            CTkButton(frame5,text="Get Details",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=display_details).place(x=400,y=300)
            show_content(frame5)
        CTkButton(frame2,text="🔍 Account",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=account_details).place(x=40,y=160)

        def transfer():
            frame2.place_forget()
            frame6=CTkFrame(frame,width=720,height=420,fg_color="#222224",corner_radius=20)
            
            CTkLabel(frame6,text="Sender Information  ",font=("",26,"bold"),text_color="white",).place(x=30,y=10)
            CTkLabel(frame6,text= "Account Id : ",font=("",22,"bold"),text_color="white",).place(x=50,y=50)
            CTkLabel(frame6,text= "Customer Id : ",font=("",22,"bold"),text_color="white",).place(x=50,y=100)
            CTkLabel(frame6,text= "Amount : ",font=("",22,"bold"),text_color="white",).place(x=50,y=150)
            CTkLabel(frame6,text= "Receiver Information  ",font=("",26,"bold"),text_color="white",).place(x=30,y=200)
            CTkLabel(frame6,text= "Account Id : ",font=("",22,"bold"),text_color="white",).place(x=50,y=250)
            CTkLabel(frame6,text= "Customer Id : ",font=("",22,"bold"),text_color="white",).place(x=50,y=300)

            sacc_id_entry=CTkEntry(frame6,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Account Id",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            sacc_id_entry.place(x=210,y=45)
            scust_id_entry=CTkEntry(frame6,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Customer Id",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            scust_id_entry.place(x=210,y=95)
            amount_entry=CTkEntry(frame6,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Amount",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            amount_entry.place(x=210,y=145)

            racc_id_entry=CTkEntry(frame6,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Account Id",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            racc_id_entry.place(x=210,y=245)
            rcust_id_entry=CTkEntry(frame6,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Customer Id",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            rcust_id_entry.place(x=210,y=295)
            result_label=CTkLabel(frame6,text_color="white",text="Enter The Details To Transfer",font=("",20,"bold"))
            result_label.place(x=30,y=355)
            def transfer_ammount():
                sacc_id=sacc_id_entry.get()
                scust_id=scust_id_entry.get()
                amount=amount_entry.get()
                racc_id=racc_id_entry.get()
                rcust_id=rcust_id_entry.get()
                if not all([sacc_id,scust_id,amount,racc_id,rcust_id]):
                    result_label.configure(text="All fields are required",text_color="red")
                    return
                try:
                    sacc_id=int(sacc_id)
                    scust_id=int(scust_id)
                    amount=int(amount)
                    racc_id=int(racc_id)
                    rcust_id=int(rcust_id)
                except Exception as e:
                    result_label.configure(text="Invalid Input",text_color="red")
                    print(e)
                    return
                try:
                    connection =connect_db()
                    cursor=connection.cursor()
                    cursor.execute("select balance from account where account_id=:1 and customer_id=:2",(sacc_id,scust_id))
                    balance=cursor.fetchone()
                    if balance:
                        cursor.execute("select * from account where account_id=:1 and customer_id=:2",(racc_id,rcust_id))
                        receiverdetails=cursor.fetchone()
                        if receiverdetails:
                            if balance[0]>amount:
                                cursor.execute("update account set balance=balance-:1 where account_id=:2 and customer_id  = :3",(amount,sacc_id,scust_id))
                                cursor.execute("update account set balance=balance+:1 where account_id=:2 and customer_id  = :3",(amount,racc_id,rcust_id))
                                sdescription=f"Bank transfer to {racc_id} amount : {amount}"
                                rdescription=f"Bank transfer from {sacc_id} amount : {amount}"
                                cursor.execute("insert into transactions(txn_id, account_id, txn_type, amount, txn_date, description)  values(txn_seq.NEXTVAL, :1, 'Bank Transfer', :2, trunc(sysdate),:3)",(sacc_id,amount,sdescription))
                                cursor.execute("insert into transactions(txn_id, account_id, txn_type, amount, txn_date, description)  values(txn_seq.NEXTVAL, :1, 'Bank Transfer', :2, trunc(sysdate),:3)",(racc_id,amount,rdescription))
                                connection.commit()
                                result_label.configure(text="Amount Transfered Successfully",text_color="green")
                                amount_entry.delete(0,"end")
                                racc_id_entry.delete(0,"end")
                                rcust_id_entry.delete(0,"end")
                                sacc_id_entry.delete(0,"end")
                                scust_id_entry.delete(0,"end")
                            else:
                                result_label.configure(text="Insuficient Balance",text_color="red")
                                amount_entry.delete(0,"end")
                                racc_id_entry.delete(0,"end")
                                rcust_id_entry.delete(0,"end")
                                sacc_id_entry.delete(0,"end")
                                scust_id_entry.delete(0,"end")
                        else:
                            result_label.configure(text="Invalid Receiver Details",text_color="red")
                    else:
                        result_label.configure(text="Invalid Sender Details",text_color="red")
                except Exception as e:
                    print(e)
                    result_label.configure(text="Error connecting to DB",text_color="yellow")
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()
            CTkButton(frame6,text="Transfer",text_color="white",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=transfer_ammount).place(x=500,y=350)
            show_content(frame6)
        CTkButton(frame2,text="🔄 Transfer",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=transfer).place(x=40,y=220)

        def pay_loan():
            frame2.place_forget()

            detailsframe=CTkFrame(frame,fg_color="#222224",width=720,height=420,corner_radius=20)

            CTkLabel(detailsframe,text="Account Id : ",font=("",22,"bold"),text_color="white").place(x=30,y=35)
            CTkLabel(detailsframe,text="Customer Id : ",font=("",22,"bold"),text_color="white").place(x=30,y=95)
            CTkLabel(detailsframe,text="Loan Id : ",font=("",22,"bold"),text_color="white").place(x=30,y=155)
            CTkLabel(detailsframe,text="Loan Type : ",font=("",22,"bold"),text_color="white").place(x=30,y=215)
            CTkLabel(detailsframe,text="Amount : ",font=("",22,"bold"),text_color="white").place(x=30,y=275)
            
            accountid_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Account Id ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=300,corner_radius=20, height=45)
            accountid_entry.place(x=200,y=30)

            customerid_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Customer Id ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=300,corner_radius=20, height=45)
            customerid_entry.place(x=200,y=90)

            loanid_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Loan Id ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=300,corner_radius=20, height=45)
            loanid_entry.place(x=200,y=150)

            loan_type_entry =CTkComboBox(detailsframe,text_color="white",values=["Home Loan","Personal Loan","Business Loan","Education Loan"],button_color="blue",font=("",19,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
            loan_type_entry.place(x=200,y=210)
            loan_type_entry.set("Loan Type")

            amount_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Amount ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=300,corner_radius=20, height=45)
            amount_entry.place(x=200,y=270)
            
            result_label=CTkLabel(detailsframe,text="Enter The Details To Pay Loan",font=("",26,"bold"),text_color="white")
            result_label.place(x=30,y=350)
            
            def pay():
                accountid=accountid_entry.get()
                customerid=customerid_entry.get()
                loanid=loanid_entry.get()
                loantype=loan_type_entry.get()
                amount=amount_entry.get()

                if not all([accountid,customerid,loanid,loantype,amount]):
                    result_label.configure(text="Fill All The Details",text_color="red")
                    return
                
                try:
                    accountid=int(accountid)
                except Exception as e:
                    result_label.configure(text="Invalid Account Id",text_color="red")
                    return
                    print(e)

                try:
                    customerid=int(customerid)
                except Exception as e:
                    
                    result_label.configure(text="Invalid Customer Id",text_color="red")
                    print(e)
                    return
                try:
                    loanid=int(loanid)
                except Exception as e:
                    result_label.configure(text="Invalid Loan Id",text_color="red")
                    print(e)
                    return

                if loantype.lower() not in ("home loan","personal loan","business loan","education loan"):
                    result_label.configure(text="Invalid Loan Type",text_color="red")
                    return
                
                try:
                    amount=float(amount)
                except Exception as e:
                    result_label.configure(text="Invalid Amount",text_color="red")
                    print(e)
                    return
                try:
                    connection =connect_db()
                    cursor=connection.cursor()
                    cursor.execute("select * from loan where loan_id=:1 and account_id=:2 and customer_id=:3 and loan_type=:4",(loanid,accountid,customerid,loantype))
                    res=cursor.fetchone()
                    if res and res[9]=="Settled":
                        result_label.configure(text="Loan Already Settled",text_color="red")
                        return
                    if res:
                        cursor.execute("select balance from account where account_id =:1 and customer_id= :2",(accountid,customerid))
                        row = cursor.fetchone()
                        if row and row[0]>=amount:
                            cursor.execute("select * from loan_payment where loan_id=:1 and account_id=:2 and customer_id=:3 order by payment_date desc fetch first 1 row only",(loanid,accountid,customerid))
                            result=cursor.fetchone()
                            if result:
                                if result[6]>=amount:
                                    query="""insert into loan_payment(payment_id, loan_id, customer_id, account_id, payment_date, amount_paid, balance_left, payment_mode, status)
                                            values(payment_id_seq.NEXTVAL, :1, :2, :3, sysdate , :4, :5, :6, :7)"""
                                    cursor.execute(query,(loanid,customerid,accountid,amount,result[6]-amount,"online","Successful"))
                                    cursor.execute("update account set balance=balance-:1 where account_id=:2 and customer_id=:3",(amount,accountid,customerid))
                                    cursor.execute("insert into transactions(txn_id,account_id,txn_type,amount,txn_date,description) values(txn_seq.nextval,:1,:2,:3,trunc(sysdate),:4)",(accountid,"Cash",amount,"Loan payment"))
                                    if result[6]-amount==0:
                                        cursor.execute("update loan set status='Settled' where loan_id=:1",(loanid,))
                                        connection.commit()
                                    connection.commit()
                                    result_label.configure(text="Payment Successful",text_color="green")
                                    accountid_entry.delete(0,"end")
                                    customerid_entry.delete(0,"end")
                                    loanid_entry.delete(0,"end")
                                    loan_type_entry.set("Loan Type")
                                    amount_entry.delete(0,"end")
                                else:
                                    result_label.configure(text="The amount is more than\nthe amount to pay",text_color="red")
                                    amount_entry.delete(0,"end")
                            else:
                                result_label.configure(text="Invalid Loan Id",text_color="red")
                        else:
                            result_label.configure(text="Insufficient Balance",)
                    else:
                        result_label.configure(text="No matching loan found",text_color="red")
                except Exception as e:
                    print(e)
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()
            CTkButton(detailsframe,text="pay",text_color="white",fg_color="blue",bg_color="#222224",font=("",20,"bold"),height=40,width=100,corner_radius=20,command=pay).place(x=550,y=350)
            show_content(detailsframe)
        CTkButton(frame2,text="Pay loan",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=pay_loan).place(x=40,y=280)

        def loanhistory():
            frame2.place_forget()
            detailsframe = CTkFrame(frame, width=720, height=420, fg_color="#222224", corner_radius=20)
            
            
            CTkLabel(detailsframe,text= "Account Id : ",font=("",22,"bold"),text_color="white",).place(x=50,y=50)
            CTkLabel(detailsframe,text= "Customer Id : ",font=("",22,"bold"),text_color="white",).place(x=50,y=100)
            CTkLabel(detailsframe,text="Loan Id : ",font=("",22,"bold"),text_color="white").place(x=50,y=150)
            
            result_label=CTkLabel(detailsframe,text="Enter the Details To See Loan History",text_color="white",font=("",20,"bold"))
            result_label.place(x=30,y=250)

            accountid_entry=CTkEntry(detailsframe,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Account Id",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            accountid_entry.place(x=210,y=45)

            customerid_entry=CTkEntry(detailsframe,fg_color="black",text_color="white",font=("",20,"bold"),placeholder_text="Customer Id",placeholder_text_color="white",width=300,height=40,corner_radius=20)
            customerid_entry.place(x=210,y=95)
           

            loanid_entry= CTkEntry(detailsframe, text_color="white",placeholder_text="Loan Id ", fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=300,corner_radius=25, height=40)
            loanid_entry.place(x=210,y=145)

            def checkhistroy():
                accountid=accountid_entry.get()
                customerid=customerid_entry.get()
                loanid=loanid_entry.get()

                if not accountid or not customerid or not loanid:
                    result_label.configure(text="Fill All The Details",text_color="red")
                    return

                try:
                    accountid=int(accountid)
                except Exception as e:
                    result_label.configure(text="Invalid Account Id",text_color="red")
                    return

                try:
                    customerid=int(customerid)
                except Exception as e:
                    result_label.configure(text="Invalid Customer Id",text_color="red")
                    return

                try:
                    loanid=int(loanid)
                except Exception as e:
                    result_label.configure(text="Invalid Loan Id",text_color="red")
                    return
                
                try:
                    connection=connect_db()
                    cursor=connection.cursor()

                    cursor.execute("select * from loan where account_id=:1 and customer_id=:2 and loan_id=:3",(accountid,customerid,loanid))
                    row=cursor.fetchone()
                    print(row)
            
                    if row:
                        frame.pack_forget()
                        historyframe=CTkFrame(main,fg_color="#19191f",width=890,height=50)
                        historyframe.pack(fill="both", expand=True)

                        def back1():
                            historyframe.pack_forget()
                            teller_frame()
                        backbtn=CTkButton(historyframe,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back1)
                        backbtn.place(x=0,y=0)

                        column=["customer id","account id","payment date","amount paid","balance left","payment mode","status"]
                        data=[column]
                        cursor.execute("select  customer_id, account_id, payment_date as payment_date, amount_paid, balance_left, payment_mode, status from loan_payment where account_id=:1 and customer_id=:2 and loan_id=:3",(accountid,customerid,loanid))
                        results=cursor.fetchall()

                        if results:
                            for result in results:
                                data.append(list(result))
                        else:
                            data.append(["-","No Data","-","-","-","-","-","-"])
                        
                        tableframe=CTkScrollableFrame(historyframe,fg_color="#222224",bg_color="#19191f",width=850,height=300,corner_radius=20)
                        tableframe.place(x=0,y=40)

                        table = CTkTable(tableframe,row=len(data),column=len(column),values=data,colors=["#222224", "#2c2c2c"],header_color="#0f4bf2",hover_color="#444",font=("", 13),corner_radius=10,fg_color="#222224",text_color="white")
                        table.pack(fill="both",expand=True)
                    else:
                        result_label.configure(text="No Matching Account")
                        return
                except Exception as e:
                    print(e)

            CTkButton(detailsframe, text="Back",text_color="white",fg_color="blue",bg_color="#222224",font=("",20,"bold"),height=45,width=200,corner_radius=20,command=detailsframe.destroy).place(x=60,y=330)
            CTkButton(detailsframe,text="Check",text_color="white",fg_color="blue",bg_color="#222224",font=("",20,"bold"),height=45,width=200,corner_radius=20,command=checkhistroy).place(x=450,y=330)
            show_content(detailsframe)
        CTkButton(frame2,text="loan history",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=loanhistory).place(x=40,y=340)
         
        def logout():
            frame.pack_forget()
            login_frame()
        CTkButton(frame2,text="Logout",text_color="white",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command=logout).place(x=40,y=400)
    CTkButton(frame,text="☰",fg_color="blue",bg_color="#19191a",width=50,height=30,command=menu).place(x=0,y=0)

def customer_frame():
    main.title("Customer Frame")
    customerframe=CTkFrame(main,fg_color="#19191f",width=890,height=50)
    customerframe.pack(fill="both", expand=True)

    customerframe.grid_rowconfigure(0, weight=1)
    customerframe.grid_columnconfigure(0, weight=0) 
    customerframe.grid_columnconfigure(1, weight=1) 
    
    but_frame = CTkScrollableFrame(customerframe, fg_color="#222224", width=250, height=500)
    but_frame.grid(row=0, column=0, sticky="nsw")

    title = CTkLabel(but_frame, text="Dashboard",font=("Segoe UI", 24, "bold"))
    title.pack() 

    dis_frame = CTkFrame(customerframe, fg_color="#19191a", width=591, height=500)
    dis_frame.grid(row=0, column=1, sticky="nsew")  

    welcome = CTkLabel(dis_frame, text="Welcome to Banking System 🏦",font=("Segoe UI", 24, "bold"))
    welcome.pack(expand=True)

    def checkbalance():
        
        balancedisplay = CTkFrame(dis_frame, fg_color="#222224",corner_radius=20)
        balancedisplay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        CTkLabel(balancedisplay,text="Account Id :",font=("", 22, "bold")).place(x=40,y=28)
        CTkLabel(balancedisplay,text="Customer Id :",font=("", 22, "bold")).place(x=40,y=90)

        account_id_entry = CTkEntry(balancedisplay, text_color="white",placeholder_text="Account Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        account_id_entry.place(x=190, y=20)

        customer_id_entry = CTkEntry(balancedisplay, text_color="white",placeholder_text="Customer Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        customer_id_entry.place(x=190, y=80)

        result_label = CTkLabel(balancedisplay, text="    Enter the details to check balance", font=("Arial", 18, "bold"),bg_color="#222224",fg_color="#222224")
        result_label.place(x=40, y=170)

        def check():

            account_id=account_id_entry.get().strip()
            customer_id=customer_id_entry.get().strip()

            if not account_id or not customer_id:
                result_label.configure(text="           Both fields are required", text_color="red")
                return
            try:
                account_id = int(account_id)
                customer_id = int(customer_id)
            except ValueError:
                result_label.configure(text="Invalid accountid or customerid", text_color="red")
                return

            try:
                connection = connect_db()
                cursor = connection.cursor()
                query = "select balance FROM account WHERE account_id = :1 AND customer_id = :2"
                cursor.execute(query, (account_id, customer_id))
                row = cursor.fetchone()
                print("Entered:", account_id, customer_id)
                print("DB Row:", row)
                if row:
                    result_label.configure(text="Your Current Balance : " + str(row[0]), text_color="lightgreen")
                    account_id_entry.delete(0,"end")
                    customer_id_entry.delete(0,"end")
                else:
                    result_label.configure(text="No matching account", text_color="red")

            except Exception as e:
                result_label.configure(text="Error connecting to DB", text_color="yellow")
                print("Error:", e)

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

        CTkButton(balancedisplay, text="Check",font=("Arial", 18, "bold"),fg_color="#0f4bf2", text_color="white",width=150, height=45,command=check).place(x=60,y=260)
        CTkButton(balancedisplay,text="Back",font=("Arial", 18, "bold"), fg_color="#0f4bf2", text_color="white",width=150, height=45,command=balancedisplay.destroy).place(x=250,y=260)
    CTkButton(but_frame,text="💳 Balance", font=("", 19, "bold"),height=35, width=170,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=checkbalance ).pack(pady=10)

    def deposit():
        depositdisplay = CTkFrame(dis_frame, fg_color="#222224",corner_radius=20)
        depositdisplay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        CTkLabel(depositdisplay,text="Account Id :",font=("", 22, "bold")).place(x=40,y=28)
        CTkLabel(depositdisplay,text="Customer Id :",font=("", 22, "bold")).place(x=40,y=80)
        CTkLabel(depositdisplay,text="Amount :",font=("", 22, "bold")).place(x=40,y=130)
        CTkLabel(depositdisplay,text="Description :",font=("", 22, "bold")).place(x=40,y=178)

        account_id_entry = CTkEntry(depositdisplay, text_color="white",placeholder_text="Account Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        account_id_entry.place(x=190, y=20)

        customer_id_entry = CTkEntry(depositdisplay, text_color="white",placeholder_text="Customer Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        customer_id_entry.place(x=190, y=70)

        amount_entry= CTkEntry(depositdisplay, text_color="white",placeholder_text="Amount ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        amount_entry.place(x=190,y=120)

        description_entry= CTkEntry(depositdisplay, text_color="white",placeholder_text="Description ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        description_entry.place(x=190,y=170)
 
        result_label = CTkLabel(depositdisplay, text="    Enter the amount to deposit", font=("Arial", 18, "bold"),bg_color="#222224",fg_color="#222224")
        result_label.place(x=50, y=260)

        def deposit_amount():
            account_id=account_id_entry.get().strip()
            customer_id=customer_id_entry.get().strip()
            amount=amount_entry.get().strip()
            description=description_entry.get().strip()

            if not account_id or not customer_id or not amount:
                result_label.configure(text="           All fields are required", text_color="red")
                return
            try:
                account_id = int(account_id)
                customer_id = int(customer_id)
                amount = float(amount)
            except ValueError:
                result_label.configure(text="Invalid username or password", text_color="red")
                return

            try:
                connection = connect_db()
                cursor = connection.cursor()
                query = "UPDATE account SET balance = balance + :1 WHERE account_id = :2 AND customer_id = :3"
                cursor.execute(query, (amount, account_id, customer_id))
                connection.commit()

                if cursor.rowcount > 0:
                    result_label.configure(text="Deposit successful",text_color="lightgreen")
                    query="""insert into transactions(txn_id, account_id, txn_type, amount, description)
                             VALUES (txn_seq.NEXTVAL, :1, :2, :3,NVL(:4, 'N/A'))"""
                    cursor.execute(query,(account_id,"DEPOSIT",amount,description))
                    connection.commit()

                    account_id_entry.delete(0,"end")
                    customer_id_entry.delete(0,"end")
                    amount_entry.delete(0,"end")
                    description_entry.delete(0,"end")
                        
                else:
                    result_label.configure(text="No matching account", text_color="red")
                    account_id_entry.delete(0,"end")
                    customer_id_entry.delete(0,"end")
                    amount_entry.delete(0,"end")

            except Exception as e:
                result_label.configure(text="Error connecting to DB", text_color="yellow")
                account_id_entry.delete(0,"end")
                customer_id_entry.delete(0,"end")
                amount_entry.delete(0,"end")
                print("Error:", e)

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

        CTkButton(depositdisplay, text="Deposit",font=("Arial", 18, "bold"),fg_color="#0f4bf2", text_color="white",width=150, height=45,command=deposit_amount).place(x=60,y=330)
        CTkButton(depositdisplay,text="Back",font=("Arial", 18, "bold"), fg_color="#0f4bf2", text_color="white",width=150, height=45,command=depositdisplay.destroy).place(x=250,y=330)
    CTkButton(but_frame,text="💰 Deposit", font=("", 19, "bold"),height=35, width=170,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=deposit).pack(pady=10)

    def withdraw():

        withdrawdisplay = CTkFrame(dis_frame, fg_color="#222224",corner_radius=20)
        withdrawdisplay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        CTkLabel(withdrawdisplay,text="Account Id :",font=("", 22, "bold")).place(x=40,y=28)
        CTkLabel(withdrawdisplay,text="Customer Id :",font=("", 22, "bold")).place(x=40,y=80)
        CTkLabel(withdrawdisplay,text="Amount :",font=("", 22, "bold")).place(x=40,y=130)
        CTkLabel(withdrawdisplay,text="Description :",font=("", 22, "bold")).place(x=40,y=178)

        account_id_entry = CTkEntry(withdrawdisplay, text_color="white",placeholder_text="Account Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        account_id_entry.place(x=190, y=20)

        customer_id_entry = CTkEntry(withdrawdisplay, text_color="white",placeholder_text="Customer Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        customer_id_entry.place(x=190, y=70)

        amount_entry= CTkEntry(withdrawdisplay, text_color="white",placeholder_text="Amount ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        amount_entry.place(x=190,y=120)

        description_entry= CTkEntry(withdrawdisplay, text_color="white",placeholder_text="Description ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        description_entry.place(x=190,y=170)
        
        result_label = CTkLabel(withdrawdisplay, text="    Enter the amount to deposit", font=("Arial", 18, "bold"),bg_color="#222224",fg_color="#222224")
        result_label.place(x=50, y=260)

        def withdraw_amount():
            account_id=account_id_entry.get().strip()
            customer_id=customer_id_entry.get().strip()
            amount=amount_entry.get().strip()
            description=description_entry.get().strip()

            if not account_id or not customer_id or not amount:
                result_label.configure(text="           All fields are required", text_color="red")
                return
            try:
                account_id = int(account_id)
                customer_id = int(customer_id)
                amount = float(amount)
            except ValueError:
                result_label.configure(text="Invalid username or password", text_color="red")
                return

            try:
                connection = connect_db()
                cursor=connection.cursor()
                query="select balance from account where account_id=:1 and customer_id=:2"
                cursor.execute(query,(account_id,customer_id))
                row=cursor.fetchone()
                print("Entered:",account_id,customer_id,row)
                if row :
                    if row[0]>=amount:
                        query2= "update account set balance=balance-:1 where account_id=:2 and customer_id=:3"
                        cursor.execute(query2,(amount,account_id,customer_id))
                        query3="select balance from account where account_id=:1 and customer_id=:2"
                        cursor.execute(query3,(account_id,customer_id))
                        row=cursor.fetchone()
                        result_label.configure(text="Balance after withdraw: "+str(row[0]),text_color="lightgreen")

                        query="""insert into transactions(txn_id, account_id, txn_type, amount, description)
                             VALUES (txn_seq.NEXTVAL, :1, :2, :3,NVL(:4, 'N/A'))"""
                        cursor.execute(query,(account_id,"credit",amount,description))
                        connection.commit()

                        account_id_entry.delete(0,"end")
                        customer_id_entry.delete(0,"end")
                        amount_entry.delete(0,"end")
                        connection.commit()

                    else:
                        result_label.configure(text="Insufficient balance",text_color="red")
                        amount_entry.delete(0,"end")
                else:
                    result_label.configure(text="No matching account",text_color ="red")
                    account_id_entry.delete(0,"end")
                    customer_id_entry.delete(0,"end")
                    amount_entry.delete(0,"end")
            except Exception as e:
                result_label.configure(text="Error connecting to DB", text_color="yellow")
                print("Error:", e)

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

        CTkButton(withdrawdisplay, text="withdraw",font=("Arial", 18, "bold"),fg_color="#0f4bf2", text_color="white",width=150, height=45,command=withdraw_amount).place(x=60,y=330)
        CTkButton(withdrawdisplay,text="Back",font=("Arial", 18, "bold"), fg_color="#0f4bf2", text_color="white",width=150, height=45,command=withdrawdisplay.destroy).place(x=250,y=330)
    CTkButton(but_frame,text="💵 Withdraw", font=("", 19, "bold"),height=35, width=170,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=withdraw).pack(pady=10)

    def estatment():
        estatementdisplay = CTkFrame(dis_frame, fg_color="#222224", corner_radius=20)
        estatementdisplay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        CTkLabel(estatementdisplay, text="Account Id :", font=("", 22, "bold")).place(x=40, y=28)

        account_id_entry = CTkEntry(estatementdisplay, text_color="white", placeholder_text="Account Id", fg_color="black", placeholder_text_color="white", font=("", 16, "bold"), width=200, corner_radius=15, height=45)
        account_id_entry.place(x=190, y=20)

        result_label = CTkLabel(estatementdisplay, text="        Enter the account id ", font=("Arial", 18, "bold"), bg_color="#222224", fg_color="#222224")
        result_label.place(x=50, y=150)

        def checke():
            def tableframe(account_id,rows):
                frame = CTkFrame(main, width=890, height=500, fg_color="#222224")
                frame.place(x=0, y=0)

                columns = ["Account Id", "Transaction Type", "Amount", "Transaction Date", "Description"]
                data = [columns]

                if rows:
                    for row in rows:
                        data.append(list(row))
                else:
                    data.append(["-", "No Data", "-", "-", "-"])
               

                scroll_frame = CTkScrollableFrame(frame, width=850, height=250, fg_color="#222224")  
                scroll_frame.pack(pady=20)

                table = CTkTable(scroll_frame, row=len(data), column=len(columns), values=data,colors=["#222224", "#2c2c2c"], header_color="#0f4bf2", hover_color="#444",font=("Arial", 13), text_color="white", corner_radius=8)
                table.pack(fill="both", expand=True, padx=20, pady=10)

                def back():
                    frame.place_forget()
                    customer_frame()

                CTkButton(frame, text="Back", font=("", 14, "bold"),fg_color="blue", text_color="white", height=30, width=120,corner_radius=10, command=back).pack(pady=10)

            account_id = account_id_entry.get()
            if not account_id:
                result_label.configure(text="Please enter the details", text_color="red")
            else:
                try:
                    account_id = int(account_id)
                except ValueError:
                    result_label.configure(text="Invalid account id", text_color="red")
                    return

                try:
                    connection = connect_db()
                    cursor = connection.cursor()
                    query = "SELECT count(*) FROM account WHERE account_id=:1"
                    cursor.execute(query, (account_id,))
                    row = cursor.fetchone()
                    if row and row[0] > 0:
                        customerframe.pack_forget()
                        query = """SELECT account_id, txn_type, amount, TO_CHAR(txn_date,'DD-MON-YYYY') as txn_date, description FROM transactions WHERE account_id=:1 order by txn_date desc """
                        cursor.execute(query, (account_id,))
                        rows = cursor.fetchall()
                        tableframe(account_id,rows)
                    else:
                        result_label.configure(text="Invalid Account Id", text_color="red")
                except Exception as e:
                    result_label.configure(text="connection error", text_color="red")
                    print(e)
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()

        CTkButton(estatementdisplay, text="Check E", font=("Arial", 18, "bold"),fg_color="#0f4bf2", text_color="white", width=150, height=45,command=checke).place(x=60, y=330)
    CTkButton(but_frame, text="📄 E-Statement", font=("", 19, "bold"), height=35,width=170,fg_color="blue", bg_color="#222224", cursor="hand2", corner_radius=15,command=estatment).pack(pady=10)

    def applyloan():
        customerframe.pack_forget()
        loan_frame=CTkFrame(main,fg_color="#222224",width=890,height=500)
        loan_frame.pack(fill="both", expand=True)

        CTkLabel(loan_frame,text="Loan Application",font=("",30,"bold"),text_color="white").place(x=300,y=10)

        result_label=CTkLabel(loan_frame,text="vv",font=("",26,"bold"),text_color="white")
        result_label.place(x=30,y=430)

        CTkLabel(loan_frame,text="customer Id : ",font=("",22,"bold"),text_color="white").place(x=30,y=75)
        CTkLabel(loan_frame,text="Account Id : ",font=("",22,"bold"),text_color="white").place(x=30,y=125)
        CTkLabel(loan_frame,text="Loan Type : ",font=("",22,"bold"),text_color="white").place(x=30,y=175)
        CTkLabel(loan_frame,text="Principal Amount : ",font=("",22,"bold"),text_color="white").place(x=30,y=225)
        CTkLabel(loan_frame,text="Tenure Months : ",font=("",22,"bold"),text_color="white").place(x=30,y=275)
        CTkLabel(loan_frame,text="Income : ",font=("",22,"bold"),text_color="white").place(x=30,y=325)
        CTkLabel(loan_frame,text="Employment status : ",font=("",22,"bold"),text_color="white").place(x=30,y=375)

        customer_id_entry =CTkEntry(loan_frame,text_color="white",placeholder_text="customer Id ",placeholder_text_color="white",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        customer_id_entry.place(x=255,y=70)

        account_id_entry =CTkEntry(loan_frame,text_color="white",placeholder_text="Account Id ",placeholder_text_color="white",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        account_id_entry.place(x=255,y=120)

        loan_type_entry =CTkComboBox(loan_frame,text_color="white",values=["Home loan","Personal loan","Business loan","Education loan"],button_color="blue",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        loan_type_entry.place(x=255,y=170)
        loan_type_entry.set("Enter the loan type")

        principal_amount_entry =CTkEntry(loan_frame,text_color="white",placeholder_text="principal Amount ",placeholder_text_color="white",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        principal_amount_entry.place(x=255,y=220)

        tenure_months_entry =CTkEntry(loan_frame,text_color="white",placeholder_text="Tenure Months ",placeholder_text_color="white",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        tenure_months_entry.place(x=255,y=270)

        Income_entry =CTkEntry(loan_frame,text_color="white",placeholder_text="Income ",placeholder_text_color="white",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        Income_entry.place(x=255,y=320)

        employment_status_entry =CTkEntry(loan_frame,text_color="white",placeholder_text="Employment status ",placeholder_text_color="white",font=("",20,"bold"), fg_color="black",corner_radius=20,width=300,height=45)
        employment_status_entry.place(x=255,y=370)

        def request():
            customer_id=customer_id_entry.get()
            account_id=account_id_entry.get()
            loan_type=loan_type_entry.get()
            principal_amount=principal_amount_entry.get()
            tenure_months=tenure_months_entry.get()
            Income=Income_entry.get()
            employment_status=employment_status_entry.get()

            if not all([customer_id,account_id,loan_type,principal_amount,tenure_months,Income,employment_status]):
                result_label.configure(text="Fill All The details",text_color="red")
                return
            
            try:
                customer_id=int(customer_id)
                account_id=int(account_id)
                principal_amount=int(principal_amount)
                tenure_months=int(tenure_months)
                Income=float(Income)
            except Exception as e:
                print(e)

            try:
                connection =connect_db()
                cursor= connection.cursor()
                cursor.execute("select * from account where account_id=:1 and customer_id=:2",(account_id,customer_id,))
                res=cursor.fetchone()
                if res:
                    query="insert into loan_request(request_id,customer_id,account_id,loan_type,principal_amount,tenure_months,income,employment_status) values(request_id_seq.NEXTVAL,:1,:2,:3,:4,:5,:6,:7)"
                    cursor.execute(query,(customer_id,account_id,loan_type,principal_amount,tenure_months,Income,employment_status))
                    connection.commit()
                    result_label.configure(text="Loan Request Sent",text_color="green")
                    customer_id_entry.delete(0,"end")
                    account_id_entry.delete(0,"end")
                    loan_type_entry.set("Enter the loan type")
                    principal_amount_entry.delete(0,"end")
                    tenure_months_entry.delete(0,"end")
                    Income_entry.delete(0,"end")
                    employment_status_entry.delete(0,"end")

                else:
                    result_label.configure(text="Invalid AccountId or CustomerId",text_color="red")
            except Exception as e:
                print(e)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()


            
        def back():
            loan_frame.pack_forget()
            customer_frame()
        CTkButton(loan_frame,text="⬅",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=30,height=30,command=back,corner_radius=20).place(x=40,y=10)
        CTkButton(loan_frame,text="Apply",font=("",20,"bold"),fg_color="blue",bg_color="#222224",width=180,height=40,corner_radius=20,command=request).place(x=650,y=430)
    CTkButton(but_frame,text="📝 Apply Loan", font=("", 19, "bold"),height=35, width=170,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=20,command=applyloan).pack(pady=10)
   
    def pay_loan():
        customerframe.pack_forget()
        pay_loan_frame=CTkFrame(main,fg_color="#19191a",width=890,height=500)
        pay_loan_frame.pack(fill="both", expand=True)

        def back():
            pay_loan_frame.pack_forget()
            customer_frame()
        backbtn=CTkButton(pay_loan_frame,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back).place(x=0,y=0)
    
        detailsframe=CTkFrame(pay_loan_frame,fg_color="#222224",width=720,height=420,corner_radius=20)
        detailsframe.place(x=80,y=45)

        CTkLabel(detailsframe,text="Account Id : ",font=("",26,"bold"),text_color="white").place(x=30,y=35)
        CTkLabel(detailsframe,text="Customer Id : ",font=("",26,"bold"),text_color="white").place(x=30,y=95)
        CTkLabel(detailsframe,text="Loan Id : ",font=("",26,"bold"),text_color="white").place(x=30,y=155)
        CTkLabel(detailsframe,text="Loan Type : ",font=("",26,"bold"),text_color="white").place(x=30,y=215)
        CTkLabel(detailsframe,text="Amount : ",font=("",26,"bold"),text_color="white").place(x=30,y=275)
        
        accountid_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Account Id ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=220,corner_radius=20, height=45)
        accountid_entry.place(x=200,y=30)

        customerid_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Customer Id ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=220,corner_radius=20, height=45)
        customerid_entry.place(x=200,y=90)

        loanid_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Loan Id ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=220,corner_radius=20, height=45)
        loanid_entry.place(x=200,y=150)

        loan_type_entry =CTkComboBox(detailsframe,text_color="white",values=["Home Loan","Personal Loan","Business Loan","Education Loan"],button_color="blue",font=("",19,"bold"), fg_color="black",corner_radius=20,width=220,height=45)
        loan_type_entry.place(x=200,y=210)
        loan_type_entry.set("Loan Type")

        amount_entry=CTkEntry(detailsframe,text_color="white",placeholder_text="Amount ",fg_color="black",placeholder_text_color="white",font=("", 20, "bold"), width=220,corner_radius=20, height=45)
        amount_entry.place(x=200,y=270)
        
        result_label=CTkLabel(detailsframe,text="vv",font=("",26,"bold"),text_color="white")
        result_label.place(x=30,y=350)
        
        def pay():
            accountid=accountid_entry.get()
            customerid=customerid_entry.get()
            loanid=loanid_entry.get()
            loantype=loan_type_entry.get()
            amount=amount_entry.get()

            if not all([accountid,customerid,loanid,loantype,amount]):
                result_label.configure(text="Fill All The Details",text_color="red")
                return
            
            try:
                accountid=int(accountid)
            except Exception as e:
                result_label.configure(text="Invalid Account Id",text_color="red")
                return
                print(e)

            try:
                customerid=int(customerid)
            except Exception as e:
                
                result_label.configure(text="Invalid Customer Id",text_color="red")
                print(e)
                return
            try:
                loanid=int(loanid)
            except Exception as e:
                result_label.configure(text="Invalid Loan Id",text_color="red")
                print(e)
                return

            if loantype.lower() not in ("home loan","personal loan","business loan","education loan"):
                result_label.configure(text="Invalid Loan Type",text_color="red")
                return
            
            try:
                amount=float(amount)
            except Exception as e:
                result_label.configure(text="Invalid Amount",text_color="red")
                print(e)
                return
            try:
                connection =connect_db()
                cursor=connection.cursor()
                cursor.execute("select * from loan where loan_id=:1 and account_id=:2 and customer_id=:3 and loan_type=:4",(loanid,accountid,customerid,loantype))
                res=cursor.fetchone()
                if res and res[9]=="Settled":
                    result_label.configure(text="Loan Already Settled",text_color="red")
                    return
                if res:
                    cursor.execute("select balance from account where account_id =:1 and customer_id= :2",(accountid,customerid))
                    row = cursor.fetchone()
                    if row and row[0]>=amount:
                        cursor.execute("select * from loan_payment where loan_id=:1 and account_id=:2 and customer_id=:3 order by payment_date desc fetch first 1 row only",(loanid,accountid,customerid))
                        result=cursor.fetchone()
                        if result:
                            if result[6]>=amount:
                                query="""insert into loan_payment(payment_id, loan_id, customer_id, account_id, payment_date, amount_paid, balance_left, payment_mode, status)
                                        values(payment_id_seq.NEXTVAL, :1, :2, :3, trunc(sysdate), :4, :5, :6, :7)"""
                                cursor.execute(query,(loanid,customerid,accountid,amount,result[6]-amount,"online","Successful"))
                                cursor.execute("update account set balance=balance-:1 where account_id=:2 and customer_id=:3",(amount,accountid,customerid))
                                if result[6]-amount==0:
                                    cursor.execute("update loan set status='Settled' where loan_id=:1",(loanid,))
                                    connection.commit()
                                connection.commit()
                                result_label.configure(text="Payment Successful",text_color="green")
                                accountid_entry.delete(0,"end")
                                customerid_entry.delete(0,"end")
                                loanid_entry.delete(0,"end")
                                loan_type_entry.set("Loan Type")
                                amount_entry.delete(0,"end")
                            else:
                                result_label.configure(text="The amount is more than\nthe amount to pay",text_color="red")
                                amount_entry.delete(0,"end")
                        else:
                            result_label.configure(text="Invalid Loan Id",text_color="red")
                    else:
                        result_label.configure(text="Insufficient Balance",)
                else:
                    result_label.configure(text="No matching loan found",text_color="red")
            except Exception as e:
                print(e)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        CTkButton(detailsframe,text="pay",text_color="white",fg_color="blue",bg_color="#222224",font=("",20,"bold"),height=40,width=100,corner_radius=20,command=pay).place(x=550,y=350)

    def loanhistory():
        detailsframe = CTkFrame(dis_frame, fg_color="#222224", corner_radius=20)
        detailsframe.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        
        CTkLabel(detailsframe,text="Account Id :",font=("", 22, "bold")).place(x=40,y=68)
        CTkLabel(detailsframe,text="Customer Id :",font=("", 22, "bold")).place(x=40,y=128)
        CTkLabel(detailsframe,text="Loan Id :",font=("", 22, "bold")).place(x=40,y=188)

        result_label=CTkLabel(detailsframe,text="",text_color="white",font=("",20,"bold"))
        result_label.place(x=30,y=250)


        accountid_entry = CTkEntry(detailsframe, text_color="white",placeholder_text="Account Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        accountid_entry.place(x=190, y=60)

        customerid_entry = CTkEntry(detailsframe, text_color="white",placeholder_text="Customer Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        customerid_entry.place(x=190, y=120)

        loanid_entry= CTkEntry(detailsframe, text_color="white",placeholder_text="Loan Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        loanid_entry.place(x=190,y=180)

        def checkhistroy():
            accountid=accountid_entry.get()
            customerid=customerid_entry.get()
            loanid=loanid_entry.get()

            if not all([accountid,customerid,loanid]):
                result_label.configure(text="Fill All The Details",text_color="red")
                return

            try:
                accountid=int(accountid)
            except Exception as e:
                result_label.configure(text="Invalid Account Id",text_color="red")
                return
            try:
                customerid=int(customerid)
            except Exception as e:
                result_label.configure(text="Invalid =Customer Id",text_color="red")
                return
            try:
                loanid=int(loanid)
            except Exception as e:
                result_label.configure(text="Invalid Loan Id",text_color="red")
                return
            try:
                connection=connect_db()
                cursor=connection.cursor()

                cursor.execute("select * from loan where account_id=:1 and customer_id=:2 and loan_id=:3",(accountid,customerid,loanid))
                row=cursor.fetchone()
        
                if row:
                    customerframe.pack_forget()
                    historyframe=CTkFrame(main,fg_color="#19191f",width=890,height=50)
                    historyframe.pack(fill="both", expand=True)

                    def back1():
                        historyframe.pack_forget()
                        customer_frame()
                    backbtn=CTkButton(historyframe,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back1)
                    backbtn.place(x=0,y=0)

                    column=["customer id","account id","payment date","amount paid","balance left","payment mode","status"]
                    data=[column]
                    cursor.execute("select  customer_id, account_id, TO_CHAR(payment_date,'DD-MON-YYYY') as payment_date, amount_paid, balance_left, payment_mode, status from loan_payment where account_id=:1 and customer_id=:2 and loan_id=:3",(accountid,customerid,loanid))
                    results=cursor.fetchall()

                    if results:
                        for result in results:
                            data.append(list(result))
                    else:
                        data.append(["-","No Data","-","-","-","-","-","-"])
                    
                    tableframe=CTkScrollableFrame(historyframe,fg_color="#222224",bg_color="#19191f",width=850,height=300,corner_radius=20)
                    tableframe.place(x=0,y=40)

                    table = CTkTable(tableframe,row=len(data),column=len(column),values=data,colors=["#222224", "#2c2c2c"],header_color="#0f4bf2",hover_color="#444",font=("", 13),corner_radius=10,fg_color="#222224",text_color="white")
                    table.pack(fill="both",expand=True)
                else:
                    result_label.configure(text="No Matching Account")
                    return
            except Exception as e:
                print(e)

        CTkButton(detailsframe, text="Back",font=("Arial", 18, "bold"),fg_color="#0f4bf2", text_color="white",width=150, height=45,command=detailsframe.destroy).place(x=60,y=330)
        CTkButton(detailsframe,text="Check",font=("Arial", 18, "bold"), fg_color="#0f4bf2", text_color="white",width=150, height=45,command=checkhistroy).place(x=250,y=330)

    def loandetails():
        detailsframe = CTkFrame(dis_frame, fg_color="#222224", corner_radius=20)
        detailsframe.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        CTkLabel(detailsframe,text="Account Id :",font=("", 22, "bold")).place(x=40,y=68)
        CTkLabel(detailsframe,text="Customer Id :",font=("", 22, "bold")).place(x=40,y=128)
        CTkLabel(detailsframe,text="Loan Id :",font=("", 22, "bold")).place(x=40,y=188)

        result_label=CTkLabel(detailsframe,text="",text_color="white",font=("",20,"bold"))
        result_label.place(x=30,y=250)

        accountid_entry = CTkEntry(detailsframe, text_color="white",placeholder_text="Account Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        accountid_entry.place(x=190, y=60)

        customerid_entry = CTkEntry(detailsframe, text_color="white",placeholder_text="Customer Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        customerid_entry.place(x=190, y=120)

        loanid_entry= CTkEntry(detailsframe, text_color="white",placeholder_text="Loan Id ", fg_color="black",placeholder_text_color="white",font=("", 16, "bold"), width=200,corner_radius=15, height=45)
        loanid_entry.place(x=190,y=180)

        def showdetails():
            accountid=accountid_entry.get()
            customerid=customerid_entry.get()
            loanid=loanid_entry.get()

            if not all([accountid,customerid,loanid]):
                result_label.configure(text="Fill All The Details",text_color="red")
                return

            try:
                accountid=int(accountid)
            except Exception as e:
                result_label.configure(text="Invalid Account Id",text_color="red")
                return
            try:
                customerid=int(customerid)
            except Exception as e:
                result_label.configure(text="Invalid =Customer Id",text_color="red")
                return
            try:
                loanid=int(loanid)
            except Exception as e:
                result_label.configure(text="Invalid Loan Id",text_color="red")
                return
            try:
                connection=connect_db()
                cursor=connection.cursor()
                cursor.execute("select * from loan where account_id=:1 and customer_id=:2 and loan_id=:3",(accountid,customerid,loanid))
                result=cursor.fetchone()
                if result:
                    customerframe.pack_forget()
                    detailsframe=CTkFrame(main,fg_color="#19191f",width=890,height=50)
                    detailsframe.pack(fill="both", expand=True)
                    def back1():
                        detailsframe.pack_forget()
                        customer_frame()
                    backbtn=CTkButton(detailsframe,text="⬅",fg_color="blue",bg_color="#19191f",width=50,height=30,command=back1)
                    backbtn.place(x=0,y=0)

                    tableframe=CTkScrollableFrame(detailsframe,fg_color="#222224",bg_color="#19191f",width=780,height=400,corner_radius=20)
                    tableframe.place(x=40,y=40)

                    cursor.execute("select customer_id,account_id,loan_id,loan_type,principal_amount,annual_interest_rate,monthly_interest_rate,interest_amount,tenure_months,to_char(start_date,'DD-MON-YY') as start_date,to_char(end_date,'DD-MON-YY') as end_date,status from loan where loan_id=:1 and account_id=:2",(loanid,accountid))
                    row=cursor.fetchone()
                    
                    CTkLabel(tableframe,text="Loan Info",text_color="white",font=("",28,"bold")).pack(anchor="n", pady=10, padx=20)
                    CTkLabel(tableframe,text=f"Customer ID : {row[0]}",text_color="white",font=("",26,"bold")).pack(anchor="w", pady=10, padx=10)
                    CTkLabel(tableframe,text=f"Account ID : {row[1]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Loan ID : {row[2]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Loan Type : {row[3]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Amount : {row[4]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Annual Interest Rate : {row[5]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Monthly Interest Rate : {row[6]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Interest Amount : {row[7]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Tenure Month : {row[8]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Start Date : {row[9]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"End Date : {row[10]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                    CTkLabel(tableframe,text=f"Status : {row[11]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=10,pady=10)
                
                else:
                    result_label.configure(text="No Mathch Found",text_color="red")
            except Exception as e:
                print(e)
        CTkButton(detailsframe, text="Back",font=("Arial", 18, "bold"),fg_color="#0f4bf2", text_color="white",width=150, height=45,command=detailsframe.destroy).place(x=60,y=330)
        CTkButton(detailsframe,text="Check",font=("Arial", 18, "bold"), fg_color="#0f4bf2", text_color="white",width=150, height=45,command=showdetails).place(x=250,y=330)

    menu = tk.Menu(main,fg="white",bg="black", tearoff=0)
    menu.add_command(label="Pay Loan", command=pay_loan)
    menu.add_command(label="Loan History",command=loanhistory)
    menu.add_command(label="Loan Details",command=loandetails)

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    loan_details=CTkButton(but_frame,text="Loan Details", font=("", 19, "bold"),height=35, width=170,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15)
    loan_details.pack(pady=10)
    loan_details.bind("<Button-1>", show_menu)

    def logout():
        customerframe.pack_forget()
        login_frame()
    CTkButton(but_frame,text="🔙 Logout", font=("", 19, "bold"),height=35, width=170,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=logout).pack(pady=10)
    
    def profile():
        customerframe.pack_forget()
        profile_frame=CTkScrollableFrame(main,fg_color="#19191a",width=840,height=450)
        profile_frame.place(x=10,y=10)
        def back():
            profile_frame.pack_forget()
            customer_frame()
        CTkButton(profile_frame,text="⬅",text_color="white",fg_color="blue",bg_color="#19191a",width=50,height=30,command=back).pack(anchor="w")
        CTkLabel(profile_frame,text="Profile",text_color="white",font=("",30,"bold")).pack()

        try:
            connection = connect_db()
            cursor = connection.cursor()

            cursor.execute("select account_id,account_type,balance,to_char(opened_on,'DD-MON-YYYY') as opened_on ,status FROM account where customer_id=:1 ",(globalcustomerid,))
            account_info = cursor.fetchone()


            cursor.execute("SELECT customer_id,name,To_char(dob,'DD-MON-YYYY') as dob ,gender,address,phone,email FROM customer WHERE customer_id=:1",(globalcustomerid,))
            customer_info = cursor.fetchone()
            
            CTkLabel(profile_frame,text= "Customer Info :",text_color="white",font=("",28,"bold")).pack(anchor="w", pady=10, padx=20)
            CTkLabel(profile_frame,text=f"Customer id : {customer_info[0]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)
            CTkLabel(profile_frame,text=f"Name : {customer_info[1]} ",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)
            CTkLabel(profile_frame,text=f"Date of birth : {customer_info[2]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)
            CTkLabel(profile_frame,text=f"Gender : {customer_info[3]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)
            CTkLabel(profile_frame,text=f"Address : {customer_info[4]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)
            CTkLabel(profile_frame,text=f"Phone Number : {customer_info[5]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)
            CTkLabel(profile_frame,text=f"Email : {customer_info[6]}",text_color="white",font=("",26,"bold")).pack(anchor="w",padx=70,pady=10)

            CTkLabel(profile_frame,text= "Account Info :",text_color="white",font=("",28,"bold")).pack(anchor="w", pady=10, padx=20)
            CTkLabel(profile_frame, text=f"Account Id : {account_info[0]}",text_color="white", font=("", 26, "bold")).pack(anchor="w", pady=10, padx=40)
            CTkLabel(profile_frame, text=f"Account Type : {account_info[1]}",text_color="white", font=("", 26, "bold")).pack(anchor="w", pady=10, padx=40)
            CTkLabel(profile_frame, text=f"Balance : {account_info[2]}",text_color="white", font=("", 26, "bold")).pack(anchor="w", pady=10, padx=40)
            CTkLabel(profile_frame, text=f"Opened Date : {account_info[3]}",text_color="white", font=("", 26, "bold")).pack(anchor="w", pady=10, padx=40)
            CTkLabel(profile_frame, text=f"Status : {account_info[4]}",text_color="white", font=("", 26, "bold")).pack(anchor="w", pady=10, padx=40)

        except Exception as e:
            print(e)
    CTkButton(but_frame,text="👤", font=("", 19, "bold"),height=30, width=30,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=profile).place(x=0,y=0)

def create_customer_account():
    customerdetails = CTkFrame(main, width=890, height=500, fg_color="#19191a")
    customerdetails.pack(fill="both", expand=True)

    main.title("Create customer account")

    customerdetails.grid_rowconfigure(0, weight=1)
    customerdetails.grid_columnconfigure(0, weight=1)

    frame1 = CTkFrame(customerdetails, fg_color="#222224", width=790, height=400)
    frame1.place(relx=0.5, rely=0.5, anchor="center") 

    CTkLabel(frame1,text="First-Time User Registration",text_color="white",font=("",28,"bold"),bg_color="#222224").place(x=260,y=20)
    def back():
        customerdetails.pack_forget()
        login_frame()

    CTkButton(frame1,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back).place(x=20,y=25)

    CTkLabel(frame1,text="Customer Id : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=30,y=75)
    CTkLabel(frame1,text="Full Name : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=30,y=120)
    CTkLabel(frame1,text="Date of birth : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=30,y=165)
    CTkLabel(frame1,text="Gender : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=30,y=210)
    CTkLabel(frame1,text="Address : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=30,y=255)
    CTkLabel(frame1,text="Number :  ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=30,y=300)
    
    CTkLabel(frame1,text="Email : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=400,y=75)
    CTkLabel(frame1,text="Account Id : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=400,y=120)
    CTkLabel(frame1,text="Account Type : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=400,y=165)
    CTkLabel(frame1,text="User Id :",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=400,y=210)
    CTkLabel(frame1,text="User Name : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=400,y=255)
    CTkLabel(frame1,text="Password : ",text_color="white",font=("",21,"bold"),bg_color="#222224",).place(x=400,y=300)

    customer_id_entry = CTkEntry(frame1,text_color="white",placeholder_text="Customer Id  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_id_entry.place(x=185,y=70)

    customer_name_entry = CTkEntry(frame1,text_color="white",placeholder_text="Customer Name ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_name_entry.place(x=185,y=115)

    customer_dob_entry = CTkEntry(frame1,text_color="white",placeholder_text="Date of Birth  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_dob_entry.place(x=185,y=160)

    customer_gender_entry=CTkComboBox(frame1,values=["Male","Female","Other"],text_color="white",button_color="blue", fg_color="black",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_gender_entry.place(x=185,y=205)
    customer_gender_entry.set("Enter your gender")

    customer_address_entry = CTkEntry(frame1,text_color="white",placeholder_text="Address  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_address_entry.place(x=185,y=250)

    customer_number_entry = CTkEntry(frame1,text_color="white",placeholder_text="Phone Number  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_number_entry.place(x=185,y=295)

    customer_email_entry = CTkEntry(frame1,text_color="white",placeholder_text="Email  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_email_entry.place(x=560,y=70)

    account_id_entry = CTkEntry(frame1,text_color="white",placeholder_text="Account Id  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    account_id_entry.place(x=560,y=115)

    account_type_entry = CTkEntry(frame1,text_color="white",placeholder_text="Account Type ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    account_type_entry.place(x=560,y=160)

    customer_userid_entry= CTkEntry(frame1,text_color="white",placeholder_text="User ID  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_userid_entry.place(x=560,y=205)

    customer_username_entry = CTkEntry(frame1,text_color="white",placeholder_text="User Name   ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    customer_username_entry.place(x=560,y=250)

    password_entry= CTkEntry(frame1,text_color="white",placeholder_text="Password ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    password_entry.place(x=560,y=295)

    res_label=CTkLabel(frame1,text="Fill All The Details ",text_color="white",font=("",20,"bold"),bg_color="#222224")
    res_label.place(x=30,y=355)

    def create():
        customer_id=customer_id_entry.get()
        customer_name=customer_name_entry.get()
        customer_dob =customer_dob_entry.get() 
        customer_gender=customer_gender_entry.get()       
        customer_address=customer_address_entry.get()
        customer_number=customer_number_entry.get()
        customer_email=customer_email_entry.get()
        account_id=account_id_entry.get()
        account_type=account_type_entry.get()
        user_id=customer_userid_entry.get()
        customer_username=customer_username_entry.get()
        password=password_entry.get()

        if not customer_id or not customer_name or not customer_dob or not customer_address or not customer_number or not customer_email or not account_id or not account_type or not user_id or not customer_username or not password:
            res_label.configure(text="Enter All the details",text_color="red")
            return
        try:
            customer_dob = dt.datetime.strptime(customer_dob_entry.get(), "%d-%m-%Y").date()
        except ValueError:
            res_label.configure(text="Invalid Date! Use DD-MM-YYYY", text_color="red")
            return 
        if customer_gender not in ["Male", "Female", "Other"]:
            res_label.configure(text="Invalid gender", text_color="red")
            return 
        try:
            customer_id = int(customer_id)
            account_id=int(account_id)
            user_id=int(user_id)

        except Exception as e:
            res_label.configure(text="Invalid Number Format", text_color="red")
            print(e)

        try:
            connection = connect_db()
            cursor=connection.cursor()
            query="select a.account_id,a.customer_id,u.user_id from account a join users u on a.customer_id=u.customer_id where a.account_id=:1 and a.customer_id=:2 and u.user_id=:3"
            cursor.execute(query,(account_id,customer_id,user_id))
            result=cursor.fetchone()
            if result:
                res_label.configure(text="already account in that user id or customer id or account id",text_color ="red")
            else:
                cursor.execute("select username from users where username=:1",(customer_username,))
                if cursor.fetchone():
                    res_label.configure(text="Username already exist",text_color="red")
                    return
                cursor.execute("insert into customer(customer_id, name, dob, gender, address, phone, email) values(:1,:2,TO_DATE(:3,'DD-MM-YYYY'),:4,:5,:6,:7)",(customer_id,customer_name,customer_dob,customer_gender,customer_address,customer_number,customer_email))
                cursor.execute("insert into account (account_id, customer_id, account_type) values(:1,:2,:3)",(account_id,customer_id,account_type))
                cursor.execute("insert into users(user_id, username, password, role, customer_id,employee_id) values(:1,:2,:3,:4,:5,:6)",(user_id,customer_username,password,"customer",customer_id,None))
                res_label.configure(text="account created successfully ",text_color ="green")
                connection.commit()
                

                time.sleep(3)
                customerdetails.pack_forget()
                login_frame()

        except Exception as e:
            res_label.configure(text="Connection Error",text_color="red")
            print(e)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    CTkButton(frame1,text="Create",font=("",20,"bold"),fg_color="blue",bg_color="#222224",text_color="white",height=40,corner_radius=10,command=create).place(x=600,y=346)

def create_employee_account():
    emp_frame=CTkFrame(main,width=890,height=500,fg_color="#19191a")
    emp_frame.pack(fill="both",expand=True)

    main.title("Create employee account")

    frame1 = CTkFrame(emp_frame, fg_color="#222224", width=790, height=400)
    frame1.place(relx=0.5, rely=0.5, anchor="center") 

    def back():
        emp_frame.pack_forget()
        login_frame()

    CTkButton(frame1,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back).place(x=20,y=25)

    CTkLabel(frame1,text="Employee Registration",text_color="white",font=("",28,"bold")).place(x=260,y=20)

    CTkLabel(frame1,text ="Employee Id : ",text_color="white",font=("",22,"bold")).place(x=30,y=75)
    CTkLabel(frame1,text ="Full Name : ",text_color="white",font=("",22,"bold")).place(x=30,y=120)
    CTkLabel(frame1,text ="Date of Birth : ",text_color="white",font=("",22,"bold")).place(x=30,y=165)
    CTkLabel(frame1,text ="Gender : ",text_color="white",font=("",22,"bold")).place(x=30,y=210)
    CTkLabel(frame1,text ="Email : ",text_color="white",font=("",22,"bold")).place(x=30,y=255)
    CTkLabel(frame1,text ="Phone : ",text_color="white",font=("",22,"bold")).place(x=30,y=300)

    CTkLabel(frame1,text ="Address : ",text_color="white",font=("",22,"bold")).place(x=430,y=75)
    CTkLabel(frame1,text ="Job Role : ",text_color="white",font=("",22,"bold")).place(x=430,y=120)
    CTkLabel(frame1,text ="Salary : ",text_color="white",font=("",22,"bold")).place(x=430,y=165)
    CTkLabel(frame1,text ="User ID : ",text_color="white",font=("",22,"bold")).place(x=430,y=210)
    CTkLabel(frame1,text ="Username : ",text_color="white",font=("",22,"bold")).place(x=430,y=255)
    CTkLabel(frame1,text ="Password : ",text_color="white",font=("",22,"bold")).place(x=430,y=300)

    emp_id_entry= CTkEntry(frame1,text_color="white",placeholder_text="Employee Id  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_id_entry.place(x=185,y=70)

    emp_fullname_entry= CTkEntry(frame1,text_color="white",placeholder_text="Full Name  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_fullname_entry.place(x=185,y=115)

    emp_dob_entry= CTkEntry(frame1,text_color="white",placeholder_text="Date of Birth ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_dob_entry.place(x=185,y=160)

    emp_gender_entry=CTkComboBox(frame1,values=["Male","Female","Other"],text_color="white",button_color="blue", fg_color="black",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_gender_entry.place(x=185,y=205)
    emp_gender_entry.set("Enter your gender")

    emp_email_entry= CTkEntry(frame1,text_color="white",placeholder_text="Email ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_email_entry.place(x=185,y=250)

    emp_phone_entry= CTkEntry(frame1,text_color="white",placeholder_text="Phone ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_phone_entry.place(x=185,y=295)


    emp_address_entry= CTkEntry(frame1,text_color="white",placeholder_text="Address ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_address_entry.place(x=560,y=70)

    emp_jobrole_entry=CTkComboBox(frame1,values=["Teller","Customer Service","Loan Officer","Relationship Manager"],text_color="white",button_color="blue", fg_color="black",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_jobrole_entry.place(x=560,y=115)
    emp_jobrole_entry.set("Enter your job role")

    emp_salary_entry= CTkEntry(frame1,text_color="white",placeholder_text="Salary  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_salary_entry.place(x=560,y=160)

    emp_userid_entry= CTkEntry(frame1,text_color="white",placeholder_text="User ID  ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_userid_entry.place(x=560,y=205)

    emp_username_entry= CTkEntry(frame1,text_color="white",placeholder_text="Username ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_username_entry.place(x=560,y=250)

    emp_password_entry= CTkEntry(frame1,text_color="white",placeholder_text="Password ", fg_color="black",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
    emp_password_entry.place(x=560,y=295)

    res_label= CTkLabel(frame1,text ="Please Fill All The Details .",text_color="white",font=("",20,"bold"),)
    res_label.place(x=30,y=355)

    def get_detailse():

        emp_id = emp_id_entry.get()
        emp_fullname = emp_fullname_entry.get()
        emp_dob = emp_dob_entry.get()
        emp_gender = emp_gender_entry.get()
        emp_email = emp_email_entry.get()
        emp_phone = emp_phone_entry.get()
        emp_address = emp_address_entry.get()
        emp_jobrole = emp_jobrole_entry.get()
        emp_salary = emp_salary_entry.get()
        emp_userid = emp_userid_entry.get()
        emp_username = emp_username_entry.get()
        emp_password = emp_password_entry.get()

        if not all([emp_id, emp_fullname, emp_dob, emp_gender, emp_email, emp_phone,
                    emp_address, emp_jobrole, emp_salary, emp_userid, emp_username, emp_password]):
            res_label.configure(text="Please fill all the details", text_color="red")
            return

        try:
            emp_dob = dt.datetime.strptime(emp_dob, "%d-%m-%Y").date()
        except ValueError:
            res_label.configure(text="Invalid Date! Use DD-MM-YYYY", text_color="red")
            return
        
        if emp_gender not in ["Male", "Female", "Other"]:
            res_label.configure(text="Invalid gender", text_color="red")
            return

        try:
            emp_id = int(emp_id)
        except Exception as e:
            res_label.configure(text="Invalid Employee Id ", text_color="red")
            return
        
        try:  
            emp_phone = int(emp_phone)
        except Exception as e:
            res_label.configure(text="Invalid Phone number ", text_color="red")
            return
        
        if emp_jobrole not in ["Teller", "Customer Service", "Loan Officer", "Relationship Manager"]:
            res_label.configure(text="Invalid job role", text_color="red")
            return
        
        try:
            emp_salary = float(emp_salary)
        except Exception as e:
            res_label.configure(text="Invalid number field", text_color="red")
            return
        
        try:
            emp_userid = int(emp_userid)
        except Exception as e:
            res_label.configure(text="Invalid UserId ", text_color="red")
            return
         
        

        try:
            connection = connect_db()
            cursor = connection.cursor()
            
            cursor.execute("select employee_id from employee where employee_id=:1",(emp_id,))
            if cursor.fetchone():
                res_label.configure(text="Employee id already exist",text_color="red")
                return 
            
            cursor.execute("select user_id from users where user_id=:1",(emp_userid,))
            if cursor.fetchone():
                res_label.configure(text="User id already exist",text_color="red")
                return
            
            cursor.execute("select username from users where username=:1",(emp_username,))
            if cursor.fetchone():
                res_label.configure(text="Username already exist",text_color="red")
                return
            query="""insert into employee(employee_id,full_name, dob, gender, email, phone_number, address, hire_date, job_role, salary)
                    values(:1,:2,:3,:4,:5,:6,:7,sysdate,:8,:9) """
            cursor.execute(query,(emp_id,emp_fullname,emp_dob,emp_gender,emp_email,emp_phone,emp_address,emp_jobrole,emp_salary))
            res_label.configure(text="Employee created successfully",text_color="green")
            cursor.execute("insert into users(user_id,username,password,role) values(:1,:2,:3,:4)",(emp_userid,emp_username,emp_password,"employee"))
            
            connection.commit()
            time.sleep(3)
            emp_frame.pack_forget()
            login_frame()

        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    CTkButton(frame1,text="Create",font=("",20,"bold"),fg_color="blue",bg_color="#222224",text_color="white",height=40,corner_radius=10,command=get_detailse).place(x=600,y=346)

def loanofficer_frame():
    main.title("Loan Officer")
    mainframe=CTkFrame(main,width=890,height=500,fg_color="#19191a")
    mainframe.pack(fill="both", expand=True)

    def menu():
        frame2=CTkScrollableFrame(mainframe,width=250,height=480,fg_color="#222224",corner_radius=10)
        frame2.grid(row=0, column=0, sticky="nsw")


        def back():
            frame2.grid_forget()
        backbtn=CTkButton(frame2,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back).place(x=0,y=0)
        CTkLabel(frame2, text="Dashboard",font=("Segoe UI", 24, "bold")).pack()
        def loan_requests():
            frame2.grid_forget()

            frame3=CTkFrame(mainframe,width=890,height=500,fg_color="#222224")
            frame3.pack(fill="both", expand=True)

            
            
            def table():
                table_frame = CTkScrollableFrame(frame3, width=850, height=250,  corner_radius=20)
                table_frame.place(x=0,y=40)

                columns = ["requestid", "customerid", "accountid", "loan type", "amount","tenure months","income","employment status","application date","status","remarks"]
                data = [columns]

                try:
                    connection = connect_db()
                    cursor = connection.cursor()
                    query =  """
                        SELECT request_id, customer_id, account_id, loan_type,
                            principal_amount, tenure_months, income,
                            employment_status, TO_CHAR(application_date, 'YYYY-MM-DD') AS application_date, status, remarks
                            FROM loan_request
                            WHERE status = 'Pending'
                            ORDER BY application_date DESC"""
                    cursor.execute(query)
                    rows = cursor.fetchall()

                    if rows:
                        for row in rows:
                            data.append(list(row))
                    else:
                        data.append(["-", "No data", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
                except Exception as e:
                    print("DB Error:", e)
                    data.append(["-", "DB Error", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

                loan_request_table = CTkTable(table_frame,row=len(data),column=len(columns),values=data,colors=["#222224", "#2c2c2c"],header_color="#0f4bf2",hover_color="#444",font=("", 13),corner_radius=10,fg_color="#222224",text_color="white")
                loan_request_table.pack(fill="both",expand=True)
                
            table()
            CTkLabel(frame3,text="Request Id :",font=("",22,"bold"),text_color="white",bg_color="#222224").place(x=20,y=345)
            CTkLabel(frame3,text="Customer Id :",font=("",22,"bold"),text_color="white",bg_color="#222224").place(x=370,y=345)
            CTkLabel(frame3,text="Account Id :",font=("",22,"bold"),text_color="white",bg_color="#222224").place(x=20,y=395)
            res_label=CTkLabel(frame3,text="vv",font=("",22,"bold"),text_color="white",bg_color="#222224")
            res_label.place(x=50,y=450)

            request_id_entry=CTkEntry(frame3,text_color="white",fg_color="black",bg_color="#222224",placeholder_text="Request Id",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
            request_id_entry.place(x=160,y=340)

            customer_id_entry=CTkEntry(frame3,text_color="white",fg_color="black",bg_color="#222224",placeholder_text="Customer Id",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
            customer_id_entry.place(x=530,y=340)

            account_id_entry=CTkEntry(frame3,text_color="white",fg_color="black",bg_color="#222224",placeholder_text="Account Id",placeholder_text_color="white",font=("", 18, "bold"), width=200,corner_radius=15, height=40)
            account_id_entry.place(x=160,y=390)

            def approve():
                request_id=request_id_entry.get()
                customer_id=customer_id_entry.get()
                account_id=account_id_entry.get()
                
                try:
                    request_id=int(request_id)
                except Exception as e:
                    res_label.configure(text="Invalid Request Id",text_color="red")
                    print(e)
                    
                try:
                    customer_id=int(customer_id)
                except Exception as e:
                    print(e)
                    res_label.configure(text="Invalid Customer Id",text_color="red")
                try:
                    account_id=int(account_id)
                except Exception as e:
                    print(e)
                    res_label.configure(text="Invalid Account Id",text_color="red")

                try:
                    connection=connect_db()
                    cursor=connection.cursor()
                    query="select * from loan_request where request_id=:1 and customer_id=:2 and account_id=:3"
                    cursor.execute(query,(request_id,customer_id,account_id))
                    result=cursor.fetchone()
                    print(result)
                    if result:
                        query1="update loan_request set status='Approved' where request_id=:1 and customer_id=:2 and account_id=:3"
                        cursor.execute(query1,(request_id,customer_id,account_id))
                        connection.commit()

                        if result[3].lower()=="home loan":
                            annual_interest_rate=8.0
                            interest_rate=round((8.0/12)/100,4)
                        elif result[3].lower() == "education loan":
                            annual_interest_rate=4.0
                            interest_rate = round((4.0/12)/100,4)
                        elif result[3].lower() == "car loan":
                            annual_interest_rate=10.0
                            interest_rate = round((10.0/12)/100,4)
                        elif result[3].lower() == "personal loan":
                            annual_interest_rate=12.0
                            interest_rate = round((12.0/12)/100,4)
                        elif result[3].lower() == "business loan":
                            annual_interest_rate=30.0
                            interest_rate = round((30.0/12)/100,4)
                        
                        interest_amount=result[4]*interest_rate*result[5]

                        query3="""INSERT INTO loan(loan_id, customer_id , account_id , loan_type,
                                principal_amount, annual_interest_rate, monthly_interest_rate,
                                interest_amount,tenure_months,start_date,end_date)
                                VALUES(loan_id_seq.nextval,:1,:2,:3,:4,:5,:6,:7,:8,trunc(sysdate),add_months(trunc(sysdate),:9))"""
                        cursor.execute(query3,(result[1],result[2],result[3],result[4], annual_interest_rate,interest_rate,interest_amount,result[5],result[5] ))
                        cursor.execute("update account set balance=balance+:1 where account_id=:2 and customer_id=:3",(result[4],account_id,customer_id))
                        query4="""insert into loan_payment(payment_id, loan_id, customer_id, account_id, payment_date, amount_paid, balance_left, payment_mode)
                                    values(payment_id_seq.nextval,loan_id_seq.currval,:1,:2,sysdate,:3,:4,:5) """
                        cursor.execute(query4,(customer_id,account_id,0,result[4]+interest_amount,"-"))
                        connection.commit()
                        request_id_entry.delete(0,END)
                        customer_id_entry.delete(0,END)
                        account_id_entry.delete(0,END)
                        res_label.configure(text="loan approved",text_color="green")
                        # time.sleep(2)
                        # table_frame.place_forget()
                        table()
                        
                    else:
                        res_label.configure(text="No mathes found",text_color="red")
                        request_id_entry.delete(0,END)
                        customer_id_entry.delete(0,END)
                        account_id_entry.delete(0,END)
                except Exception as e:
                    print(e)
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()

            CTkButton(frame3,text="approve",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=40,corner_radius=20,command =approve).place(x=600,y=450)
            def back1():
                frame3.pack_forget()
                
            backbtn=CTkButton(frame3,text="⬅",fg_color="blue",bg_color="#222224",width=50,height=30,command=back1)
            backbtn.place(x=0,y=0)
        CTkButton(frame2,text="Loan Requests",fg_color="blue",bg_color="#222224",font=("",20,"bold"),width=180,height=35,corner_radius=20,command=loan_requests).pack(padx=20,pady=10)
        
        def logout():
            mainframe.pack_forget()
            login_frame()
        CTkButton(frame2,text="Logout", font=("", 20, "bold"),height=35, width=180,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=logout).pack(pady=10)
    
    CTkButton(mainframe,text="☰",fg_color="blue",bg_color="#222224",width=50,height=30,command=menu).place(x=0,y=0)

def manager_frame():
    managerframe=CTkFrame(main,width=890,height=500,fg_color="#19191a")
    managerframe.pack(fill="both", expand=True)

    main.title("Manager frame")

    def menu():
        frame2=CTkScrollableFrame(managerframe,width=250,height=480,fg_color="#222224",corner_radius=10)
        frame2.grid(row=0, column=0, sticky="nsw")

        def back():
            frame2.grid_forget()
        backbtn=CTkButton(frame2,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back).place(x=0,y=0)
        
        CTkLabel(frame2, text="Dashboard",font=("Segoe UI", 24, "bold")).pack()

        def viewemployee():
            frame2.grid_forget()
            viewemployeeframe=CTkFrame(managerframe,width=890,height=500,fg_color="#222224")
            viewemployeeframe.pack(fill="both", expand=True)

            current_table = None 
            def placetable(ct):
                nonlocal current_table
                if current_table is not None :
                    current_table.pack_forget()

                current_table = ct
                current_table.pack(fill="both", expand=True, padx=0, pady=0)
             
            def back():
                viewemployeeframe.pack_forget()
                manager_frame()
            CTkButton(viewemployeeframe,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back).place(x=0,y=0)

            canvas = tk.Canvas(viewemployeeframe, width=1100, height=250, bg="#222224", highlightthickness=0)
            canvas.place(x=0, y=40)

            h_scroll = tk.Scrollbar(viewemployeeframe, orient="horizontal", command=canvas.xview)
            h_scroll.place(x=0, y=290, width=1100)

            v_scroll = tk.Scrollbar(viewemployeeframe, orient="vertical", command=canvas.yview)
            v_scroll.place(x=1090, y=40, height=250)

            canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

            table_frame =CTkFrame(canvas, fg_color="#222224",width=990, height=250, corner_radius=20)
            canvas.create_window((0, 0), window=table_frame, anchor="nw")

            columns = ["id", "Name", "Date of Birth", "gender", "email", "number", "address", "job role", "salary"]
            data = [columns]

            CTkLabel(viewemployeeframe,text="Employee Id : ",text_color="white",font=("",22,"bold")).place(x=30,y=300)
            CTkLabel(viewemployeeframe,text="Employee Name : ",text_color="white",font=("",22,"bold")).place(x=30,y=360)

            empid_entry=CTkEntry(viewemployeeframe,text_color="white",font=("",20,"bold"),placeholder_text="Employee Id",placeholder_text_color="white",fg_color="black",corner_radius=20,height=45,width=200)
            empid_entry.place(x=230,y=290)

            empname_entry=CTkEntry(viewemployeeframe,text_color="white",font=("",20,"bold"),placeholder_text="Employee Name",placeholder_text_color="white",fg_color="black",corner_radius=20,height=45,width=200)
            empname_entry.place(x=230,y=350)

            result_label=CTkLabel(viewemployeeframe,text="",text_color="white",font=("",22,"bold"))
            result_label.place(x=30,y=420)

            try:
                connection = connect_db()
                cursor = connection.cursor()
                cursor.execute("select employee_id, full_name, TO_CHAR(dob,'DD-MON-YYYY'), gender, email, phone_number, address, job_role, salary from employee")
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        data.append(list(row))
                else:
                    data.append(["-", "No data", "-", "-", "-", "-", "-", "-","-"])
            except Exception as e:
                pass

            table = CTkTable(
                master=table_frame,
                row=len(data),
                column=len(columns),
                values=data,
                colors=["#222224", "#2c2c2c"],
                header_color="#0f4bf2",
                hover_color="#444",
                font=("", 13),
                corner_radius=10,
                fg_color="#222224",
                text_color="white"
            )
            placetable(table)

            def update_scroll(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            def search():
                empid=empid_entry.get().strip()
                empname=empname_entry.get().lower().strip()

                if not empid or not empname:
                    result_label.configure(text="Fill Both The Details ",text_color="red")
                    return
                try:
                    empid=int(empid)
                except Exception as e:
                    result_label.configure(text="Invalid Employee Id ",text_color="red")
                    print(e)
                    return

                try:
                    connection=connect_db()
                    cursor=connection.cursor()
                    cursor.execute("select employee_id, full_name, TO_CHAR(dob,'DD-MON-YYYY'), gender, email, phone_number, address, job_role, salary from employee where employee_id=:1 and lower(full_name)=:2",(empid,empname))
                    result=cursor.fetchone()
                    print(result)
                    if result:
                        data2=[columns]
                        data2.append(list(result))
                        table2 = CTkTable(
                            master=table_frame,
                            row=len(data),
                            column=len(columns),
                            values=data2,
                            colors=["#222224", "#2c2c2c"],
                            header_color="#0f4bf2",
                            hover_color="#444",
                            font=("", 13),
                            corner_radius=10,
                            fg_color="#222224",
                            text_color="white"
                        )
                        def back2():
                            viewemployeeframe.pack_forget()
                            viewemployee()
                        CTkButton(viewemployeeframe,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back2).place(x=0,y=0)
                
                        placetable(table2)
                        empid_entry.delete(0,"end")
                        empname_entry.delete(0,"end")
                    else:
                        result_label.configure(text="No Match Found",text_color="red")
                except Exception as e:
                    print(e)
            CTkButton(viewemployeeframe,text="search",text_color="white", font=("", 20, "bold"),fg_color="blue",bg_color="#222224",width=150,height=45,corner_radius=20,command=search).place(x=700,y=400)     
        

            table_frame.bind("<Configure>", update_scroll)
        CTkButton(frame2,text="Employees Details", font=("", 20, "bold"),height=35, width=180,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=viewemployee).pack(pady=10)

        def viewcustomers():
            frame2.grid_forget()
            viewcustomerframe=CTkFrame(managerframe,width=890,height=500,fg_color="#222224")
            viewcustomerframe.pack(fill="both", expand=True)

            current_table = None
            def placetable(ct):
                nonlocal current_table
                if current_table is not None :
                    current_table.pack_forget()

                current_table = ct
                current_table.pack(fill="both", expand=True, padx=0, pady=0)
             

            def back():
                viewcustomerframe.pack_forget()
                manager_frame()
            CTkButton(viewcustomerframe,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back).place(x=0,y=0)

            canvas = tk.Canvas(viewcustomerframe, width=1090, height=250, bg="#222224", highlightthickness=0)
            canvas.place(x=0, y=40)

            h_scroll = tk.Scrollbar(viewcustomerframe, orient="horizontal", command=canvas.xview)
            h_scroll.place(x=0, y=290, width=1100)

            v_scroll = tk.Scrollbar(viewcustomerframe, orient="vertical", background="blue",troughcolor="lightgray",activebackground="red",command=canvas.yview)
            v_scroll.place(x=1090, y=40, height=250)

            canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

            table_frame =CTkFrame(canvas, fg_color="#222224",width=990, height=250, corner_radius=20)
            canvas.create_window((0, 0), window=table_frame, anchor="nw")

            columns = ["id", "Name", "Date of Birth", "gender", "address", "number", "email"]
           
            data = [columns]

            try:
                connection = connect_db()
                cursor = connection.cursor()
                cursor.execute("select customer_id, name, TO_CHAR(dob,'DD-MON-YYYY'), gender, address, phone, email FROM customer")
                rows = cursor.fetchall()

                if rows:
                    for row in rows:
                        data.append(list(row))
                else:
                    data.append(["-", "No data", "-", "-", "-", "-", "-", "-"])
            except Exception as e:
                pass
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            table = CTkTable(
                master=table_frame,
                row=len(data),
                column=len(columns),
                values=data,
                colors=["#222224", "#2c2c2c"],
                header_color="#0f4bf2",
                hover_color="#444",
                font=("", 13),
                corner_radius=10,
                fg_color="#222224",
                text_color="white"
            )
            placetable(table)

            def update_scroll(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            
            table_frame.bind("<Configure>", update_scroll)

            CTkLabel(viewcustomerframe,text="Customer Id : ",text_color="white",font=("",22,"bold")).place(x=30,y=300)
            CTkLabel(viewcustomerframe,text="Custoomer Name : ",text_color="white",font=("",22,"bold")).place(x=30,y=360)

            customerid_entry=CTkEntry(viewcustomerframe,text_color="white",font=("",20,"bold"),placeholder_text="Customer Id",placeholder_text_color="white",fg_color="black",corner_radius=20,height=45,width=200)
            customerid_entry.place(x=230,y=290)

            customername_entry=CTkEntry(viewcustomerframe,text_color="white",font=("",20,"bold"),placeholder_text="Customer Name",placeholder_text_color="white",fg_color="black",corner_radius=20,height=45,width=200)
            customername_entry.place(x=230,y=350)

            result_label=CTkLabel(viewcustomerframe,text="",text_color="white",font=("",22,"bold"))
            result_label.place(x=30,y=420)
            
            def search():
                customerid=customerid_entry.get().strip()
                customername=customername_entry.get().lower().strip()

                if not customerid or not customername:
                    result_label.configure(text="Fill Both The Details ",text_color="red")
                    return
                try:
                    customerid=int(customerid)
                except Exception as e:
                    result_label.configure(text="Invalid Customer Id ",text_color="red")
                    print(e)
                    return

                try:
                    connection=connect_db()
                    cursor=connection.cursor()
                    cursor.execute("select customer_id, name, TO_CHAR(dob,'DD-MON-YYYY'), gender, address, phone, address, email from customer where customer_id=:1 and lower(name)=:2",(customerid,customername))
                    result=cursor.fetchone()
                    if result:
                        data2=[columns]
                        data2.append(list(result))
                        table2 = CTkTable(
                            master=table_frame,
                            row=len(data),
                            column=len(columns),
                            values=data2,
                            colors=["#222224", "#2c2c2c"],
                            header_color="#0f4bf2",
                            hover_color="#444",
                            font=("", 13),
                            corner_radius=10,
                            fg_color="#222224",
                            text_color="white"
                        )
                        placetable(table2)
                        def back2():
                            viewcustomerframe.pack_forget()
                            viewcustomers()
                        CTkButton(viewcustomerframe,text="⬅",fg_color="blue",bg_color="#222224",width=40,height=30,command=back2).place(x=0,y=0)
                        customerid_entry.delete(0,"end")
                        customername_entry.delete(0,"end")
                    else:
                        result_label.configure(text="No Match Found",text_color="red")
                except Exception as e:
                    print(e)
            CTkButton(viewcustomerframe,text="search",text_color="white", font=("", 20, "bold"),fg_color="blue",bg_color="#222224",width=150,height=45,corner_radius=20,command=search).place(x=700,y=400)     
        CTkButton(frame2,text="Customer Details", font=("", 20, "bold"),height=35, width=210,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=viewcustomers).pack(pady=10)

        # def changeemp_details():
            

        def logout():
            managerframe.pack_forget()
            login_frame()
        CTkButton(frame2,text="Logout", font=("", 20, "bold"),height=35, width=210,fg_color="blue",bg_color="#222224",cursor="hand2", corner_radius=15,command=logout).pack(pady=10)
    
    CTkButton(managerframe,text="☰",fg_color="blue",bg_color="#222224",width=50,height=30,command=menu).place(x=0,y=0)

# teller_frame()

# manager_frame()
# customer_frame()
# create_employee_account()
login_frame()

# loanofficer_frame()

main.mainloop()