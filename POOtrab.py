from models import DatabaseManager, Usuario, Quiz, Resultado, Questao # Importa as classes do arquivo models.py

# -----------------------------------
#       PROGRAMA PRINCIPAL
# -----------------------------------
# Nome do Programa: Quiz Python Console
#
# Função do Programa
# -> Gerenciar o fluxo do jogo de Quiz via terminal (Console)
# -> Controlar autenticação, execução de testes e exibição de estatísticas
# -> Objetos instanciados: DatabaseManager, Usuario, Quiz, Questao, Resultado
# -----------------------------------

# -----------------------------------
#           ATRIBUTOS
# -----------------------------------
# db_manager: Instância global responsável por gerenciar a conexão com o banco de dados
# -----------------------------------

db_manager = DatabaseManager() # Instancia o gerenciador de banco de dados globalmente

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: conectar
#
# Para que serve: Estabelecer uma conexão direta com o banco de dados
#
# Retorno do método:
# -> Objeto de conexão do SQLite
# -----------------------------------
def conectar():
    return db_manager.conectar() # Retorna a conexão ativa do gerenciador

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: criar_tabelas
#
# Para que serve: Inicializar a estrutura do banco de dados
#
# -----------------------------------
def criar_tabelas():
    db_manager.criar_tabelas() # Chama o método para criar as tabelas se não existirem

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: inserir_questoes
#
# Para que serve: Popular o banco com questões padrão
#
# -----------------------------------
def inserir_questoes():
    db_manager.inserir_questoes() # Insere as questões iniciais no banco de dados

