import sys
import csv
from GPy import kern
kern
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QListWidget, QListWidgetItem, QLabel, QApplication, QDialog, 
 QMessageBox,QTableWidget,QTableWidgetItem,QPushButton,QHeaderView,QDialogButtonBox, QGridLayout,
 QLineEdit, QMenu, QMenuBar, QGroupBox, QSpinBox, QTextEdit,QVBoxLayout,QHBoxLayout,QFormLayout,QErrorMessage)

#################### Search functions ##########################3

global rows
def updaterows():
    global rows
    header=True
    with open('data.csv', 'w',encoding="utf-8") as f:
        for r in rows:
                w = csv.DictWriter(f, r.keys())
                if header:
                    w.writeheader()
                    header=False
                w.writerow(r)

def deleteBook(txt):
    header=True
    with open('data.csv', 'w',encoding="utf-8") as f:
        for i,r in enumerate(rows):
            if txt in r['Título']:
                del(rows[i])  
            else:
                w = csv.DictWriter(f, r.keys())
                if header:
                    w.writeheader()
                    header=False
                w.writerow(r)
     

def Search():
    title=[""]
    author=[]
    fullinfo=[]
    with open('data.csv',encoding="utf-8") as File:
        reader = csv.DictReader(File)
        for row in reader:
            title.append(row['Título'])
            author.append(row['Autor'])
            fullinfo.append(row)
    return fullinfo,list(dict.fromkeys(author)),title

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox

class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)
        self.start=False
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.setStyleSheet('''
QListView {background-color:#AFEEEE}
QListView::item:selected { color: red; background-color: lightgray; min-width: 1000px; }
QComboBox { color:black;max-width: 500px; min-height: 40px;background-color:#AFEEEE}
QComboBox QAbstractItemView::item { min-height: 150px;background-color:#AFEEEE}



''')
        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)
        self.currentIndexChanged.connect(self.selectionchange)

    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    
     

    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)    

    def selectionchange(self,i):
        if self.start==False:
            return
        global rows
        libros=[]
        txt=self.itemText(i)
        exPopup = ExamplePopup(txt, self)
        
        for i in rows:
            if txt == i['Título']:
                libros.append(i)
                exPopup.filltable(libros)
                exPopup.show()
                return 
            elif txt == i['Autor']:
                libros.append(i)  
        exPopup.filltable(libros)
        exPopup.show()          
        
    


class buttonBook(QPushButton):
    def __init__(self, parent=None):
        super(buttonBook, self).__init__(parent)
        self.setText("Agregar Libro")
        self.setFont(QtGui.QFont("Arial", 10))
        self.setFixedWidth(180)
        self.clicked.connect(self.agregarlibro)
    def agregarlibro(self):
        book=NuevoLibro(self)
        book.table()
        book.show()
