import re
import smtplib
from email.message import EmailMessage
from datetime import datetime

def verificar_nome(arg):
    if arg.replace(' ', '').isalpha():
        return 1
    else:
        return 0
    
def email_valido(email):
    # Padrão de expressão regular para validar um endereço de e-mail
    email_valido = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    # Verifica se o email corresponde ao padrão
    if re.match(email_valido, email):
        return 1
    else:
        return 0
    
def EnviaEmail(destinatario,mensagem):
    # Configurar email e senha
    EMAIL_ADDRESS = 'cineplus.gerencia@gmail.com'
    EMAIL_PASSWORD = 'qyskmjhoyapdvjay'

    # Criar um email...
    msg = EmailMessage()
    msg['Subject'] = 'COMPROVANTE DE AGENDAMENTO'
    msg['From'] = 'cineplus.gerencia@gmail.com'
    msg['To'] = destinatario
    msg.set_content(mensagem)

    # Ecnviar email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)   
        
def EnviaEmail_Barbeiro(destinatario,mensagem):
    # Configurar email e senha
    EMAIL_ADDRESS = 'cineplus.gerencia@gmail.com'
    EMAIL_PASSWORD = 'qyskmjhoyapdvjay'

    # Criar um email...
    msg = EmailMessage()
    msg['Subject'] = 'AVISO!'
    msg['From'] = 'cineplus.gerencia@gmail.com'
    msg['To'] = destinatario
    msg.set_content(mensagem)

    # Ecnviar email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg) 
        

def formatar_mensagem(nome_cliente, data, horarios):
    data_objeto = datetime.strptime(data, "%Y-%m-%d").date()
    data_formatada = data_objeto.strftime("%d/%m/%Y")
    horarios_formatados = "\n".join(horarios)
    formato_mensagem = f'''        
Olá, {nome_cliente}!

Gostaríamos de informar que seu agendamento para o dia {data_formatada}, nos seguintes horários: {horarios_formatados}, foi realizada com sucesso.

Por favor, lembre-se de comparecer no horário marcado. Estamos ansiosos para receber você em nosso estabelecimento!


Atenciosamente,
Equipe da Barbearia'''

    return formato_mensagem

def formatar_mensagem_perdao(nome_cliente, data, horarios):
    print('entrou auqi')
    horarios_formatados = "\n".join(horarios)
    formato_mensagem = f'''        
Olá, {nome_cliente}!

Gostaríamos de pedir desculpas, mas não conseguiremos atendê-lo no dia {data}, nos seguintes horários:

{horarios_formatados}

Pedimos desculpas pelo inconveniente e esperamos poder atendê-lo em outra ocasião.


Atenciosamente,
Equipe da Barbearia'''

    return formato_mensagem


def formatar_mensagem_lista_perdao(nome_cliente, data, horarios):
    formato_mensagem = f'''        
Olá, {nome_cliente}!

Gostaríamos de pedir desculpas, mas não conseguiremos atendê-lo no dia {data}, nos seguintes horários:

{horarios}

Pedimos desculpas pelo inconveniente e esperamos poder atendê-lo em outra ocasião.


Atenciosamente,
Equipe da Barbearia'''

    return formato_mensagem