import sqlite3
import random

class DatabaseManager:
    def __init__(self, db_path="quizcode.db"):
        self.db_path = db_path
    
    def conectar(self):
        return sqlite3.connect(self.db_path)
    
    def criar_tabelas(self):
        db = self.conectar()
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
    
    def inserir_questoes(self):
        db = self.conectar()
        cursor = db.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM questoes")
        qtd = cursor.fetchone()[0]
        
        if qtd > 0:
            db.close()
            return
        
        questoes = [
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

class Usuario:
    def __init__(self, db_manager, usuario_id=None, nome=None, senha=None):
        self.db_manager = db_manager
        self.id = usuario_id
        self.nome = nome
        self.senha = senha
    
    def cadastrar(self, usuario, senha):
        db = self.db_manager.conectar()
        cursor = db.cursor()
        
        try:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
            db.commit()
            db.close()
            return True
        except sqlite3.IntegrityError:
            db.close()
            return False
    
    def login(self, usuario, senha):
        db = self.db_manager.conectar()
        cursor = db.cursor()
        
        cursor.execute("SELECT id FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
        resultado = cursor.fetchone()
        db.close()
        
        if resultado:
            self.id = resultado[0]
            self.nome = usuario
            return self.id
        return None
    
    def buscar_por_id(self, usuario_id):
        db = self.db_manager.conectar()
        cursor = db.cursor()
        
        cursor.execute("SELECT id, usuario FROM usuarios WHERE id=?", (usuario_id,))
        resultado = cursor.fetchone()
        db.close()
        
        if resultado:
            self.id = resultado[0]
            self.nome = resultado[1]
            return self
        return None

class Questao:
    def __init__(self, questao_id=None, pergunta=None, alternativa_a=None, alternativa_b=None, 
                 alternativa_c=None, alternativa_d=None, correta=None, nivel=None):
        self.id = questao_id
        self.pergunta = pergunta
        self.alternativaA = alternativa_a
        self.alternativaB = alternativa_b
        self.alternativaC = alternativa_c
        self.alternativaD = alternativa_d
        self.correta = correta
        self.nivel = nivel
    
    def to_dict(self, incluir_resposta=False):
        questao_dict = {
            'id': self.id,
            'pergunta': self.pergunta,
            'alternativaA': self.alternativaA,
            'alternativaB': self.alternativaB,
            'alternativaC': self.alternativaC,
            'alternativaD': self.alternativaD,
            'nivel': self.nivel
        }
        if incluir_resposta:
            questao_dict['correta'] = self.correta
        return questao_dict
    
    def verificar_resposta(self, resposta):
        return resposta.strip().upper() == self.correta

class Quiz:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.questoes = []
    
    def gerar(self, nivel=None, quantidade=10):
        db = self.db_manager.conectar()
        cursor = db.cursor()
        
        if nivel:
            cursor.execute("SELECT * FROM questoes WHERE nivel=? ORDER BY RANDOM() LIMIT ?", (nivel, quantidade))
        else:
            cursor.execute("SELECT * FROM questoes ORDER BY RANDOM() LIMIT ?", (quantidade,))
        
        questoes_db = cursor.fetchall()
        db.close()
        
        self.questoes = []
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
            self.questoes.append(questao)
        
        return self.questoes
    
    def obter_questao_por_id(self, questao_id):
        for questao in self.questoes:
            if questao.id == questao_id:
                return questao
        return None
    
    def to_dict_list(self, incluir_resposta=False):
        return [q.to_dict(incluir_resposta) for q in self.questoes]
    
    def calcular_resultado(self, respostas):
        acertos = 0
        total = len(self.questoes)
        
        for resp in respostas:
            questao_id = resp.get('questao_id')
            resposta_usuario = resp.get('resposta', '').strip().upper()
            
            questao = self.obter_questao_por_id(questao_id)
            if questao and questao.verificar_resposta(resposta_usuario):
                acertos += 1
        
        return acertos, total

class Resultado:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def salvar(self, usuario_id, nota):
        db = self.db_manager.conectar()
        cursor = db.cursor()
        
        cursor.execute("INSERT INTO resultados (usuario_id, nota) VALUES (?, ?)", (usuario_id, nota))
        db.commit()
        db.close()
    
    def obter_estatisticas(self, usuario_id):
        db = self.db_manager.conectar()
        cursor = db.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_testes,
                AVG(nota) as media,
                MAX(nota) as melhor_nota,
                MIN(nota) as pior_nota
            FROM resultados 
            WHERE usuario_id=?
        """, (usuario_id,))
        
        resultado = cursor.fetchone()
        db.close()
        
        if not resultado or resultado[0] == 0:
            return {
                'total_testes': 0,
                'media': 0,
                'melhor_nota': 0,
                'pior_nota': 0
            }
        
        return {
            'total_testes': resultado[0],
            'media': round(resultado[1] or 0, 1),
            'melhor_nota': resultado[2] or 0,
            'pior_nota': resultado[3] or 0
        }
    
    def calcular_rank(self, porcentagem):
        if porcentagem >= 80:
            return "Desenvolvedor Senior"
        elif porcentagem >= 60:
            return "Desenvolvedor Pleno"
        else:
            return "Desenvolvedor Junior"

