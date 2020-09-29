from dotenv import load_dotenv
load_dotenv()

import os
import shutil
from pathlib import Path
import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from helpers.captcha import reCaptchaSolver
from helpers.seleniumDriver import TemplateDriver
from helpers import util

import pandas as pd
import re
import numpy as np

import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests
from pymongo import MongoClient

UFS_AVAILABLE_NFCS = ['BA','SE','RS','RJ','PE','PA','RO','RN','PI','AL','AC','RR']
ufs = ['','BA','DF','ES','SE','RS','RJ','PE','PB','PA','MA','RO','RN','TO','PI','AL','AC','AP']
site_key_pattern = 'data-sitekey="(.+?)"'

def nfCodeFromSource(source_code):

    re_exps = [
        [r'chave: ([0-9]*)</body>', lambda x: x],
        [r'<chNFe>([0-9]*)</chNFe>', lambda x: x],
        [r'qrcode\?p=([0-9]*)\|', lambda x: x],
        [r'ConsultarNFCe\.aspx\?p=([0-9]*)\|', lambda x: x],
        [r'\/NFCE\/\?p=([0-9]*)\|', lambda x: x],
        [r'\/consultarNFCe.jsp\?p=([0-9]*)\|', lambda x: x],
        [r'\/qrcode.aspx\?p=([0-9]*)\|', lambda x: x],
        [r'\/NFCE-COM.aspx\?p=([0-9]*)\|', lambda x: x],
        [r'\/NFCEC_consulta_chave_acesso.aspx\?p=([0-9]*)\|', lambda x: x],
        [r'\/consultaNFCe/QRCode\?p=([0-9]*)\|', lambda x: x],
        [r'\/nfce/consulta\?p=([0-9]*)\|', lambda x: x],
        [r'\/nfce\?p=([0-9]*)\|', lambda x: x],
        [r'\/nfce/nfceForm.seam?p=([0-9]*)\|', lambda x: x],
        [r'\/NFCe/mDadosNFCe.aspx?p=([0-9]*)\|', lambda x: x],
        [r'\/consultarNFCe\?p=([0-9]*)\|', lambda x: x],
        [r'\/nfceForm.seam\?p=([0-9]*)\|', lambda x: x],
        [r'\/efetuarLoginCertificado\?p=([0-9]*)\|', lambda x: x],
        [r'\/NFeAutorizacao4.asmx\?p=([0-9]*)\|', lambda x: x],
        [r'\/NFeAutorizacao4.asmx\?p=([0-9]*)\|', lambda x: x],
        [r'<span id="lbl_cod_chave_acesso" style="display:inline-block;width:100%;">[\s]+([0-9\s]+)</span>', lambda x:  re.sub(r'\s', "", x)],
    ]

    codes = []
    re_types = []
    for i, re_exp in enumerate(re_exps):
        tmp_codes = re.findall(re_exp[0], source_code, flags=0)
        tmp_codes = [re_exp[1](x) for x in tmp_codes]
        codes += tmp_codes
        if len(tmp_codes) > 0: re_types.append(i)

    codes = list(set(codes))

    return codes, re_types


