from flask import Flask, render_template, request, redirect  # Importa as bibliotecas necessárias do Flask

app = Flask(__name__)  # Cria uma instância da aplicação Flask

@app.route("/")  # Define a rota para a página inicial
def index():
    return render_template("index.html")  # Renderiza o template index.html

@app.route("/cadastrar_aluno", methods=['POST'])  # Define a rota para cadastrar alunos, aceita apenas métodos POST
def cadastrar_aluno():
    nome_aluno = request.form["nome_aluno"]  # Obtém o nome do aluno do formulário
    notas = [
        float(request.form["nota1"]),  # Obtém a primeira nota
        float(request.form["nota2"]),  # Obtém a segunda nota
        float(request.form["nota3"]),  # Obtém a terceira nota
        float(request.form["nota4"])   # Obtém a quarta nota
    ]
    media = sum(notas) / len(notas)  # Calcula a média das notas

    caminho_arquivo = 'alunos.txt'  # Define o caminho do arquivo onde os dados dos alunos serão armazenados

    with open(caminho_arquivo, 'a') as arquivo:  # Abre o arquivo em modo de anexar
        arquivo.write(f"{nome_aluno};{media:.2f}\n")  # Escreve o nome e a média do aluno no arquivo

    return redirect("/consulta")  # Redireciona para a página de consulta após o cadastro

@app.route("/consulta")  # Define a rota para consultar alunos
def consultar_alunos():
    alunos = []  # Lista para armazenar os alunos
    caminho_arquivo = 'alunos.txt'  # Caminho do arquivo com os dados dos alunos

    try:
        with open(caminho_arquivo, 'r') as arquivo:  # Tenta abrir o arquivo em modo de leitura
            for aluno in arquivo:  # Para cada linha no arquivo
                item = aluno.strip().split(';')  # Remove espaços em branco e divide a linha em nome e média
                alunos.append({
                    'nome': item[0],  # Adiciona o nome do aluno ao dicionário
                    'media': item[1]  # Adiciona a média do aluno ao dicionário
                })
    except FileNotFoundError:  # Caso o arquivo não exista
        pass  # Ignora o erro

    return render_template("consulta_alunos.html", alunos=alunos)  # Renderiza o template de consulta passando a lista de alunos

@app.route("/deletar_aluno", methods=['POST'])  # Define a rota para deletar um aluno, aceita apenas métodos POST
def deletar_aluno():
    nome_aluno = request.form["nome_aluno"]  # Obtém o nome do aluno a ser deletado do formulário
    caminho_arquivo = 'alunos.txt'  # Caminho do arquivo com os dados dos alunos

    alunos = []  # Lista para armazenar os alunos restantes
    try:
        with open(caminho_arquivo, 'r') as arquivo:  # Tenta abrir o arquivo em modo de leitura
            for aluno in arquivo:  # Para cada linha no arquivo
                item = aluno.strip().split(';')  # Remove espaços em branco e divide a linha em nome e média
                if item[0] != nome_aluno:  # Se o aluno não for o que deseja deletar
                    alunos.append(aluno.strip())  # Adiciona à lista de alunos restantes
    except FileNotFoundError:  # Caso o arquivo não exista
        pass  # Ignora o erro

    with open(caminho_arquivo, 'w') as arquivo:  # Abre o arquivo em modo de escrita (sobrescreve)
        for aluno in alunos:  # Para cada aluno restante
            arquivo.write(f"{aluno}\n")  # Escreve no arquivo

    return redirect("/consulta")  # Redireciona para a página de consulta após a exclusão

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    app.run(host='127.0.0.1', port=80, debug=True)  # Inicia a aplicação Flask em modo de debug
