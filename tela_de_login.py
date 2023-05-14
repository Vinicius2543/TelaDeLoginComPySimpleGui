from PySimpleGUI import PySimpleGUI as sg
import mysqly

try:
    print(mysqly.cria_banco_tabela())
except:
    print('Banco de dados já criada')

def janela_de_Login():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Usuario'), sg.Input(key='usuario')],
        [sg.Text('Senha'), sg.Input(key='senha')],
        [sg.Text('Não é cadastrado?'), sg.Button('Cadastrar-se')],
        [sg.Button('Entrar')]
    ]
    return sg.Window('Login', layout=layout, finalize=True)


def logado():
    sg.theme('Reddit')
    banco = mysqly.valores_database()
    cursor = banco.cursor()
    cursor.execute("SElECT * FROM pessoas WHERE usuario ='{}' ".format(valores['usuario']))
    dados = cursor.fetchall()
    layout = [
        [sg.Text(f'Seja bem vindo(a) {ola_user}!')],
        [sg.Text(f'Nome: {dados[0][0]}')],
        [sg.Text(f'Usuário: {dados[0][1]}')],
        [sg.Text(f'Senha: {dados[0][2]}')],
        [sg.Button('Sair')]
    ]
    return sg.Window('Logado', layout=layout, finalize=True, )


def cadastro():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Nome'), sg.Input(key='nome')],
        [sg.Text('Nome de Usuário'), sg.Input(key='login')],
        [sg.Text('Senha'), sg.Input(key='senha')],
        [sg.Text('Repita a Senha'), sg.Input(key='rept_senha')],
        [sg.Text('Deseja excluir um usuário?'), sg.Button('Deletar')],
        [sg.Button('Voltar'), sg.Button('Cadastrar')]
    ]
    return sg.Window('Tela de Cadastro', layout=layout, finalize=True)


def excluir():
    sg.theme('Reddit')
    layout = [
        [sg.Text('EXCLUSÂO DE USUARIOS')],
        [sg.Text('Digite o nome do usuario para excluir')],
        [sg.Input(key='usuario')],
        [sg.Button('Voltar'), sg.Button('Excluir')]
    ]
    return sg.Window('Excluir usuario', layout=layout, finalize=True)


janela1, janela2, janela3, janela4 = janela_de_Login(), None, None, None

while True:
    window, eventos, valores = sg.read_all_windows()
    # se a janela for fechada
    if window == janela1 and eventos == sg.WIN_CLOSED:
        break
    if window == janela1 and eventos == 'Entrar':
        banco = mysqly.valores_database()
        cursor = banco.cursor()
        cursor.execute("SElECT senha FROM pessoas WHERE usuario ='{}' ".format(valores['usuario']))
        senha_bd = cursor.fetchall()
        try:
            senha = senha_bd[0][0]
        except:
            sg.popup_no_titlebar('Este usuário não existe!', background_color='gray')
            senha = ''
        ola_user = valores['usuario']
        try:
            if valores['senha'] == senha:
                janela2 = logado()
                janela1.hide()
        except:
            int(senha)
            if valores['senha'] == senha:
                janela2 = logado()
                janela1.hide()
        banco.close


    if window == janela2 and eventos == 'Sair':
        janela2.hide()
        janela1.un_hide()
    if window == janela1 and eventos == 'Cadastrar-se':
        janela3 = cadastro()
        janela1.hide()
    if window == janela2 and eventos == sg.WIN_CLOSED:
        break
    if window == janela3 and eventos == sg.WIN_CLOSED:
        break
    if window == janela3 and eventos == 'Voltar':
        janela3.hide()
        janela1.un_hide()
    if window == janela3 and eventos == 'Cadastrar':
        if valores['senha'] != valores['rept_senha']:
            sg.popup_no_titlebar('Senhas diferentes', background_color='gray')
        elif valores['senha'] == valores['rept_senha']:
            try:
                banco = mysqly.valores_database()
                cursor = banco.cursor()
                nome = str(valores['nome'])
                usuario = str(valores['login'])
                senha_temp = str(valores['senha'])
                cursor.execute("SElECT usuario FROM pessoas WHERE usuario ='{}' ".format(usuario))
                pessoa_exist = cursor.fetchall()
                try:
                    pessoa = pessoa_exist[0][0]
                except:
                    pessoa = ''
                if usuario == pessoa:
                    sg.popup_no_titlebar('Este nome de usuario ja existe', background_color='gray')
                if usuario != pessoa:
                    comando_sql = "INSERT INTO pessoas (nome,usuario,senha) VAlUES ('{}','{}','{}')".format(nome,
                                                                                                            usuario,
                                                                                                            senha_temp)
                    cursor.execute(comando_sql)
                    banco.commit()
                    banco.close
                    sg.popup_no_titlebar('Cadastro efetuado com sucesso!', background_color='gray')
            except:
                print('DEU ERRO')
    if window == janela3 and eventos == 'Deletar':
        janela4 = excluir()
        janela3.hide()
    if window == janela4 and eventos == sg.WIN_CLOSED:
        break
    if window == janela4 and eventos == 'Voltar':
        janela4.hide()
        janela3.un_hide()
    if window == janela4 and eventos == 'Excluir':
        try:
            user = valores['usuario']
            banco = mysqly.valores_database()
            cursor = banco.cursor()
            cursor.execute("SElECT usuario FROM pessoas WHERE usuario ='{}' ".format(user))
            pessoa_exist = cursor.fetchall()
            try:
                pessoa = pessoa_exist[0][0]
            except:
                pessoa = ''
            if user == pessoa:
                cursor.execute('DELETE FROM pessoas WHERE usuario = "{}"'.format(user))
                banco.commit()
                banco.close
                sg.popup_no_titlebar('Usuário deletado com sucesso!', background_color='gray')
            elif user != pessoa:
                sg.popup_no_titlebar('O usuário {} não esta cadastrado'.format(user), background_color='gray')
        except:
            sg.popup_no_titlebar('Desculpe, ocorreu algum erro.', background_color='gray')
