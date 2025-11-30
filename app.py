from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import POOtrab as db

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Permite requisições do frontend

# Inicializar banco de dados na primeira execução
db.criar_tabelas()
db.inserir_questoes()

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
    
    try:
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return jsonify({'sucesso': True, 'mensagem': 'Cadastro realizado com sucesso!'})
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário já existe! Escolha outro nome.'}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    usuario = data.get('usuario', '').strip()
    senha = data.get('senha', '').strip()
    
    if not usuario or not senha:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário e senha são obrigatórios!'}), 400
    
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return jsonify({'sucesso': True, 'user_id': resultado[0], 'usuario': usuario})
    else:
        return jsonify({'sucesso': False, 'mensagem': 'Usuário ou senha inválidos!'}), 401

@app.route('/api/gerar-quiz', methods=['POST'])
def api_gerar_quiz():
    data = request.json or {}
    nivel = data.get('nivel', None)
    
    quiz = db.gerar_quiz(nivel)
    
    # Remover resposta correta antes de enviar 
    # A resposta será verificada via API separada
    quiz_seguro = []
    for q in quiz:
        questao_data = {
            'id': q['id'],
            'pergunta': q['pergunta'],
            'alternativaA': q['alternativaA'],
            'alternativaB': q['alternativaB'],
            'alternativaC': q['alternativaC'],
            'alternativaD': q['alternativaD'],
            'nivel': q['nivel']
            
        }
        quiz_seguro.append(questao_data)
    
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
    
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT correta FROM questoes WHERE id=?", (questao_id,))
    resultado = cursor.fetchone()
    conn.close()
    
    if not resultado:
        return jsonify({'sucesso': False, 'mensagem': 'Questão não encontrada!'}), 404
    
    correta = resultado[0]
    acertou = resposta == correta
    
    return jsonify({
        'sucesso': True,
        'acertou': acertou,
        'resposta_correta': correta
    })

@app.route('/api/submeter-quiz', methods=['POST'])
def api_submeter_quiz():
    data = request.json
    user_id = data.get('user_id')
    respostas = data.get('respostas', [])  # [{questao_id, resposta}, ...]
    
    if not user_id or not respostas:
        return jsonify({'sucesso': False, 'mensagem': 'Dados inválidos!'}), 400
    
    try:
        user_id = int(user_id)
    except:
        return jsonify({'sucesso': False, 'mensagem': 'ID de usuário inválido!'}), 400
    
    # Verificar respostas
    conn = db.conectar()
    cursor = conn.cursor()
    acertos = 0
    total = len(respostas)
    
    for resp in respostas:
        questao_id = resp.get('questao_id')
        resposta_usuario = resp.get('resposta', '').strip().upper()
        
        try:
            questao_id = int(questao_id)
        except:
            continue
        
        cursor.execute("SELECT correta FROM questoes WHERE id=?", (questao_id,))
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] == resposta_usuario:
            acertos += 1
    
    # Salvar resultado
    nota = acertos
    cursor.execute("INSERT INTO resultados (usuario_id, nota) VALUES (?, ?)", (user_id, nota))
    conn.commit()
    conn.close()
    
    porcentagem = (acertos / total * 100) if total > 0 else 0
    
    # Determinar rank
    if porcentagem >= 80:
        rank = "Desenvolvedor Senior"
    elif porcentagem >= 60:
        rank = "Desenvolvedor Pleno"
    else:
        rank = "Desenvolvedor Junior"
    
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
    
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_testes,
            AVG(nota) as media,
            MAX(nota) as melhor_nota,
            MIN(nota) as pior_nota
        FROM resultados 
        WHERE usuario_id=?
    """, (user_id,))
    
    resultado = cursor.fetchone()
    conn.close()
    
    if not resultado or resultado[0] == 0:
        return jsonify({
            'sucesso': True,
            'total_testes': 0,
            'media': 0,
            'melhor_nota': 0,
            'pior_nota': 0
        })
    
    return jsonify({
        'sucesso': True,
        'total_testes': resultado[0],
        'media': round(resultado[1] or 0, 1),
        'melhor_nota': resultado[2] or 0,
        'pior_nota': resultado[3] or 0
    })

if __name__ == '__main__':
    print("Servidor Flask iniciado!")
    print("http://localhost:5000")
    app.run(debug=True, port=5000)

