from datetime import date
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient(port=27017)
db = client["yanivDB"]
books_collection = db["books"]

class Book:
    def __init__(self, author, title, nop):
        self.author = author
        self.title = title
        self.num_of_pages = nop


class Shelf:
    def __init__(self):
        self.books = []  # max 5 books
        self.is_shelf_full = False

    def addBook(self, book):
        if len(self.books) < 5:
            self.books.append(book)
            print("New book has been added")
        else:
            print("No more spcae")
            self.is_shelf_full = True

    def replace_books(self, num1, num2):
        try:
            self.books[num1], self.books[num2 ] = self.books[num2], self.books[num1]
            print("Location changed successfully")
        except IndexError:       
            print("Book location is empty")

    def order_books(self):
        # print(list((self.books[0].num_of_pages, self.books[1].num_of_pages)))

        nopBooks = list(map(lambda book : book.num_of_pages ,self.books))
        print(f"Before sorting {nopBooks}")

        #sorting books list
        booksSortedAsc = sorted(self.books, key=lambda book: book.num_of_pages)
        print(f"After sorting {list(map(lambda book : book.num_of_pages ,booksSortedAsc))}")

class Reader:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.books = []

    def read_book(self, bookTitle):
        today = date.today()
        currentDate = today.strftime("%b-%d-%Y")
        # print(currentDate)
        self.books.append({"title": bookTitle, "date": currentDate})
        print("book has been added to reader")        

class Library:
    def __init__(self, s1, s2, s3):
        self.shelves = [s1, s2, s3] #list of 3 Shelf objects
        self.readers = [] #list of Reader objects
    
    def is_there_place_for_new_book(self):
        self.place_in_library == False
        for shelf in self.shelves:
            if shelf.is_shelf_full == False:
                self.place_in_library == True
                break
        
        return self.place_in_library

    
    #add book object to the first Shelf with a free space
    def add_new_book(self, bookOBJ):
        for shelf in self.shelves:
            if shelf.is_shelf_full == False:
                shelf.addBook(bookOBJ)
                break

    #delete the Book object from the library.
    def delete_book(self, book_title):
        for shelf in self.shelves:
            for book in shelf.books:
                if book.title == book_title:
                    shelf.books.remove(book)
                    print("Book has been deleted")
                    # print(shelf.books[0].title)

    #replace between 2 Books objects (their locations in the shelves).
    def change_locations(self, bookTitle1, bookTitle2):
        flag = True
        for i in range(2):
            if flag == False:
                if (index_book1 and index_book2) is not None:
                    self.change_locations_in_same_shelf(index_shelf, index_book1, index_book2)
                else:
                    print("Please replace books title in the same shelf")
                return
            for book in self.shelves[i].books:
                if book.title == bookTitle1:
                    index_book1 = self.shelves[i].books.index(book)
                    index_shelf = i
                    flag = False
                if book.title == bookTitle2:
                    index_book2 = self.shelves[i].books.index(book)
                    index_shelf = i
                    flag = False

        # placeBook1 = self.shelves[index_shelf].books[index_book1]
        # placeBook2 = self.shelves[index_shelf].books[index_book2]   
        # placeBook1, placeBook2 = placeBook2, placeBook1
        # print("Location changed successfully")        


    #receives a shelf number, and books locations and replace between these 2 Books objects.
    def change_locations_in_same_shelf(self, shelfNumber, bookLocation1, bookLocation2):
        self.shelves[shelfNumber].replace_books(bookLocation1, bookLocation2)
        
    #order all books in each shelf by their num_of_pages
    def order_books(self):
        for shelf in self.shelves:
            shelf.order_books()

    #receives a new reader name and id and add it to the readers list.
    def register_reader(self, reader_id, reader_name):
        reader = Reader(reader_id, reader_name)
        self.readers.append(reader)
        print(f"Your reader id: {reader_id} has been added")

    #receives a reader name and removes it from the readers list.
    def remove_reader(self, reader_name):
        for reader in self.readers:
            if reader.name == reader_name:
                self.readers.remove(reader)
                print(f"Reader {reader_name} has been removed")

    #receives a book title and a reader name and add this book title to the reader’s books list
    def reader_read_book(self, book_title, reader_name):
        for reader in self.readers:
            if reader.name == reader_name:
                reader.read_book(book_title)
        
    #receives an author name and returns all books titles this author wrote
    def search_by_author(self, author_name):
        author_books = []
        for shelf in self.shelves:
            book_by_author = list(filter(lambda book: book.author == author_name ,shelf.books))
            if len(book_by_author) > 0:
                author_books = [*book_by_author]
            else:
                return False
        # print(author_books)
        books_titles_by_author = list(map(lambda book: book.title, author_books))
        return books_titles_by_author





