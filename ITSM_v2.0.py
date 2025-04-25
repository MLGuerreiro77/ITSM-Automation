import time
import os
import customer_dic

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert

# Copie os eventos para o arquivo "eventos.txt" e execute esse script.
# Os arquivos ITSM_v1.8.py,customers_dict.py e eventos.txt devem estar na mesma pasta.

arquivo = open('eventos.txt', 'r', encoding= 'utf-8').read()
listaSplit = arquivo.split()
iterList = iter(listaSplit)
evento = []

#for value in iterList:
#    if value == "Closed":
#        next_element = next(iterList)
#        evento.append(next_element)
    #elif value != ('Closed'):
    #    buscar = 'EVT'
    #    evento = [ s for s in listaSplit if buscar in s ]

os.system("cls")
template = ''
temp_check = True

while temp_check == True:
    print('1 - Normalizado durante os testes\n2 - Tratativa em outro ticket')
    template = input('\nDigite o número do template: ')
    if template == '' or template >= '3' or template <= '0':
        os.system("cls")
        print('\n\033[31m[ERRO]: Digite um template válido!\033[m')
    elif template == '1':
        temp_check = False
        break
    elif template == '2':
        tratativaEvt = ''          
        tratativaEvt = input('\nDigite o ticket primário: ')
        temp_check = False
        break

# Setup e abertura do Firefox/Geckodriver

# Bloco headless
'''
options = Options()
options.add_argument("--headless")
firefox_driver = "C:\Python\Webdrivers\geckodriver.exe"
driver = webdriver.Firefox(options=options)
'''
#Bloco normal head
firefox_options = Options()
firefox_driver = "C:\Python\Webdrivers\geckodriver.exe"
driver = webdriver.Firefox()
# Maximizar janela
driver.maximize_window()

#Espera implicita
driver.implicitly_wait(10)

# Abertura da página inicial do ITSM
time.sleep(1)
driver.get("https:// >>>>>PUT YOUR ITSM URL HERE<<<<<")
time.sleep(3)
os.system("cls")

