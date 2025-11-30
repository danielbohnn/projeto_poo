import sqlite3
import random
from pathlib import Path

# -----------------------------------
# CONFIGURAÇÃO DO BANCO DE DADOS
# -----------------------------------
DB_PATH = "quizcode.db"

def conectar():
    return sqlite3.connect(DB_PATH)

# -----------------------------------
# CRIAÇÃO DAS TABELAS
# -----------------------------------
def criar_tabelas():
    db = conectar()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT NOT NULL,
            alternativaA TEXT,
            alternativaB TEXT,
            alternativaC TEXT,
            alternativaD TEXT,
            correta TEXT,
            nivel TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nota INTEGER,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    db.commit()
    db.close()

# -----------------------------------
# POPULAR BANCO COM 100 QUESTÕES
# -----------------------------------
def inserir_questoes():
    db = conectar()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM questoes")
    qtd = cursor.fetchone()[0]

    if qtd > 0:
        db.close()
        return

    questoes = [
        # BÁSICO (40 questões)
        ("Qual comando imprime algo na tela em Python?", "echo()", "print()", "mostrar()", "display()", "B", "basico"),
        ("Qual operador cria comentários em Python?", "//", "<!-- -->", "#", "/**/", "C", "basico"),
        ("Qual tipo representa números inteiros?", "int", "float", "real", "decimal", "A", "basico"),
        ("Como criar uma variável em Python?", "var x = 10", "x = 10", "int x = 10", "declare x = 10", "B", "basico"),
        ("Qual o resultado de: 10 // 3?", "3.33", "3", "4", "3.0", "B", "basico"),
        ("Como criar uma string em Python?", "string = 'texto'", "Todas as alternativas", "string = \"texto\"", "string = '''texto'''", "B", "basico"),
        ("Qual palavra-chave define uma função?", "function", "def", "func", "define", "B", "basico"),
        ("Como criar uma lista vazia?", "lista = []", "lista = ()", "lista = {}", "lista = list", "A", "basico"),
        ("Qual método adiciona um item ao final de uma lista?", "add()", "append()", "insert()", "push()", "B", "basico"),
        ("Como verificar o tipo de uma variável?", "typeof()", "type()", "checktype()", "vartype()", "B", "basico"),
        ("Qual operador verifica igualdade?", "=", "==", "===", "equals", "B", "basico"),
        ("Como criar um loop for que itera de 0 a 4?", "for i in range(5)", "for i in 0..4", "for i = 0 to 4", "for i in [0,4]", "A", "basico"),
        ("Qual palavra-chave inicia uma condição?", "if", "when", "condition", "check", "A", "basico"),
        ("Como converter string para inteiro?", "int()", "toInt()", "parseInt()", "str2int()", "A", "basico"),
        ("Qual o resultado de: len([1,2,3])?", "2", "3", "4", "Erro", "B", "basico"),
        ("Como criar um dicionário vazio?", "dict = []", "dict = ()", "dict = {}", "dict = dict()", "C", "basico"),
        ("Qual palavra-chave é usada para importar módulos?", "include", "import", "require", "using", "B", "basico"),
        ("Como escrever um loop infinito?", "while True:", "loop forever:", "while 1:", "A e C estão corretas", "D", "basico"),
        ("Qual método remove o último item de uma lista?", "remove()", "delete()", "pop()", "drop()", "C", "basico"),
        ("Como verificar se uma chave existe em um dicionário?", "key in dict", "dict.has(key)", "dict.contains(key)", "key.exists(dict)", "A", "basico"),
        ("Qual o resultado de: 'python'[0]?", "python", "p", "y", "Erro", "B", "basico"),
        ("Como concatenar strings?", "'a' + 'b'", "'a'.concat('b')", "concat('a','b')", "join('a','b')", "A", "basico"),
        ("Qual palavra-chave interrompe um loop?", "stop", "break", "exit", "end", "B", "basico"),
        ("Como criar uma tupla?", "tupla = []", "tupla = ()", "tupla = {}", "tupla = tuple", "B", "basico"),
        ("Qual o resultado de: bool(0)?", "True", "False", "0", "Erro", "B", "basico"),
        ("Como pegar entrada do usuário?", "input()", "get()", "read()", "scan()", "A", "basico"),
        ("Qual operador para 'e' lógico?", "&&", "and", "&", "AND", "B", "basico"),
        ("Como arredondar um número?", "round()", "ceil()", "floor()", "int()", "A", "basico"),
        ("Qual o resultado de: 'ABC'.lower()?", "ABC", "abc", "Abc", "aBc", "B", "basico"),
        ("Como dividir uma string?", "split()", "divide()", "separate()", "break()", "A", "basico"),
        ("Qual palavra-chave pula para próxima iteração?", "skip", "next", "continue", "pass", "C", "basico"),
        ("Como criar um set vazio?", "set = {}", "set = set()", "set = []", "set = ()", "B", "basico"),
        ("Qual o resultado de: 2 ** 3?", "5", "6", "8", "9", "C", "basico"),
        ("Como verificar o tamanho de uma string?", "len()", "size()", "length()", "count()", "A", "basico"),
        ("Qual palavra-chave define uma classe?", "class", "struct", "object", "type", "A", "basico"),
        ("Como criar uma lista de 0 a 9?", "list(range(10))", "[0:9]", "list(0,9)", "range[10]", "A", "basico"),
        ("Qual o resultado de: 10 % 3?", "3", "1", "0", "10", "B", "basico"),
        ("Como verificar se lista está vazia?", "if not lista:", "if lista == []:", "if len(lista) == 0:", "Todas as alternativas", "D", "basico"),
        ("Qual método transforma lista em string?", "join()", "concat()", "merge()", "toString()", "A", "basico"),
        ("Como copiar uma lista?", "lista.copy()", "lista[:]", "list(lista)", "Todas as alternativas", "D", "basico"),
        
        # INTERMEDIÁRIO (40 questões)
        ("O que é list comprehension?", "Uma função", "Uma forma concisa de criar listas", "Um tipo de loop", "Um método de lista", "B", "intermediario"),
        ("Qual a diferença entre append() e extend()?", "Nenhuma", "append adiciona 1 item, extend adiciona múltiplos", "extend é mais rápido", "append não existe", "B", "intermediario"),
        ("O que são args e kwargs?", "Tipos de dados", "Argumentos variáveis", "Métodos especiais", "Palavras reservadas", "B", "intermediario"),
        ("O que é uma função lambda?", "Função sem nome", "Função recursiva", "Função assíncrona", "Função de classe", "A", "intermediario"),
        ("Qual a diferença entre deepcopy e copy?", "Nenhuma", "deepcopy copia objetos aninhados", "copy é mais rápido", "deepcopy não existe", "B", "intermediario"),
        ("O que é um decorator?", "Uma função que modifica outra função", "Um tipo de classe", "Um loop especial", "Um comentário", "A", "intermediario"),
        ("Como tratar exceções em Python?", "try/except", "try/catch", "handle/error", "check/error", "A", "intermediario"),
        ("O que é um generator?", "Um tipo de lista", "Função que retorna iterador", "Um loop infinito", "Uma classe especial", "B", "intermediario"),
        ("Qual a diferença entre is e ==?", "Nenhuma", "is compara identidade, == compara valor", "== é mais rápido", "is verifica tipo", "B", "intermediario"),
        ("O que faz o método __init__?", "Inicia o programa", "Construtor da classe", "Deleta objeto", "Importa módulos", "B", "intermediario"),
        ("Como criar um iterador customizado?", "Implementar __iter__ e __next__", "Usar função iter()", "Herdar de Iterator", "Usar @iterator", "A", "intermediario"),
        ("O que é slicing?", "Cortar strings", "Fatiar sequências", "Dividir números", "Todas as alternativas", "B", "intermediario"),
        ("Qual a diferença entre list e tuple?", "list é mutável, tuple não", "tuple é mais rápido", "list usa menos memória", "A e B estão corretas", "D", "intermediario"),
        ("O que é uma closure?", "Função dentro de função", "Função que acessa variáveis externas", "Função sem return", "Função recursiva", "B", "intermediario"),
        ("Como funciona o with statement?", "Cria contexto e gerencia recursos", "Define variável", "Cria loop", "Importa módulo", "A", "intermediario"),
        ("O que são métodos estáticos?", "Métodos da classe, não da instância", "Métodos finais", "Métodos privados", "Métodos sem parâmetros", "A", "intermediario"),
        ("Qual a diferença entre sort() e sorted()?", "sort modifica lista, sorted cria nova", "Nenhuma", "sorted é mais rápido", "sort não existe", "A", "intermediario"),
        ("O que é duck typing?", "Sistema de tipos do Python", "Verificação de tipo em runtime", "Tipagem estática", "Conversão de tipos", "B", "intermediario"),
        ("Como criar propriedades em classes?", "Usar @property", "Usar get/set", "Usar variáveis privadas", "Usar __getattr__", "A", "intermediario"),
        ("O que faz o método map()?", "Aplica função a cada item", "Cria dicionário", "Mapeia variáveis", "Itera sobre lista", "A", "intermediario"),
        ("Qual a diferença entre __str__ e __repr__?", "__str__ para humanos, __repr__ para debug", "Nenhuma", "__repr__ é mais rápido", "__str__ não existe", "A", "intermediario"),
        ("O que são context managers?", "Gerenciam recursos com with", "Gerenciam memória", "Gerenciam threads", "Gerenciam imports", "A", "intermediario"),
        ("Como funciona a função zip()?", "Compacta arquivos", "Combina iteráveis", "Cria tuplas", "B e C estão corretas", "D", "intermediario"),
        ("O que é um namespace?", "Espaço de nomes para variáveis", "Tipo de string", "Função especial", "Módulo do Python", "A", "intermediario"),
        ("Qual a diferença entre método e função?", "Método pertence a classe", "Nenhuma", "Função é mais rápida", "Método não retorna valor", "A", "intermediario"),
        ("O que faz filter()?", "Filtra elementos de iterável", "Remove duplicatas", "Ordena lista", "Valida dados", "A", "intermediario"),
        ("Como criar método de classe?", "Usar @classmethod", "Usar @staticmethod", "Usar def classmethod", "Não é possível", "A", "intermediario"),
        ("O que é unpacking?", "Desempacotar sequências", "Comprimir dados", "Remover elementos", "Copiar listas", "A", "intermediario"),
        ("Qual a diferença entre shallow e deep copy?", "shallow copia referência, deep copia valor", "Nenhuma", "deep é mais rápido", "shallow não existe", "A", "intermediario"),
        ("O que são magic methods?", "Métodos especiais com __", "Métodos secretos", "Métodos rápidos", "Métodos de debug", "A", "intermediario"),
        ("Como criar um singleton em Python?", "Usar __new__", "Usar @singleton", "Usar global", "Não é possível", "A", "intermediario"),
        ("O que faz enumerate()?", "Adiciona índice ao iterar", "Conta elementos", "Enumera tipos", "Lista variáveis", "A", "intermediario"),
        ("Qual diferença entre shallow e deep equality?", "Compara referência vs valor recursivo", "Nenhuma", "deep é mais preciso", "shallow é mais rápido", "A", "intermediario"),
        ("O que é método estático?", "Não recebe self nem cls", "Método final", "Método privado", "Método sem retorno", "A", "intermediario"),
        ("Como funciona o operador *?", "Desempacota sequências", "Multiplica valores", "Cria ponteiro", "A e B estão corretas", "D", "intermediario"),
        ("O que são assertions?", "Verificações de debug", "Exceções", "Testes unitários", "Comentários", "A", "intermediario"),
        ("Qual a diferença entre get() e []?", "get retorna None se não existe", "Nenhuma", "[] é mais rápido", "get não existe", "A", "intermediario"),
        ("O que é múltipla herança?", "Classe herda de várias classes", "Várias classes em arquivo", "Instâncias múltiplas", "Métodos duplicados", "A", "intermediario"),
        ("Como criar variável privada?", "Usar _ ou __ no início", "Usar @private", "Usar private keyword", "Não é possível", "A", "intermediario"),
        ("O que faz reduce()?", "Reduz iterável a um valor", "Remove elementos", "Diminui tamanho", "Simplifica código", "A", "intermediario"),
        
        # AVANÇADO (20 questões)
        ("O que é o GIL?", "Global Interpreter Lock", "Gerenciador de imports", "Gerador de listas", "Garbage collector", "A", "avancado"),
        ("Como funciona o garbage collector?", "Coleta objetos sem referências", "Remove arquivos temporários", "Limpa memória cache", "Otimiza código", "A", "avancado"),
        ("O que são metaclasses?", "Classes que criam classes", "Classes abstratas", "Classes finais", "Classes de metadados", "A", "avancado"),
        ("Como funciona asyncio?", "Programação assíncrona", "Sincronização de threads", "I/O paralelo", "Todas as alternativas", "A", "avancado"),
        ("O que é descriptor protocol?", "Protocolo para controlar atributos", "Sistema de tipos", "Padrão de projeto", "Protocolo de rede", "A", "avancado"),
        ("Qual a diferença entre thread e process?", "Threads compartilham memória", "Nenhuma", "Processes são mais rápidos", "Threads são mais seguras", "A", "avancado"),
        ("O que é monkey patching?", "Modificar código em runtime", "Corrigir bugs", "Testar código", "Otimizar performance", "A", "avancado"),
        ("Como funciona o método __getattr__?", "Chamado quando atributo não existe", "Retorna todos atributos", "Define atributo", "Remove atributo", "A", "avancado"),
        ("O que é type hinting?", "Anotações de tipo", "Sistema de tipos dinâmico", "Conversão de tipos", "Verificação de tipos", "A", "avancado"),
        ("Como criar um context manager customizado?", "Implementar __enter__ e __exit__", "Usar with statement", "Herdar de Context", "Usar @context", "A", "avancado"),
        ("O que é o método __call__?", "Torna instância chamável", "Chama método", "Executa função", "Retorna callable", "A", "avancado"),
        ("Qual a diferença entre new e init?", "__new__ cria instância, __init__ inicializa", "Nenhuma", "__init__ é mais usado", "__new__ não existe", "A", "avancado"),
        ("O que são coroutines?", "Funções assíncronas", "Threads leves", "Processos paralelos", "Funções geradoras", "A", "avancado"),
        ("Como funciona o import system?", "sys.modules, finders, loaders", "Importa módulos diretamente", "Usa cache global", "Compila código", "A", "avancado"),
        ("O que é MRO?", "Method Resolution Order", "Multiple Return Object", "Memory Reference Order", "Module Resource Object", "A", "avancado"),
        ("Como funciona weakref?", "Referências fracas que não impedem GC", "Referências fortes", "Referências circulares", "Referências globais", "A", "avancado"),
        ("O que são abstract base classes?", "Classes base que não podem ser instanciadas", "Classes abstratas", "Classes de interface", "Todas as alternativas", "D", "avancado"),
        ("Como funciona __slots__?", "Limita atributos e economiza memória", "Define métodos", "Cria propriedades", "Inicializa classe", "A", "avancado"),
        ("O que é memoryview?", "Visualiza buffer de memória sem cópia", "Monitora uso de memória", "Cache de objetos", "Profiler de memória", "A", "avancado"),
        ("Como implementar iterator protocol?", "Definir __iter__ e __next__", "Usar yield", "Herdar de Iterator", "Usar @iterator", "A", "avancado"),
    ]

    sql = """
        INSERT INTO questoes (pergunta, alternativaA, alternativaB, alternativaC, alternativaD, correta, nivel)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.executemany(sql, questoes)
    db.commit()
    db.close()
    print("✓ 100 questões inseridas com sucesso!")

# -----------------------------------
# CADASTRO DE NOVO USUÁRIO
# -----------------------------------
def cadastrar_usuario():
    db = conectar()
    cursor = db.cursor()

    print("\n---- CADASTRO ----")
    
    while True:
        usuario = input("Escolha um nome de usuário: ").strip()
        
        if not usuario:
            print("Usuário não pode ser vazio!")
            continue
            
        senha = input("Escolha uma senha: ").strip()
        
        if not senha:
            print("Senha não pode ser vazia!")
            continue
        
        confirma_senha = input("Confirme a senha: ").strip()
        
        if senha != confirma_senha:
            print("As senhas não coincidem! Tente novamente.\n")
            continue
        
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            db.commit()
            print("\n✓ Cadastro realizado com sucesso!\n")
            db.close()
            return True
        except sqlite3.IntegrityError:
            print("Usuário já existe! Escolha outro nome.\n")

# -----------------------------------
# LOGIN
# -----------------------------------
def login():
    db = conectar()
    cursor = db.cursor()

    print("\n---- LOGIN ----")

    tentativas = 0
    max_tentativas = 3

    while tentativas < max_tentativas:
        user = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        cursor.execute("SELECT id FROM usuarios WHERE usuario=? AND senha=?", (user, senha))
        resultado = cursor.fetchone()

        if resultado:
            print("\n✓ Login realizado com sucesso!\n")
            db.close()
            return resultado[0]
        else:
            tentativas += 1
            restantes = max_tentativas - tentativas
            if restantes > 0:
                print(f"✗ Usuário ou senha inválidos. Tentativas restantes: {restantes}\n")
            else:
                print("✗ Número máximo de tentativas excedido.")
                db.close()
                return None

# -----------------------------------
# GERAR TESTE (10 questões aleatórias)
# -----------------------------------
def gerar_quiz(nivel=None):
    db = conectar()
    cursor = db.cursor()

    if nivel:
        cursor.execute("SELECT * FROM questoes WHERE nivel=? ORDER BY RANDOM() LIMIT 10", (nivel,))
    else:
        cursor.execute("SELECT * FROM questoes ORDER BY RANDOM() LIMIT 10")
    
    questoes = cursor.fetchall()
    
    db.close()
    
    # Converte para lista de dicionários
    quiz = []
    for q in questoes:
        quiz.append({
            'id': q[0],
            'pergunta': q[1],
            'alternativaA': q[2],
            'alternativaB': q[3],
            'alternativaC': q[4],
            'alternativaD': q[5],
            'correta': q[6],
            'nivel': q[7]
        })
    
    return quiz

# -----------------------------------
# REALIZAR TESTE
# -----------------------------------
def fazer_teste(quiz):
    acertos = 0
    print("\n" + "="*50)
    print("INICIANDO TESTE - 10 QUESTÕES")
    print("="*50)

    for i, q in enumerate(quiz, 1):
        print(f"\n[Questão {i}/10] - Nível: {q['nivel'].upper()}")
        print(f"{q['pergunta']}")
        print(f"A) {q['alternativaA']}")
        print(f"B) {q['alternativaB']}")
        print(f"C) {q['alternativaC']}")
        print(f"D) {q['alternativaD']}")

        while True:
            resp = input("\nSua resposta (A/B/C/D): ").strip().upper()
            if resp in ['A', 'B', 'C', 'D']:
                break
            print("Resposta inválida! Digite A, B, C ou D.")

        if resp == q["correta"]:
            acertos += 1
            print("✓ Correto!")
        else:
            print(f"✗ Errado! A resposta correta era: {q['correta']}")

    print("\n" + "="*50)
    print(f"RESULTADO FINAL: {acertos}/10 ({acertos*10}%)")
    print("="*50)
    
    return acertos

# -----------------------------------
# SALVAR RESULTADO
# -----------------------------------
def salvar_resultado(user_id, nota):
    db = conectar()
    cursor = db.cursor()

    cursor.execute("INSERT INTO resultados (usuario_id, nota) VALUES (?, ?)", (user_id, nota))

    db.commit()
    db.close()

# -----------------------------------
# VER ESTATÍSTICAS DO USUÁRIO
# -----------------------------------
def ver_estatisticas(user_id):
    db = conectar()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_testes,
            AVG(nota) as media,
            MAX(nota) as melhor_nota,
            MIN(nota) as pior_nota
        FROM resultados 
        WHERE usuario_id=?
    """, (user_id,))
    
    stats = cursor.fetchone()
    
    db.close()

    if stats[0] == 0:
        print("\n✗ Você ainda não realizou nenhum teste.")
    else:
        print("\n" + "="*50)
        print("SUAS ESTATÍSTICAS")
        print("="*50)
        print(f"Total de testes realizados: {stats[0]}")
        print(f"Média geral: {stats[1]:.1f}/10 ({stats[1]*10:.1f}%)")
        print(f"Melhor nota: {stats[2]}/10")
        print(f"Pior nota: {stats[3]}/10")
        print("="*50)

