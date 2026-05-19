import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
import sqlite3

class ShoeShopApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.init_ui()
        
    def init_db(self):
        self.conn = sqlite3.connect('shoes.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS products
                         (id INTEGER PRIMARY KEY, 
                         name TEXT, 
                         price REAL, 
                         size INTEGER)''')
        self.c.execute("INSERT OR IGNORE INTO products VALUES (1, 'Кроссовки Nike', 5000, 42)")
        self.c.execute("INSERT OR IGNORE INTO products VALUES (2, 'Ботинки Adidas', 6000, 40)")
        self.conn.commit()

    def init_ui(self):
        self.setWindowTitle('Магазин обуви')
        self.setGeometry(100, 100, 800, 600)
        
        # Основной контейнер
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        
        # Панель навигации
        self.navbar = QtWidgets.QTabWidget()
        self.navbar.addTab(self.create_home_tab(), "Главная")
        self.navbar.addTab(self.create_catalog_tab(), "Каталог")
        self.navbar.addTab(self.create_cart_tab(), "Корзина")
        self.layout.addWidget(self.navbar)
        
        self.load_products()
        self.show()
        
    def create_home_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Добро пожаловать в магазин обуви!")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        tab.setLayout(layout)
        return tab
        
    def create_catalog_tab(self):
        self.catalog_tab = QtWidgets.QWidget()
        self.catalog_layout = QtWidgets.QGridLayout()
        
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QGridLayout(self.scroll_content)
        
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.catalog_layout.addWidget(self.scroll_area)
        self.catalog_tab.setLayout(self.catalog_layout)
        return self.catalog_tab
    
    def create_cart_tab(self):
        self.cart_tab = QtWidgets.QWidget()
        self.cart_layout = QtWidgets.QVBoxLayout()
        
        self.cart_list = QtWidgets.QListWidget()
        self.total_label = QtWidgets.QLabel("Итого: 0 Р.")
        self.clear_btn = QtWidgets.QPushButton("Очистить корзину")
        self.clear_btn.clicked.connect(self.clear_cart)
        
        self.cart_layout.addWidget(self.cart_list)
        self.cart_layout.addWidget(self.total_label)
        self.cart_layout.addWidget(self.clear_btn)
        self.cart_tab.setLayout(self.cart_layout)
        return self.cart_tab
    
    def load_products(self):
        self.c.execute("SELECT * FROM products")
        products = self.c.fetchall()
        
        for i, (id, name, price, size) in enumerate(products):
            product_frame = QtWidgets.QGroupBox(name)
            layout = QtWidgets.QVBoxLayout()
            
            label = QtWidgets.QLabel(f"""
                Цена: {price} Р.
                Размер: {size}
            """)
            
            buy_btn = QtWidgets.QPushButton("Купить")
            buy_btn.clicked.connect(lambda _, p=price, n=name: self.add_to_cart(p, n))
            
            layout.addWidget(label)
            layout.addWidget(buy_btn)
            product_frame.setLayout(layout)
            
            self.scroll_layout.addWidget(product_frame, i//2, i%2)
    
    def add_to_cart(self, price, name):
        item = QtWidgets.QListWidgetItem(f"{name} - {price} Р.")
        self.cart_list.addItem(item)
        total = float(self.total_label.text().split(": ")[1].replace(" Р.", "")) + price
        self.total_label.setText(f"Итого: {total} Р.")
    
    def clear_cart(self):
        self.cart_list.clear()
        self.total_label.setText("Итого: 0 Р.")
    
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ShoeShopApp()
    sys.exit(app.exec_())