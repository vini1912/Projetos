from flask import Flask, render_template, redirect, request
import requests  # Importação correta de requests

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    # Verifica se a requisição é do tipo POST
    if request.method == 'POST':
        # Obtém os valores das entradas do formulário
        moeda_real = request.form.get("real")
        moeda_dolar = request.form.get("dolar")
        cotacao = request.form.get("cotacao")

        # Faz uma requisição para obter a cotação atual do USD para BRL
        requisicao = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        cotacao_api = requisicao.json()

        # Converte as entradas para float, se não forem fornecidas, usa 0
        moeda_real = float(moeda_real) if moeda_real else 0
        moeda_dolar = float(moeda_dolar) if moeda_dolar else 0
        # Se não houver cotação informada, utiliza a da API
        cotacao = float(cotacao) if cotacao else float(cotacao_api['USD']['bid'])

        # Calcula o valor da moeda real ou dólar baseado no que foi fornecido
        if moeda_real == 0:
            moeda_real = moeda_dolar * cotacao
        elif moeda_dolar == 0:
            moeda_dolar = moeda_real / cotacao

        # Renderiza o template com os resultados calculados
        return render_template("index.html", moeda_real=str(moeda_real),
                               moeda_dolar=str(moeda_dolar), 
                               cotacao=str(cotacao))
    else:
        # Se a requisição não for POST, renderiza o template vazio
        return render_template("index.html")

@app.route("/teste")
def teste():
    # Renderiza o template de teste
    return render_template("teste.html")

if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run("127.0.0.1", port=80, debug=True)
