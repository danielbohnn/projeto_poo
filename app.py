from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import DatabaseManager, Usuario, Quiz, Resultado, Questao

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

db_manager = DatabaseManager()
db_manager.criar_tabelas()
db_manager.inserir_questoes()

# -----------------------------------
# ROTAS DA API
# -----------------------------------

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/cadastrar', methods=['POST'])
def api_cadastrar():
    data = request.json
    usuario = data.get('usuario', '').strip()
    senha = data.get('senha', '').strip()
    confirma_senha = data.get('confirma_senha', '').strip()
    
    if not usuario or not senha:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário e senha são obrigatórios!'}), 400
    
    if senha != confirma_senha:
        return jsonify({'sucesso': False, 'mensagem': 'As senhas não coincidem!'}), 400
    
    user = Usuario(db_manager)
    if user.cadastrar(usuario, senha):
        return jsonify({'sucesso': True, 'mensagem': 'Cadastro realizado com sucesso!'})
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário já existe! Escolha outro nome.'}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    usuario = data.get('usuario', '').strip()
    senha = data.get('senha', '').strip()
    
    if not usuario or not senha:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário e senha são obrigatórios!'}), 400
    
    user = Usuario(db_manager)
    user_id = user.login(usuario, senha)
    
    if user_id:
        return jsonify({'sucesso': True, 'user_id': user_id, 'usuario': usuario})
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário ou senha inválidos!'}), 401

@app.route('/api/gerar-quiz', methods=['POST'])
def api_gerar_quiz():
    data = request.json or {}
    nivel = data.get('nivel', None)
    
    quiz = Quiz(db_manager)
    quiz.gerar(nivel)
    quiz_seguro = quiz.to_dict_list(incluir_resposta=False)
    
    return jsonify({'sucesso': True, 'quiz': quiz_seguro})

@app.route('/api/verificar-resposta', methods=['POST'])
def api_verificar_resposta():
    data = request.json
    questao_id = data.get('questao_id')
    resposta = data.get('resposta', '').strip().upper()
    
    if not questao_id or not resposta:
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos!'}), 400
    
    try:
        questao_id = int(questao_id)
    except:
        return jsonify({'sucesso': False, 'mensagem': 'ID de questão inválido!'}), 400
    
    db = db_manager.conectar()
    cursor = db.cursor()
    cursor.execute("SELECT correta FROM questoes WHERE id=?", (questao_id,))
    resultado = cursor.fetchone()
    db.close()
    
    if not resultado:
        return jsonify({'sucesso': False, 'mensagem': 'Questão não encontrada!'}), 404
    
    correta = resultado[0]
    questao = Questao(correta=correta)
    acertou = questao.verificar_resposta(resposta)
    
    return jsonify({
        'sucesso': True,
        'acertou': acertou,
        'resposta_correta': correta
    })

@app.route('/api/submeter-quiz', methods=['POST'])
def api_submeter_quiz():
    data = request.json
    user_id = data.get('user_id')
    respostas = data.get('respostas', [])
    
    if not user_id or not respostas:
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos!'}), 400
    
    try:
        user_id = int(user_id)
    except:
        return jsonify({'sucesso': False, 'mensagem': 'ID de usuário inválido!'}), 400
    
    db = db_manager.conectar()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM questoes WHERE id IN ({})".format(','.join(['?'] * len(respostas))), 
                   [r.get('questao_id') for r in respostas])
    questoes_db = cursor.fetchall()
    db.close()
    
    quiz = Quiz(db_manager)
    for q in questoes_db:
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
        quiz.questoes.append(questao)
    
    acertos, total = quiz.calcular_resultado(respostas)
    nota = acertos
    porcentagem = (acertos / total * 100) if total > 0 else 0
    
    resultado = Resultado(db_manager)
    resultado.salvar(user_id, nota)
    rank = resultado.calcular_rank(porcentagem)
    
    return jsonify({
        'sucesso': True,
        'acertos': acertos,
        'total': total,
        'nota': nota,
        'porcentagem': round(porcentagem, 1),
        'rank': rank
    })

@app.route('/api/estatisticas', methods=['GET'])
def api_estatisticas():
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({'sucesso': False, 'mensagem': 'user_id é obrigatório!'}), 400
    
    resultado = Resultado(db_manager)
    stats = resultado.obter_estatisticas(user_id)
    
    return jsonify({
        'sucesso': True,
        'total_testes': stats['total_testes'],
        'media': stats['media'],
        'melhor_nota': stats['melhor_nota'],
        'pior_nota': stats['pior_nota']
    })

if __name__ == '__main__':
    print("Servidor Flask iniciado!")
    print("http://localhost:5000")
    app.run(debug=True, port=5000)

