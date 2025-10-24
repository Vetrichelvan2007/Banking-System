import tkinter as tk
from tkinter import ttk
root=tk.Tk()

root.geometry("300x300")
root.title("Contact Book")
root.config(bg="#22262e") 

def but1():

    def details():
        dis.config(text="",fg="white")
        name=entry_name.get().strip()
        number =entry_number.get()
        email=entry_email.get()
        if not name or not number or not email:
            dis.config(text="Please fill all fields.",fg="red")
            return
        try:
            with open ("contacts.txt","r") as file:
                contacts=file.readlines()
                for contact in contacts:
                   na,nu,em= contact.split(",")
                   if nu.split(":")[1].strip()==number.strip():
                    dis.config(text="contact already exist on that number!",fg="red")
                    return 
        except FileNotFoundError:
            pass
        if not number.isdigit() or len(number) != 10:
            dis.config(text="Invalid input. Please enter a valid number.",fg="red")
            return
        
        try:
            with open("contacts.txt","a") as file:
                file.write(f"Name: {name}, Number: {number}, Email: {email}\n")
                dis.config(text="Contact added successfully.")
        except FileNotFoundError:
            return


    root1=tk.Toplevel(root)
    root1.geometry("300x300")
    root1.title("Add Contact")
    root1.config(bg="#22262e")
    
    lab1=tk.Label(root1,text="Enter contact name:",bg="#22262e",fg="white",font=("Arial Rounded MT Bold ",9,"bold"))
    lab1.grid(row=0, column=0, padx=10, pady=10, sticky="w") 

    entry_name=tk.Entry(root1,width=15,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"))
    entry_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    lab2=tk.Label(root1,text="Enter the phone number: ",bg="#22262e",fg="white",font=("Arial Rounded MT Bold ",9,"bold"))
    lab2.grid(row=2, column=0, padx=10, pady=10, sticky="w") 

    entry_number=tk.Entry(root1,width=15,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"))
    entry_number.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    lab3=tk.Label(root1,text="Enter the email address: ",bg="#22262e",fg="white",font=("Arial Rounded MT Bold ",9,"bold"))
    lab3.grid(row=4, column=0, padx=10, pady=10, sticky="w") 

    entry_email=tk.Entry(root1,width=15,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"))
    entry_email.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    dis=tk.Label(root1,text="",font=("Arial Rounded MT Bold ",12,"bold"),bg="#22262e",fg="white")
    dis.place(x=14, y=230)

    save=tk.Button(root1,text="Save",width=10,height=1,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"),command=details)
    save.place(x=80,y=160)

    exit=tk.Button(root1,text="Exit",width=10,height=1,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"),command=root1.destroy)
    exit.place(x=80,y=200)

    

def but2():
    try:
        with open ("contacts.txt","r") as file:
            contacts=file.readlines()
            if contacts:
                root2=tk.Toplevel(root)
                # root2.geometry("300x300")
                root2.title("View Contacts")
                root2.config(bg="#22262e")
                tree= ttk.Treeview(root2,columns=("Name","Number","Email"),show="headings")
                style = ttk.Style()
                style.configure("Treeview",background="#22262e",foreground="white",rowheight=25,    fieldbackground="#22262e")
                style.map("Treeview", background=[("selected", "#42506b")])

                tree.heading("Name", text="Name")
                tree.heading("Number", text="Number")
                tree.heading("Email", text="Email")
                for contact in contacts:
                    name,number,email=contact.strip().split(",")
                    name= name.split(":")[1].strip()
                    number= number.split(":")[1].strip()    
                    email= email.split(":")[1].strip()
                    tree.insert("", "end", values=(name, number, email))
                tree.pack(expand=True, fill="both")

    except FileNotFoundError:
        root2=tk.Toplevel(root)
        # root2.geometry("300x300")
        root2.title("View Contacts")
        root2.config(bg="#22262e")
        
        lab3=tk.Label(root2,text="no contacts found",bg="#22262e",fg="white",font=("Arial Rounded MT Bold ",9,"bold"))
        lab3.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        

button1=tk.Button(root,text= "Add contact",width= 20,height= 2,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"),command=but1)
button1.pack(pady=10, expand=True)

button2=tk.Button(root,text= "View contacts",width= 20,height= 2,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"),command=but2)
button2.pack(pady=10, expand=True)

button3=tk.Button(root,text= "Delete contact",width= 20,height= 2,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"))
button3.pack(pady=10, expand=True)

button3=tk.Button(root,text= "Exit",width= 20,height= 2,bg="#42506b",fg="white",font=("Arial Rounded MT Bold ",12,"bold"),command=root.destroy)
button3.pack(pady=10, expand=True)

root.mainloop()

