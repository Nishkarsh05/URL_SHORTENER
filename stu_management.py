import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def create_table():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            course TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database table
create_table()

# Functions for CRUD operations
def add_student():
    name = entry_name.get()
    roll_no = entry_roll.get()
    course = entry_course.get()
    grade = entry_grade.get()

    if name and roll_no and course and grade:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, roll_no, course, grade)
            VALUES (?, ?, ?, ?)
        ''', (name, roll_no, course, grade))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        clear_entries()
        view_students()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

def view_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    # Clear the listbox before displaying new data
    listbox_students.delete(0, tk.END)

    # Insert data into the listbox
    for row in rows:
        listbox_students.insert(tk.END, row)

def update_student():
    selected_student = listbox_students.get(tk.ACTIVE)
    if selected_student:
        student_id = selected_student[0]
        name = entry_name.get()
        roll_no = entry_roll.get()
        course = entry_course.get()
        grade = entry_grade.get()

        if name and roll_no and course and grade:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students
                SET name=?, roll_no=?, course=?, grade=?
                WHERE id=?
            ''', (name, roll_no, course, grade, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student updated successfully!")
            clear_entries()
            view_students()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")
    else:
        messagebox.showwarning("Selection Error", "Please select a student to update!")

def delete_student():
    selected_student = listbox_students.get(tk.ACTIVE)
    if selected_student:
        student_id = selected_student[0]
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student deleted successfully!")
        clear_entries()
        view_students()
    else:
        messagebox.showwarning("Selection Error", "Please select a student to delete!")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_grade.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x400")

# Labels
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Roll No").grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, text="Course").grid(row=2, column=0, padx=10, pady=10)
tk.Label(root, text="Grade").grid(row=3, column=0 , padx=10, pady=10)

# Entry fields
entry_name = tk.Entry(root)
entry_roll = tk.Entry(root)
entry_course = tk.Entry(root)
entry_grade = tk.Entry(root)

entry_name.grid(row=0, column=1, padx=10, pady=10)
entry_roll.grid(row=1, column=1, padx=10, pady=10)
entry_course.grid(row=2, column=1, padx=10, pady=10)
entry_grade.grid(row=3, column=1, padx=10, pady=10)

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Update Student", command=update_student).grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Student", command=delete_student).grid(row=4, column=2, padx=10, pady=10)

# Listbox to display students
listbox_students = tk.Listbox(root, width=50)
listbox_students.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# View existing students on startup
view_students()

# Run the application
root.mainloop()