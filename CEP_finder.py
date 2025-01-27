import pandas as pd
import requests
def reconhecer_uf(estado):
    estados_ufs = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO"
    }

    return estados_ufs.get(estado, "Estado não encontrado")
info = input("Digite o nome do seu estado, a sua cidade e seu endereço(rua), separados por vírgula: ")
infos = [i.strip() for i in info.split(",")]
estado, cidade, endereco = infos   
uf = reconhecer_uf(estado)
if uf == "Estado não encontrado":
    print("Estado não encontrado, tente novamente.")
else:
    link = f"https://viacep.com.br/ws/{uf}/{cidade}/{endereco}/json/"
    req = requests.get(link)
    dados = req.json()
    tab = pd.DataFrame(dados)
    traducao_colunas = {
        "endereço": "logradouro",
        "cidade": "localidade",
        "cep": "cep",
        "bairro": "bairro",
        "uf": "uf",
        "estado": "uf"
    }
    parcela = input("Deseja ver seu CEP por inteiro? Digite s/n: ")
    if parcela == "s":
        print(tab)
    elif parcela == "n":
        espec = input("Digite as informações desejadas:")
        coluna_usuario = [i.strip() for i in espec.split(",")]
        colunas_traduzidas = [traducao_colunas.get(coluna.lower(), coluna) for coluna in coluna_usuario]
        colunas_validas = [col for col in colunas_traduzidas if col in tab.columns]
        if colunas_validas:
            print(tab[colunas_validas])
        else:
            print("Nenhuma coluna válida. Tente novamente")
    else:
        print("Opção inválida, digite somente s/n.")

#fazer um dicionario p 