import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QToolBar, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon

class Navegador(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialização da interface
        self.browser = QTabWidget()
        self.setCentralWidget(self.browser)
        self.browser.setTabsClosable(True)
        self.browser.tabCloseRequested.connect(self.close_tab)

        self.init_ui()

    def init_ui(self):
        """Configura a interface do usuário."""
        # Definindo o nome do aplicativo e o ícone
        self.setWindowTitle("Navinux Lite - Navegador Muito Leve")
        self.setWindowIcon(QIcon('icon.png'))  # Ícone do navegador

        # Configuração da barra de menu
        menubar = self.menuBar()

        # Menu de Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        # Ação para nova aba
        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)
        
        # Ação para fechar
        close_action = QAction("Fechar", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        # Barra de navegação
        self.toolbar = self.addToolBar("Barra de Navegação")
        
        # Barra de URL (QLineEdit)
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)  # Navegar ao pressionar Enter
        
        # Adiciona a barra de URL à barra de ferramentas
        self.toolbar.addWidget(self.url_bar)

        # Criar a primeira aba
        self.new_tab()

    def new_tab(self):
        """Função para abrir uma nova aba."""
        tab = QWidget()
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://www.google.com"))  # Página inicial

        # Conecta a mudança de URL para atualizar a barra
        browser.urlChanged.connect(self.update_url_bar)

        # Adiciona o navegador à aba
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)

        # Adiciona a nova aba
        index = self.browser.addTab(tab, "Nova Aba")
        self.browser.setCurrentIndex(index)

    def close_tab(self, index):
        """Função para fechar uma aba."""
        if self.browser.count() > 1:
            self.browser.removeTab(index)
        else:
            self.close()

    def navigate_to_url(self):
        """Navegar para a URL digitada na barra de URL."""
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser = self.browser.currentWidget().findChild(QWebEngineView)
        current_browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        """Atualizar a barra de URL conforme o navegador navega."""
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    navegador = Navegador()
    navegador.show()
    sys.exit(app.exec())
