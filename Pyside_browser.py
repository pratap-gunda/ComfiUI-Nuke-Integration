from PySide6 import QtCore, QtWidgets, QtWebEngineCore, QtWebEngineWidgets
import sys
import os

class BrowserWindow(QtWidgets.QMainWindow):
    def __init__(self, home_url='https://www.comflowy.com/blog/ten-models-worth-downloading'):
        super(BrowserWindow, self).__init__()

        self.setWindowTitle('PySide6 Browser')
        self.setGeometry(300, 150, 1200, 800)

        self.home_url = home_url

        # Layout and central widget
        layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Navigation bar layout (for back, forward, etc.)
        nav_layout = QtWidgets.QHBoxLayout()

        # Back button
        back_button = QtWidgets.QPushButton('Back')
        back_button.clicked.connect(self.browser_back)
        nav_layout.addWidget(back_button)

        # Forward button
        forward_button = QtWidgets.QPushButton('Forward')
        forward_button.clicked.connect(self.browser_forward)
        nav_layout.addWidget(forward_button)

        # Reload button
        reload_button = QtWidgets.QPushButton('Reload')
        reload_button.clicked.connect(self.browser_reload)
        nav_layout.addWidget(reload_button)

        # Home button
        home_button = QtWidgets.QPushButton('Home')
        home_button.clicked.connect(self.browser_home)
        nav_layout.addWidget(home_button)

        # Add navigation bar to layout
        layout.addLayout(nav_layout)

        # Address bar
        self.url_bar = QtWidgets.QLineEdit()
        self.url_bar.setPlaceholderText('Enter URL...')
        layout.addWidget(self.url_bar)

        # Load button
        load_button = QtWidgets.QPushButton('Go')
        load_button.clicked.connect(self.load_url)
        layout.addWidget(load_button)

        # Web view
        self.browser = QtWebEngineWidgets.QWebEngineView()
        layout.addWidget(self.browser)

        # Enable WebEngine settings (JavaScript, WebGL, etc.)
        settings = self.browser.settings()
        settings.setAttribute(QtWebEngineCore.QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QtWebEngineCore.QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QtWebEngineCore.QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QtWebEngineCore.QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QtWebEngineCore.QWebEngineSettings.Accelerated2dCanvasEnabled, True)

        # Connect the downloadRequested signal
        profile = self.browser.page().profile()
        profile.downloadRequested.connect(self.on_downloadRequested)

        # Set home page
        self.browser_home()

    @QtCore.Slot()
    def load_url(self):
        """Load the URL entered in the address bar."""
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QtCore.QUrl(url))

    @QtCore.Slot()
    def browser_home(self):
        """Navigate to the default home URL."""
        self.browser.setUrl(QtCore.QUrl(self.home_url))
        self.url_bar.setText(self.home_url)

    @QtCore.Slot()
    def browser_back(self):
        """Go back to the previous page."""
        self.browser.back()

    @QtCore.Slot()
    def browser_forward(self):
        """Go forward to the next page."""
        self.browser.forward()

    @QtCore.Slot()
    def browser_reload(self):
        """Reload the current page."""
        self.browser.reload()

    @QtCore.Slot(QtWebEngineCore.QWebEngineDownloadRequest)
    def on_downloadRequested(self, download_request):
        """Slot to handle download requests."""
        url = download_request.url()
        file_path = url.path()
        file_name = os.path.basename(file_path)
        file_parts = file_name.split(".")
        
        # Check if the file has the .safetensors extension
        if len(file_parts) > 1 and file_parts[-1].lower() == "safetensors":
            # Suggest download to the checkpoints folder for .safetensors files
            default_path = os.path.join('C:\\Users\\vishr\\Downloads\\checkpoints', file_name)
        else:
            # Default to general Downloads folder for other files
            default_path = os.path.join('C:\\Users\\vishr\\Downloads', file_name)

        # Open save file dialog with the default path pre-filled
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Save File", 
            default_path, 
            f"*.{file_parts[-1].lower()}"  # Filter based on the file extension
        )
        
        if path:
            download_request.setPath(path)
            download_request.accept()
            print(f"Downloaded to {path}")
        else:
            download_request.cancel()

    @QtCore.Slot()
    def download_finished(self):
        """Slot to handle download completion."""
        print("Download finished!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    browser_window = BrowserWindow()
    browser_window.show()
    sys.exit(app.exec())
