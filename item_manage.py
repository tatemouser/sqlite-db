import sqlite3

class Item:
    def __init__(self, item_id, title, item_type, availability):
        self.item_id = item_id
        self.title = title
        self.item_type = item_type
        self.availability = availability

    def to_json(self):
        item_json = {
            "item_id": self.item_id,
            "title": self.title,
            "item_type": self.item_type,
            "availability": self.availability
        }
        return item_json

def add_item(title, item_type, availability):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO items (title, type, availability) VALUES (?, ?, ?)",
                   (title, item_type, availability))
    conn.commit()
    conn.close()

def search_items(title):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE title LIKE ?", ('%' + title + '%',))
    items = cursor.fetchall()

    conn.close()
    return items
