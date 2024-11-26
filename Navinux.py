import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class Navegador(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Inicialização
        self.browser = QTabWidget()
        self.setCentralWidget(self.browser)
        self.browser.setTabsClosable(True)
        self.browser.tabCloseRequested.connect(self.close_tab)
        
        # Menu
        self.init_ui()
        
    def init_ui(self):
        # Definindo o nome do aplicativo
        self.setWindowTitle("Navinux - Navegador Leve")
        self.setWindowIcon(QIcon('icon.png'))  # Ícone do navegador
        
        # Configuração da barra de menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Arquivo")
        
        # Ação para nova aba
        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)
        
        # Ação para fechar
        close_action = QAction("Fechar", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)
        
        # Criar a barra de ferramentas
        self.toolbar = self.addToolBar("Barra de Navegação")
        
        # Barra de navegação (QLineEdit)
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # Adiciona o QLineEdit à barra de ferramentas
        self.toolbar.addWidget(self.url_bar)
        
        # Criar a primeira aba
        self.new_tab()

    def new_tab(self):
        # Criar um navegador para uma nova aba
        tab = QWidget()
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://www.google.com"))
        browser.urlChanged.connect(self.update_url_bar)
        
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)
        
        index = self.browser.addTab(tab, "Nova Aba")
        self.browser.setCurrentIndex(index)

    def close_tab(self, index):
        if self.browser.count() > 1:
            self.browser.removeTab(index)
        else:
            self.close()

    def navigate_to_url(self):
        # Navegar para a URL digitada
        url = self.url_bar.text()
        current_browser = self.browser.currentWidget().findChild(QWebEngineView)
        current_browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        # Atualizar a barra de URL conforme o navegador navega
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    navegador = Navegador()
    navegador.show()
    sys.exit(app.exec_())
