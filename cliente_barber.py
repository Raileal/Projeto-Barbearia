#OUTRAS FUNÇÕES
import sys
import socket
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QTimeEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QTime
from funcoes.Auxiliares import *
#TELAS
from telas.tela_calendario_cliente_ui import *
 
ip = '192.168.2.105'
porta = 8007
addr = ((ip,porta))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(addr)
except Exception as e:
    print(f'Ocorreu uma exceção: {e}')
    exit()
            


class Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()
        self.stack0 = QtWidgets.QMainWindow()

        
        self.tela_calendario_cliente = Ui_Tela_calendario_cliente()
        self.tela_calendario_cliente.setupUi(self.stack0)


        self.QtStack.addWidget(self.stack0)


class Ui_Main(QMainWindow, Main):
    
    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)
        #Possiveis Variaveis
        self.datas = []
        ##Funcionar Telas

        #tela_calendario
        self.tela_calendario_cliente.calendarWidget.selectionChanged.connect(self.funciona_data_calendario)
        self.tela_calendario_cliente.pushButton.clicked.connect(self.fecharAplicacao)
        self.tela_calendario_cliente.pushButton_2.clicked.connect(self.botao_confirma)
        self.tela_calendario_cliente.listView.clicked.connect(self.Excluir_click)
        self.atualiza_cor_calendario()
        
        
    ##Funções
    def fecharAplicacao(self):
        client_socket.send('0'.encode())
        sys.exit()
    
    def tela_inicial_cliente(self):
        self.QtStack.setCurrentIndex(0)
        
                
    def funciona_data_calendario(self):
        self.atualiza_cor_calendario()
        data_selecionada = self.tela_calendario_cliente.calendarWidget.selectedDate()
            
        print('o meu clique-> ',data_selecionada)
        data_qdate = QDate(data_selecionada)
        self.data_enviar = data_qdate.toString("yyyy-MM-dd")
        print('esta enviando isso ->',self.data_enviar)

        # Agora captura os horários selecionados
        self.horarios_selecionados = self.mostrar_escolhidos_Qbox(self.data_enviar)
        print('Horarios Selecionados ->',self.horarios_selecionados)
        print('Datas selecionadas ->',self.data_enviar)

        self.mostrar_escolhidos_list(self.data_enviar, self.horarios_selecionados)
        # client_socket.send('6'.encode())
        
    def mostrar_escolhidos_list(self, data_formatada, horarios):
        self.atualiza_cor_calendario()
        if any([not horario for horario in horarios]):
            self.items = []
            QMessageBox.warning(self, "Aviso", "Um ou mais horários não foram especificados.")
        else:
            self.items = [f"Data: {data_formatada}, Hora(s): {horario}" for horario in horarios]
        
        model = QStringListModel()
        model.setStringList(self.items)
        self.tela_calendario_cliente.listView.setModel(model)
        

        
        
    def mostrar_escolhidos_Qbox(self, data_formatada):
        self.atualiza_cor_calendario()
        print('entrou no mostrar_escolhidos')
        
        client_socket.send('7'.encode())
        client_socket.send(str(data_formatada).encode())
        data_hora_string = client_socket.recv(4096).decode().strip()
        print('Recebi do servidor-->', data_hora_string)
        print('Recebi do servidor-->', type(data_hora_string))

        dialog = QDialog()
        dialog.setWindowTitle(data_formatada)
        dialog.resize(400, 300)

        layout = QVBoxLayout()

        label = QLabel("Selecione horários:")
        layout.addWidget(label)

        horLayout = QHBoxLayout()

        timeComboBox = QComboBox()
        horLayout.addWidget(timeComboBox)

        addButton = QPushButton("Adicionar")
        horLayout.addWidget(addButton)
        

        removeButton = QPushButton("Remover")
        horLayout.addWidget(removeButton)

        layout.addLayout(horLayout)

        listWidget = QListWidget()
        layout.addWidget(listWidget)

        # Preenche o QListWidget e o QComboBox com as horas recebidas
        horas = [item.split()[1] if len(item.split()) > 1 else '' for item in data_hora_string.split("\n") if item]

        print('qbox ->', horas)

        timeComboBox.addItems(horas)

        def adicionar_horario():
            novo_horario = timeComboBox.currentText()
            if novo_horario:
                if novo_horario not in [listWidget.item(i).text() for i in range(listWidget.count())]:
                    listWidget.addItem(novo_horario)

        def remover_horario():
            item = listWidget.takeItem(listWidget.currentRow())
            if item:
                horario_removido = item.text()
                if horario_removido not in horas:
                    horas.append(horario_removido)
                    timeComboBox.addItem(horario_removido)

        def on_ok_clicked():
            dialog.accept()

        addButton.clicked.connect(adicionar_horario)
        removeButton.clicked.connect(remover_horario)
        
        okButton = QPushButton("OK")
        okButton.clicked.connect(on_ok_clicked)
        layout.addWidget(okButton)

        cancelButton = QPushButton("Cancelar")
        cancelButton.clicked.connect(dialog.reject)

        layout.addWidget(cancelButton)

        dialog.setLayout(layout)

        selectedTimes = []  # Inicializar selectedTimes antes do diálogo ser exibido
        if dialog.exec_() == QDialog.Accepted:
            selectedTimes = [listWidget.item(i).text() for i in range(listWidget.count())]

        return selectedTimes  # Retorna a lista de horários selecionados independentemente do resultado do diálogo
    
    def Excluir_click(self,index):
        if index.isValid():
            item_selecionado = index.data()
            print(item_selecionado)
            reply = QMessageBox.question(
                self,
                'Confirmação',
                f'Deseja retirar o horario marcado?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if item_selecionado in self.items:
                    print('Está aqui em!')
                    self.items.remove(item_selecionado)
                    model = QStringListModel()
                    model.setStringList(self.items)
                    self.tela_calendario_cliente.listView.setModel(model)

    def botao_confirma(self):
        self.atualiza_cor_calendario()
        self.nome = self.tela_calendario_cliente.lineEdit_3.text()
        email = self.tela_calendario_cliente.lineEdit.text()
        if self.nome == '' or email == '':
            QtWidgets.QMessageBox.information(self, 'Erro', 'Digite valores válidos.')
        elif not verificar_nome(self.nome):
            QtWidgets.QMessageBox.information(self, 'Erro', 'Nome inválido. Digite apenas letras.')
        elif not email_valido(email):
            QtWidgets.QMessageBox.information(self, 'Erro', 'Email inválido.')
        elif self.tela_calendario_cliente.listView.model() is None or self.tela_calendario_cliente.listView.model().rowCount() == 0:
            QtWidgets.QMessageBox.information(self, 'Erro', 'Selecione pelo menos um horário.')
        else:
            horarios_selecionados = self.horarios_selecionados
            data_hora_nome = f"{self.data_enviar} {', '.join(horarios_selecionados)} {self.nome} {email}"
            print(data_hora_nome)
            # Adiciona um diálogo de confirmação
            reply = QtWidgets.QMessageBox.question(self, 'Confirmação', 'Tem certeza que deseja agendar este horário?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                client_socket.send('5'.encode())
                client_socket.send(data_hora_nome.encode())
                recv = client_socket.recv(4096).decode()
                print('Recebi ->',recv)
                if recv == '1':
                    QMessageBox.information(self, 'Agenda', 'Horario Agendado com sucesso.')
                    mensagem = formatar_mensagem(self.nome,self.data_enviar,horarios_selecionados)
                    EnviaEmail(email,mensagem)
                    self.nome = self.tela_calendario_cliente.lineEdit_3.clear()
                    email = self.tela_calendario_cliente.lineEdit.clear() 
                elif recv == '2':
                    QMessageBox.information(self, 'Agenda', 'Horario já Agendado por outra pessoa.') 
                else:
                    QMessageBox.information(self, 'Agenda', 'Horario nao Agendado.') 
                    
                self.tela_calendario_cliente.listView.model().setStringList([]) 
                         
            
    def atualiza_cor_calendario(self):
        print('Calendario...')
        client_socket.send('2'.encode())
        data_hora_string = client_socket.recv(4096).decode().strip()
        print('list ->', data_hora_string)
        datas = data_hora_string.split('\n')
        print('Calendario->', datas)
        text_format = QtGui.QTextCharFormat()
        original_dates = set()  # Armazena as datas originais para verificar posteriormente
        if data_hora_string != '0':  # Verifica se há dados a serem processados
            for data in datas:
                date_str = data.split('\t')[0]  # Pega apenas a primeira parte, que é a data
                date = QtCore.QDate.fromString(date_str, "yyyy-MM-dd")
                text_format.setBackground(QtGui.QColor(QtCore.Qt.red))
                text_format.setForeground(QtGui.QColor(QtCore.Qt.black))
                self.tela_calendario_cliente.calendarWidget.setDateTextFormat(date, text_format)
                original_dates.add(date)  # Adiciona a data original ao conjunto

            # Voltar a cor original das datas que não estão mais no banco de dados
            for date_widget in self.tela_calendario_cliente.calendarWidget.dateTextFormat().keys():
                if date_widget not in original_dates:
                    text_format.setBackground(QtGui.QColor(QtCore.Qt.white))  # Cor original (branco)
                    text_format.setForeground(QtGui.QColor(QtCore.Qt.black))
                    self.tela_calendario_cliente.calendarWidget.setDateTextFormat(date_widget, text_format)
        else:  # Se não há dados a serem processados, voltar todas as datas à cor original
            for date_widget in self.tela_calendario_cliente.calendarWidget.dateTextFormat().keys():
                text_format.setBackground(QtGui.QColor(QtCore.Qt.white))  # Cor original (branco)
                text_format.setForeground(QtGui.QColor(QtCore.Qt.black))
                self.tela_calendario_cliente.calendarWidget.setDateTextFormat(date_widget, text_format)



        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Ui_Main()
    sys.exit(app.exec_())