class NuevoLibro(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar un Nuevo Libro")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.mainLayout = QVBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.mainLayout.addWidget(self.tableWidget)
        self.mainLayout.addWidget(buttonBox)
        self.setLayout(self.mainLayout)
        self.setGeometry(0, 0, 700, 400)
    def table(self):
        self.etiqueta=["Autor","Título","Cuarto","Mueble","Nivel","Posición"]   
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(10)
        for j,k in enumerate(self.etiqueta):
                header=QtWidgets.QTableWidgetItem(k)
                header.setBackground(QtGui.QColor(63, 136, 143))
                self.tableWidget.setHorizontalHeaderItem(j,header)
                
    def accept(self):
        txt=''
        for j in range(0,10):
            dicc={}
            for i,k in enumerate(self.etiqueta): 
                try:
                    dicc[k]=self.tableWidget.item(j,i).text()
                except:
                    dicc[k]=""
            if dicc["Título"]!="" and dicc["Cuarto"]!="" and dicc["Mueble"]!="":   
                with open('data.csv', 'a',encoding="utf-8") as f:  
                    writer = csv.writer(f)
                    writer.writerow([dicc["Cuarto"], dicc["Mueble"],dicc["Nivel"],dicc["Posición"],dicc["Título"], dicc["Autor"]])
                    
                if txt!='':
                    txt=txt+' , ' 
                txt=txt+dicc["Título"]
            else:
                if dicc["Autor"]=="" and dicc["Título"]=="" and dicc["Cuarto"]=="" and dicc["Mueble"]=="": 
                    break
                elif dicc["Título"]!="" or dicc["Cuarto"]!="" or dicc["Mueble"]!="":
                    QMessageBox.about(self, "No se ha agregado toda la informacion", "El libro que quiere ingresar esta incompleto")
                    
        if txt!='':
            QMessageBox.about(self, "Libro Agregado", "Se ha agregado los libros "+txt)
            self.destroy()
        else:
            QMessageBox.about(self, "No se ha agregado informacion", "Porfavor vuelva a llenar la tabla en orden")
    

class ExamplePopup(QDialog):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Resultados de la Busqueda de "+ name)
        self.setGeometry(0, 0, 900, 400)
    
    def filltable(self,libros):
        self.tableWidget = QTableWidget(self)
        self.x=len(libros)
        button=[]
        #deleteButton.clicked.connect(self.deleteClicked)

        self.etiqueta=["Autor","Título","Cuarto","Mueble","Nivel","Posición"]
        
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(self.x)
        Header = self.tableWidget.horizontalHeader()
        for j,k in enumerate(self.etiqueta):
                header=QtWidgets.QTableWidgetItem(k)
                header.setBackground(QtGui.QColor(63, 136, 143))
                self.tableWidget.setHorizontalHeaderItem(j,header)
                Header.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)
        header=QtWidgets.QTableWidgetItem("Eliminar")        
        header.setBackground(QtGui.QColor(63, 136, 143))
        self.tableWidget.setHorizontalHeaderItem(6,header)
        Header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(0,self.x):
            button.append(QPushButton("x"))
            button[i].clicked.connect(self.close_application)
            button[i].setFixedWidth(60)
            for j,k in enumerate(self.etiqueta):
                h=QtWidgets.QTableWidgetItem(i)
                h.setBackground(QtGui.QColor(63, 136, 143))
                self.tableWidget.setVerticalHeaderItem(i,h)
                #############################################
                header=QtWidgets.QTableWidgetItem(libros[i][k])
                header.setBackground(QtGui.QColor(93, 193, 185))
                self.tableWidget.setItem(i,j,header)
            self.tableWidget.setCellWidget(i,6, button[i])
               
        self.tableWidget.move(0,0)
        self.layout.addWidget(self.tableWidget)
        Update=QPushButton("Actualzar informacion de los libros")    
        Update.clicked.connect(self.savechanges)
        self.layout.addWidget(Update,alignment=QtCore.Qt.AlignRight)
    def savechanges(self):
        choice = QMessageBox.question(self, 'Actualizar Informacion ',
                                            "Esta seguro de querer cambiar la informacion ",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.actualizar()
        else:
            pass
    def actualizar(self):
        global rows
        if self.x>1:
            autor=self.tableWidget.item(0,0).text()
            i=0
            for x in rows:
                if x['Autor']==autor:
                    for j,k in enumerate(self.etiqueta):
                        x[k]=self.tableWidget.item(i,j).text()
                    i=+1
        elif self.x==1:
            title=self.tableWidget.item(0,1).text()
            for x in rows:
                if x['Título']==title:
                    for j,k in enumerate(self.etiqueta):
                        x[k]=self.tableWidget.item(0,j).text()
                    break
        updaterows()        
            
    def close_application(self):
        button = self.sender()
        row = self.tableWidget.indexAt(button.pos()).row()
        libro=self.tableWidget.item(row,1).text()
        choice = QMessageBox.question(self, 'Eliminar '+libro,
                                            "Quieres eliminar"+libro,
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            deleteBook(libro)
            self.tableWidget.removeRow(row)
            #sys.exit()
        else:
            pass

        #self.tableWidget.removeRow(row)    

if __name__ == "__main__":
    import sys
    from PyQt5.QtGui import QStandardItemModel
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QStringListModel
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
    #app = QApplication(sys.argv)
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    rows,title,author=Search()
    combo = ExtendedComboBox()
    comboTitulo = ExtendedComboBox()
    # either fill the standard model of the combobox
    combo.addItems(author)
    comboTitulo.addItems(title)
    combo.start=True
    comboTitulo.start=True

    # or use another model
    #combo.setModel(QStringListModel(string_list))
    titulo=QLabel("BUSQUEDA POR TITULO")
    titulo.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
    titulo.setAlignment(QtCore.Qt.AlignCenter)
    autor=QLabel("BUSQUEDA POR AUTOR")
    autor.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
    autor.setAlignment(QtCore.Qt.AlignCenter)
    button=buttonBook()
    #QPushButton("AGREGAR UN LIBRO")

    layout.addWidget(autor)
    layout.addWidget(comboTitulo)
    layout.addWidget(titulo)
    layout.addWidget(combo)
    layout.addWidget(button,alignment=QtCore.Qt.AlignRight)  
  
    #combo.show()
    #comboTitulo.show()
    window.setLayout(layout)
    window.setWindowTitle("Busqueda de libros por Autor o Titulo")
    window.resize(300,300)
    window.setStyleSheet("background-color: #81D8D0;")
    
    window.show()
    
    
    sys.exit(app.exec_())
