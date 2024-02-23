#OUTRAS FUNÇÕES
import sys
import socket
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QTimeEdit, QMessageBox, QLineEdit
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QTableWidgetItem


#TELAS
from telas.tela_barbeiro_ui import *
from telas.Tela_Buscar_Barbeiro_ui import *
from telas.Tela_Agenda_Barber_ui import *
from funcoes.Auxiliares import *
 
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
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()


        self.tela_barbeiro_ui = Ui_Tela_Barbeiro()
        self.tela_barbeiro_ui.setupUi(self.stack0)
        
        self.Tela_Buscar_Barbeiro_ui = Ui_Tela_busca_Barbeiro()
        self.Tela_Buscar_Barbeiro_ui.setupUi(self.stack1)
        
        self.Tela_Agenda_Barber_ui = Ui_Tela_Agenda_barber()
        self.Tela_Agenda_Barber_ui.setupUi(self.stack2)


        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)

class Ui_Main(QMainWindow, Main):
    
    def __init__(self):
        super(Main, self).__init__(None)
        self.setupUi(self)
        #Possiveis Variaveis
        self.dados_envio = []
        self.lista_original = []
        self.lista_error = []
        ##Funcionar Telas
        
        #tela barbeiro
        #feha a aplicação
        self.tela_barbeiro_ui.pushButton_3.clicked.connect(self.fecharAplicacao)
        #Vai para outra tela
        self.tela_barbeiro_ui.pushButton.clicked.connect(self.ir_tela_busca_barber)
        #Serve para usar o calendario
        self.tela_barbeiro_ui.calendarWidget.selectionChanged.connect(self.funciona_data_calendario) 
        
        #Começa sempre pela data atual
        self.tela_barbeiro_ui.calendarWidget.setSelectedDate(QtCore.QDate.currentDate())
        
        #clica no confirmarTarefa
        self.tela_barbeiro_ui.pushButton_2.clicked.connect(self.marcar_na_agenda)
        
        #Clica para ver agenda
        self.tela_barbeiro_ui.pushButton_4.clicked.connect(self.mostra_D_H_escolhidas)

        # tela_buscar_agenda
        self.Tela_Buscar_Barbeiro_ui.pushButton.clicked.connect(self.ir_tela_barber)
        self.Tela_Buscar_Barbeiro_ui.pushButton_2.clicked.connect(self.liberar_datas_e_horarios)
        self.Tela_Buscar_Barbeiro_ui.listView.clicked.connect(self.Excluir_hora_clicada)

        # #tela Agenda
        self.Tela_Agenda_Barber_ui.pushButton.clicked.connect(self.ir_tela_barber)
        self.Tela_Agenda_Barber_ui.pushButton_2.clicked.connect(self.buscar_por_data)
        self.Tela_Agenda_Barber_ui.pushButton_4.clicked.connect(self.desmarcar_data)
        self.Tela_Agenda_Barber_ui.pushButton_3.clicked.connect(self.exibir_lista_original)
        self.Tela_Agenda_Barber_ui.listWidget.itemClicked.connect(self.excluir_por_data_e_hora)
        

        
    ##Funções
    def fecharAplicacao(self):
        client_socket.send('0'.encode())
        sys.exit()
        
    def ir_tela_busca_barber(self):
        self.QtStack.setCurrentIndex(1)
        
        
    def ir_tela_barber(self):
        self.QtStack.setCurrentIndex(0)
        
        
    def mostrar_escolhidos_Qbox(self, data_formatada):
        dialog = QDialog()
        dialog.setWindowTitle(data_formatada)
        dialog.resize(400, 300)

        layout = QVBoxLayout()
        label = QLabel("Selecione horários:")
        layout.addWidget(label)

        horLayout = QHBoxLayout()
        timeEdit = QTimeEdit()
        timeEdit.setTime(QTime.currentTime())
        timeEdit.setDisplayFormat("HH:mm")
        horLayout.addWidget(timeEdit)

        addButton = QPushButton("Adicionar")
        horLayout.addWidget(addButton)

        removeButton = QPushButton("Remover")
        horLayout.addWidget(removeButton)

        layout.addLayout(horLayout)

        listWidget = QListWidget()
        layout.addWidget(listWidget)

        addButton.clicked.connect(lambda: adicionar_horario(listWidget, timeEdit))
        removeButton.clicked.connect(lambda: listWidget.takeItem(listWidget.currentRow()))

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancelar")
        okButton.clicked.connect(dialog.accept)
        cancelButton.clicked.connect(dialog.reject)

        layout.addWidget(okButton)
        layout.addWidget(cancelButton)

        dialog.setLayout(layout)

        def adicionar_horario(listWidget, timeEdit):
            novo_horario = timeEdit.time().toString("HH:mm")
            if novo_horario not in [listWidget.item(i).text() for i in range(listWidget.count())]:
                listWidget.addItem(novo_horario)

        selectedTimes = []  # Inicializar selectedTimes antes do diálogo ser exibido
        if dialog.exec_() == QDialog.Accepted:
            selectedTimes = [listWidget.item(i).text() for i in range(listWidget.count())]

        return selectedTimes  # Retorna a lista de horários selecionados independentemente do resultado do diálogo


    ##Tela_principal_Barber
    
    def mostrar_escolhidos_list(self, data_formatada, horarios):
        items = [f"{data_formatada} - {horario}" for horario in horarios]
        model = QStringListModel()
        model.setStringList(items)
        self.tela_barbeiro_ui.listView.setModel(model)
        

    ##Tela_principal_Barber
    def mostrar_no_ver_marcacoes(self, data_formatada, horarios):
        model = self.Tela_Buscar_Barbeiro_ui.listView.model()
        if model is None:
            model = QStringListModel()

        # Adicionar novos itens à lista existente ou substituir se a data já existir
        self.items = model.stringList()
        novos_itens = []

        # Verificar se a data já existe na lista
        data_existente = any(data_formatada in item for item in self.items)

        if data_existente:
            # Substituir a data existente pelos novos horários
            novos_itens = [f"{data_formatada} : {horario}" for horario in horarios]
            self.items = [item for item in self.items if not item.startswith(data_formatada)]
        else:
            # Adicionar a nova data com seus horários
            novos_itens = [f"{data_formatada} : {horario}" for horario in horarios]

        # Adicionar os novos itens à lista
        self.items += novos_itens

        # Definir a nova lista no modelo da listView
        model.setStringList(self.items)
        self.Tela_Buscar_Barbeiro_ui.listView.setModel(model)

    ##Tela_principal_Barber
    def funciona_data_calendario(self):
        data_selecionada = self.tela_barbeiro_ui.calendarWidget.selectedDate()
        data_qdate = QDate(data_selecionada)
        self.data_enviar = data_qdate.toString("yyyy-MM-dd")

        # Agora captura os horários selecionados
        self.horarios_selecionados = self.mostrar_escolhidos_Qbox(self.data_enviar)
        
        
        # Passa tanto a data quanto os horários para mostrar_escolhidos_list
        self.mostrar_escolhidos_list(self.data_enviar, self.horarios_selecionados)
               
    ##Tela_principal_Barber          
    def marcar_na_agenda(self):
        if self.tela_barbeiro_ui.listView.model() is not None and self.tela_barbeiro_ui.listView.model().rowCount() > 0:
            self.mostrar_no_ver_marcacoes(self.data_enviar, self.horarios_selecionados)
            
            QMessageBox.information(self, "Confirmação de data", "Marcado na Agenda!")
            self.tela_barbeiro_ui.listView.model().setStringList([]) 
        else:
            QMessageBox.warning(self, "Lista Vazia", "A lista de horários está vazia. Adicione horários antes de confirmar.")
            
    ##Tela_Marcações ##list1
    def liberar_datas_e_horarios(self):
        model = self.Tela_Buscar_Barbeiro_ui.listView.model()
        if model is not None:
            if model.rowCount() != 0:
                self.dados_envio.append(self.items)
                reply = QMessageBox.question(
                    self,
                    'Confirmação',
                    f'Deseja continuar?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if self.dados_envio:
                        client_socket.send('1'.encode())
                        client_socket.send(str(self.dados_envio).encode())
                            
                        QMessageBox.information(self, "Confirmação", "Sucesso.")
                        self.dados_envio = []
                    else:
                        QMessageBox.warning(self, "Dados Vazios", "Nenhum dado para enviar.")
                            # Limpa a lista apenas se os dados foram enviados com sucesso
                    self.Tela_Buscar_Barbeiro_ui.listView.model().setStringList([])
                else: 
                    QMessageBox.warning(self, "Lista", "Não enviou.")
            else:
                QMessageBox.warning(self, "Lista Vazia", "A lista de horários está vazia. Adicione horários antes de confirmar.")
        else:
            QMessageBox.warning(self, "Erro de Modelo", "O modelo da lista não está definido.")
            
            
    ##Tela_Marcações
    def Excluir_hora_clicada(self,index):
        
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
                    self.Tela_Buscar_Barbeiro_ui.listView.setModel(model)

    def mostra_D_H_escolhidas(self):
        try:
            # Enviar mensagem '2' para solicitar datas e horas marcadas
            client_socket.send('2'.encode())

            # Receber os dados do servidor
            dados_recebidos = client_socket.recv(4096).decode()
            
            if dados_recebidos == '0':
                QMessageBox.warning(self, 'Aviso', 'Nenhuma data e hora disponível.')
                return
            
            dados = dados_recebidos.split('\n')

            # Limpar todos os itens existentes no QListWidget
            self.Tela_Agenda_Barber_ui.listWidget.clear()

            # Adicionar cabeçalho
            self.Tela_Agenda_Barber_ui.listWidget.addItem("  Data\t\t\tHorário\t\t\tNome")

            # Adicionar os novos dados ao QListWidget
            for dado in dados:
                self.Tela_Agenda_Barber_ui.listWidget.addItem(dado)

            self.QtStack.setCurrentIndex(2)
        except Exception as e:
            print(f"Erro ao mostrar datas e horas escolhidas: {e}")



    def exibir_lista_original(self):
        self.mostra_D_H_escolhidas()




    
    ##Tela_Agenda_Buscando_por_data_e_exibindo
    def buscar_por_data(self):
        data = self.Tela_Agenda_Barber_ui.lineEdit_2.text()
        print('Aqui foi escrito algo --:>', data)
        client_socket.send('3'.encode())
        
        if data.strip():
            
            client_socket.send(data.encode())
            
            data_hora_string = client_socket.recv(4096).decode().strip()  # Remova espaços em branco extras
            
            print(data_hora_string)
            if data_hora_string == '0':
                QMessageBox.warning(self, 'Aviso', 'Nenhuma data e hora disponível.')
                return
            
            dados = data_hora_string.split('\n')

            # Limpar todos os itens existentes no QListWidget
            self.Tela_Agenda_Barber_ui.listWidget.clear()

            # Adicionar cabeçalho
            self.Tela_Agenda_Barber_ui.listWidget.addItem("  Data\t\t\tHorário\t\t\tNome")

            # Adicionar os novos dados ao QListWidget
            for dado in dados:
                self.Tela_Agenda_Barber_ui.listWidget.addItem(dado)

            data = self.Tela_Agenda_Barber_ui.lineEdit_2.clear()        
        else:
            QMessageBox.warning(self, "Campo Vazio", "Por favor, insira uma data antes de buscar.")
            
    def on_remover_clicked(self, lineEdit):
        data = lineEdit.text()
        if data:            
            print(data)
            self.envia_lista_email(data)
            client_socket.send('4'.encode())
            client_socket.send(str(data).encode())
            recv = client_socket.recv(4096).decode()
            print('recebi-> ', recv)
            if recv == '1':
                QMessageBox.information(self, "Exclusão", "Excluido.")    
                self.QtStack.setCurrentIndex(0)
            else:
                QMessageBox.information(self, "Exclusão", "Data não excluída.")
        else:
            QMessageBox.information(self, "Erro", "Por favor, insira uma data válida.")
    

    def desmarcar_data(self):
        dialog = QDialog()
        dialog.setWindowTitle('Excluir da Agenda')
        dialog.resize(300, 200)

        layout = QVBoxLayout()

        # Adiciona um QLabel com instruções para o usuário
        label = QLabel("Digite a data no formato yyyy-mm-dd:")
        layout.addWidget(label)

        # Adiciona um QLineEdit para inserir a data
        lineEdit = QLineEdit()
        layout.addWidget(lineEdit)

        # Adiciona um QPushButton para remover a data
        removeButton = QPushButton("Remover")
        layout.addWidget(removeButton)

        cancelButton = QPushButton("Cancelar")
        layout.addWidget(cancelButton)

        dialog.setLayout(layout)

        # Conecta o botão de remover para chamar a função on_remover_clicked
        removeButton.clicked.connect(lambda: self.on_remover_clicked(lineEdit))

        # Conecta o botão de remover para aceitar o diálogo
        removeButton.clicked.connect(dialog.accept)

        # Conecta o botão de cancelar para rejeitar o diálogo
        cancelButton.clicked.connect(dialog.reject)

        # Abre o diálogo
        dialog.exec_()

    def excluir_por_data_e_hora(self, item):
        data_hora_nome = item.text()
        reply = QMessageBox.question(
                self,
                'Confirmação',
                f'Deseja retirar o horario marcado?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
        if reply == QMessageBox.Yes:
            data, hora, nome = data_hora_nome.split()
            print("Data:", data)
            print("Hora:", hora)
            print("Nome:", nome)
            client_socket.send('6'.encode())
            client_socket.send(f"{data} {hora}".encode())
            
            recv = client_socket.recv(4096).decode()
            if recv == '1':
                QMessageBox.information(self, "Exclusão", "Data e Hora excluída.")
                self.QtStack.setCurrentIndex(0)
            elif recv == '2':
                reply = QMessageBox.question(
                self,
                'Confirmação',
                f'Esse horario já foi escolhido por alguem, deseja remover mesmo assim?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.envia_email(data,hora,nome)
                    client_socket.send('6.1'.encode())
                    client_socket.send(f"{data} {hora}".encode())
                    recv6 = client_socket.recv(4096).decode()
                    if recv6 == '3':
                        QMessageBox.information(self, "Exclusão", "Data e Hora excluída.")
                        self.QtStack.setCurrentIndex(0)
            else:
                QMessageBox.information(self, "Exclusão", "Data e Hora não excluída.")

    def envia_email(self,data,hora,nome):
        client_socket.send('8'.encode())
        print(nome)
        client_socket.send(f"{data} {hora} {str(nome)}".encode())
        
        email = client_socket.recv(4096).decode()
        print(email)
        mensagem = formatar_mensagem_perdao(nome,data,hora)
        EnviaEmail_Barbeiro(email,mensagem)
        
    def envia_lista_email(self,data):
        print('entrou aqiui')
        
        client_socket.send('9'.encode())
        client_socket.send(str(data).encode())
        recebi = client_socket.recv(4096).decode()
        print('recebi os dados do 9->',recebi)
        if recebi == '1':
            QMessageBox.information(self, "Envio", "Email Enviado com Sucesso.")
                

    print('Acabou a função')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Ui_Main()
    sys.exit(app.exec_())