# -----------------------------------
# MENU PRINCIPAL
# -----------------------------------
def menu(user_id):
    quiz_atual = None

    while True:
        print("""
╔════════════════════════════════════════╗
║           QUIZ PYTHON - MENU           ║
╚════════════════════════════════════════╝
  1 - Fazer teste (aleatório)
  2 - Fazer teste por nível
  3 - Refazer último teste
  4 - Gerar novo teste
  5 - Ver estatísticas
  6 - Sair
""")

        opc = input("Escolha uma opção: ").strip()

        if opc == "1":
            quiz_atual = gerar_quiz()
            nota = fazer_teste(quiz_atual)
            salvar_resultado(user_id, nota)

        elif opc == "2":
            print("\nEscolha o nível:")
            print("1 - Básico")
            print("2 - Intermediário")
            print("3 - Avançado")
            
            nivel_opc = input("Opção: ").strip()
            nivel_map = {"1": "basico", "2": "intermediario", "3": "avancado"}
            
            if nivel_opc in nivel_map:
                quiz_atual = gerar_quiz(nivel_map[nivel_opc])
                nota = fazer_teste(quiz_atual)
                salvar_resultado(user_id, nota)
            else:
                print("✗ Opção inválida!")

        elif opc == "3":
            if quiz_atual is None:
                print("\n✗ Não existe teste criado ainda. Gere um novo teste primeiro.")
            else:
                nota = fazer_teste(quiz_atual)
                salvar_resultado(user_id, nota)

        elif opc == "4":
            quiz_atual = gerar_quiz()
            print("\n✓ Novo teste gerado com sucesso!")

        elif opc == "5":
            ver_estatisticas(user_id)

        elif opc == "6":
            print("\n👋 Obrigado por usar o Quiz Python! Até logo!")
            break

        else:
            print("\n✗ Opção inválida! Escolha um número de 1 a 6.")

# -----------------------------------
# TELA INICIAL
# -----------------------------------
def tela_inicial():
    print("""
╔════════════════════════════════════════╗
║       BEM-VINDO AO QUIZ PYTHON!        ║
║     Teste seus conhecimentos em        ║
║    Python: Básico, Intermediário       ║
║          e Avançado                    ║
╚════════════════════════════════════════╝
""")
    
    while True:
        print("\n1 - Login")
        print("2 - Cadastrar")
        print("3 - Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            user_id = login()
            if user_id:
                return user_id
            else:
                print("\nRetornando ao menu inicial...")
                
        elif opcao == "2":
            if cadastrar_usuario():
                print("Agora faça login com suas credenciais:")
                user_id = login()
                if user_id:
                    return user_id
                    
        elif opcao == "3":
            print("\n👋 Até logo!")
            exit()
            
        else:
            print("\n✗ Opção inválida!")

# -----------------------------------
# INICIALIZAÇÃO
# -----------------------------------
if __name__ == "__main__":
    print("Inicializando banco de dados...")
    criar_tabelas()
    inserir_questoes()
    
    user_id = tela_inicial()
    menu(user_id)