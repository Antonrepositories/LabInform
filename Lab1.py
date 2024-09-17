import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

class Table:
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema  # Схема таблиці: {назва_поля: тип}
        self.rows = []

    def add_row(self, row_data):
        if len(row_data) != len(self.schema):
            raise ValueError("Кількість значень не відповідає кількості полів")
        self.rows.append(row_data)

    def get_rows(self):
        return self.rows

    def search_rows(self, field_name, pattern):
        # Пошук по полю
        field_index = list(self.schema.keys()).index(field_name)
        matched_rows = []
        for row in self.rows:
            if pattern in str(row[field_index]):
                matched_rows.append(row)
        return matched_rows

class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def create_table(self, table_name, schema):
        if table_name in self.tables:
            raise ValueError(f"Таблиця '{table_name}' вже існує")
        self.tables[table_name] = Table(table_name, schema)

    def get_table(self, table_name):
        if table_name not in self.tables:
            raise ValueError(f"Таблиця '{table_name}' не знайдена")
        return self.tables[table_name]

    def save_to_file(self, filename):
        data = {
            "name": self.name,
            "tables": {}
        }
        for table_name, table in self.tables.items():
            table_data = {
                "schema": table.schema,
                "rows": table.rows
            }
            data["tables"][table_name] = table_data

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        database = Database(data['name'])
        for table_name, table_data in data['tables'].items():
            table = Table(table_name, table_data['schema'])
            table.rows = table_data['rows']
            database.tables[table_name] = table
        
        return database

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система Управління Табличною Базою Даних")
        
        self.database = None
        self.schema_fields = []

        # Головний фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Поле для вводу назви бази даних
        ttk.Label(main_frame, text="Назва бази даних:").grid(row=0, column=0, sticky=tk.W)
        self.db_name_entry = ttk.Entry(main_frame)
        self.db_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Кнопка створення бази даних
        self.create_db_button = ttk.Button(main_frame, text="Створити базу", command=self.create_database)
        self.create_db_button.grid(row=0, column=2, sticky=tk.W)

        # Кнопка завантаження бази даних
        self.load_db_button = ttk.Button(main_frame, text="Завантажити базу", command=self.load_database)
        self.load_db_button.grid(row=0, column=3, sticky=tk.W)
        
        # Поле для вибору таблиці
        ttk.Label(main_frame, text="Таблиця:").grid(row=1, column=0, sticky=tk.W)
        self.table_name_entry = ttk.Entry(main_frame)
        self.table_name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Поле для введення кількості полів
        ttk.Label(main_frame, text="Кількість полів:").grid(row=2, column=0, sticky=tk.W)
        self.num_fields_entry = ttk.Entry(main_frame)
        self.num_fields_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Кнопка для додавання полів
        self.add_fields_button = ttk.Button(main_frame, text="Додати поля", command=self.add_fields)
        self.add_fields_button.grid(row=2, column=2, sticky=tk.W)

        # Фрейм для динамічного додавання полів
        self.fields_frame = ttk.Frame(main_frame)
        self.fields_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Поле для введення рядка
        ttk.Label(main_frame, text="Рядок (через ;):").grid(row=4, column=0, sticky=tk.W)
        self.row_entry = ttk.Entry(main_frame)
        self.row_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))
        
        # Кнопка додавання рядка
        self.add_row_button = ttk.Button(main_frame, text="Додати рядок", command=self.add_row)
        self.add_row_button.grid(row=4, column=2, sticky=tk.W)
        
        # Поле для перегляду рядків таблиці
        self.table_view = tk.Text(main_frame, height=10, width=50)
        self.table_view.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Поле для пошуку за шаблоном
        ttk.Label(main_frame, text="Поле пошуку:").grid(row=6, column=0, sticky=tk.W)
        self.search_field_entry = ttk.Entry(main_frame)
        self.search_field_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="Шаблон:").grid(row=7, column=0, sticky=tk.W)
        self.search_pattern_entry = ttk.Entry(main_frame)
        self.search_pattern_entry.grid(row=7, column=1, sticky=(tk.W, tk.E))

        # Кнопка пошуку
        self.search_button = ttk.Button(main_frame, text="Шукати", command=self.search)
        self.search_button.grid(row=7, column=2, sticky=tk.W)

        # Кнопка для відображення рядків
        self.show_rows_button = ttk.Button(main_frame, text="Показати рядки", command=self.show_rows)
        self.show_rows_button.grid(row=8, column=0, columnspan=3)

        # Кнопка збереження бази
        self.save_button = ttk.Button(main_frame, text="Зберегти базу", command=self.save_database)
        self.save_button.grid(row=9, column=0, columnspan=3)

    def create_database(self):
        db_name = self.db_name_entry.get()
        if not db_name:
            messagebox.showerror("Помилка", "Введіть назву бази даних")
            return
        self.database = Database(db_name)
        messagebox.showinfo("Успіх", f"База даних '{db_name}' створена")

    def load_database(self):
        db_name = self.db_name_entry.get()
        if not db_name:
            messagebox.showerror("Помилка", "Введіть назву бази для завантаження")
            return
        filename = f"{db_name}.json"
        try:
            self.database = Database.load_from_file(filename)
            messagebox.showinfo("Успіх", f"База даних '{db_name}' завантажена")
        except FileNotFoundError:
            messagebox.showerror("Помилка", f"Файл '{filename}' не знайдено")

    def add_fields(self):
        try:
            num_fields = int(self.num_fields_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Введіть правильну кількість полів")
            return
        
        # Очищуємо попередні поля
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        self.schema_fields = []
        for i in range(num_fields):
            field_frame = ttk.Frame(self.fields_frame)
            field_frame.grid(row=i, column=0, sticky=(tk.W, tk.E))

            ttk.Label(field_frame, text=f"Поле {i+1} Назва:").grid(row=0, column=0, sticky=tk.W)
            field_name_entry = ttk.Entry(field_frame)
            field_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

            ttk.Label(field_frame, text=f"Тип:").grid(row=0, column=2, sticky=tk.W)
            field_type_entry = ttk.Combobox(field_frame, values=["integer", "real", "char", "string", "date", "dateInvl"])
            field_type_entry.grid(row=0, column=3, sticky=(tk.W, tk.E))

            self.schema_fields.append((field_name_entry, field_type_entry))

        # Кнопка створення таблиці
        self.create_table_button = ttk.Button(self.fields_frame, text="Створити таблицю", command=self.create_table)
        self.create_table_button.grid(row=num_fields, column=0, columnspan=4)

    def create_table(self):
        if not self.database:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        
        table_name = self.table_name_entry.get()
        if not table_name:
            messagebox.showerror("Помилка", "Введіть назву таблиці")
            return
        
        schema = {}
        for field_name_entry, field_type_entry in self.schema_fields:
            field_name = field_name_entry.get()
            field_type = field_type_entry.get()
            if not field_name or not field_type:
                messagebox.showerror("Помилка", "Усі поля повинні бути заповнені")
                return
            schema[field_name] = field_type

        try:
            self.database.create_table(table_name, schema)
            messagebox.showinfo("Успіх", f"Таблиця '{table_name}' створена")
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def add_row(self):
        if not self.database:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        
        table_name = self.table_name_entry.get()
        if not table_name:
            messagebox.showerror("Помилка", "Введіть назву таблиці")
            return

        row_data = self.row_entry.get().split(';')
        table = self.database.get_table(table_name)

        # Перевірка кількості введених значень
        if len(row_data) != len(table.schema):
            messagebox.showerror("Помилка", "Кількість значень не відповідає кількості полів")
            return
        
        # Приведення типів
        for i, (key, field_type) in enumerate(table.schema.items()):
            if field_type == "integer":
                row_data[i] = int(row_data[i])
            elif field_type == "real":
                row_data[i] = float(row_data[i])
            elif field_type == "date":
                row_data[i] = datetime.strptime(row_data[i], "%Y-%m-%d").date()
            elif field_type == "dateInvl":
                start_date, end_date = row_data[i].split(' - ')
                row_data[i] = (datetime.strptime(start_date, "%Y-%m-%d").date(),
                               datetime.strptime(end_date, "%Y-%m-%d").date())
                print(row_data[i])
            # Інші типи залишаються як string або char

        try:
            table.add_row(row_data)
            messagebox.showinfo("Успіх", "Рядок додано")
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def show_rows(self):
        if not self.database:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        table_name = self.table_name_entry.get()
        if not table_name:
            messagebox.showerror("Помилка", "Введіть назву таблиці")
            return
        
        table = self.database.get_table(table_name)
        rows = table.get_rows()
        self.table_view.delete(1.0, tk.END)
        for row in rows:
            self.table_view.insert(tk.END, f"{row}\n")

    def search(self):
        if not self.database:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        table_name = self.table_name_entry.get()
        field_name = self.search_field_entry.get()
        pattern = self.search_pattern_entry.get()
        if not table_name or not field_name or not pattern:
            messagebox.showerror("Помилка", "Заповніть усі поля для пошуку")
            return

        table = self.database.get_table(table_name)
        matched_rows = table.search_rows(field_name, pattern)
        self.table_view.delete(1.0, tk.END)
        for row in matched_rows:
            self.table_view.insert(tk.END, f"{row}\n")

    def save_database(self):
        if not self.database:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        filename = f"{self.database.name}.json"
        self.database.save_to_file(filename)
        messagebox.showinfo("Успіх", f"База даних збережена у файл '{filename}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