# -----------------------------------
#             MÉTODO
# -----------------------------------
# Nome do método: cadastrar_usuario
#
# Para que serve: Interagir com o usuário para criar uma nova conta
#
# Retorno do método:
# -> True (bool) se o cadastro for bem-sucedido (ou loop infinito até conseguir/desistir)
# -----------------------------------
def cadastrar_usuario():
    user = Usuario(db_manager) # Instancia um objeto Usuario com o gerenciador de DB
    
    print("\n---- CADASTRO ----") # Imprime o cabeçalho da seção de cadastro
    
    while True: # Inicia um loop infinito para o formulário
        usuario = input("Escolha um nome de usuário: ").strip() # Recebe o nome e remove espaços vazios
        
        if not usuario: # Verifica se o nome está vazio
            print("Usuário não pode ser vazio!") # Avisa o erro ao usuário
            continue # Reinicia o loop
            
        senha = input("Escolha uma senha: ").strip() # Recebe a senha e remove espaços vazios
        
        if not senha: # Verifica se a senha está vazia
            print("Senha não pode ser vazia!") # Avisa o erro
            continue # Reinicia o loop
        
        confirma_senha = input("Confirme a senha: ").strip() # Recebe a confirmação da senha
        
        if senha != confirma_senha: # Compara as duas senhas
            print("As senhas não coincidem! Tente novamente.\n") # Avisa se forem diferentes
            continue # Reinicia o loop para tentar novamente
        
        if user.cadastrar(usuario, senha): # Tenta realizar o cadastro no banco
            print("\n✓ Cadastro realizado com sucesso!\n") # Informa sucesso
            return True # Retorna verdadeiro e sai da função
        else:
            print("Usuário já existe! Escolha outro nome.\n") # Informa erro de duplicidade e o loop continua

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: login
#
# Para que serve: Autenticar o usuário no sistema
#
# Retorno do método:
# -> user_id (int): ID do usuário se logado com sucesso
# -> None: Se exceder o número de tentativas
# -----------------------------------
def login():
    user = Usuario(db_manager) # Instancia objeto Usuario para validação
    
    print("\n---- LOGIN ----") # Imprime cabeçalho de login

    tentativas = 0 # Inicializa contador de tentativas
    max_tentativas = 3 # Define limite máximo de erros

    while tentativas < max_tentativas: # Loop enquanto não exceder tentativas
        usuario = input("Usuário: ").strip() # Recebe usuário limpo
        senha = input("Senha: ").strip() # Recebe senha limpa

        user_id = user.login(usuario, senha) # Tenta logar e recebe o ID (ou None)

        if user_id: # Se o ID for válido
            print("\n✓ Login realizado com sucesso!\n") # Informa sucesso
            return user_id # Retorna o ID do usuário
        else:
            tentativas += 1 # Incrementa o contador de erros
            restantes = max_tentativas - tentativas # Calcula tentativas restantes
            if restantes > 0: # Se ainda houver chances
                print(f"✗ Usuário ou senha inválidos. Tentativas restantes: {restantes}\n") # Avisa erro e tentativas
            else:
                print("✗ Número máximo de tentativas excedido.") # Avisa bloqueio
                return None # Retorna vazio (falha no login)

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: gerar_quiz
#
# Para que serve: Buscar questões no banco e preparar a lista para o jogo
#
# Parâmetros de entrada:
# -> nivel: (Opcional) String indicando a dificuldade ('basico', etc.)
#
# Retorno do método:
# -> quiz_list (list): Lista de dicionários contendo os dados das questões
# -----------------------------------
def gerar_quiz(nivel=None):
    quiz = Quiz(db_manager) # Instancia o gerenciador de Quiz
    questoes = quiz.gerar(nivel) # Busca objetos Questao do banco (filtrado ou não)
    
    quiz_list = [] # Inicializa lista vazia para os dados
    for q in questoes: # Itera sobre os objetos Questao
        quiz_list.append(q.to_dict(incluir_resposta=True)) # Converte para dicionário e adiciona à lista
    
    return quiz_list # Retorna a lista pronta para uso

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: fazer_teste
#
# Para que serve: Executar o loop de perguntas e respostas do jogo
#
# Parâmetros de entrada:
# -> quiz: Lista de dicionários com as questões
#
# Retorno do método:
# -> acertos (int): Número total de respostas corretas
# -----------------------------------
def fazer_teste(quiz):
    acertos = 0 # Inicializa contador de acertos
    print("\n" + "="*50) # Imprime linha separadora
    print("INICIANDO TESTE - 10 QUESTÕES") # Imprime título do teste
    print("="*50) # Imprime linha separadora

    for i, q in enumerate(quiz, 1): # Itera sobre as questões numerando de 1 a 10
        print(f"\n[Questão {i}/10] - Nível: {q['nivel'].upper()}") # Exibe número e nível da questão
        print(f"{q['pergunta']}") # Exibe o enunciado
        print(f"A) {q['alternativaA']}") # Exibe alternativa A
        print(f"B) {q['alternativaB']}") # Exibe alternativa B
        print(f"C) {q['alternativaC']}") # Exibe alternativa C
        print(f"D) {q['alternativaD']}") # Exibe alternativa D

        while True: # Loop para validar a entrada da resposta
            resp = input("\nSua resposta (A/B/C/D): ").strip().upper() # Lê a resposta e normaliza para maiúscula
            if resp in ['A', 'B', 'C', 'D']: # Verifica se é uma opção válida
                break # Sai do loop se válido
            print("Resposta inválida! Digite A, B, C ou D.") # Avisa erro se inválido

        questao_obj = Questao(correta=q['correta']) # Cria objeto temporário com a resposta correta
        if questao_obj.verificar_resposta(resp): # Verifica se o usuário acertou
            acertos += 1 # Incrementa acertos
            print("✓ Correto!") # Feedback positivo
        else:
            print(f"✗ Errado! A resposta correta era: {q['correta']}") # Feedback negativo com correção

    print("\n" + "="*50) # Imprime separador
    # Imprime resultado final formatado
    print(f"RESULTADO FINAL: {acertos}/10 ({acertos*10}%)")
    print("="*50) # Imprime separador
    
    return acertos # Retorna o total de acertos

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: salvar_resultado
#
# Para que serve: Gravar a pontuação do usuário no banco de dados
#
# Parâmetros de entrada:
# -> user_id: ID do usuário
# -> nota: Nota obtida no teste
# -----------------------------------
def salvar_resultado(user_id, nota):
    resultado = Resultado(db_manager) # Instancia objeto Resultado
    resultado.salvar(user_id, nota) # Executa método de salvamento

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: ver_estatisticas
#
# Para que serve: Exibir o histórico de desempenho do usuário
#
# Parâmetros de entrada:
# -> user_id: ID do usuário
# -----------------------------------
def ver_estatisticas(user_id):
    resultado = Resultado(db_manager) # Instancia objeto Resultado
    stats = resultado.obter_estatisticas(user_id) # Busca dicionário de estatísticas

    if stats['total_testes'] == 0: # Se não houver testes realizados
        print("\n✗ Você ainda não realizou nenhum teste.") # Avisa o usuário
    else:
        print("\n" + "="*50) # Imprime separador
        print("SUAS ESTATÍSTICAS") # Título da seção
        print("="*50) # Imprime separador
        print(f"Total de testes realizados: {stats['total_testes']}") # Exibe total
        print(f"Média geral: {stats['media']:.1f}/10 ({stats['media']*10:.1f}%)") # Exibe média formatada
        print(f"Melhor nota: {stats['melhor_nota']}/10") # Exibe melhor nota
        print(f"Pior nota: {stats['pior_nota']}/10") # Exibe pior nota
        print("="*50) # Imprime separador final

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: menu
#
# Para que serve: Gerenciar a navegação principal do usuário logado
#
# Parâmetros de entrada:
# -> user_id: ID do usuário logado
#
# Retorno do método: Nenhum (Loop infinito até sair)
# -----------------------------------
def menu(user_id):
    quiz_atual = None # Variável para armazenar o último quiz gerado

    while True: # Loop principal do menu
        # Imprime as opções do menu visualmente
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

        opc = input("Escolha uma opção: ").strip() # Captura opção do usuário

        if opc == "1": # Se escolheu teste aleatório
            quiz_atual = gerar_quiz() # Gera quiz sem filtro
            nota = fazer_teste(quiz_atual) # Executa o teste
            salvar_resultado(user_id, nota) # Salva o resultado

        elif opc == "2": # Se escolheu teste por nível
            print("\nEscolha o nível:") # Pede o nível
            print("1 - Básico")
            print("2 - Intermediário")
            print("3 - Avançado")
            
            nivel_opc = input("Opção: ").strip() # Captura a escolha do nível
            nivel_map = {"1": "basico", "2": "intermediario", "3": "avancado"} # Mapa de conversão
            
            if nivel_opc in nivel_map: # Se o nível for válido
                quiz_atual = gerar_quiz(nivel_map[nivel_opc]) # Gera quiz com o nível escolhido
                nota = fazer_teste(quiz_atual) # Executa o teste
                salvar_resultado(user_id, nota) # Salva resultado
            else:
                print("✗ Opção inválida!") # Avisa erro de opção

        elif opc == "3": # Se escolheu refazer teste
            if quiz_atual is None: # Verifica se existe teste anterior
                print("\n✗ Não existe teste criado ainda. Gere um novo teste primeiro.") # Avisa erro
            else:
                nota = fazer_teste(quiz_atual) # Executa o mesmo teste novamente
                salvar_resultado(user_id, nota) # Salva o novo resultado

        elif opc == "4": # Se escolheu apenas gerar novo teste
            quiz_atual = gerar_quiz() # Gera e armazena novo quiz
            print("\n✓ Novo teste gerado com sucesso!") # Confirmação

        elif opc == "5": # Se escolheu ver estatísticas
            ver_estatisticas(user_id) # Chama função de estatísticas

        elif opc == "6": # Se escolheu sair
            print("\n👋 Obrigado por usar o Quiz Python! Até logo!") # Mensagem de despedida
            break # Encerra o loop do menu

        else: # Qualquer outra opção
            print("\n✗ Opção inválida! Escolha um número de 1 a 6.") # Mensagem de erro

