import threading
import socket
from funcoes.Bd import *
from funcoes.armazena_agenda import *
from funcoes.Auxiliares import *
from datetime import datetime

host = ''
porta = 8007
addr = (host, porta)

mydb = configure_mysql_connection()
db = create_database()


##agenda
dados_agenda = Armazenar_agenda(mydb)

def menu(con, cliente):

    conectado = True

    while conectado:
        mensagem = con.recv(4096).decode()
        if mensagem == '0':
            conectado = False
         
        
        elif mensagem == '1':
            receber_mensagem = con.recv(4096).decode()
            print('1-:>', receber_mensagem)
            try:
                dados_lista = eval(receber_mensagem)
            except Exception as e:
                print(f"Erro ao avaliar a mensagem recebida como lista: {e}")
            
            for itens in dados_lista:
                for item in itens:
                    print('item->', item)
                    data_hora = item.split(' : ')
                    data = data_hora[0].strip()
                    hora = data_hora[1].strip() 
                    if not dados_agenda.verificar_data_e_hora(data, hora):
                        mensagem = dados_agenda.inserir_data_hora_nome(data, hora, "Disponível", "Disponível")
                            
        ###Falta vir o nome, ou seja, uma busca mais refinada.
        elif mensagem == '2':
            try:
                datas_marcadas = dados_agenda.buscar_todos_os_registros()
                print('retorno ->', datas_marcadas)
                print(type(datas_marcadas))
                
                if not datas_marcadas:  # Se a lista estiver vazia
                    con.send('0'.encode())
                else:
                    datas_formatadas = '\n'.join([f"{data[0]}\t\t\t{datetime.strptime(data[1], '%H:%M:%S').strftime('%H:%M:%S')}\t\t\t{data[2]}" for data in datas_marcadas])

                    if datas_formatadas:
                        con.send(datas_formatadas.encode())
            except Exception as e:
                print("Erro:", e)
                con.send('0'.encode())

                
        elif mensagem == '3':
            receber_mensagem = con.recv(4096).decode()
            print('recebi ->', receber_mensagem)
            try:
                datas_marcadas = dados_agenda.buscar_nome_horario_por_data(receber_mensagem)
                print('retorno ->', datas_marcadas)
                datas_formatadas = '\n'.join([f"{data[0]} {datetime.strptime(data[1], '%H:%M:%S').strftime('%H:%M:%S')}" for data in datas_marcadas])
                
                if not datas_marcadas:  # Se a lista estiver vazia
                    con.send('0'.encode())
                else:
                    datas_formatadas = '\n'.join([f"{data[0]}\t\t\t{datetime.strptime(data[1], '%H:%M:%S').strftime('%H:%M:%S')}\t\t\t{data[2]}" for data in datas_marcadas])
                    
                    if datas_formatadas:
                        con.send(datas_formatadas.encode())
            except:
                con.send('0'.encode())
                
        elif mensagem == '4':
            print('Entrou no 4')
            receber_mensagem = con.recv(4096).decode()
            print('recebi 4 ->', receber_mensagem)
            try:
                verifica = dados_agenda.verificar_data_escolhida(receber_mensagem)
                print('4',verifica)
                if verifica:
                    if dados_agenda.drop_data_agenda(receber_mensagem):
                        con.send('1'.encode())
                    else:
                        con.send('0'.encode())
                else:
                    con.send('0'.encode())
            except mysql.connector.Error as err:
                print(f"Erro ao tentar excluir os registros da data {receber_mensagem}: {err}")
                con.send('0'.encode())

                
        ##Inserir agenda.       
        elif mensagem == '5':
            receber_mensagem = con.recv(4096).decode()
            print('recebi',receber_mensagem)
            dados_lista = receber_mensagem.split(' ')
            print(type(dados_lista))
            print(dados_lista)
            data = dados_lista[0]
            hora = dados_lista[1]
            nome = dados_lista[2]
            email = dados_lista[3]
            print(data)
            print(hora)
            print(nome)
            print(email)
            if dados_agenda.verificar_hora_data_escolhida(data, hora) == 1:
                agenda = dados_agenda.atualizar_nome(data,hora,nome,email)
                if not agenda:
                    con.send('1'.encode())
                else:
                    con.send('0'.encode())
            else:
                con.send('2'.encode())
                
                
        elif mensagem == '6':
            print('entrou no 6')
            receber_mensagem = con.recv(4096).decode()
            print('recebi',receber_mensagem)
            dados_lista = receber_mensagem.split(' ')
            data = dados_lista[0]
            hora = dados_lista[1]
            if dados_agenda.verificar_hora_data_escolhida(data, hora) == 1:
                exclui = dados_agenda.drop_data_hora_agenda(data,hora)
                if exclui:
                    con.send('1'.encode())
                else:
                    con.send('0'.encode())
            else:
                con.send('2'.encode())
        
        elif mensagem == '6.1':
            print('entrou no 6.1')
            receber_mensagem = con.recv(4096).decode()
            print('recebi',receber_mensagem)
            dados_lista = receber_mensagem.split(' ')
            data = dados_lista[0]
            hora = dados_lista[1]
            exclui = dados_agenda.drop_data_hora_agenda(data,hora)
            if exclui:
                con.send('3'.encode())
            else:
                con.send('0'.encode())

        elif mensagem == '7':
            receber_mensagem = con.recv(4096).decode()
            print('recebi ->', receber_mensagem)

            try:
                datas_marcadas = dados_agenda.buscar_nome_horario_por_data(receber_mensagem)
                print('retorno ->', datas_marcadas)
                datas_formatadas = '\n'.join([f"{data[0]} {datetime.strptime(data[1], '%H:%M:%S').strftime('%H:%M:%S')}" for data in datas_marcadas])

                if datas_formatadas:
                    datas_formatadas_lista = datas_formatadas.splitlines()
                    print('Datas formatadas lista ->', datas_formatadas_lista)
                    print("tipo ->", type(datas_formatadas_lista))

                    horarios_elegiveis = []  # Lista para armazenar todas as datas e horas elegíveis
                    for datas in datas_formatadas_lista:
                        data, hora = datas.split(' ')
                        print(data)
                        print(hora)
                        if dados_agenda.verificar_hora_data_escolhida(data, hora) == 1:
                            print(str(f'{data} {hora} que são elegíveis'))
                            horarios_elegiveis.append(f'{data} {hora}')
                    if horarios_elegiveis:
                        # Enviar todas as datas e horas elegíveis como uma única mensagem
                        con.send('\n'.join(horarios_elegiveis).encode())
                    else:
                        con.send('0'.encode())  # Envie '0' se nenhuma hora estiver disponível
                else:
                    con.send('0'.encode())
            except Exception as e:
                print("Erro:", e)
                con.send('0'.encode())

        elif mensagem == '8':
            receber_mensagem = con.recv(4096).decode()
            print('recebi ->', receber_mensagem)
            dados_lista = receber_mensagem.split(' ')
            data = dados_lista[0]
            hora = dados_lista[1]
            nome = dados_lista[2]
            email = dados_agenda.buscar_email_pelo_nome(data, hora, nome)
            print('email buscado->',email)
            if email:                                                
                con.send(str(email).encode())
            else:
                con.send('0'.encode())
                
        #rnviar_email
        elif mensagem == '9':
            dados = con.recv(4096).decode()
            datas_marcadas = dados_agenda.buscar_nome_horario_por_data(dados)
            if datas_marcadas:
                datas_formatadas = '\n'.join([f"{data[0]} {datetime.strptime(data[1], '%H:%M:%S').strftime('%H:%M:%S')} {data[2]} {data[3]}" for data in datas_marcadas])
                print(datas_formatadas)
                if datas_formatadas:
                    datas_formatadas_lista = datas_formatadas.splitlines()
                    print('Datas formatadas lista ->', datas_formatadas_lista)
                    for datas in datas_formatadas_lista:
                        data, hora, nome, email = datas.split(' ')
                        if email == 'Disponível':
                            print('Não envia nada')
                        else:
                            mensagem = formatar_mensagem_lista_perdao(nome,data,hora)
                            EnviaEmail_Barbeiro(email,mensagem)
            con.send('1'.encode())

    print(f"[DESCONECTADO]")
    con.close()
    print("[INICIADO] Aguardando conexão...")


def main():
    print("[INICIADO] Aguardando conexão...")
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.bind(addr)
    serv_socket.listen()

    while True:
        con, cliente = serv_socket.accept()
        thread = threading.Thread(target=menu, args=(con, cliente))
        thread.start()

if __name__ == "__main__":
    try:
        main()
    finally:
        dados_agenda.drop_tabela_agenda()
        exit()



##Ou criar um novo mensagme, ou melhorar oque tem.