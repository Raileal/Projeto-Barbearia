import mysql.connector

class Armazenar_agenda:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.drop_tabela_agenda()
        self.create_armazena_data_table()
        
    def create_armazena_data_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("USE barber")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS barber_agenda (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE,
            hora TIME,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        self.db_connection.commit()
        cursor.close()  
    
    # Insere no bd com nome.
    def inserir_data_hora_nome(self, data, hora, nome, email):
        cursor = self.db_connection.cursor()
        select_query = "SELECT COUNT(*) FROM barber_agenda WHERE data = %s AND hora = %s"
        cursor.execute(select_query, (data, hora))
        result = cursor.fetchone()
        if result[0] == 0:
            insert_query = "INSERT INTO barber_agenda (data, hora, nome, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (data, hora, nome, email))
            self.db_connection.commit()
        cursor.close()

    
    def atualizar_nome(self, data, hora, nome, email):
        cursor = self.db_connection.cursor()
        update_query = "UPDATE barber_agenda SET nome = %s, email = %s WHERE data = %s AND hora = %s"
        cursor.execute(update_query, (nome, email, data, hora))
        self.db_connection.commit()
        cursor.close()


    def verificar_hora_data_escolhida(self, data, hora):
        cursor = self.db_connection.cursor()
        select_query = "SELECT COUNT(*) FROM barber_agenda WHERE data = %s AND hora = %s AND nome = 'Disponivel'"
        cursor.execute(select_query, (data, hora))
        result = cursor.fetchone()
        cursor.close()
        return 1 if result[0] > 0 else 0
    
    def verificar_data_escolhida(self, data):
        cursor = self.db_connection.cursor()
        select_query = "SELECT COUNT(*) FROM barber_agenda WHERE data = %s"
        cursor.execute(select_query, (data,))
        result = cursor.fetchone()
        cursor.close()
        return 1 if result[0] > 0 else 0
    


    def verificar_data_e_hora(self, data, hora):
        cursor = self.db_connection.cursor()
        select_query = "SELECT COUNT(*) FROM barber_agenda WHERE data = %s AND hora = %s"
        cursor.execute(select_query, (data, hora))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0

    
    def buscar_nome_horario_por_data(self, data):
        cursor = self.db_connection.cursor()
        select_query = "SELECT data, hora, nome FROM barber_agenda WHERE data = %s ORDER BY data, hora"
        cursor.execute(select_query, (data,))
        datas_horarios_nomes = []
        for result in cursor.fetchall():
            data_str = result[0].strftime('%Y-%m-%d')
            hora_str = str(result[1].seconds // 3600).zfill(2) + ":" + str((result[1].seconds % 3600) // 60).zfill(2) + ":" + str(result[1].seconds % 60).zfill(2)
            datas_horarios_nomes.append((data_str, hora_str, result[2]))
        cursor.close()
        return datas_horarios_nomes


    
    def buscar_todos_os_registros(self):
        cursor = self.db_connection.cursor()
        select_query = "SELECT data, hora, nome FROM barber_agenda ORDER BY data, hora"
        cursor.execute(select_query)
        registros = []
        for result in cursor.fetchall():
            data_str = result[0].strftime('%Y-%m-%d')
            hora_str = str(result[1].seconds // 3600).zfill(2) + ":" + str((result[1].seconds % 3600) // 60).zfill(2) + ":" + str(result[1].seconds % 60).zfill(2)
            registros.append((data_str, hora_str, result[2]))
        cursor.close()
        return registros
    
    def buscar_email_pelo_nome(self, data, hora, nome):
        print('entrou no buscar email')
        print(data)
        print(hora)
        print(nome)
        
        cursor = self.db_connection.cursor()
        select_query = "SELECT email FROM barber_agenda WHERE nome = %s AND data = %s AND hora = %s"
        cursor.execute(select_query, (nome, data, hora))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None


    def buscar_nome_horario_por_data(self, data):
        cursor = self.db_connection.cursor()
        select_query = "SELECT data, hora, nome, email FROM barber_agenda WHERE data = %s ORDER BY data, hora"
        cursor.execute(select_query, (data,))
        datas_horarios_nomes = []
        for result in cursor.fetchall():
            data_str = result[0].strftime('%Y-%m-%d')
            hora_str = str(result[1].seconds // 3600).zfill(2) + ":" + str((result[1].seconds % 3600) // 60).zfill(2) + ":" + str(result[1].seconds % 60).zfill(2)
            datas_horarios_nomes.append((data_str, hora_str, result[2], result[3]))
        cursor.close()
        print('bd',datas_horarios_nomes)
        return datas_horarios_nomes


        
    def drop_tabela_agenda(self):
        exclui = '0'
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("USE barber")
            delete_query = "DELETE FROM barber_agenda"
            cursor.execute(delete_query)
            self.db_connection.commit()
            print("Todos os registros da tabela barber_agenda foram excluídos com sucesso.")
            exclui = '1'
        except mysql.connector.Error as err:
            print(f"Erro ao tentar excluir os registros da tabela barber_agenda: {err}")
            self.db_connection.rollback()
        finally:
            cursor.close()
        return exclui
    
    def drop_data_agenda(self, data):
        cursor = self.db_connection.cursor()
        try:
            delete_query = "DELETE FROM barber_agenda WHERE data = %s"
            cursor.execute(delete_query, (data,))
            self.db_connection.commit()
            print(f"Registros da data {data} foram excluídos com sucesso.")
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao tentar excluir os registros da data {data}: {err}")
            self.db_connection.rollback()
            return False
        finally:
            cursor.close()
    
    def drop_data_hora_agenda(self, data, hora):
        cursor = self.db_connection.cursor()
        try:
            delete_query = "DELETE FROM barber_agenda WHERE data = %s AND hora = %s"
            cursor.execute(delete_query, (data, hora))
            self.db_connection.commit()
            print(f"Registros da data {data} e hora {hora} foram excluídos com sucesso.")
            return True
        except mysql.connector.Error as err:
            print(f"Erro ao tentar excluir os registros da data {data} e hora {hora}: {err}")
            self.db_connection.rollback()
            return False
        finally:
            cursor.close()


        

