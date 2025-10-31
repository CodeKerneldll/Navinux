# navegador_md.py
import sys, re
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLineEdit, QToolBar, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon

class Navegador(QMainWindow):
    def __init__(self, md_extensions=None):
        super().__init__()
        self.browser = QTabWidget()
        self.setCentralWidget(self.browser)
        self.browser.setTabsClosable(True)
        self.browser.tabCloseRequested.connect(self.close_tab)
        
        self.md_extensions = md_extensions or []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Navinux Lite - Extensível .md")
        self.setWindowIcon(QIcon('icon.png'))

        menubar = self.menuBar()
        file_menu = menubar.addMenu("Arquivo")

        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)

        close_action = QAction("Fechar", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        self.toolbar = self.addToolBar("Barra de Navegação")
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        self.new_tab()

    def new_tab(self):
        tab = QWidget()
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://www.google.com"))
        browser.urlChanged.connect(self.update_url_bar)

        # Executa extensões .md
        for md_file in self.md_extensions:
            self.load_md_extension(md_file, browser)

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
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser = self.browser.currentWidget().findChild(QWebEngineView)
        current_browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def load_md_extension(self, md_file, browser):
        """Lê o .md, extrai blocos de Python e executa como extensão"""
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            code_blocks = re.findall(r"```python(.*?)```", content, re.DOTALL)
            for code in code_blocks:
                exec(code, {"browser": browser})
        except Exception as e:
            print(f"Erro na extensão {md_file}: {e}")

if __name__ == "__main__":
    # exemplo: extensão em markdown
    md_files = ["adblock.md"]
    app = QApplication(sys.argv)
    navegador = Navegador(md_extensions=md_files)
    navegador.show()
    sys.exit(app.exec())
