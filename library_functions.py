import library_data as db


def add_book(title, author, year, type_book, copies, price, sold, global_rating=0.0):
    book_id = db.current_id
    db.library[book_id] = {
        "id": book_id,
        "title": title,
        "author": author,
        "year": year,
        "type_book": type_book,
        "copies": copies,
        "price": price,
        "sold": sold,
        "global_rating": global_rating
    }
    db.current_id += 1
    return book_id
def delete_book(book_id):
    if book_id in db.library:
        deleted_book = db.library.pop(book_id)
        return deleted_book
    else:
        return None

def update_book(book_id, new_title=None, new_author=None, new_year=None, new_type_book=None, new_global_rating=None):
    
    if book_id not in db.library:
        return None

    book = db.library[book_id]

    if new_title is not None:
        book["title"] = new_title
    if new_author is not None:
        book["author"] = new_author
    if new_year is not None:
        book["year"] = new_year
    if new_type_book is not None:
        book["type_book"] = new_type_book
    if new_global_rating is not None:   
        book["global_rating"] = new_global_rating

    return "updated"


print(update_book(2, "mohamed", "ali", 2008, "fantasy", new_global_rating=4.5))



def get_book(book_id):
    return db.library.get(book_id)
 


def search_book_by_title(title):
    matching_books = []

    for book in db.library.values():
        book_title = book["title"].lower()
        search_title = title.lower()

        if search_title in book_title:
            matching_books.append(book)

    return matching_books



def import_book(file_path):
    file = open(file_path, "r")
    
    for line in file:
        line = line.strip()
        parts = line.split(",")

        if len(parts) == 8:
            title = parts[0]
            author = parts[1]
            year = parts[2]
            type_book = parts[3]
            global_rating = float(parts[4])
            copies = int(parts[5])
            price = float(parts[6])
            sold = int(parts[7])

            book = {
                "title": title,
                "author": author,
                "year": year,
                "type_book": type_book,
                "global_rating": global_rating,
                "copies": copies,
                "price": price,
                "sold": sold
            }

            db.library[title] = book

    file.close()
    return "Import completed"


def export_book(file_path):
    exported_count = 0
    exported_books = {}  
    file = open(file_path, "w")   

    for book_id, book in db.library.items():  
        title = book["title"]
        author = book["author"]
        year = book["year"]
        type_book = book["type_book"]
        global_rating = book["global_rating"]
        copies = book.get("copies", 0)
        price = book.get("price", 0.0)
        sold = book.get("sold", 0)

        line = (
            title + "," + author + "," + str(year) + "," + type_book + "," +
            str(global_rating) + "," + str(copies) + "," + str(price) + "," + str(sold) + "\n"
        )
        file.write(line)

        exported_books[book_id] = book 
        exported_count += 1     

    file.close()   
    return exported_books, exported_count


def display_all_books():  
    all_books = []
    for book_id, book in db.library.items():
        book['id'] = book_id 
        all_books.append(book)
    return all_books


def borrow_book(book_id, borrower_name, days):
    if book_id not in db.library:
        return None
    book = db.library[book_id]
    if book.get("borrowed") == True:
        return None
    book["borrowed"] = True
    book["borrower_name"] = borrower_name
    book["days"] = days
    book["due_day"] = days 
    return book


def return_book(book_id):
    if book_id not in db.library:
        return None
    
    book = db.library[book_id]

    if book.get("borrowed") != True:
        return None

    book["borrowed"] = False

    if book.get("days", 0) > 7:
        book["overdue"] = True
    else:
        book["overdue"] = False

    book["borrower_name"] = None
    book["days"] = 0

    return book


def book_by_author(author):
    author_books = [] 

    for book in db.library.values():
        if book["author"] == author:
            author_books.append(book)

    return author_books



def book_by_year(year):
    year_books = [] 
    for book in db.library.values():
        if book["year"] == year:
            year_books.append(book)

    return year_books

def library_stats(library):
    # Get the list of books
    library_list = list(db.library.values())  

    if not library_list:
        print("The library is empty.")
        return

    total_books = len(library_list)

    # Initialize with the first book
    oldest_book = library_list[0]
    newest_book = library_list[0]
    
    for book in library_list:
        # --- THE FIX IS HERE ---
        # We try to convert the year. If it fails (bad data), we skip this book.
        try:
            current_year = int(book['year'])
            oldest_year = int(oldest_book['year'])
            newest_year = int(newest_book['year'])
            
            if current_year < oldest_year:
                oldest_book = book
            if current_year > newest_year:
                newest_book = book
        except ValueError:
            # This skips books that have bad years (like "Unknown" or "")
            continue 
        # -----------------------

    type_counts = {}
    for book in library_list:
        # Use .get() here to be safe if a book is missing the type
        book_type = book.get('type_book', 'Unknown')
        
        if book_type in type_counts:
            type_counts[book_type] += 1
        else:
            type_counts[book_type] = 1

    print("total books:", total_books)
    # Use .get() in the print statements to prevent crashes on missing titles/authors
    print("oldest book:", oldest_book.get('title'), "(", oldest_book.get('year'), ") by", oldest_book.get('author'))
    print("newest book:", newest_book.get('title'), "(", newest_book.get('year'), ") by", newest_book.get('author'))
    print("books by type:")
    for i in type_counts:
        print(" ", str(i) + ":", type_counts[i])

def clear_library():
    deleted_books = list(db.library.values()) 
    db.library.clear()  
    return deleted_books

def search_books_by_type(library, wanted_type):
    print("Available book types:")
    print("Fiction | Classic | Fantasy/Sci-Fi | Non-Fiction | Biography/Memoir | Mystery/Thriller | Horror | Self-Help | Poetry/Drama | Romance|Comedy| Action| Horror| Scientific| Family")

    result = {}
    for name in library:
        if library[name]["type_book"] == wanted_type:
            result[name] = library[name]

    return result

purchase_history = {}

# Function 1: Calculate total price
def generate_total(book, quantity):
    """
    Calculates total price for a given book and quantity.
    """
    return book["price"] * quantity


# Function 2: Buy a book
def buy_book(user_id, book_id, quantity, book_dict):
   
    if book_id not in book_dict:
        return "Book not found."

    book = book_dict[book_id]

    if quantity > book["copies"]:
        return f"Only {book['copies']} copies available."

    # Calculate total
    total = generate_total(book, quantity)

    # Update library
    book["copies"] -= quantity
    book["sold"] += quantity

    # Record purchase
    if user_id not in purchase_history:
        purchase_history[user_id] = []

    purchase_history[user_id].append({
        "book_id": book_id,
        "quantity": quantity,
        "total": total
    })

    # Generate receipt
    receipt = f"""
----- RECEIPT -----
User ID: {user_id}
Book: {book['title']}
Quantity: {quantity}
Total: {total} EGP
-------------------
"""
    return receipt


def sort_books_by_title():
    books_list = []

    for book in db.library.values():
        books_list.append(book)

    books_list.sort(key=lambda book: book["title"].lower())
    return books_list

def count_books_by_type():
    counts = {}

    for book in db.library.values():
        t = book["type_book"]
        if t in counts:
            counts[t] += 1
        else:
            counts[t] = 1

    return counts