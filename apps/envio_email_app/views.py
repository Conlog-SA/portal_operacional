import smtplib
from smtplib import SMTPRecipientsRefused
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Envio_Email():
    def __init__(self, cod_empresa=12):
        self.host = 'smtp-mail.outlook.com'
        self.port = '587'
        if cod_empresa == 12:
            self.login = 'no-reply@conlogsa.com.br'
            self.senha = 'RaLsPc@965214!@#'
        elif cod_empresa == 17:
            self.login = 'no-reply@deeplogistica.com.br'
            self.senha = 'RaLsPc@965214!@#'


    def envia_email_alerta_adm(self, msg):
        server_email = smtplib.SMTP(self.host, self.port)
        server_email.starttls()
        server_email.login(self.login, self.senha)
        email_msg = MIMEMultipart()
        email_msg['FROM'] = self.login #'desenvolvimento@conlogsa.com.br'
        email_msg['CCO'] = '; '.join(["danilo.costa@conlogsa.com.br", "kaian.almeida@conlogsa.com.br", "maria.carvalho@conlogsa.com.br"])
        email_msg['Subject'] = "Solicitação Acesso Portal Operacional"

        corpo_email = f'''
                <div style="background-color: rgba(53, 59, 65, 0.8);
                    position: absolute;
                    padding: 2rem;
                    border-radius: 0.5rem;
                    font-size: 1.25rem;
                    color: white;
                    text-align: center;
                    min-width:550px;
                    max-width: 550px;tgn@7944!tgn@7944!
                    margin-top: 2%;
                    margin-left: 2%;
                    text-decoration: none;
                    ">
                        <h1> PORTAL OPERACIONAL </h1> <br/>
                        {msg}
                        <br><br>            
                        <img class="" src="https://operacional.conlogsa.com.br/static/img/logo_conlog_completa.png" width="210" height="65.109"/>   
                </div>
                '''

        email_msg.attach(MIMEText(corpo_email, 'html'))

        server_email.sendmail(email_msg['FROM'], email_msg['CCO'].split(';'), email_msg.as_string())
        server_email.quit()

    def envia_email_solicitacao_acesso_adm(self, obj_usuario_solicitante):
        server_email = smtplib.SMTP(self.host, self.port)
        server_email.starttls()
        server_email.login(self.login, self.senha)
        email_msg = MIMEMultipart()
        email_msg['FROM'] = self.login #'desenvolvimento@conlogsa.com.br'
        email_msg['CCO'] = '; '.join(["danilo.costa@conlogsa.com.br", "kaian.almeida@conlogsa.com.br", "maria.carvalho@conlogsa.com.br"])
        email_msg['Subject'] = "Solicitação Acesso Portal Operacional"

        corpo_email = f'''
        <div style="background-color: rgba(53, 59, 65, 0.8);
            position: absolute;
            padding: 2rem;
            border-radius: 0.5rem;
            font-size: 1.25rem;
            color: white;
            text-align: center;
            min-width:550px;
            max-width: 550px;
            margin-top: 2%;
            margin-left: 2%;
            text-decoration: none;
            ">
                <h1> PORTAL OPERACIONAL </h1> <br/>
                O usuário <strong>{obj_usuario_solicitante.nome_usu}!</strong>, email : {obj_usuario_solicitante.email_usu}
                <br>Solicita acesso com dados da filial: {obj_usuario_solicitante.cod_filial.desc_filial}, 
                {obj_usuario_solicitante.cod_filial.cod_empresa.desc_empresa}, ao portal operacional. Solicite o mesmo 
                o chamado com a descrição dos módulos necessários a serem liberados.
                <br><br>           
                <img src="https://operacional.conlogsa.com.br/static/img/logo_conlog_completa.png" width="210" height="65.109"/>    
        </div>
        '''

        email_msg.attach(MIMEText(corpo_email, 'html'))

        server_email.sendmail(email_msg['FROM'], email_msg['CCO'].split(';'), email_msg.as_string())
        server_email.quit()

    def envia_email_preenchimento_entrevista_desligamento(self, obj_usuario_resposta):
        server_email = smtplib.SMTP(self.host, self.port)
        server_email.starttls()
        server_email.login(self.login, self.senha)
        email_msg = MIMEMultipart()
        email_msg['FROM'] = self.login #'desenvolvimento@conlogsa.com.br'
        email_msg['CCO'] = "leticia.felix@conlogsa.com.br"
        email_msg['Subject'] = f"Entrevista de desligamento realizada! {obj_usuario_resposta['nome']}"

        corpo_email = f'''
            O ex-colaborador {obj_usuario_resposta['nome']} preencheu preencheu a entrevista de desligamento!
        '''

        email_msg.attach(MIMEText(corpo_email, 'html'))

        server_email.sendmail(email_msg['FROM'], email_msg['CCO'], email_msg.as_string())
        server_email.quit()

    def envia_email_layout_generico_safety_deep(self, lista_email_cco, assunto_email, msg_email):
        server_email = smtplib.SMTP(self.host, self.port)
        server_email.starttls()
        server_email.login(self.login, self.senha)
        email_msg = MIMEMultipart()
        email_msg['FROM'] = self.login
        email_msg['CCO'] = '; '.join(lista_email_cco)
        email_msg['Subject'] = assunto_email

        corpo_email = f'''
                <div style="background-color: rgba(33, 37, 41, 0.8);
                    position: absolute;
                    padding: 2rem;
                    border-radius: 0.5rem;
                    font-size: 1.25rem;
                    color: white;
                    text-align: lef;
                    width:80%;
                    margin-top: 2%;
                    margin-left: 2%;
                    text-decoration: none;
                    ">
                        <div style="text-align: center;">
                            <h1 style="fot-size:2rem;text-transform:uppercase;color: #3b8eed; font-weight: 800;">
                                Safety
                            </h1>
                        </div>
                        {msg_email}
                        <br>  
                        <div style="text-align: center;">
                            <img src="https://operacional.conlogsa.com.br/static/img/logo-deep-small.png" 
                            style="width: 120px;">
                        </div>         

                </div>

            '''

        email_msg.attach(MIMEText(corpo_email, 'html'))
        server_email.sendmail(email_msg['FROM'], email_msg['CCO'].split(';'), email_msg.as_string())
        server_email.quit()