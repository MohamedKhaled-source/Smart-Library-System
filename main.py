import library_functions as lib
import library_data as db
import sys

# Ensure database has a current_id
if not hasattr(db, 'current_id'):
    if db.library:
        db.current_id = max(db.library.keys()) + 1
    else:
        db.current_id = 1

def print_menu():
    print("\n" + "="*30)
    print("   ZEWAIL CITY LIBRARY SYSTEM   ")
    print("="*30)
    print("1. Display all books")
    print("2. Search book by Title")
    print("3. Search books by Type")
    print("4. Add a new book")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. Show Library Statistics")
    print("8. Export/Save Data")
    print("9. BUY A BOOK (New!)")
    print("10. Show Books Sorted by Title (New!)")
    print("0. Exit")
    print("="*30)

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            books = lib.display_all_books()
            print(f"Displaying {min(len(books), 20)} of {len(books)} books:") 
            for book in books[:20]: 
                print(f"ID: {book.get('id')} | {book.get('title')} | Price: {book.get('price')} EGP")
        
        elif choice == '2':
            title = input("Enter title: ")
            results = lib.search_book_by_title(title)
            for book in results:
                print(f"FOUND: {book['title']} (ID: {book.get('id')})")

        elif choice == '3':
            b_type = input("Enter type: ")
            results = lib.search_books_by_type(b_type)
            for b_id, book in results.items():
                 print(f"{book['title']} -- {book['author']}")

        elif choice == '4':
            print("--- Add New Book ---")
            try:
                title = input("Title: ")
                author = input("Author: ")
                year = int(input("Year: "))
                type_book = input("Type: ")
                copies = int(input("Copies: "))
                price = float(input("Price: "))
                sold = 0
                new_id = lib.add_book(title, author, year, type_book, copies, price, sold)
                print(f"Success! Book added with ID: {new_id}")
            except ValueError:
                print("Error: Invalid number input.")

        elif choice == '5':
            try:
                book_id = int(input("Enter Book ID: "))
                name = input("Borrower Name: ")
                days = int(input("Days: "))
                if lib.borrow_book(book_id, name, days):
                    print("Book borrowed.")
                else:
                    print("Error borrowing book.")
            except ValueError:
                print("Invalid input.")

        elif choice == '6':
            try:
                book_id = int(input("Enter Book ID: "))
                res = lib.return_book(book_id)
                if res:
                    print(f"Returned: {res['title']}")
                else:
                    print("Error returning book.")
            except ValueError:
                print("Invalid input.")

        elif choice == '7':
            lib.library_stats(db.library)

        elif choice == '8':
            filename = input("Filename to save: ")
            if not filename: filename = "data.csv"
            lib.export_book(filename)
            print("Saved.")

        elif choice == '9': # BUY BOOK
            try:
                user_id = input("Enter your User Name/ID: ")
                book_id = int(input("Enter Book ID to buy: "))
                quantity = int(input("How many copies? "))
                
                receipt = lib.buy_book(user_id, book_id, quantity,db.library)
                print(receipt)
            except ValueError:
                print("Error: ID and Quantity must be numbers.")


        elif choice == '10': 
                    sorted_books = lib.sort_books_by_title()
                    total_books = len(sorted_books)
                    batch_size = 50
                    start_index = 0
                    
                    while start_index < total_books:
                        # 1. "Clear" the screen so the user only sees the new batch
                        # (Printing 50 empty lines pushes the old text up out of view)
                        print("\n" * 50) 
                        
                        end_index = min(start_index + batch_size, total_books)
                        print(f"--- Books Sorted by Title (Showing {start_index + 1} to {end_index} of {total_books}) ---")
                        
                        # 2. Get the specific slice of 50 books
                        current_batch = sorted_books[start_index : end_index]
                        
                        for book in current_batch:
                            # Safe .get() to avoid crashing
                            print(f"{book.get('title')} ({book.get('year')})")
                        
                        # 3. Check if we reached the end
                        if end_index >= total_books:
                            print("\n--- End of List ---")
                            break

                        # 4. Ask to continue
                        user_response = input("\nPress Enter to view the next 50 (or type 'q' to stop): ")
                        if user_response.lower() == 'q':
                            break
                        
                        # 5. Move the start index forward
                        start_index += batch_size
                
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()