"""
RipTunes transfers songs from iPod to your local machine.
Copyright (C) 2009  Thierry Lam

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ManageRip import *

NAME, ARTIST, ALBUM, LOCATION = range(4)


class MainWindow(QMainWindow):
    """
    The Main Qt Application

    Usage:
        All Platforms:
            python RipTunes.pyw
        Windows:
            <double-click on> RipTunes.pyw
    """

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.setGeometry(300, 300, 860, 500)
        self.setWindowTitle("RipTunes")
        self.mainFrame = MainFrame(self)
        self.mainFrame.setApp(app)
        self.setCentralWidget(self.mainFrame)

class MainFrame(QFrame):

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.application = None

        self.bold_font = QFont()
        self.bold_font.setWeight(QFont.Bold)

        directoryLabel = QLabel("Destination Folder:")
        self.directoryComboBox = self.createComboBox(QDir.currentPath() + QString(os.sep + "ripped_tunes"))
        browseButton = QPushButton("&Browse", self)
        self.connect(browseButton, SIGNAL("clicked()"), self.browse)

        splitter = QSplitter(Qt.Horizontal)
        browseLayout = QHBoxLayout()
        browseLayout.addWidget(directoryLabel)
        browseLayout.addWidget(self.directoryComboBox)
        browseLayout.addWidget(browseButton)
        widget = QWidget()
        widget.setLayout(browseLayout)
        splitter.addWidget(widget)

        self.rip_button = QPushButton("Rip", self)
        self.connect(self.rip_button, SIGNAL("clicked()"), self.rip)

        self.tableWidget = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addWidget(self.rip_button)
        layout.addLayout(self.createListWidgets())
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.createStatusBar())
        self.setLayout(layout)

        QTimer.singleShot(0, self.initialLoad)

    def setApp(self, app):
        self.application = app   

    def getApp(self):
        return self.application

    def initialLoad(self):
        self.timer = QtCore.QBasicTimer()
        self.manageRip = ManageRip()
        self.tunes = self.manageRip.tunes(self.progressBar, self)
        self.populateTable(self.tunes.items())
        self.modeLabel.setText("Loading Complete")

    def createComboBox(self, text=""):
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return comboBox

    def browse(self):
        """
        Browse button slot, opens a folder browser when the Browse button is 
        clicked.
        """

        destination = QFileDialog.getExistingDirectory(self, "Select Destination Folder", QDir.currentPath())
        self.directoryComboBox.addItem(destination)
        self.directoryComboBox.setCurrentIndex(self.directoryComboBox.currentIndex() + 1)

    def populateTable(self, tunes):
        """
        Populates the tunes table.  The table is populated at start-up, when 
        artist or ablum name is selected.
        @param tunes, the list of tunes used to populate the table
        """

        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setRowCount(len(tunes))
        headers = ["Name", "Artist", "Album", "Location"]
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        self.tableWidget.horizontalHeader().setFont(self.bold_font)

        self.artistQStringList = QStringList()
        self.albumQStringList = QStringList()

        row = 0
        for tune_entry in tunes:
            tune = tune_entry[1]

            nameItem = QTableWidgetItem(tune.title())
            nameItem.setFlags(Qt.ItemIsSelectable)
            self.tableWidget.setItem(row, NAME, nameItem)

            if not self.artistQStringList.contains(tune.artist()):
                self.artistQStringList.append(QString(tune.artist()))

            artistItem = QTableWidgetItem(tune.artist())
            # Set flag Qt.ItemIsEditable to prevent it from being selected
            artistItem.setFlags(Qt.ItemIsEditable)
            self.tableWidget.setItem(row, ARTIST, artistItem)

            if not self.albumQStringList.contains(tune.album()):
                self.albumQStringList.append(QString(tune.album()))

            albumItem = QTableWidgetItem(tune.album())
            # Set flag Qt.ItemIsEditable to prevent it from being selected
            albumItem.setFlags(Qt.ItemIsEditable)
            self.tableWidget.setItem(row, ALBUM, albumItem)

            locationItem = QTableWidgetItem(tune.full_path())
            # Set flag Qt.ItemIsEditable to prevent it from being selected
            locationItem.setFlags(Qt.ItemIsEditable)
            self.tableWidget.setItem(row, LOCATION, locationItem)
            row += 1

        self.artistQStringList.sort()
        # Calculate the number of artists and enter it at index 0 of the list
        self.artistQStringList.insert(0, "All (%i Artists)" % (self.artistQStringList.count()))
        self.albumQStringList.sort()
        if self.artistList.count() == 0:
            self.artistList.addItems(self.artistQStringList)
        if self.albumList.count() == 0:
            self.albumList.addItems(self.albumQStringList)

        self.tableWidget.hideColumn(LOCATION)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.sortItems(0)

        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)

    def createStatusBar(self):
        """
        Create the status bar along with the progress bar in it.
        """

        self.progressBar = QProgressBar(self)
        self.progressBar.setTextVisible(True)
        self.statusBar = QStatusBar(self)
        self.modeLabel = QLabel("Loading Tunes")
        self.statusBar.addWidget(self.progressBar)
        self.statusBar.addWidget(self.modeLabel)

        return self.statusBar

    def createListWidgets(self):
        """
        Create two QListWidgets side by side, one represents the artist 
        and the album for the other.
        """

        layout = QGridLayout()
        self.artistList = QListWidget()
        self.albumList = QListWidget()

        artistLabel = QLabel("Artist")
        artistLabel.setIndent(2)
        artistLabel.setFont(self.bold_font)

        albumLabel = QLabel("Album")
        albumLabel.setIndent(2)
        albumLabel.setFont(self.bold_font)

        layout.addWidget(artistLabel, 0, 0)
        layout.addWidget(albumLabel, 0, 1)
        layout.addWidget(self.artistList, 1, 0)
        layout.addWidget(self.albumList, 1, 1)

        self.connect(self.artistList, SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"), self.artistSelected)
        self.connect(self.albumList, SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"), self.albumSelected)

        return layout

    def artistSelected(self):
        """
        SLOT for the artist QListWidget
        Populate the album QListWidget based on the artist selected.
        Show the tunes from the selected artist in the table
        """

        # Do nothing when focus is switching between QListWidget
        if not self.artistList.currentItem():
            return

        # Show all albums from the selected artist
        currentArtist = self.artistList.currentItem().text()
        albumList = QStringList()
        tune_list = []

        for tune_entry in self.tunes.items():
            tune = tune_entry[1]
            if tune.artist() == currentArtist or str(currentArtist).startswith("All ("):
                tune_list.append(tune_entry)
                if not albumList.contains(QString(tune.album())):
                    albumList.append(QString(tune.album()))

        self.albumList.clear()
        self.populateTable(tune_list)

    def albumSelected(self):
        """
        SLOT for the album QListWidget
        Show the tunes from the selected album
        """

        # Do nothing when focus is switching between QListWidget
        if not self.albumList.currentItem() or not self.artistList.currentItem():
            return

        currentAlbum = self.albumList.currentItem().text()
        currentArtist = self.artistList.currentItem().text()
        tune_list = []

        for tune_entry in self.tunes.items():
            tune = tune_entry[1]
            if tune.album() == currentAlbum and (tune.artist() == currentArtist or str(currentArtist).startswith("All (")):
                tune_list.append(tune_entry)

        self.populateTable(tune_list)

    def rip(self):
        """
        Rip button slot, it copies the selected tunes to the destination folder
        """

        self.modeLabel.setText("Ripping tunes")
        self.statusBar.reformat()
        step = 0
        self.progressBar.setValue(step)
        self.progressBar.setMaximum(len(self.tableWidget.selectedItems()))
        for item in self.tableWidget.selectedItems():
            step += 1
            self.progressBar.setValue(step)
            sourcePath = self.tableWidget.item(item.row(), LOCATION).text()
            self.manageRip.rip(self.tunes[str(sourcePath)], str(self.directoryComboBox.currentText()))
        self.progressBar.setValue(step)


app = QApplication(sys.argv)
window = MainWindow(app)
window.show()
app.exec_()
