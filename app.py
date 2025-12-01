from flask import Flask, request, jsonify, send_from_directory # Importa componentes do framework Flask
from flask_cors import CORS # Importa extensão para manipular CORS (Cross-Origin Resource Sharing)
from models import DatabaseManager, Usuario, Quiz, Resultado, Questao # Importa as classes definidas no arquivo models.py

# -----------------------------------
# ANTES DA CONFIGURAÇÃO GLOBAL (Tratado como Classe/App)
# -----------------------------------
# Nome da Aplicação (Script)
#
# Função da Aplicação
# -> Configurar o servidor web Flask
# -> Definir as rotas da API (endpoints)
# -> Gerenciar a conexão global com o banco de dados
# -> Objetos instanciados: Flask, DatabaseManager
# -----------------------------------

# -----------------------------------
# ANTES DOS ATRIBUTOS GLOBAIS
# -----------------------------------
# app: Instância principal da aplicação Flask
# db_manager: Instância responsável por gerenciar a conexão e criação do banco de dados
# -----------------------------------

app = Flask(__name__, static_folder='.', static_url_path='') # Inicializa a aplicação Flask servindo arquivos estáticos da pasta atual
CORS(app) # Habilita CORS para permitir requisições de outras origens

db_manager = DatabaseManager() # Instancia o gerenciador de banco de dados
db_manager.criar_tabelas() # Cria as tabelas necessárias se não existirem
db_manager.inserir_questoes() # Insere questões padrão no banco se estiver vazio

