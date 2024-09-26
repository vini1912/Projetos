from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Adicione uma chave secreta para mensagens

def get_alunos():
    """Lê os alunos do arquivo e retorna como uma lista de dicionários."""
    alunos = []
    caminho_arquivo = 'alunos.txt'
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            for aluno in arquivo:
                item = aluno.strip().split(';')
                if len(item) == 3:  # Espera ID, nome e IMC
                    alunos.append({
                        'id': item[0],
                        'nome': item[1],
                        'imc': item[2]
                    })
    except FileNotFoundError:
        pass
    return alunos

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar_aluno", methods=['POST'])
def cadastrar_aluno():
    try:
        nome_aluno = request.form["nome_aluno"]
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])

        # Calcula o IMC
        imc = peso / (altura ** 2)

        caminho_arquivo = 'alunos.txt'
        alunos = get_alunos()
        novo_id = str(len(alunos) + 1)  # Gera um novo ID

        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{novo_id};{nome_aluno};{imc:.2f}\n")  # Armazena ID, nome e IMC

        flash("Aluno cadastrado com sucesso!")
        return redirect("/consulta")

    except ValueError:
        flash("Erro: Insira valores válidos para peso e altura.")
        return redirect("/")

@app.route("/consulta")
def consultar_alunos():
    alunos = get_alunos()
    return render_template("consulta_alunos.html", alunos=alunos)

@app.route("/deletar_aluno", methods=['POST'])
def deletar_aluno():
    aluno_id = request.form.get("aluno_id")  # Use get para evitar KeyError
    if aluno_id is None:
        flash("Erro: ID do aluno não fornecido.")
        return redirect("/consulta")

    caminho_arquivo = 'alunos.txt'
    alunos = get_alunos()
    alunos_filtrados = [aluno for aluno in alunos if aluno['id'] != aluno_id]

    with open(caminho_arquivo, 'w') as arquivo:
        for aluno in alunos_filtrados:
            arquivo.write(f"{aluno['id']};{aluno['nome']};{aluno['imc']}\n")

    flash("Aluno deletado com sucesso!")
    return redirect("/consulta")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)