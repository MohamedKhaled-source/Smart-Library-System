import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import library_data as db
import library_functions as lib
import os
import datetime

# ==========================================
# HELPER: TRANSACTION LOGGING
# ==========================================
def log_transaction(message):
    """Writes a message with a timestamp to transaction_log.txt"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        # Appends to the file in the same directory as the script
        with open("transaction_log.txt", "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Logging failed: {e}")

# ==========================================
# MAIN GUI CLASS
# ==========================================
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System - Professional Edition")
        self.root.geometry("1100x750")
        
        # Styles
        style = ttk.Style()
        style.theme_use('clam')

        # Create Tabs
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")

        # Initialize Tabs
        self.tab_manage = ttk.Frame(self.tabs)
        self.tab_borrow = ttk.Frame(self.tabs)
        self.tab_shop = ttk.Frame(self.tabs)
        self.tab_stats = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_manage, text="Manage Books")
        self.tabs.add(self.tab_borrow, text="Borrow / Return")
        self.tabs.add(self.tab_shop, text="Shop / Sales")
        self.tabs.add(self.tab_stats, text="Statistics & Logs")

        # Build Interfaces
        self.build_manage_tab()
        self.build_borrow_tab()
        self.build_shop_tab()
        self.build_stats_tab()

    # =========================================================================
    # TAB 1: MANAGE BOOKS (CRUD + SEARCH)
    # =========================================================================
    def build_manage_tab(self):
        left_panel = tk.Frame(self.tab_manage)
        left_panel.pack(side="top", fill="x", padx=10, pady=5)

        # --- INPUTS ---
        frame_input = ttk.LabelFrame(left_panel, text="Book Details")
        frame_input.pack(fill="x", pady=5)

        self.var_id = tk.StringVar()
        self.var_title = tk.StringVar()
        self.var_author = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_type = tk.StringVar()
        self.var_copies = tk.IntVar(value=1)
        self.var_price = tk.DoubleVar(value=0.0)
        self.var_rating = tk.DoubleVar(value=0.0)

        # Row 0
        tk.Label(frame_input, text="ID (Auto):").grid(row=0, column=0, padx=5, pady=5)
        ent_id = tk.Entry(frame_input, textvariable=self.var_id, state='readonly', width=10)
        ent_id.grid(row=0, column=1, sticky="w")

        tk.Label(frame_input, text="Title:*").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(frame_input, textvariable=self.var_title, width=30).grid(row=0, column=3, columnspan=3, sticky="w")

        # Row 1
        tk.Label(frame_input, text="Author:*").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame_input, textvariable=self.var_author).grid(row=1, column=1)

        tk.Label(frame_input, text="Year:*").grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(frame_input, textvariable=self.var_year, width=10).grid(row=1, column=3, sticky="w")

        tk.Label(frame_input, text="Type:*").grid(row=1, column=4, padx=5, pady=5)
        types = ["Fiction", "Classic", "Fantasy", "Sci-Fi", "Non-Fiction", "Mystery", "Horror", "Comedy", "Action"]
        self.combo_type = ttk.Combobox(frame_input, textvariable=self.var_type, values=types, width=12)
        self.combo_type.grid(row=1, column=5)

        # Row 2
        tk.Label(frame_input, text="Copies:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(frame_input, textvariable=self.var_copies, width=10).grid(row=2, column=1, sticky="w")

        tk.Label(frame_input, text="Price:").grid(row=2, column=2, padx=5, pady=5)
        tk.Entry(frame_input, textvariable=self.var_price, width=10).grid(row=2, column=3, sticky="w")
        
        tk.Label(frame_input, text="Rating:").grid(row=2, column=4, padx=5, pady=5)
        tk.Entry(frame_input, textvariable=self.var_rating, width=10).grid(row=2, column=5, sticky="w")

        # --- BUTTONS ---
        frame_btns = tk.Frame(left_panel)
        frame_btns.pack(fill="x", pady=5)
        
        tk.Button(frame_btns, text="Add Book", bg="#d9fdd3", command=self.add_book_gui).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Update Selected", bg="#ffebcd", command=self.update_book_gui).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Delete Selected", bg="#ffcccb", command=self.delete_book_gui).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Clear Input", command=self.clear_fields).pack(side="left", padx=5)
        
        # Red Delete All Button
        tk.Button(frame_btns, text="DELETE ALL BOOKS", bg="red", fg="white", command=self.clear_library_gui).pack(side="right", padx=5)

        # --- SEARCH & FILTER ---
        frame_search = ttk.LabelFrame(left_panel, text="Search & Filter Books")
        frame_search.pack(fill="x", pady=10)

        tk.Label(frame_search, text="By ID:").pack(side="left", padx=5)
        self.search_id_var = tk.StringVar()
        tk.Entry(frame_search, textvariable=self.search_id_var, width=10).pack(side="left", padx=5)
        tk.Button(frame_search, text="Find", command=self.search_by_id_gui).pack(side="left", padx=2)

        tk.Label(frame_search, text="| By Author:").pack(side="left", padx=10)
        self.search_auth_var = tk.StringVar()
        tk.Entry(frame_search, textvariable=self.search_auth_var, width=15).pack(side="left", padx=5)
        tk.Button(frame_search, text="Filter", command=self.filter_by_author_gui).pack(side="left", padx=2)

        tk.Label(frame_search, text="| By Year:").pack(side="left", padx=10)
        self.search_year_var = tk.StringVar()
        tk.Entry(frame_search, textvariable=self.search_year_var, width=10).pack(side="left", padx=5)
        tk.Button(frame_search, text="Filter", command=self.filter_by_year_gui).pack(side="left", padx=2)

        tk.Button(frame_search, text="Reset List", bg="lightgray", command=self.refresh_table).pack(side="right", padx=10)

        # --- TREEVIEW (TABLE) ---
        self.tree = ttk.Treeview(self.tab_manage, columns=("ID", "Title", "Author", "Year", "Type", "Copies", "Price", "Rating", "Sold"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Copies", text="Qty")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Rating", text="Rate")
        self.tree.heading("Sold", text="Sold")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Year", width=50, anchor="center")
        self.tree.column("Copies", width=40, anchor="center")
        self.tree.column("Price", width=50, anchor="center")
        self.tree.column("Rating", width=40, anchor="center")
        self.tree.column("Sold", width=40, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Initial Load
        self.refresh_table()

    # --- CRITICAL FIX: TABLE LOADING ---
    def refresh_table(self, dataset=None):
        """Reloads data. USES KEYS TO ENSURE IDs APPEAR."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        if dataset is None:
            # SHOW ALL: Loop through .items() to get ID from key
            for key_id, book in db.library.items():
                display_id = book.get('id', key_id)
                self.tree.insert("", "end", values=(
                    display_id, 
                    book.get('title', ''), 
                    book.get('author', ''), 
                    book.get('year', ''), 
                    book.get('type_book', ''), 
                    book.get('copies', 0), 
                    book.get('price', 0.0), 
                    book.get('global_rating', 0.0), 
                    book.get('sold', 0)
                ))
        else:
            # SHOW FILTERED
            for book in dataset:
                b_id = book.get('id', 'N/A')
                self.tree.insert("", "end", values=(
                    b_id, 
                    book.get('title', ''), 
                    book.get('author', ''), 
                    book.get('year', ''), 
                    book.get('type_book', ''), 
                    book.get('copies', 0), 
                    book.get('price', 0.0), 
                    book.get('global_rating', 0.0), 
                    book.get('sold', 0)
                ))

    def clear_fields(self):
        self.var_id.set("")
        self.var_title.set("")
        self.var_author.set("")
        self.var_year.set("")
        self.var_type.set("")
        self.var_copies.set(1)
        self.var_price.set(0.0)
        self.var_rating.set(0.0)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        item = self.tree.item(selected_item)
        values = item['values']
        
        try:
            raw_id = values[0]
            # Attempt to find book by ID
            book = None
            if raw_id in db.library:
                book = db.library[raw_id]
            else:
                try:
                    int_id = int(raw_id)
                    if int_id in db.library:
                        book = db.library[int_id]
                except:
                    pass
            
            if book:
                self.var_id.set(book.get('id', raw_id))
                self.var_title.set(book.get('title', ''))
                self.var_author.set(book.get('author', ''))
                self.var_year.set(book.get('year', ''))
                self.var_type.set(book.get('type_book', ''))
                self.var_copies.set(book.get('copies', 0))
                self.var_price.set(book.get('price', 0.0))
                self.var_rating.set(book.get('global_rating', 0.0))
        except Exception:
            pass

    # --- INPUT VALIDATION ---
    def validate_inputs(self):
        # 1. Check Empty Fields
        t = self.var_title.get().strip()
        a = self.var_author.get().strip()
        y_str = self.var_year.get().strip()
        tp = self.var_type.get().strip()
        
        if not t or not a or not y_str or not tp:
            messagebox.showerror("Error", "Title, Author, Year, and Type are required!")
            return False

        # 2. Validate Year
        try:
            y = int(y_str)
            if y < -800 or y > 2026:
                messagebox.showerror("Validation Error", "Year must be between -800 and 2026.")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Year must be a valid number.")
            return False

        # 3. Validate Price
        try:
            p = float(self.var_price.get())
            if p > 100:
                messagebox.showerror("Validation Error", "Price cannot exceed 100.")
                return False
            if p < 0:
                messagebox.showerror("Validation Error", "Price cannot be negative.")
                return False
        except:
             messagebox.showerror("Validation Error", "Invalid Price.")
             return False

        # 4. Validate Rating
        try:
            r = float(self.var_rating.get())
            if r > 5.0:
                messagebox.showerror("Validation Error", "Rating cannot exceed 5.")
                return False
            if r < 0:
                messagebox.showerror("Validation Error", "Rating cannot be negative.")
                return False
        except:
             messagebox.showerror("Validation Error", "Invalid Rating.")
             return False

        return True

    # --- BUTTON HANDLERS ---
    def add_book_gui(self):
        if not self.validate_inputs(): return

        try:
            new_id = lib.add_book(
                self.var_title.get().strip(), 
                self.var_author.get().strip(), 
                int(self.var_year.get()), 
                self.var_type.get().strip(), 
                int(self.var_copies.get()), 
                float(self.var_price.get()), 
                0, 
                float(self.var_rating.get())
            )
            log_transaction(f"Added book: '{self.var_title.get()}' (ID: {new_id})")
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", "Book Added Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def update_book_gui(self):
        raw_id = self.var_id.get()
        if not raw_id:
            messagebox.showerror("Error", "No book selected!")
            return
        
        if not self.validate_inputs(): return
        
        try:
            b_id = int(raw_id) if str(raw_id).isdigit() else raw_id

            lib.update_book(
                b_id, 
                new_title=self.var_title.get().strip(), 
                new_author=self.var_author.get().strip(),
                new_year=int(self.var_year.get()), 
                new_type_book=self.var_type.get().strip(),
                new_global_rating=float(self.var_rating.get())
            )
            # Safe Update for other fields
            if b_id in db.library:
                db.library[b_id]['copies'] = int(self.var_copies.get())
                db.library[b_id]['price'] = float(self.var_price.get())
            
            log_transaction(f"Updated book ID {b_id}")
            self.refresh_table()
            messagebox.showinfo("Success", "Book Updated!")
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    def delete_book_gui(self):
        raw_id = self.var_id.get()
        if not raw_id:
            # Fallback to selection
            sel = self.tree.selection()
            if sel: raw_id = self.tree.item(sel)['values'][0]
            else:
                messagebox.showerror("Error", "Please select a book to delete.")
                return

        b_id = int(raw_id) if str(raw_id).isdigit() else raw_id
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            lib.delete_book(b_id)
            log_transaction(f"Deleted book ID {b_id}")
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Deleted", "Book deleted successfully.")

    def clear_library_gui(self):
        if messagebox.askyesno("WARNING", "Delete ALL books?\nA backup will be created.\nProceed?"):
            backup_file = "backup_data.txt"
            try:
                # 1. Backup
                with open(backup_file, "w") as f:
                    for book in db.library.values():
                        line = (f"{book['title']},{book['author']},{book['year']},{book['type_book']},"
                                f"{book['global_rating']},{book['copies']},{book['price']},{book['sold']}\n")
                        f.write(line)
                
                # 2. Clear & Reset
                db.library.clear() # Direct Clear
                db.current_id = 1  # Reset ID Counter
                
                log_transaction(f"LIBRARY CLEARED. Backup: {backup_file}")
                self.refresh_table()
                self.clear_fields()
                messagebox.showinfo("Done", f"Library emptied.\nBackup saved to:\n{os.path.abspath(backup_file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Backup failed: {e}")

    # --- SEARCH ---
    def search_by_id_gui(self):
        try:
            bid = int(self.search_id_var.get())
            book = lib.get_book(bid)
            if book: self.refresh_table([book])
            else: messagebox.showwarning("Not Found", "No book found.")
        except: messagebox.showerror("Error", "ID must be a number.")

    def filter_by_author_gui(self):
        auth = self.search_auth_var.get()
        if not auth: return
        res = lib.book_by_author(auth)
        if res: self.refresh_table(res)
        else: messagebox.showinfo("Info", "No books found.")

    def filter_by_year_gui(self):
        y = self.search_year_var.get()
        if not y: return
        res = lib.book_by_year(y) 
        if not res and y.isdigit(): res = lib.book_by_year(int(y))
        if res: self.refresh_table(res)
        else: messagebox.showinfo("Info", "No books found.")

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path: return
        
        count = 0
        try:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line: continue 
                    parts = line.split(",")
                    if len(parts) >= 8:
                        try:
                            # Strict Parse
                            t, a, y, tp = parts[0].strip(), parts[1].strip(), int(parts[2]), parts[3].strip()
                            r, c, p, s = float(parts[4]), int(parts[5]), float(parts[6]), int(parts[7])
                            
                            nid = lib.add_book(t, a, y, tp, c, p, s, r)
                            # Fix sold count
                            if nid in db.library: db.library[nid]['sold'] = s
                            count += 1
                        except: continue 

            log_transaction(f"Imported {count} books from {file_path}")
            self.refresh_table()
            messagebox.showinfo("Success", f"Imported {count} books.")
        except Exception as e:
            messagebox.showerror("Error", f"File error: {e}")

    # =========================================================================
    # TAB 4: STATISTICS & I/O
    # =========================================================================
    def build_stats_tab(self):
        frame = ttk.LabelFrame(self.tab_stats, text="Library Statistics")
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.stats_text = tk.Text(frame, height=14, font=("Consolas", 10), state='disabled')
        self.stats_text.pack(fill="both", padx=5, pady=5)
        
        tk.Button(frame, text="Refresh Stats", bg="#d0e1f9", command=self.show_stats).pack(pady=5)

        frame_io = ttk.LabelFrame(self.tab_stats, text="Data Import / Export")
        frame_io.pack(padx=10, pady=10, fill="x")
        
        tk.Button(frame_io, text="Export Library to .txt", command=self.export_data).pack(side="left", padx=20, pady=20)
        tk.Button(frame_io, text="Import Library from .txt", command=self.import_data).pack(side="left", padx=20, pady=20)

    def show_stats(self):
        lib_list = list(db.library.values())
        if not lib_list:
            rpt = "Library is empty."
        else:
            # Stats Logic
            total = len(lib_list)
            years = [int(b['year']) for b in lib_list if str(b['year']).isdigit()]
            
            old_str, new_str = "N/A", "N/A"
            if years:
                # Find objects matching min/max year
                mn, mx = min(years), max(years)
                old_b = next((b for b in lib_list if int(b['year']) == mn), None)
                new_b = next((b for b in lib_list if int(b['year']) == mx), None)
                if old_b: old_str = f"{old_b['title']} ({mn})"
                if new_b: new_str = f"{new_b['title']} ({mx})"

            counts = {}
            for b in lib_list:
                t = b.get('type_book', 'Unknown')
                counts[t] = counts.get(t, 0) + 1

            rpt = f"=== STATISTICS ===\nTotal Books: {total}\nOldest: {old_str}\nNewest: {new_str}\n\n[GENRES]\n"
            for k, v in counts.items(): rpt += f"- {k}: {v}\n"

        self.stats_text.config(state='normal')
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, rpt)
        self.stats_text.config(state='disabled')

    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if not path: return
        try:
            with open(path, "w") as f:
                for b in db.library.values():
                    line = f"{b['title']},{b['author']},{b['year']},{b['type_book']},{b['global_rating']},{b['copies']},{b['price']},{b['sold']}\n"
                    f.write(line)
            messagebox.showinfo("Success", "Exported.")
        except Exception as e: messagebox.showerror("Error", str(e))

    # =========================================================================
    # TABS 2 & 3: BORROW / SHOP
    # =========================================================================
    def build_borrow_tab(self):
        frame = ttk.LabelFrame(self.tab_borrow, text="Borrowing")
        frame.pack(padx=20, pady=20, fill="both")
        
        tk.Label(frame, text="Book ID:").grid(row=0, column=0, pady=10)
        self.borrow_id = tk.Entry(frame)
        self.borrow_id.grid(row=0, column=1)
        
        tk.Label(frame, text="Name:").grid(row=1, column=0, pady=10)
        self.borrow_name = tk.Entry(frame)
        self.borrow_name.grid(row=1, column=1)
        
        tk.Label(frame, text="Days:").grid(row=2, column=0, pady=10)
        self.borrow_days = tk.Entry(frame)
        self.borrow_days.grid(row=2, column=1)
        
        tk.Button(frame, text="Borrow", bg="lightblue", command=self.do_borrow).grid(row=3, columnspan=2, pady=10, sticky="ew")
        
        ttk.Separator(frame).grid(row=4, columnspan=2, sticky="ew", pady=10)
        
        tk.Label(frame, text="Return ID:").grid(row=5, column=0)
        self.return_id = tk.Entry(frame)
        self.return_id.grid(row=5, column=1)
        tk.Button(frame, text="Return", bg="lightgreen", command=self.do_return).grid(row=6, columnspan=2, pady=10, sticky="ew")

    def do_borrow(self):
        try:
            bid = int(self.borrow_id.get())
            if lib.borrow_book(bid, self.borrow_name.get(), int(self.borrow_days.get())):
                log_transaction(f"Borrowed ID {bid} to {self.borrow_name.get()}")
                messagebox.showinfo("Success", "Borrowed.")
            else: messagebox.showerror("Error", "Unavailable.")
        except: messagebox.showerror("Error", "Invalid Input.")

    def do_return(self):
        try:
            bid = int(self.return_id.get())
            if lib.return_book(bid):
                log_transaction(f"Returned ID {bid}")
                messagebox.showinfo("Success", "Returned.")
            else: messagebox.showerror("Error", "Failed.")
        except: messagebox.showerror("Error", "Invalid ID.")

    def build_shop_tab(self):
        frame = ttk.LabelFrame(self.tab_shop, text="Shop")
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        tk.Label(frame, text="User ID:").grid(row=0, column=0, pady=5)
        self.shop_uid = tk.Entry(frame)
        self.shop_uid.grid(row=0, column=1)
        
        tk.Label(frame, text="Book ID:").grid(row=1, column=0, pady=5)
        self.shop_bid = tk.Entry(frame)
        self.shop_bid.grid(row=1, column=1)
        
        tk.Label(frame, text="Qty:").grid(row=2, column=0, pady=5)
        self.shop_qty = tk.Entry(frame)
        self.shop_qty.grid(row=2, column=1)
        
        tk.Button(frame, text="BUY", bg="gold", command=self.do_buy).grid(row=3, columnspan=2, pady=15, sticky="ew")
        
        self.receipt = tk.Text(frame, height=10, width=40)
        self.receipt.grid(row=4, columnspan=2)

    def do_buy(self):
        try:
            bid, qty = int(self.shop_bid.get()), int(self.shop_qty.get())
            uid = self.shop_uid.get()
            msg = lib.buy_book(uid, bid, qty, db.library)
            self.receipt.delete("1.0", tk.END)
            self.receipt.insert(tk.END, msg)
            if "RECEIPT" in msg:
                self.refresh_table()
                log_transaction(f"SALE: User {uid} bought {qty} of ID {bid}")
        except: messagebox.showerror("Error", "Invalid Input.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    # Init default data
    lib.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Classic", 5, 100.0, 0, 4.8)
    app.refresh_table()
    root.mainloop()
