# 🟩 Zepto Delivery Management System 
# Developed in Python + SQLite + Tkinter GUI

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE CONNECTION ---------------- #
conn = sqlite3.connect("zepto_delivery.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    item_name TEXT NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL
)
""")
conn.commit()

# ---------------- FUNCTIONS ---------------- #

def add_order():
    name = entry_name.get()
    item = entry_item.get()
    amt = entry_amount.get()
    status = status_var.get()

    if not (name and item and amt):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    cursor.execute("INSERT INTO Orders (customer_name, item_name, amount, status) VALUES (?, ?, ?, ?)",
                   (name, item, amt, status))
    conn.commit()
    messagebox.showinfo("Success", "Order Added Successfully!")
    clear_fields()
    fetch_orders()

def fetch_orders():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM Orders")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def delete_order():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an order to delete.")
        return
    order_id = tree.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM Orders WHERE order_id=?", (order_id,))
    conn.commit()
    fetch_orders()
    messagebox.showinfo("Deleted", "Order Deleted Successfully!")

def update_status():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an order to update.")
        return
    order_id = tree.item(selected_item)['values'][0]
    new_status = status_var.get()
    cursor.execute("UPDATE Orders SET status=? WHERE order_id=?", (new_status, order_id))
    conn.commit()
    fetch_orders()
    messagebox.showinfo("Updated", "Order Status Updated Successfully!")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    status_var.set("Pending")

# ---------------- GUI DESIGN ---------------- #
root = tk.Tk()
root.title("Zepto Delivery Management System")
root.geometry("800x600")
root.config(bg="#e8f0f7")

# --- Title --- #
title_label = tk.Label(root, text="🚚 Zepto Delivery Management System", font=("Arial", 18, "bold"), bg="#004aad", fg="white", pady=10)
title_label.pack(fill=tk.X)

# --- Input Frame --- #
frame = tk.Frame(root, bg="#e8f0f7", pady=10)
frame.pack(fill=tk.X)

tk.Label(frame, text="Customer Name:", bg="#e8f0f7", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_name = tk.Entry(frame, width=25, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Item Name:", bg="#e8f0f7", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_item = tk.Entry(frame, width=25, font=("Arial", 12))
entry_item.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Amount (₹):", bg="#e8f0f7", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_amount = tk.Entry(frame, width=25, font=("Arial", 12))
entry_amount.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="Status:", bg="#e8f0f7", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
status_var = tk.StringVar(value="Pending")
status_menu = ttk.Combobox(frame, textvariable=status_var, values=["Pending", "Delivered", "Cancelled"], state="readonly", width=22, font=("Arial", 12))
status_menu.grid(row=3, column=1, padx=10, pady=5)

# --- Buttons --- #
btn_frame = tk.Frame(root, bg="#e8f0f7")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Order", command=add_order, bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=12).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Update Status", command=update_status, bg="#007bff", fg="white", font=("Arial", 12, "bold"), width=12).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Delete Order", command=delete_order, bg="#dc3545", fg="white", font=("Arial", 12, "bold"), width=12).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Clear Fields", command=clear_fields, bg="#ffc107", fg="black", font=("Arial", 12, "bold"), width=12).grid(row=0, column=3, padx=10)

# --- Order Table --- #
tree_frame = tk.Frame(root)
tree_frame.pack(pady=20)

columns = ("Order ID", "Customer Name", "Item Name", "Amount", "Status")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=140)
tree.pack(side="left", fill="y")

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

fetch_orders()

root.mainloop()
conn.close()