for evt in evento:
    if evt != (''):
        try:

            # Informando o ticket atual
            print(f'Verificando o {evt}. Aguarde...')

            # Acessando o iFrame default (Necessário para fechar mais de 1 EVT)
            driver.switch_to.default_content()
            
            # Click na lupa de busca da página inicial
            lupa = driver.find_element(By.XPATH, '/html/body/div/div/div/header/div[1]/div/div[2]/div/div[4]/form').click()

            # Inserção e busca pelo EVENTO
            busca = driver.find_element(By.XPATH, '//*[@id="sysparm_search"]')
            busca.send_keys(evt)
            busca.send_keys(Keys.ENTER)
            time.sleep(5)
            busca.clear()
            time.sleep(5)
            
            
            # Acessando o iFrame onde estão os elementos da página
            driver.switch_to.frame("gsft_main")

            ########################## FUNÇÃO PARA SALVAR ##########################
            def salvar():
                saveBtn = driver.find_element(By.XPATH, '//*[@id="sysverb_update_and_stay"]')
                saveBtn.click()
                time.sleep(5)

            ########################## VALIDAR O STATUS ATUAL ##########################
            closed_by = driver.find_element(By.XPATH, '//*[@id="sys_readonly.u_rim_event.closed_at"]').get_attribute('value')
            time.sleep(1)
            if closed_by != '':
                print(f'\033[32m{evt} previamente encerrado! Continuando...\033[m\n')
                continue

            external_status = driver.find_element(By.XPATH, '//*[@id="sys_readonly.u_rim_event.u_external_status"]').get_attribute('value')            
            if external_status != '7':
                print(f'\033[33m{evt} com status Ativo! Continuando...\033[m\n')
                continue

            ########################## VERIFICANDO CONFIGURATION ITEM (CI) ##########################
            config_item = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_contract_ci"]').get_attribute('value')
            company_check = driver.find_element(By.XPATH, '//*[@id="u_rim_event.company_label"]').get_attribute('value')
            
            """ def ci_input():
                customer_ci = customer_dic.config_item[company_check]
                send_ci = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_contract_ci"]')
                send_ci.send_keys(customer_ci)
                time.sleep(2)
                send_ci.send_keys(Keys.TAB) 
                time.sleep(5) """

            def ci_skip():
                    short_desc = driver.find_element(By.XPATH, '//*[@id="u_rim_event.short_description"]')
                    short_desc.click()
                    time.sleep(1)
                    short_desc.send_keys(Keys.HOME)
                    short_desc.send_keys('SEM CI - ')
                    #time.sleep(3)
            
            """ if config_item == '':
                if company_check in customer_dic.config_item:
                    ci_input()
                    time.sleep(1)
                    salvar()
                    time.sleep(3) """

            config_item = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_contract_ci"]').get_attribute('value')
            if config_item == '':
                ci_skip()
                time.sleep(1)
                salvar()
                time.sleep(3)
                print(f'\033[33m{evt} sem Configuration item/CI.Continuando...\033[m\n')
                continue

            # VERIFICAR TEMPLATE APLICADO     
            abaClosDet = driver.find_element(By.XPATH, '/html/body/div[2]/form/div[1]/span[6]/span[1]').click()
            variavel_auxiliar = False
            
            # Check Classification, Resolution code e Root cause preenchidos            
            classifi = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_classification"]').get_attribute('value')
            if classifi == '':
                variavel_auxiliar = True
            resolution_code_check = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_task_resolution_code"]').get_attribute('value')            
            if resolution_code_check == '':
                variavel_auxiliar = True
            root_cause_check = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_task_rootcause"]').get_attribute('value')
            if root_cause_check == '':
                variavel_auxiliar = True

            if variavel_auxiliar == True:
                         # ****** APLICAÇÃO DO TEMPLATE (Oscilação de CPU/Memória/Disco/Link) ******
                match template:
                    case '1':
                        dotsClick = driver.find_element(By.XPATH, '//*[@id="toggleMoreOptions"]').click()
                        time.sleep(0.5)
                        tempBar = driver.find_element(By.XPATH, '//*[@id="template-toggle-button"]').click()
                        time.sleep(0.5)
                        dotsBarClick = driver.find_element(By.XPATH, '//*[@id="template-bar-aria-container"]/div/button[1]').click()
                        time.sleep(0.5)
                        filtTemp = driver.find_element(By.XPATH, '//*[@id="overflowTemplateSearch"]')
                        filtTemp.send_keys("Normalizado Durante Testes")
                        time.sleep(1)
                        tempClick = driver.find_element(By.XPATH, '//*[@id="templateOverflowContainer"]/div/ul/li[8]/a[1]').click() 
                        time.sleep(7)
                        barClose = driver.find_element(By.XPATH, '//*[@id="template-bar-aria-container"]/div/button[3]').click()
                        time.sleep(1)
                        salvar()
                     # ****** APLICAÇÃO DO TEMPLATE (Tratativa em outro ticket) ******
                    case '2':
                        dotsClick = driver.find_element(By.XPATH, '//*[@id="toggleMoreOptions"]').click()
                        time.sleep(0.5)
                        tempBar = driver.find_element(By.XPATH, '//*[@id="template-toggle-button"]').click()
                        time.sleep(0.5)
                        dotsBarClick = driver.find_element(By.XPATH, '//*[@id="template-bar-aria-container"]/div/button[1]').click()
                        time.sleep(0.5)
                        filtTemp = driver.find_element(By.XPATH, '//*[@id="overflowTemplateSearch"]')
                        filtTemp.send_keys("Tratativa")
                        time.sleep(1)
                        tempClick = driver.find_element(By.XPATH, '//*[@id="templateOverflowContainer"]/div/ul/li[6]/a[1]').click()
                        time.sleep(7)
                        barClose = driver.find_element(By.XPATH, '//*[@id="template-bar-aria-container"]/div/button[3]').click()
                        time.sleep(1)
                        closDetails = driver.find_element(By.XPATH, '//*[@id="u_rim_event.close_notes"]')
                        closDetails.clear()
                        closDetails.send_keys(f"Evento tratado em outro ticket {tratativaEvt}")
                        rootComms = driver.find_element(By.XPATH, '//*[@id="u_rim_event.u_root_cause_comments"]')
                        rootComms.clear()
                        rootComms.send_keys(f"Evento tratado em outro ticket {tratativaEvt}")
                        time.sleep(1)
                        salvar()

            ########################## CAMPOS QUE REQUEREM FILA E NOME ##########################
            fila = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_owner_group"]').get_attribute('value')
            nome = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_owner"]').get_attribute('value')

            def requester():
                if company_check in customer_dic.companies:
                    customer_name = customer_dic.companies[company_check]
                    name_requester = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_caller"]')
                    name_requester.send_keys(customer_name)
                    time.sleep(1)
                    name_requester.send_keys(Keys.TAB) 
                    time.sleep(2)

            def check_fila():
                res_group = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_responsible_owner_group"]')
                time.sleep(1)
                res_group.clear()
                res_group.send_keys(fila)
                time.sleep(2)
                res_group.send_keys(Keys.TAB)
                time.sleep(3)

            def check_name():
                res_owner = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_responsible_owner"]')
                res_owner.clear()
                time.sleep(1)
                res_owner.send_keys(nome)
                time.sleep(2)
                res_owner.send_keys(Keys.TAB)
                time.sleep(3)

            def resolved_person():
                res_by = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_resolved_by"]')
                res_by.send_keys(nome)
                time.sleep(1)
                res_by.send_keys(Keys.TAB)
                time.sleep(2)

            requester_check = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_caller"]').get_attribute('value')
            if requester_check == '':
                requester()

            responsible_group = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_responsible_owner_group"]').get_attribute('value')
            if responsible_group == '' or responsible_group != fila:
                check_fila()

            responsible_owner = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_responsible_owner"]').get_attribute('value')
            if responsible_owner == '' or responsible_owner != nome:
                check_name()

            resolved_by = driver.find_element(By.XPATH, '//*[@id="sys_display.u_rim_event.u_resolved_by"]').get_attribute('value')
            aba_clos_details = driver.find_element(By.XPATH, '/html/body/div[2]/form/div[1]/span[6]/span[1]').click()
            if resolved_by == '':
                resolved_person()

            ########################## FUNÇÕES DE ENCERRAMENTO ##########################
            previous_action = (driver.find_element(By.XPATH, '//*[@id="sys_readonly.u_rim_event.u_next_step"]').get_attribute('value'))
            
            def close_cancel():
                dropdown = driver.find_element(By.NAME, "u_rim_event.u_next_step_displayed")
                ddown = Select(dropdown)
                ddown.select_by_visible_text("Close or cancel task")
                time.sleep(2)

            def set_close():
                time.sleep(2)
                dropdown = driver.find_element(By.NAME, "u_rim_event.u_next_step_displayed")
                ddown = Select(dropdown)
                time.sleep(1)
                ddown.select_by_visible_text("Set to closed")
                time.sleep(2)
                alert = Alert(driver)
                alert.accept()
                time.sleep(2)
                return

            match previous_action:
                case '30':
                    close_cancel()
                    salvar()
                    set_close()
                case '220':
                    set_close()
                    salvar()

        
            ########################## VALIDANDO ENCERRAMENTO ##########################
            time.sleep(3)
            evt_final_status = driver.find_element(By.XPATH, '//*[@id="sys_readonly.u_rim_event.state"]').get_attribute('value')
            if evt_final_status == '7':
                print(f'\033[32m{evt} encerrado com sucesso!\033[m\n')
                time.sleep(2)
            else:
                print(f'\033[31m[ERRO]: Não foi possível encerrar o {evt}!\033[m')
                print(f'\033[31mTente novamente ou encerre manualmente.\033[m\n')
                time.sleep(3)
                continue

        except:
            print(f'\033[31m[ERRO]: Não foi possível encerrar o {evt}!\033[m')
            print(f'\033[31mTente novamente ou encerre manualmente.\033[m\n')
            time.sleep(3)
            continue
                
driver.close()
driver.quit()
os.system("pause")