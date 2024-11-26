import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class BrowserTab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.google.com"))
        self.urlChanged.connect(self.update_url)

    def update_url(self, q):
        self.browser_window.update_url(q)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializa a janela principal
        self.setWindowTitle("Navenux Versão Beta By Codekernel")

        # Criação do central widget para o navegador
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Ações da barra de navegação
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Botão de voltar
        back_btn = QAction("Voltar", self)
        back_btn.triggered.connect(self.back)
        navbar.addAction(back_btn)

        # Botão de avançar
        forward_btn = QAction("Avançar", self)
        forward_btn.triggered.connect(self.forward)
        navbar.addAction(forward_btn)

        # Botão de recarregar
        reload_btn = QAction("Recarregar", self)
        reload_btn.triggered.connect(self.reload)
        navbar.addAction(reload_btn)

        # Barra de endereço
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Criar uma aba inicial
        self.add_new_tab()

        # Ativar histórico de navegação
        self.history = []

        # Atualizar a barra de endereços quando mudar de URL
        self.current_tab().urlChanged.connect(self.update_url)

    def current_tab(self):
        # Certifique-se de que uma aba está aberta
        return self.tabs.currentWidget() if self.tabs.count() > 0 else None

    def add_new_tab(self):
        new_tab = BrowserTab()
        new_tab.browser_window = self  # Conectar a janela principal à aba
        self.tabs.addTab(new_tab, "Nova Aba")
        self.tabs.setCurrentWidget(new_tab)

    def back(self):
        tab = self.current_tab()
        if tab:
            tab.back()

    def forward(self):
        tab = self.current_tab()
        if tab:
            tab.forward()

    def reload(self):
        tab = self.current_tab()
        if tab:
            tab.reload()

    def navigate_to_url(self):
        url = self.url_bar.text()
        tab = self.current_tab()
        if tab:
            tab.setUrl(QUrl(url))
            self.history.append(url)  # Adicionar ao histórico

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def closeEvent(self, event):
        self.save_cookies()

    def save_cookies(self):
        # Exemplo de salvamento e leitura de cookies
        cookie_jar = self.current_tab().profile().cookieStore()
        cookie_jar.cookiesChanged.connect(self.on_cookies_changed)

    def on_cookies_changed(self, cookies):
        print(f"Cookies atualizados: {cookies}")

if __name__ == '__main__':
    # Configurar antes de criar o QApplication
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    window = BrowserWindow()
    window.show()

    sys.exit(app.exec_())
