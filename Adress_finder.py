import requests
cep = input("Digite o seu número de CEP:\n")
parcela = input("Deseja ver seu CEP por inteiro? s/n\n")
link = f"https://viacep.com.br/ws/{cep}/json/"
cep = cep.replace(" ", "").replace("-", "").replace(".", "")
req = requests.get(link)
dados = req.json()

if parcela.lower() == "s" :
    print(dados)

elif parcela.lower() == "n":
    info = str(input("Digite as informações que deseja consultar:\n"))
    infos = [i.strip() for i in info.split(",")]
    busca = []
    nao_encontradas = []
    for i in infos :
        if i in dados:
            busca[i] = dados[i]
        else:
            nao_encontradas.append(i)
    for chave, valor in busca.items():
        print(f"{chave}: {valor}")

    if nao_encontradas:
        print("As informaçãoes inseridas não são válidas")
        for i in nao_encontradas:
            print(f"-{i}")
else:
    print("Opção inválida. Por favor, digite s para ver o CEP inteiro ou n para consultar uma informação específica.")


