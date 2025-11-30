from models import DatabaseManager, Usuario, Quiz, Resultado, Questao

db_manager = DatabaseManager()

def conectar():
    return db_manager.conectar()

def criar_tabelas():
    db_manager.criar_tabelas()

def inserir_questoes():
    db_manager.inserir_questoes()

def cadastrar_usuario():
    user = Usuario(db_manager)
    
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
        
        if user.cadastrar(usuario, senha):
            print("\n✓ Cadastro realizado com sucesso!\n")
            return True
        else:
            print("Usuário já existe! Escolha outro nome.\n")

def login():
    user = Usuario(db_manager)
    
    print("\n---- LOGIN ----")

    tentativas = 0
    max_tentativas = 3

    while tentativas < max_tentativas:
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        user_id = user.login(usuario, senha)

        if user_id:
            print("\n✓ Login realizado com sucesso!\n")
            return user_id
        else:
            tentativas += 1
            restantes = max_tentativas - tentativas
            if restantes > 0:
                print(f"✗ Usuário ou senha inválidos. Tentativas restantes: {restantes}\n")
            else:
                print("✗ Número máximo de tentativas excedido.")
                return None

def gerar_quiz(nivel=None):
    quiz = Quiz(db_manager)
    questoes = quiz.gerar(nivel)
    
    quiz_list = []
    for q in questoes:
        quiz_list.append(q.to_dict(incluir_resposta=True))
    
    return quiz_list

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

        questao_obj = Questao(correta=q['correta'])
        if questao_obj.verificar_resposta(resp):
            acertos += 1
            print("✓ Correto!")
        else:
            print(f"✗ Errado! A resposta correta era: {q['correta']}")

    print("\n" + "="*50)
    print(f"RESULTADO FINAL: {acertos}/10 ({acertos*10}%)")
    print("="*50)
    
    return acertos

def salvar_resultado(user_id, nota):
    resultado = Resultado(db_manager)
    resultado.salvar(user_id, nota)

def ver_estatisticas(user_id):
    resultado = Resultado(db_manager)
    stats = resultado.obter_estatisticas(user_id)

    if stats['total_testes'] == 0:
        print("\n✗ Você ainda não realizou nenhum teste.")
    else:
        print("\n" + "="*50)
        print("SUAS ESTATÍSTICAS")
        print("="*50)
        print(f"Total de testes realizados: {stats['total_testes']}")
        print(f"Média geral: {stats['media']:.1f}/10 ({stats['media']*10:.1f}%)")
        print(f"Melhor nota: {stats['melhor_nota']}/10")
        print(f"Pior nota: {stats['pior_nota']}/10")
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