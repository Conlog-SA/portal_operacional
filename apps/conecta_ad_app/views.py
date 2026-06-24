from django.shortcuts import render

from django.shortcuts import render
import os
from ldap3 import Server, Connection, SIMPLE, SUBTREE, ALL_ATTRIBUTES
import json


class Conexao_AD:
    ip_server = '172.16.40.2'
    user_adm = 'administrador'
    senha_adm = 'RaLsPc@965214!@#'
    #Senha anterior : lLhBtApClEJ@911!@# / JeDmKb@365214!@#

    def __init__(self):
        server = Server(f'LDAP://{self.ip_server}', use_ssl=True)
        self.__conn = Connection(server, user=f'conlog\\{self.user_adm}', password=self.senha_adm, authentication=SIMPLE)
        self.__conn.bind()


    def identificacao_ad(self, usuario, senha):
        msg_erro = ''
        result_validacao = False
        usu_ad = None
        try:
            self.__conn.bind()
            self.__conn.search(search_base='dc=conlog,dc=local', search_filter=f'(sAMAccountName={usuario})',
                               search_scope=SUBTREE,  attributes=['cn', 'userAccountControl', 'mail'])
            if len(self.__conn.entries) == 0:
                msg_erro = 'Usuário não encontrado!'
            else:
                nome_completo_usu = self.__conn.entries[0].cn
                status_conta_usu = self.__conn.entries[0].userAccountControl
                email_usu = self.__conn.entries[0].mail
                if self.__conn.rebind(user=f'conlog\\{usuario}', password=senha):
                    result_validacao = True

                    ''' 66048 = Ativo / 66050 = Inativo'''

                    status_usu_ad = 'A'
                    if str(status_conta_usu) == '66050':
                        status_usu_ad = 'I'
                    usu_ad = {
                        'login_usu': usuario,
                        'nome_completo_usu': nome_completo_usu,
                        'email_usu': email_usu,
                        'status': status_usu_ad
                    }
                else:
                    msg_erro = 'Credenciais Inválidas!'
        except Exception as e:
            msg_erro = e
        finally:
            self.__conn.unbind()

        return result_validacao, msg_erro, usu_ad


