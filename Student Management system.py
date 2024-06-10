import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Database operations
def create_table():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def generate_roll_no():
    year = "22"
    dept = "CSR"
    num = len(get_students()) + 1
    return f"{year}{dept}{num:03d}"

def insert_student(roll_no, name, email, age, gender):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (roll_no, name, email, age, gender) VALUES (?, ?, ?, ?, ?)
    ''', (roll_no, name, email, age, gender))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    rows = cur.fetchall()
    conn.close()
    return rows

def update_student(roll_no, name, email, age, gender):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    UPDATE students SET name = ?, email = ?, age = ?, gender = ? WHERE roll_no = ?
    ''', (name, email, age, gender, roll_no))
    conn.commit()
    conn.close()

def delete_student(roll_no):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
    DELETE FROM students WHERE roll_no = ?
    ''', (roll_no,))
    conn.commit()
    conn.close()

def validate_input(name, email, age, gender, roll_no=None):
    if not name:
        messagebox.showerror('Error', 'Name cannot be empty')
        return False
    if not email or '@' not in email:
        messagebox.showerror('Error', 'Invalid email')
        return False
    if not age.isdigit():
        messagebox.showerror('Error', 'Age must be an integer')
        return False
    if gender not in ['Male', 'Female', 'Other']:
        messagebox.showerror('Error', 'Gender must be Male, Female, or Other')
        return False
    if roll_no and not (roll_no.startswith("22CSR") and len(roll_no) == 8 and roll_no[5:].isdigit()):
        messagebox.showerror('Error', 'Roll No must be in the format 22CSRxxx')
        return False
    return True

# GUI operations
def show_frame(frame):
    frame.tkraise()

def add_student():
    name = name_entry.get()
    email = email_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    if validate_input(name, email, age, gender):
        age = int(age)
        roll_no = generate_roll_no()
        insert_student(roll_no, name, email, age, gender)
        messagebox.showinfo('Success', 'Student added')
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        gender_var.set('')

def update_student_details():
    roll_no = roll_no_entry_update.get()
    name = name_entry_update.get()
    email = email_entry_update.get()
    age = age_entry_update.get()
    gender = gender_var_update.get()
    if validate_input(name, email, age, gender, roll_no):
        age = int(age)
        update_student(roll_no, name, email, age, gender)
        messagebox.showinfo('Success', 'Student updated')
        roll_no_entry_update.delete(0, tk.END)
        name_entry_update.delete(0, tk.END)
        email_entry_update.delete(0, tk.END)
        age_entry_update.delete(0, tk.END)
        gender_var_update.set('')

def delete_student_details():
    roll_no = roll_no_entry_delete.get()
    if roll_no:
        delete_student(roll_no)
        messagebox.showinfo('Success', 'Student deleted')
        roll_no_entry_delete.delete(0, tk.END)
    else:
        messagebox.showerror('Error', 'Roll No cannot be empty')

def refresh_view():
    for row in view_tree.get_children():
        view_tree.delete(row)
    for row in get_students():
        view_tree.insert('', tk.END, values=row)

root = tk.Tk()
root.title('Student Management System')
root.geometry('800x600')

create_table()

# Apply styles
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 12), padding=5)
style.configure('TEntry', font=('Helvetica', 12), padding=5)
style.configure('TCombobox', font=('Helvetica', 12), padding=5)
style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))
style.configure('Treeview', font=('Helvetica', 12))

# Define frames
add_frame = tk.Frame(root)
update_frame = tk.Frame(root)
delete_frame = tk.Frame(root)
view_frame = tk.Frame(root)

for frame in (add_frame, update_frame, delete_frame, view_frame):
    frame.grid(row=0, column=1, sticky='nsew', padx=20, pady=20)

# Add frame layout
ttk.Label(add_frame, text='Add Student', font=('Helvetica', 18, 'bold')).pack(pady=10)
ttk.Label(add_frame, text='Name:').pack(pady=5)
name_entry = ttk.Entry(add_frame)
name_entry.pack(pady=5)
ttk.Label(add_frame, text='Email:').pack(pady=5)
email_entry = ttk.Entry(add_frame)
email_entry.pack(pady=5)
ttk.Label(add_frame, text='Age:').pack(pady=5)
age_entry = ttk.Entry(add_frame)
age_entry.pack(pady=5)
ttk.Label(add_frame, text='Gender:').pack(pady=5)
gender_var = tk.StringVar()
gender_dropdown = ttk.Combobox(add_frame, textvariable=gender_var, values=['Male', 'Female', 'Other'])
gender_dropdown.pack(pady=5)
ttk.Button(add_frame, text='Add', command=add_student, style='Add.TButton').pack(pady=10)

# Update frame layout
ttk.Label(update_frame, text='Update Student', font=('Helvetica', 18, 'bold')).pack(pady=10)
ttk.Label(update_frame, text='Roll No:').pack(pady=5)
roll_no_entry_update = ttk.Entry(update_frame)
roll_no_entry_update.pack(pady=5)
ttk.Label(update_frame, text='Name:').pack(pady=5)
name_entry_update = ttk.Entry(update_frame)
name_entry_update.pack(pady=5)
ttk.Label(update_frame, text='Email:').pack(pady=5)
email_entry_update = ttk.Entry(update_frame)
email_entry_update.pack(pady=5)
ttk.Label(update_frame, text='Age:').pack(pady=5)
age_entry_update = ttk.Entry(update_frame)
age_entry_update.pack(pady=5)
ttk.Label(update_frame, text='Gender:').pack(pady=5)
gender_var_update = tk.StringVar()
gender_dropdown_update = ttk.Combobox(update_frame, textvariable=gender_var_update, values=['Male', 'Female', 'Other'])
gender_dropdown_update.pack(pady=5)
ttk.Button(update_frame, text='Update', command=update_student_details, style='Update.TButton').pack(pady=10)

# Delete frame layout
ttk.Label(delete_frame, text='Delete Student', font=('Helvetica', 18, 'bold')).pack(pady=10)
ttk.Label(delete_frame, text='Roll No:').pack(pady=5)
roll_no_entry_delete = ttk.Entry(delete_frame)
roll_no_entry_delete.pack(pady=5)
ttk.Button(delete_frame, text='Delete', command=delete_student_details, style='Delete.TButton').pack(pady=10)

# View frame layout
ttk.Label(view_frame, text='View Students', font=('Helvetica', 18, 'bold')).pack(pady=10)
columns = ('ID', 'Roll No', 'Name', 'Email', 'Age', 'Gender')
view_tree = ttk.Treeview(view_frame, columns=columns, show='headings')
for col in columns:
    view_tree.heading(col, text=col)
view_tree.pack(pady=10, fill='both', expand=True)
refresh_view()

# Sidebar layout
sidebar = tk.Frame(root, bg='#333')
sidebar.grid(row=0, column=0)

ttk.Button(sidebar, text='Add Student', command=lambda: show_frame(add_frame), style='Sidebar.TButton').pack(fill='x', pady=4)
ttk.Button(sidebar, text='Update Student', command=lambda: show_frame(update_frame), style='Sidebar.TButton').pack(fill='x', pady=4)
ttk.Button(sidebar, text='Delete Student', command=lambda: show_frame(delete_frame), style='Sidebar.TButton').pack(fill='x', pady=4)
ttk.Button(sidebar, text='View Students', command=lambda: show_frame(view_frame), style='Sidebar.TButton').pack(fill='x', pady=4)

show_frame(add_frame)

# Define button styles
style.configure('Add.TButton', background='green')
style.configure('Update.TButton', background='orange')
style.configure('Delete.TButton', background='red')
style.configure('Sidebar.TButton', background='#333')

root.mainloop()
