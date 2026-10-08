import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3



conn = sqlite3.connect("student_management.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    city TEXT,
    age INTEGER NOT NULL,
    occupation TEXT NOT NULL
)
""")

conn.commit()




cursor.execute("PRAGMA table_info(students)")
columns_in_db = [column[1] for column in cursor.fetchall()]



if "occupation" not in columns_in_db:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN occupation TEXT
    """)

    conn.commit()




root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x700")
root.configure(bg="#EAF4FF")
root.resizable(True, True)





def clear_fields():
    fullname_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    occupation_entry.delete(0, tk.END)

    for item in tree.selection():
        tree.selection_remove(item)


def load_students():
    
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("""
        SELECT
            id,
            fullname,
            email,
            phone,
            city,
            age,
            occupation
        FROM students
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert(
            "",
            tk.END,
            values=row
        )


def get_form_data():
    fullname = fullname_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    city = city_entry.get().strip()
    age = age_entry.get().strip()
    occupation = occupation_entry.get().strip()

    return (
        fullname,
        email,
        phone,
        city,
        age,
        occupation
    )


def validate_form():
    fullname, email, phone, city, age, occupation = get_form_data()

    
    if fullname == "":
        messagebox.showerror(
            "Error",
            "Full Name is required."
        )
        return None

    
    if age == "":
        messagebox.showerror(
            "Error",
            "Age is required."
        )
        return None

    
    try:
        age = int(age)

        if age <= 0 or age > 120:
            messagebox.showerror(
                "Error",
                "Age must be between 1 and 120."
            )
            return None

    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return None

    
    if occupation == "":
        messagebox.showerror(
            "Error",
            "Occupation is required."
        )
        return None

    return (
        fullname,
        email,
        phone,
        city,
        age,
        occupation
    )


def add_student():
    data = validate_form()

    if data is None:
        return

    fullname, email, phone, city, age, occupation = data

    try:
        cursor.execute("""
            INSERT INTO students (
                fullname,
                email,
                phone,
                city,
                age,
                occupation
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            fullname,
            email,
            phone,
            city,
            age,
            occupation
        ))

        conn.commit()

        load_students()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not add student.\n\n{error}"
        )


def select_student(event=None):
    selected = tree.selection()

    if not selected:
        return

    values = tree.item(
        selected[0],
        "values"
    )

    
    fullname_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    occupation_entry.delete(0, tk.END)

    
    fullname_entry.insert(
        0,
        values[1]
    )

    email_entry.insert(
        0,
        values[2]
    )

    phone_entry.insert(
        0,
        values[3]
    )

    city_entry.insert(
        0,
        values[4]
    )

    age_entry.insert(
        0,
        values[5]
    )

    occupation_entry.insert(
        0,
        values[6]
    )


def update_student():
    selected = tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a student first."
        )
        return

    student_id = tree.item(
        selected[0],
        "values"
    )[0]

    data = validate_form()

    if data is None:
        return

    fullname, email, phone, city, age, occupation = data

    try:
        cursor.execute("""
            UPDATE students
            SET
                fullname = ?,
                email = ?,
                phone = ?,
                city = ?,
                age = ?,
                occupation = ?
            WHERE id = ?
        """, (
            fullname,
            email,
            phone,
            city,
            age,
            occupation,
            student_id
        ))

        conn.commit()

        load_students()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not update student.\n\n{error}"
        )


def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a student first."
        )
        return

    student_id = tree.item(
        selected[0],
        "values"
    )[0]

    answer = messagebox.askyesno(
        "Delete Student",
        "Are you sure you want to delete this student?"
    )

    if not answer:
        return

    try:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()

        load_students()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not delete student.\n\n{error}"
        )


def close_window():
    conn.close()
    root.destroy()




title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#EAF4FF",
    fg="#1E3A5F"
)

title.pack(pady=15)




input_frame = tk.Frame(
    root,
    bg="#EAF4FF"
)

input_frame.pack(pady=5)



tk.Label(
    input_frame,
    text="Full Name *",
    font=("Arial", 11, "bold"),
    bg="#EAF4FF"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

fullname_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11)
)

fullname_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)



tk.Label(
    input_frame,
    text="Email",
    font=("Arial", 11, "bold"),
    bg="#EAF4FF"
).grid(
    row=0,
    column=2,
    padx=10,
    pady=8,
    sticky="w"
)

email_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11)
)

email_entry.grid(
    row=0,
    column=3,
    padx=10,
    pady=8
)


tk.Label(
    input_frame,
    text="Phone",
    font=("Arial", 11, "bold"),
    bg="#EAF4FF"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

phone_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11)
)

phone_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    input_frame,
    text="City",
    font=("Arial", 11, "bold"),
    bg="#EAF4FF"
).grid(
    row=1,
    column=2,
    padx=10,
    pady=8,
    sticky="w"
)

city_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11)
)

city_entry.grid(
    row=1,
    column=3,
    padx=10,
    pady=8
)



tk.Label(
    input_frame,
    text="Age *",
    font=("Arial", 11, "bold"),
    bg="#EAF4FF"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

age_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11)
)

age_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    input_frame,
    text="Occupation *",
    font=("Arial", 11, "bold"),
    bg="#EAF4FF"
).grid(
    row=2,
    column=2,
    padx=10,
    pady=8,
    sticky="w"
)

occupation_entry = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 11)
)

occupation_entry.grid(
    row=2,
    column=3,
    padx=10,
    pady=8
)

button_frame = tk.Frame(
    root,
    bg="#EAF4FF"
)

button_frame.pack(pady=15)


tk.Button(
    button_frame,
    text="ADD",
    width=12,
    bg="#26A69A",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=add_student
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    button_frame,
    text="UPDATE",
    width=12,
    bg="#42A5F5",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=update_student
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    button_frame,
    text="DELETE",
    width=12,
    bg="#EF5350",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=delete_student
).grid(
    row=0,
    column=2,
    padx=5
)


tk.Button(
    button_frame,
    text="CLEAR",
    width=12,
    bg="#7E57C2",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)



table_frame = tk.Frame(
    root,
    bg="#EAF4FF"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


columns = (
    "ID",
    "Full Name",
    "Email",
    "Phone",
    "City",
    "Age",
    "Occupation"
)


tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)




for column in columns:
    tree.heading(
        column,
        text=column
    )




tree.column(
    "ID",
    width=50,
    anchor="center"
)

tree.column(
    "Full Name",
    width=180
)

tree.column(
    "Email",
    width=220
)

tree.column(
    "Phone",
    width=140
)

tree.column(
    "City",
    width=140
)

tree.column(
    "Age",
    width=70,
    anchor="center"
)

tree.column(
    "Occupation",
    width=180
)




vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=tree.xview
)

tree.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


tree.pack(
    side="left",
    fill="both",
    expand=True
)

vertical_scrollbar.pack(
    side="right",
    fill="y"
)

horizontal_scrollbar.pack(
    side="bottom",
    fill="x"
)



tree.bind(
    "<<TreeviewSelect>>",
    select_student
)



load_students()

root.protocol(
    "WM_DELETE_WINDOW",
    close_window
)

root.mainloop()