# -----------------------------------
# ROTAS DA API
# -----------------------------------

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: index
#
# Para que serve: Servir a página inicial (Frontend) da aplicação
#
# Parâmetros de entrada: Nenhum
#
# Retorno do método: 
# -> Arquivo HTML (index.html) para ser renderizado pelo navegador
# -----------------------------------
@app.route('/') # Define a rota raiz da aplicação
def index():
    return send_from_directory('.', 'index.html') # Retorna o arquivo index.html localizado no diretório atual

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: api_cadastrar
#
# Para que serve: Receber dados para registrar um novo usuário no banco de dados
#
# Parâmetros de entrada (via JSON):
# -> usuario: Nome de usuário desejado
# -> senha: Senha do usuário
# -> confirma_senha: Confirmação da senha para validação
#
# Retorno do método: 
# -> JSON: Objeto contendo 'sucesso' (bool) e 'mensagem' (str)
# -----------------------------------
@app.route('/api/cadastrar', methods=['POST']) # Define rota POST para cadastro
def api_cadastrar():
    data = request.json # Obtém o JSON enviado no corpo da requisição
    usuario = data.get('usuario', '').strip() # Extrai o usuário e remove espaços em branco
    senha = data.get('senha', '').strip() # Extrai a senha e remove espaços em branco
    confirma_senha = data.get('confirma_senha', '').strip() # Extrai a confirmação de senha
    
    if not usuario or not senha: # Verifica se campos obrigatórios estão vazios
        return jsonify({'sucesso': False, 'mensagem': 'Usuário e senha são obrigatórios!'}), 400 # Retorna erro 400 se faltar dados
    
    if senha != confirma_senha: # Verifica se as senhas são iguais
        return jsonify({'sucesso': False, 'mensagem': 'As senhas não coincidem!'}), 400 # Retorna erro 400 se senhas divergirem
    
    user = Usuario(db_manager) # Instancia objeto Usuario passando o gerenciador de DB
    if user.cadastrar(usuario, senha): # Tenta cadastrar o usuário no banco
        return jsonify({'sucesso': True, 'mensagem': 'Cadastro realizado com sucesso!'}) # Retorna sucesso se cadastrou
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário já existe! Escolha outro nome.'}), 400 # Retorna erro se usuário já existir

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: api_login
#
# Para que serve: Autenticar um usuário existente
#
# Parâmetros de entrada (via JSON):
# -> usuario: Nome de usuário
# -> senha: Senha para conferência
#
# Retorno do método:
# -> JSON: Contém 'sucesso', 'user_id' e 'usuario' em caso de êxito, ou mensagem de erro
# -----------------------------------
@app.route('/api/login', methods=['POST']) # Define rota POST para login
def api_login():
    data = request.json # Obtém o JSON do corpo da requisição
    usuario = data.get('usuario', '').strip() # Extrai e limpa o nome de usuário
    senha = data.get('senha', '').strip() # Extrai e limpa a senha
    
    if not usuario or not senha: # Verifica se campos estão preenchidos
        return jsonify({'sucesso': False, 'mensagem': 'Usuário e senha são obrigatórios!'}), 400 # Retorna erro se vazios
    
    user = Usuario(db_manager) # Instancia objeto Usuario
    user_id = user.login(usuario, senha) # Chama método de login e recebe o ID (ou None)
    
    if user_id: # Se user_id for válido (login correto)
        return jsonify({'sucesso': True, 'user_id': user_id, 'usuario': usuario}) # Retorna dados do usuário e sucesso
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário ou senha inválidos!'}), 401 # Retorna erro 401 (Não autorizado)

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: api_gerar_quiz
#
# Para que serve: Gerar e retornar uma lista de questões para o jogo
#
# Parâmetros de entrada (via JSON):
# -> nivel: (Opcional) Filtro de dificuldade das questões
#
# Retorno do método:
# -> JSON: Lista de dicionários contendo as questões (sem a resposta correta revelada)
# -----------------------------------
@app.route('/api/gerar-quiz', methods=['POST']) # Define rota POST para criar o quiz
def api_gerar_quiz():
    data = request.json or {} # Obtém JSON ou dicionário vazio se nulo
    nivel = data.get('nivel', None) # Obtém o nível selecionado (pode ser None)
    
    quiz = Quiz(db_manager) # Instancia objeto Quiz
    quiz.gerar(nivel) # Gera as questões baseadas no nível
    quiz_seguro = quiz.to_dict_list(incluir_resposta=False) # Converte para lista ocultando respostas corretas
    
    return jsonify({'sucesso': True, 'quiz': quiz_seguro}) # Retorna o quiz em formato JSON

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: api_verificar_resposta
#
# Para que serve: Validar imediatamente se uma única resposta está correta
#
# Parâmetros de entrada (via JSON):
# -> questao_id: ID da questão a ser verificada
# -> resposta: A alternativa escolhida pelo usuário (A, B, C ou D)
#
# Retorno do método:
# -> JSON: Boolean 'acertou' e a 'resposta_correta' para feedback visual
# -----------------------------------
@app.route('/api/verificar-resposta', methods=['POST']) # Define rota POST para checagem individual
def api_verificar_resposta():
    data = request.json # Obtém dados da requisição
    questao_id = data.get('questao_id') # Extrai o ID da questão
    resposta = data.get('resposta', '').strip().upper() # Extrai a resposta, limpa e converte para maiúscula
    
    if not questao_id or not resposta: # Valida se dados existem
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos!'}), 400 # Retorna erro se dados inválidos
    
    try:
        questao_id = int(questao_id) # Tenta converter ID para inteiro
    except:
        return jsonify({'sucesso': False, 'mensagem': 'ID de questão inválido!'}), 400 # Erro se ID não for número
    
    db = db_manager.conectar() # Abre conexão com banco de dados
    cursor = db.cursor() # Cria cursor para comandos SQL
    cursor.execute("SELECT correta FROM questoes WHERE id=?", (questao_id,)) # Busca a resposta correta pelo ID
    resultado = cursor.fetchone() # Pega o primeiro resultado encontrado
    db.close() # Fecha a conexão com o banco
    
    if not resultado: # Se não achou a questão
        return jsonify({'sucesso': False, 'mensagem': 'Questão não encontrada!'}), 404 # Retorna erro 404
    
    correta = resultado[0] # Extrai a letra correta da tupla
    questao = Questao(correta=correta) # Cria objeto Questão temporário com a resposta certa
    acertou = questao.verificar_resposta(resposta) # Verifica se a resposta do usuário bate com a correta
    
    # Retorna o resultado da verificação
    return jsonify({
        'sucesso': True,
        'acertou': acertou,
        'resposta_correta': correta
    })

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: api_submeter_quiz
#
# Para que serve: Processar todas as respostas ao final do jogo, calcular nota e salvar histórico
#
# Parâmetros de entrada (via JSON):
# -> user_id: ID do usuário que jogou
# -> respostas: Lista contendo objetos com 'questao_id' e a resposta dada
#
# Retorno do método:
# -> JSON: Estatísticas da partida (acertos, nota, porcentagem, rank)
# -----------------------------------
@app.route('/api/submeter-quiz', methods=['POST']) # Rota para submissão final
def api_submeter_quiz():
    data = request.json # Recebe dados
    user_id = data.get('user_id') # Pega ID do usuário
    respostas = data.get('respostas', []) # Pega lista de respostas
    
    if not user_id or not respostas: # Valida dados
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos!'}), 400 # Retorna erro
    
    try:
        user_id = int(user_id) # Garante que ID é inteiro
    except:
        return jsonify({'sucesso': False, 'mensagem': 'ID de usuário inválido!'}), 400 # Erro de conversão
    
    db = db_manager.conectar() # Conecta ao banco
    cursor = db.cursor() # Cria cursor
    
    # Monta query dinâmica SQL com placeholders (?) baseada na quantidade de respostas recebidas
    cursor.execute("SELECT * FROM questoes WHERE id IN ({})".format(','.join(['?'] * len(respostas))), 
                   [r.get('questao_id') for r in respostas]) # Executa busca das questões respondidas
    questoes_db = cursor.fetchall() # Recupera todas as questões do banco
    db.close() # Fecha conexão
    
    quiz = Quiz(db_manager) # Instancia objeto Quiz
    for q in questoes_db: # Itera sobre as questões vindas do banco
        # Reconstrói objetos Questao com dados do banco
        questao = Questao(
            questao_id=q[0],
            pergunta=q[1],
            alternativa_a=q[2],
            alternativa_b=q[3],
            alternativa_c=q[4],
            alternativa_d=q[5],
            correta=q[6],
            nivel=q[7]
        )
        quiz.questoes.append(questao) # Adiciona questão à lista do quiz
    
    acertos, total = quiz.calcular_resultado(respostas) # Calcula total de acertos comparando com gabarito
    nota = acertos # Define a nota como número de acertos
    porcentagem = (acertos / total * 100) if total > 0 else 0 # Calcula porcentagem de acerto protegendo contra divisão por zero
    
    resultado = Resultado(db_manager) # Instancia objeto Resultado
    resultado.salvar(user_id, nota) # Salva o resultado no banco
    rank = resultado.calcular_rank(porcentagem) # Calcula o rank baseado na porcentagem
    
    # Retorna JSON com os dados da performance
    return jsonify({
        'sucesso': True,
        'acertos': acertos,
        'total': total,
        'nota': nota,
        'porcentagem': round(porcentagem, 1),
        'rank': rank
    })

