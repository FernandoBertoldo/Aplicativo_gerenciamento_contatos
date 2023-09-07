import sqlite3
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMainWindow, \
    QApplication, QMessageBox


class CadastroCliente(QMainWindow):
    def __init__(self):
        super().__init__()


        #Configurações da janela principal
        self.setWindowTitle('Cadastro de clientes')
        self.setGeometry(100, 100, 400, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        #Widgets do layout
        self.lbl_nome = QLabel('nome')
        self.txt_nome = QLineEdit()
        self.lbl_sobrenome = QLabel('Sobrenome')
        self.txt_sobrenome = QLineEdit()
        self.lbl_email = QLabel('E-mail')
        self.txt_email = QLineEdit()
        self.lbl_telefone = QLabel('Telefone')
        self.txt_telefone = QLineEdit()



        #definindo as cores dos botões

        self.btn_salvar = QPushButton('Adicionar Contato')
        self.btn_salvar.setStyleSheet("background-color: lightgreen; "
                                 "border-radius: 5px; "
                                 "border: 2px solid green; "
                              )
        self.btn_editar = QPushButton('Editar Contato')
        self.btn_editar.setStyleSheet("background-color: #f1eb9c; "
                              "border-radius: 5px; "
                              "border: 2px solid orange; "
                              )
        self.btn_remover = QPushButton('Excluir Contato')
        self.btn_remover.setStyleSheet("background-color: #ff6961; "
                                "border-radius: 5px; "
                                "border: 2px solid red; "
                                )

        self.btn_limpa_Campos = QPushButton('Limpa Campos')
        self.btn_limpa_Campos.setStyleSheet("background-color: #5F9F9F; "
                                "border-radius: 5px; "
                                "border: 2px solid blue; "
                                )





        #Widget de lista para demonstrar os clintes ja cadastrados
        self.lst_clientes = QListWidget()
        self.lst_clientes.itemClicked.connect(self.selecionar_cliente)

        #Adiciona widgets ao layout
        self.layout.addWidget(self.lbl_nome)
        self.layout.addWidget(self.txt_nome)
        self.layout.addWidget(self.lbl_sobrenome)
        self.layout.addWidget(self.txt_sobrenome)
        self.layout.addWidget(self.lbl_email)
        self.layout.addWidget(self.txt_email)
        self.layout.addWidget(self.lbl_telefone)
        self.layout.addWidget(self.txt_telefone)
        self.layout.addWidget(self.lst_clientes)
        self.layout.addWidget(self.btn_salvar)
        self.layout.addWidget(self.btn_editar)
        self.layout.addWidget(self.btn_remover)
        self.layout.addWidget(self.btn_limpa_Campos)

        self.criar_banco()

        self.carregar_clientes()

        self.cliente_selecionado = None

        self.btn_salvar.clicked.connect(self.salvar_cliente)
        self.btn_editar.clicked.connect(self.editar_cliente)
        self.btn_remover.clicked.connect(self.validar_remocao)
        self.btn_limpa_Campos.clicked.connect(self.limpa_campos)

    def criar_banco(self):
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                sobrenome TEXT,
                email TEXT,
                telefone TEXT
                )
        ''')
        conexao.close()

    def limpa_campos(self):
        self.txt_nome.clear()
        self.txt_sobrenome.clear()
        self.txt_email.clear()
        self.txt_telefone.clear()

    def salvar_cliente(self):
        nome = self.txt_nome.text()
        sobrenome = self.txt_sobrenome.text()
        email = self.txt_email.text()
        telefone = self.txt_telefone.text()

        if self.btn_salvar.text() == 'Atualizar contato':
            self.btn_salvar.setText('Adicionar Contato')
        if self.btn_editar.text() == 'Cancelar':
            self.btn_editar.setText('Editar Contato')

        if nome and sobrenome and email and telefone:
            conexao = sqlite3.connect('contatos.db')
            cursor = conexao.cursor()


            if self.cliente_selecionado is None:
                cursor.execute('''
                INSERT INTO clientes(nome, sobrenome, email, telefone)
                VALUES(?, ?, ?, ?)
            ''',(nome, sobrenome, email, telefone))

            else:
                cursor.execute('''
                    UPDATE clientes 
                    SET nome = ?,  sobrenome = ?,  email = ?, telefone = ?
                    WHERE ID = ?
                ''',(nome, sobrenome, email,telefone, self.cliente_selecionado['id']))

            conexao.commit()
            conexao.close()

            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.cliente_selecionado = None
            self.carregar_clientes()


        else:
            QMessageBox.warning(self,'Aviso', 'Preencha todos os dados')

    def carregar_clientes(self):
        self.lst_clientes.clear()
        conexao = sqlite3.connect('contatos.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome, sobrenome, email, telefone FROM clientes')
        clientes = cursor.fetchall()
        conexao.close()

        for cliente in clientes:
            id_cliente, nome, sobrenome, email, telefone = cliente
            self.lst_clientes.addItem(f'{id_cliente} | {nome} {sobrenome} | {email} | {telefone}')


    def selecionar_cliente(self, item):
        self.cliente_selecionado = {
            'id': item.text().split()[0],
            'nome': self.txt_nome.text(),
            'sobrenome': self.txt_sobrenome.text(),
            'email': self.txt_email.text(),
            'telefone': self.txt_telefone.text()

        }

    def editar_cliente(self):
        if self.btn_editar.text() == 'Editar Contato':
            if self.cliente_selecionado is not None:
                conexao = sqlite3.connect('contatos.db')
                cursor = conexao.cursor()
                cursor.execute('SELECT nome, sobrenome, email, telefone FROM clientes '
                               'WHERE id = ?', self.cliente_selecionado['id'])
                cliente = cursor.fetchone()
                conexao.close()

                if cliente:
                    nome, sobrenome, email, telefone = cliente
                    self.txt_nome.setText(nome)
                    self.txt_sobrenome.setText(sobrenome)
                    self.txt_email.setText(email)
                    self.txt_telefone.setText(telefone)
                    self.btn_editar.setText('Cancelar')
                    self.btn_salvar.setText('Atualizar contato')
        else:
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.txt_telefone.clear()
            self.btn_editar.setText('Editar Contato')
            self.btn_salvar.setText('Adicionar Contato')

    def validar_remocao(self):
        if self.cliente_selecionado is not None:
            mensagem = QMessageBox()
            mensagem.setWindowTitle('Confirmação')
            mensagem.setText('Tem certeza que você deseja remover o cliente')

            botao_sim = mensagem.addButton('sim', QMessageBox.YesRole)
            botao_nao = mensagem.addButton('nao', QMessageBox.NoRole)
            #Define o icone como questionamento
            mensagem.setIcon(QMessageBox.Question)
            mensagem.exec()

            if mensagem.clickedButton() == botao_sim:
                self.remover_cliente()





    def remover_cliente(self):
        if self.cliente_selecionado is not None:
            conexao = sqlite3.connect('contatos.db')
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM clientes WHERE ID = ?',
                           (self.cliente_selecionado['id']))
            conexao.commit()
            conexao.close()
            self.carregar_clientes()
            self.txt_nome.clear()
            self.txt_sobrenome.clear()
            self.txt_email.clear()
            self.cliente_selecionado = None




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CadastroCliente()
    window.show()
    sys.exit(app.exec())
