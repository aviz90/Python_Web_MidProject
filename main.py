from Classes import *
import json
import os
import sys



mongo_books = books_collection.find({},{'_id':0})
count = books_collection.count_documents({})

booksOBJ = []
for i in range(count):
    booksOBJ.append(Book(mongo_books[i]["author"], mongo_books[i]["title"], mongo_books[i]["num_of_pages"]))

shelf1 = Shelf()
shelf2 = Shelf()
shelf3 = Shelf()
shelf1.books.append(booksOBJ[0])
shelf1.books.append(booksOBJ[1])
shelf2.books.append(booksOBJ[2])
shelf2.books.append(booksOBJ[3])
shelf3.books.append(booksOBJ[4])
shelf3.books.append(booksOBJ[5])
library = Library(shelf1, shelf2, shelf3)
rder_books()

id = 0
choice = ""
def save_library(file_name):
    file_name = file_name
    with open(os.path.join(sys.path[0], file_name + ".json"), "w") as f:
            
        shelves = []
        for shelf in library.shelves:
            books = []
            shelfObj = {}
            shelfObj["is_shelf_full"] = shelf.is_shelf_full
            for book in shelf.books:
                bookObj = {}               
                bookObj["author"] = book.author
                bookObj["title"] = book.title
                bookObj["num_of_pages"] = book.num_of_pages
                books.append(bookObj)
            
            shelfObj["books"] = books
            shelves.append(shelfObj)

        readers = []
        for r in library.readers:
            books = []
            readerObj = {}
            readerObj["id"] = r.id
            for book in r.books:
                bookObj = {}               
                bookObj["title"] = book["title"]
                bookObj["date"] = book["date"]
                books.append(bookObj)
            
            readerObj["books"] = books
            readers.append(readerObj)

        obj = {"shelves": shelves, "readers": readers}
        json.dump(obj,f)

while(choice != '11'):
    choice = input("For adding a book - Press 1.\n"
    "For deleting a book - Press 2.\n"
    "For changing books locations - Press 3.\n"
    "For registering a new reader - Press 4.\n"
    "For removing a reader - Press 5.\n"
    "For searching books by author – Press 6: \n"
    "For reading a book by a reader – Press 7.\n"
    "For ordering all books – Press 8.\n"
    "For saving all data – Press 9.\n"
    "For loading data – Press 10.\n"
    "For exit – Press 11.\n")
    
    if choice == "1":
        author = input("Insert author of book: ")
        title = input("Insert title of book: ")
        num_of_pages = input("Insert number of pages in book: ")
        book = Book(author, title, num_of_pages)
        library.add_new_book(book)
        input("Back to Menu...")
    elif choice == "2":
        book_title = input("Type the title of book to be delete: ")
        library.delete_book(book_title)
        input("Back to Menu...")
    elif choice == "3":
        title1 = input("Type the title of first book to be replaced: ")
        title2 = input("Type the title of second book to be replaced: ")
        library.change_locations(title1, title2)
        input("Back to Menu...")
    elif choice == "4":
        id += 1
        reader_name = input("What is your name?: ")
        library.register_reader(id, reader_name)
        input("Back to Menu...")
    elif choice == "5":
        reader_name = input("Type reader name to be removed: ")
        library.remove_reader(reader_name)
        input("Back to Menu...")
    elif choice == "6":
        authour_name = input("Type the author name to search by: ")
        books_titles_by_author = library.search_by_author(authour_name)
        if books_titles_by_author:
            print(books_titles_by_author)
            for title in books_titles_by_author:
                print(f'\"{title}\"')
        else:
            print("Author not found")
        input("Back to Menu...")
    elif choice == "7":
        reader_id = input("Type the reader id: ")
        try:
            reader_name = list(filter(lambda reader: str(reader.id) == reader_id ,library.readers))[0].name
        except IndexError:
            print("Reader id not found.")
        # reader_name = input("Type the reader name")
        book_title = input("Type the title of book to read: ")
        library.reader_read_book(book_title, reader_name)
        input("Back to Menu...")
    elif choice == "8":
        library.order_books()
        input("Back to Menu...")
    elif choice == "9":
        file_name = input("Type a file name to save the library data: ")
        save_library(file_name)
        print(f"Library saved in {file_name}")
    elif choice == "10":
        file_name = input("Type a file name to load a library data: ")
        with open(os.path.join(sys.path[0], file_name + ".json"),'r') as f:
            data = json.load(f)
            library.shelves = data["shelves"]
            library.readers = data["readers"]
