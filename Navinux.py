import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtGui import QIcon
import os

class Navegador(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicialização
        self.browser = QTabWidget()
        self.setCentralWidget(self.browser)
        self.browser.setTabsClosable(True)
        self.browser.tabCloseRequested.connect(self.close_tab)

        self.history = []  # Para armazenar URLs visitadas
        self.favorites = []  # Para armazenar os favoritos
        self.init_ui()

    def init_ui(self):
        # Definindo o nome do aplicativo
        self.setWindowTitle("Navinux - Navegador Leve")
        self.setWindowIcon(QIcon('icon.png'))  # Ícone do navegador

        # Configuração da barra de menu
        menubar = self.menuBar()

        # Menu de Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        # Ação para nova aba
        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_tab_action)
        
        # Ação para nova janela
        new_window_action = QAction("Nova Janela", self)
        new_window_action.triggered.connect(self.new_window)
        file_menu.addAction(new_window_action)

        # Ação para fechar
        close_action = QAction("Fechar", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        # Menu de Histórico
        history_menu = menubar.addMenu("Histórico")
        
        # Ação para mostrar o histórico
        show_history_action = QAction("Mostrar Histórico", self)
        show_history_action.triggered.connect(self.show_history)
        history_menu.addAction(show_history_action)

        # Ação para limpar o histórico
        clear_history_action = QAction("Limpar Histórico", self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)

        # Menu de Favoritos
        favorites_menu = menubar.addMenu("Favoritos")
        
        # Ação para adicionar aos favoritos
        add_favorites_action = QAction("Adicionar aos Favoritos", self)
        add_favorites_action.triggered.connect(self.add_to_favorites)
        favorites_menu.addAction(add_favorites_action)

        # Ação para mostrar favoritos
        show_favorites_action = QAction("Mostrar Favoritos", self)
        show_favorites_action.triggered.connect(self.show_favorites)
        favorites_menu.addAction(show_favorites_action)

        # Menu de Configurações
        settings_menu = menubar.addMenu("Configurações")
        
        # Ação para habilitar/desabilitar JavaScript
        self.javascript_enabled_action = QAction("Habilitar JavaScript", self, checkable=True)
        self.javascript_enabled_action.setChecked(True)
        self.javascript_enabled_action.triggered.connect(self.toggle_javascript)
        settings_menu.addAction(self.javascript_enabled_action)

        # Ação para alterar o tema (claro/escuro)
        self.toggle_theme_action = QAction("Alternar Tema (Claro/Escuro)", self, checkable=True)
        self.toggle_theme_action.setChecked(False)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(self.toggle_theme_action)

        # Ação para navegar anonimamente
        self.incognito_action = QAction("Nova Aba Anônima", self)
        self.incognito_action.triggered.connect(self.new_incognito_tab)
        settings_menu.addAction(self.incognito_action)

        # Barra de ferramentas de navegação
        self.toolbar = self.addToolBar("Barra de Navegação")
        
        # Barra de navegação (QLineEdit)
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # Adiciona o QLineEdit à barra de ferramentas
        self.toolbar.addWidget(self.url_bar)
        
        # Criar a primeira aba
        self.new_tab()

    def new_tab(self):
        tab = QWidget()
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://www.google.com"))
        browser.urlChanged.connect(self.update_url_bar)

        # Adicionar navegador ao histórico
        browser.urlChanged.connect(self.add_to_history)

        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)
        
        index = self.browser.addTab(tab, "Nova Aba")
        self.browser.setCurrentIndex(index)

    def new_window(self):
        new_window = Navegador()
        new_window.show()

    def new_incognito_tab(self):
        tab = QWidget()
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://www.google.com"))
        browser.urlChanged.connect(self.update_url_bar)

        settings = browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
        
        layout = QVBoxLayout()
        layout.addWidget(browser)
        tab.setLayout(layout)
        
        index = self.browser.addTab(tab, "Aba Anônima")
        self.browser.setCurrentIndex(index)

    def close_tab(self, index):
        if self.browser.count() > 1:
            self.browser.removeTab(index)
        else:
            self.close()

    def navigate_to_url(self):
        url = self.url_bar.text()
        current_browser = self.browser.currentWidget().findChild(QWebEngineView)
        current_browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())  # PyQt6 mantém o QUrl.toString()

    def add_to_history(self, q):
        url = q.toString()
        if url not in self.history:
            self.history.append(url)

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("Histórico")
        history_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        list_widget = QListWidget(history_dialog)
        list_widget.addItems(self.history)
        
        layout.addWidget(list_widget)
        
        history_dialog.setLayout(layout)
        history_dialog.exec()

    def clear_history(self):
        self.history.clear()

    def show_favorites(self):
        favorites_dialog = QDialog(self)
        favorites_dialog.setWindowTitle("Favoritos")
        favorites_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        list_widget = QListWidget(favorites_dialog)
        list_widget.addItems(self.favorites)
        
        layout.addWidget(list_widget)
        
        favorites_dialog.setLayout(layout)
        favorites_dialog.exec()

    def add_to_favorites(self):
        current_browser = self.browser.currentWidget().findChild(QWebEngineView)
        current_url = current_browser.url().toString()
        if current_url not in self.favorites:
            self.favorites.append(current_url)

    def toggle_javascript(self):
        current_browser = self.browser.currentWidget().findChild(QWebEngineView)
        settings = current_browser.settings()
        if self.javascript_enabled_action.isChecked():
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        else:
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, False)

    def toggle_theme(self):
        if self.toggle_theme_action.isChecked():
            self.setStyleSheet("QMainWindow { background-color: #2e2e2e; color: white; }")
        else:
            self.setStyleSheet("QMainWindow { background-color: white; color: black; }")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    navegador = Navegador()
    navegador.show()
    sys.exit(app.exec())
