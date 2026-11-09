import argparse
import json
import requests

BASE_URL = "http://localhost:8000"

def print_response(response):
    try:
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(f"Status Code: {response.status_code}")
        print(response.txt)

authentication = ("admin", "password")

def get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    print_response(response)

def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    print_response(response)


def create_book(title, author_name, author_email, year, genre, rating):
    book = {
        "id": len(requests.get(f"{BASE_URL}/books").json()) + 1,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre,
        "rating": rating
    }
    response = requests.post(f"{BASE_URL}/books/", json=book, auth=authentication)
    print_response(response)


def update_book(book_id, title, author_name, author_email, year, genre, rating):
    book = {
        "id": book_id,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre,
        "rating": rating
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=book, auth=authentication)
    print_response(response)
    print_response(response)


def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}", auth=authentication)
    print_response(response)

def search_genre(genre):
    response = requests.get(f"{BASE_URL}/books/search-genre/{genre}")
    print_response(response)

def count():
    response = requests.get(f"{BASE_URL}/books/count")
    print_response(response)



def main():
    parser = argparse.ArgumentParser(description="Book API Client")
    subparses = parser.add_subparsers(dest="command", help="API command")

    #List all books!
    subparses.add_parser("list", help="List all books")

    #Get a book!
    get_parser = subparses.add_parser("get", help="Get a book by ID")
    get_parser.add_argument("id", type=int, help="Book ID")

    #Create a book
    create_parser = subparses.add_parser("create", help="Create a new book")
    create_parser.add_argument("title", type=str, help="Book title")
    create_parser.add_argument("author_name", type=str, help="Author name")
    create_parser.add_argument("--author_email", type=str, default=None, help="Author email")
    create_parser.add_argument("year", type=int, help="Publication year")
    create_parser.add_argument("genre", type=str, help="Book genre")
    create_parser.add_argument("rating", type=float, help="Book rating")

    # Updated a book
    update_parser = subparses.add_parser("update", help="Update a book")
    update_parser.add_argument("id", type=int, help="Book ID")
    update_parser.add_argument("title", type=str, help="Book title")
    update_parser.add_argument("author_name", type=str, help="Author name")
    update_parser.add_argument("--author_email", type=str, default=None, help="Author email")
    update_parser.add_argument("year", type=int, help="Publication year")
    update_parser.add_argument("genre", type=str, help="Book genre")
    update_parser.add_argument("rating", type=float, help="Book rating")

    # Delete a book
    delete_parser = subparses.add_parser("delete", help="Delete a book")
    delete_parser.add_argument("id", type=int, help="Book ID")

    # Get a book by genre
    search_genre_parser = subparses.add_parser("search-genre", help="Get a book genre")
    search_genre_parser.add_argument("genre", type=str, help="Book Genre")

    #Count books
    count_parser = subparses.add_parser("count", help="Get book count")

    args = parser.parse_args()

    if args.command == "list":
        get_all_books()
    elif args.command == "get":
        get_book(args.id)
    elif args.command == "create":
        create_book(args.title, args.author_name, args.author_email, args.year, args.genre, args.rating)
    elif args.command == "update":
        update_book(args.id, args.title, args.author_name, args.author_email, args.year, args.genre, args.rating)
    elif args.command == "delete":
        delete_book(args.id)
    elif args.command == "search-genre":
        search_genre(args.genre)
    elif args.command == "count":
        count()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