# -----------------------------------
#            MÉTODO
# -----------------------------------
# Nome do método: tela_inicial
#
# Para que serve: Primeira tela apresentada, gerenciando Login, Cadastro ou Saída
#
# Retorno do método:
# -> user_id (int): Retorna o ID do usuário autenticado para iniciar o menu
# -----------------------------------
def tela_inicial():
    # Imprime banner de boas-vindas
    print("""
╔════════════════════════════════════════╗
║       BEM-VINDO AO QUIZ PYTHON!        ║
║     Teste seus conhecimentos em        ║
║    Python: Básico, Intermediário       ║
║          e Avançado                    ║
╚════════════════════════════════════════╝
""")
    
    while True: # Loop da tela inicial
        print("\n1 - Login") # Opção Login
        print("2 - Cadastrar") # Opção Cadastro
        print("3 - Sair") # Opção Sair
        
        opcao = input("\nEscolha uma opção: ").strip() # Captura opção
        
        if opcao == "1": # Fluxo de Login
            user_id = login() # Chama função de login
            if user_id: # Se logou com sucesso
                return user_id # Retorna ID e sai da tela inicial
            else:
                print("\nRetornando ao menu inicial...") # Se falhou, volta ao menu
                
        elif opcao == "2": # Fluxo de Cadastro
            if cadastrar_usuario(): # Se cadastrou com sucesso
                print("Agora faça login com suas credenciais:") # Pede para logar
                user_id = login() # Chama login imediatamente
                if user_id: # Se logou
                    return user_id # Retorna ID
                    
        elif opcao == "3": # Fluxo de Saída
            print("\n👋 Até logo!") # Despedida
            exit() # Encerra o programa
            
        else:
            print("\n✗ Opção inválida!") # Erro de opção

# -----------------------------------
# FUNÇÃO MAIN
# -----------------------------------
# Nome da função: Bloco Main (if __name__ == "__main__")
#
# O que ela faz:
# -> Ponto de entrada da execução do script
# -> Inicializa o banco de dados e chama as telas de interação
# -----------------------------------
if __name__ == "__main__":
    print("Inicializando banco de dados...") # Log de inicialização
    criar_tabelas() # Garante que tabelas existem
    inserir_questoes() # Garante que há questões
    
    user_id = tela_inicial() # Chama tela inicial e aguarda login válido
    menu(user_id) # Inicia o menu principal com o usuário logado