# -----------------------------------
# ANTES DE CADA MÉTODO (ROTA)
# -----------------------------------
# Nome do método: api_estatisticas
#
# Para que serve: Obter o histórico de desempenho de um usuário específico
#
# Parâmetros de entrada (via Query String):
# -> user_id: ID do usuário para busca
#
# Retorno do método:
# -> JSON: Estatísticas agregadas (média, total de testes, melhor/pior nota)
# -----------------------------------
@app.route('/api/estatisticas', methods=['GET']) # Rota GET para estatísticas
def api_estatisticas():
    user_id = request.args.get('user_id', type=int) # Obtém user_id da URL convertendo para int
    
    if not user_id: # Se user_id não foi passado
        return jsonify({'sucesso': False, 'mensagem': 'user_id é obrigatório!'}), 400 # Retorna erro
    
    resultado = Resultado(db_manager) # Instancia objeto Resultado
    stats = resultado.obter_estatisticas(user_id) # Busca estatísticas no banco
    
    # Retorna JSON com os dados estatísticos
    return jsonify({
        'sucesso': True,
        'total_testes': stats['total_testes'],
        'media': stats['media'],
        'melhor_nota': stats['melhor_nota'],
        'pior_nota': stats['pior_nota']
    })

# -----------------------------------
# FUNÇÃO MAIN
# -----------------------------------
# Nome da função: Main Block (if __name__ == '__main__')
#
# -> Verifica se o script está sendo executado diretamente
# -> Inicia o servidor de desenvolvimento do Flask na porta 5000
# -----------------------------------
if __name__ == '__main__':
    print("Servidor Flask iniciado!") # Imprime mensagem no console
    print("http://localhost:5000") # Imprime URL de acesso
    app.run(debug=True, port=5000) # Inicia o servidor Flask em modo debug na porta 5000