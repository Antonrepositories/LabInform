import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from Lab1 import DatabaseApp, Database, Table  
from tkinter import messagebox  

class TestDatabaseApp(unittest.TestCase):
    
    def setUp(self):
        """Налаштування тестового середовища перед кожним тестом"""
        root = Tk()  
        self.app = DatabaseApp(root)
        self.app.database = MagicMock(spec=Database)
        schema = {'id': 'integer', 'salary': 'real', 'name': 'string', 'worked': 'date'}
        self.app.database.tables = [Table("Test", schema)]        

    @patch('tkinter.messagebox.showerror')  
    def test_error_if_database_not_loaded(self, mock_showerror):
        """Тест перевірки помилки, якщо база даних не завантажена"""
        self.app.database = None 
        self.app.add_row()  

        mock_showerror.assert_called_once_with("Помилка", "Спочатку створіть або завантажте базу даних")
    
    @patch('tkinter.messagebox.showerror')  
    def test_error_if_empty_field(self, mock_showerror):
        """Тест перевірки помилки видалення при пустому полі"""
        self.app.table_name_entry.delete(0, "end")  
        self.app.delete_table() 

        mock_showerror.assert_called_once_with("Помилка", "Введіть назву таблиці для видалення")
    
    @patch('tkinter.messagebox.showerror') 
    def test_search_pattern(self, mock_showerror):
        """Тест додавання рядку з невірними даними дати"""
        schema = {'id': 'integer', 'salary': 'real', 'name': 'string', 'worked': 'date'}
        table = Table("Test", schema)  
        self.app.table_name_entry.insert(0, "Test")
        #print(f"{len(self.app.database.tables[0].schema)} -------------------------------")
        self.app.database.get_table.return_value = table

        self.app.row_entry.insert(0, "1;5.5;Name;1999-40-40")
        # Викликаємо додавання рядка
        self.app.add_row()
        
        mock_showerror.assert_called_once_with("Помилка", "Невірний формат")

if __name__ == '__main__':
    unittest.main()
