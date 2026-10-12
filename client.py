import json
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "http://localhost:8000/api"


def get(path: str, params: dict | None = None) -> dict | None:
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8"))
        print(f"Помилка {e.code}: {body.get('error')}")
    except urllib.error.URLError:
        print("Не вдалося підключитися. Чи запущено PHP-сервер?")
    return None


def print_books(books: list[dict]) -> None:
    if not books:
        print("Нічого не знайдено.")
        return
    print(f"\n{'ID':<4}{'Назва':<26}{'Автор':<26}{'Жанр':<18}{'Рік'}")
    print("-" * 80)
    for b in books:
        print(f"{b['id']:<4}{b['title']:<26}{b['author']:<26}{b['genre']:<18}{b['year']}")


def main() -> None:
    menu = (
        "\n=== Бібліотека книг ===\n"
        "1. Усі книги\n"
        "2. Фільтр за жанром\n"
        "3. Пошук (назва/автор)\n"
        "4. Книга за ID\n"
        "5. Список жанрів\n"
        "0. Вихід\n"
    )
    while True:
        print(menu)
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            data = get("/books")
            if data:
                print_books(data["data"])
        elif choice == "2":
            genre = input("Жанр: ").strip()
            data = get("/books", {"genre": genre})
            if data:
                print_books(data["data"])
        elif choice == "3":
            q = input("Пошуковий запит: ").strip()
            data = get("/books", {"q": q})
            if data:
                print_books(data["data"])
        elif choice == "4":
            book_id = input("ID: ").strip()
            data = get(f"/books/{urllib.parse.quote(book_id)}")
            if data:
                print_books([data["data"]])
        elif choice == "5":
            data = get("/genres")
            if data:
                print("Жанри:", ", ".join(data["data"]))
        elif choice == "0":
            print("До побачення!")
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()