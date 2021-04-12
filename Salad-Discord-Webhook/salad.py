# help :anyhelpers:

# Como usar o app:
# 1: Vai a este site: app.salad.io
# 2: Clica no cadeado ao lado do url
# 3: Vai aos cookies
# 4: Abre a pasta app-api.salad.io
# 5: Copia o Conteúdo do 'salad.antiforgery' e o 'salad.authentication' para um ficheiro ".env" como assim:
# SALAD_ANTIFORGERY='O teu codigo antiforgery aqui!'
# SALAD_AUTHENTICATION='O teu código de autenticação aqui!'
# DISCORD-WEBHOOK='O teu webhook aqui!'
# 6: Tem em conta de que o ficheiro salad.py tem que estar na mesma pasta que o .env
# 7: Dá restart


from datetime import datetime
import json
import os
import time
import traceback
try:
    with open('colors.json') as f:
        coloors = json.load(f)
    coloorswork = True
    enablesalad = coloors['settings']['enable_salad_balance_tracker']
    title = coloors['settings']['window_title']
    notifthreshold = coloors['settings']['balance_notification_every']

    class custom_colors:
        pass
    for color in coloors['custom_colors'].keys():
        setattr(custom_colors, color, coloors['custom_colors'][color])
except Exception as e:
    print(traceback.format_exc())
    print('Erro com: colors.json')
    coloorswork = False
    enablesalad = False
    title = 'fancy salad miner logs'
    notifthreshold = 1

os.system('title ' + title)
limit = 10
path = os.getenv('APPDATA')
path = path + '/salad/logs/main.log'


class default_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = '\033[37;1m'


def fancytype(words, notime=False, colors=[]):
    colorwords = ''
    for color in colors:
        colorwords = eval(color) + colorwords
    if not notime:
        words = ' ' + colorwords + timenow() + ' ' + words
    else:
        words = ' ' + colorwords + words
    strin = ''
    for let in words:
        strin = strin + let
        print(strin, end='\r')
        time.sleep(0.0078125)
    print(words + default_colors.ENDC + default_colors.DEFAULT)


with open(path) as f:
    oldest = f.readlines()[-1]


if enablesalad:
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        salad_antiforgery = os.getenv('SALAD_ANTIFORGERY')
        salad_authentication = os.getenv('SALAD_AUTHENTICATION')
        if salad_authentication is not None and salad_antiforgery is not None:
            print('[live logs] Tracking preparado!')
        else:
            print('[live logs] Problemas com o arquivo .env!')
            os.system('pause')
            exit()

    except ModuleNotFoundError:
        print('[live logs] Modulos não encontrados, clica em alguma tecla para instalar!')
        os.system('pause')
        os.system('pip install -r requirements.txt --user')
        time.sleep(5)
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        salad_antiforgery = os.getenv('SALAD_ANTIFORGERY')
        salad_authentication = os.getenv('SALAD_AUTHENTICATION')

    cookie = {
        "Salad.Antiforgery": salad_antiforgery,
        "Salad.Authentication": salad_authentication
    }
    try:
        r = requests.get(
            url='https://app-api.salad.io/api/v1/profile/balance', cookies=cookie)
        if r.status_code != 200:
            print(
                f'{default_colors.WARNING}{default_colors.BOLD}[api] Erro! Alguma coisa aconteceu a api do salad! Verifica os dados no ficheiro .env {default_colors.ENDC}')
            os.system('pause')
        jason = r.json()
        oldbalance = jason['currentBalance']
        pongbal = oldbalance
        e = 0
    except requests.ConnectionError:
        print(f'{default_colors.WARNING}{default_colors.BOLD}Erro! Sem internet! {default_colors.ENDC}')
        enablesalad = False
def timenow():
    return '[' + str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]) + ']'
url = os.getenv('discord-webhook')
data = {"username" : "Salad.io"}
while True:
    time.sleep(25)
    matches = False
    try:
        with open(path) as f:
            line = f.readlines()
            for i in range(1, limit+1):
                lien = line[-i].replace('\n', '')
                # print('-------------')
                #print(lien, i)
                # print(oldest)
                if lien == oldest:
                    matches = True
                    oldest = line[-1].replace('\n', '')
                    num = i
                    break
            if not matches:
                oldest = line[-1].replace('\n', '')
                num = limit+1
            for i in reversed(range(1, num)):
                lien = line[-i].replace('\n', '')
                if not coloorswork:
                    if 'ETH share found!' in lien:
                        fancytype(f'{lien}', notime=True, colors=[
                                  'default_colors.OKGREEN', 'default_colors.BOLD'])
                    elif 'GPU' in lien:
                        fancytype(f'{lien}', notime=True, colors=[
                                  'default_colors.OKBLUE', 'default_colors.BOLD'])
                    else:
                        fancytype(lien, notime=True)
                else:
                    found = False
                    for blah in coloors['custom_text'].keys():
                        if blah in lien:
                            fancytype(f'{lien}', notime=True,
                                      colors=coloors['custom_text'][blah])
                            found = True
                            break
                    if not found:
                        fancytype(lien, notime=True)
        if enablesalad:
            if e >= 1:
                fancytype('A espera de um pagamento.')
                cookie = {
                    "Salad.Antiforgery": salad_antiforgery,
                    "Salad.Authentication": salad_authentication
                }
                r = requests.get(
                    url='https://app-api.salad.io/api/v1/profile/balance', cookies=cookie)
                if r.status_code != 200:
                    print(
                        f'{default_colors.WARNING}{default_colors.BOLD}[api] Erro! Alguma coisa aconteceu a api do salad! Verifica os dados no ficheiro .env{default_colors.ENDC}')
                    continue
                jason = r.json()
                if jason['currentBalance'] > oldbalance:
                    diff = jason['currentBalance'] - oldbalance
                    oldbalance = jason['currentBalance']
                    fancytype('[Salad.io] Saldo aumentado em: $' + str(diff), colors=[
                              'default_colors.OKGREEN', 'default_colors.BOLD', 'default_colors.UNDERLINE'])
                    fancytype('[Salad.io] Saldo atual: $' + str(jason['currentBalance']), colors=[
                              'default_colors.OKGREEN', 'default_colors.BOLD', 'default_colors.UNDERLINE'])
                    data["embeds"] = [{"description" : ("Saldo aumentado em: **$" + str(diff) + "**" + "\nSaldo atual: **$" + str(jason['currentBalance']) + "**"),"title" : "Novo Pagamento!"}]
                    result = [requests.post(url, json = data)]              
                    if jason['currentBalance'] - pongbal > notifthreshold:
                        fancytype('[Salad.io] A enviar a notificação!', colors=[
                                  'default_colors.OKGREEN', 'default_colors.BOLD', 'default_colors.UNDERLINE'])
                        toaster.show_toast("Fancy Salad Logs", "Saldo aumentado em: $ " + str(
                            jason['currentBalance'] - pongbal) + ' Desde a ultima notificação!', threaded=True, icon_path=None, duration=3)
                        pongbal = jason['currentBalance']
            else:
                e += 1
    except Exception as o:
        print(traceback.format_exc())
        print(f'{default_colors.WARNING}{default_colors.BOLD}Erro!{default_colors.ENDC}{default_colors.DEFAULT}', str(o))