class NFEDriver(TemplateDriver):

    def saveNF(self, nf_code):

        source_code = self.driver.page_source
        with open('./NFEs/{}.html'.format(nf_code),'w') as f:
            f.write(source_code)


    def processNfeFromUrl(self, url, save_if_Available = True, tipo = None):

        try:
            if url[-4:] =='.pdf':
                return []
            else:
                r = requests.get(url, allow_redirects=True).text
                codes, re_types = nfCodeFromSource(r)

                if len(codes) > 1:
                    raise ValueError('Multiple nf codes found', codes, type_codes) 
                if len(codes) == 0:
                    raise ValueError('No nf codes found') 

                if codes[0][20:22] == '65' and util.ufCodetoShort(codes[0][:2]) in UFS_AVAILABLE_NFCS:
                    self.driver.get(url)
                    time.sleep(2)
                    self.saveNF(codes[0])
                
                return codes[0]

        except Exception as inst:
            print(inst, url)


    def getNFE(self, nfe_code):
        url = "http://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx?tipoConsulta=completa&tipoConteudo=XbSeqxE8pl8="
        self.driver.get(url)
        time.sleep(1)
        input_elem = self.driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_txtChaveAcessoResumo"]')
        input_elem.send_keys(nfe_code)
        site_key = re.search(site_key_pattern, self.driver.page_source).group(1)
        continue_button = self.driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_btnConsultar"]')

        if reCaptchaSolver(url,site_key, self.driver):
            self.driver.execute_script("arguments[0].click();", continue_button)
            time.sleep(self.delay_period)
            
            print_button = self.driver.find_element(By.XPATH,'//*[@title="Preparar documento para impressão"]')
            print_button.click()

            main_handle = self.driver.current_window_handle
            #get first child window
            chwnd = self.driver.window_handles
            for w in chwnd:
                #switch focus to child window
                if(w!=main_handle):
                    self.driver.switch_to.window(w)
                    break

            time.sleep(self.delay_period)
            self.saveNF(nfe_code)

            self.driver.close()
            self.driver.switch_to.window(main_handle)

        else:
            print('Captcha failed:{}'.format(nfe_code))

    def getNFCE_BA(self, nfce_code):
        url = "http://nfe.sefaz.ba.gov.br/servicos/nfce/modulos/geral/NFCEC_consulta_chave_acesso.aspx?p={}|2|1|4|CFD1A7D44FA81DB99D2F5151FD4E6F39DCA84B20".format(nfce_code)
        self.driver.get(url)
        time.sleep(1)
        self.saveNF(nfce_code)


    def getNFCE_SE(self, nfce_code):
        url = "http://www.nfce.se.gov.br/portal/consultarNFCe.jsp?p={}|2|1|2|1FD0BB8FED815DC16701B4567AF6B8F57F07F86C".format(nfce_code)
        self.driver.get(url)
        time.sleep(1)
        self.saveNF(nfce_code)



if __name__ == '__main__':
    nfe_driver = NFEDriver()
    client = MongoClient('mongodb://%s:%s@127.0.0.1/?authSource=admin' % (os.getenv("MONGO_INITDB_ROOT_USERNAME"), os.getenv("MONGO_INITDB_ROOT_PASSWORD")))
    db = client.cota_parlamentar
    col = db.despesas


    for row in col.find(
        {
            "descricao":'COMBUSTÍVEIS E LUBRIFICANTES.',
            #  "nfe_code": {"$exists": False}
        }
    ):
        row['nfe_code'] = nfe_driver.processNfeFromUrl(row['urlDocumento'], row['tipoDocumento'])
        print(row['nfe_code'])
        col.save(row)
    # nfe_driver = NFEDriver()
    # nfe_driver.getNFE('26200201199880000130550010000026731007307270')
    # nfe_driver.closeDriver()

# ano,cnpjCPF,codigoLegislatura,cpf,dataEmissao,descricao,descricaoEspecificacao,fornecedor,idDeputado,idDocumento,legislatura,lote,mes,nomeParlamentar,numero,numeroCarteiraParlamentar,numeroDeputadoID,numeroEspecificacaoSubCota,numeroSubCota,parcela,passageiro,ressarcimento,restituicao,siglaPartido,siglaUF,tipoDocumento,trecho,urlDocumento,valorDocumento,valorGlosa,valorLiquido
# 2020,011.998.800/0013-0 ,56,33155623420,2020-08-03T00:00:00,COMBUSTÍVEIS E LUBRIFICANTES.,Veículos Automotores,POSTO LUPP LTDA,160665,7083847,2019,1711931,7,Augusto Coutinho,3159  ,141,2236,1,3,0,,,,SOLIDARIEDADE,PE,4,,http://camara.leg.br/cota-parlamentar/nota-fiscal-eletronica?ideDocumentoFiscal=7083847,1448.9,0,1448.9
# 2020,070.233.950/0019-7 ,56,24263630530,2020-05-05T00:00:00,COMBUSTÍVEIS E LUBRIFICANTES.,Veículos Automotores,AUTO POSTO PREC,160666,7052281,2019,1695155,5,Félix Mendonça r,290124,195,2307,1,3,0,,,,PDT,BA,          4,,http://camara.leg.br/cota-parlamentar/nota-fiscal-eletronica?ideDocumentoFiscal=7052281,206.05,0,206.05
