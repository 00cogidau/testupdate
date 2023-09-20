import sys
import requests
import zipfile
import io
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

class UpdateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Auto Update App')
        self.setGeometry(100, 100, 400, 200)
        
        btn = QPushButton('Check for Update', self)
        btn.clicked.connect(self.check_for_update)
        btn.resize(btn.sizeHint())
        btn.move(150, 80) 

    def check_for_update(self):
        # Replace with your GitHub API endpoint for releases
        api_url = 'https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/releases/latest'
        
        try:
            response = requests.get(api_url)
            data = response.json()
            latest_version = data['tag_name']
            current_version = 'v1.0.0'  # Replace this with your app's current version

            if latest_version > current_version:
                QMessageBox.information(self, 'Update Available', f'New version {latest_version} is available!')
                # Download the release asset, assuming it's a zip file
                asset_url = data['assets'][0]['browser_download_url']
                response = requests.get(asset_url)
                z = zipfile.ZipFile(io.BytesIO(response.content))
                z.extractall(path='path_to_your_app_directory')  # Replace this path
                QMessageBox.information(self, 'Update Completed', 'The app has been updated. Please restart it.')
            else:
                QMessageBox.information(self, 'No Update', 'You are using the latest version.')
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UpdateApp()
    ex.show()
    sys.exit(app.exec_())
