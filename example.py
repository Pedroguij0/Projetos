state = str(input("Digite o nome do seu estado"))
def reconhecer_uf(estado):
    estados_ufs = {
        "Bahia": "BA",
        "São Paulo": "SP",
        "Rio de Janeiro": "RJ",
        "Minas Gerais": "MG",
        "Paraná": "PR",
        "Rio Grande do Sul": "RS",
        "Santa Catarina": "SC",
        "Ceará": "CE",
        "Pernambuco": "PE",
    }

    return estados_ufs.get(estado, "Estado não encontrado")  # Retorna o UF ou uma mensagem padrão


print(reconhecer_uf(state))
