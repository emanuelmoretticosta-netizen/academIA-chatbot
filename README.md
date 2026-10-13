# AcademIA 🏋️

Assistente virtual de educação física desenvolvido em Python, que funciona
como um personal trainer acessível e inteligente. O usuário conversa com
uma IA que monta planos de treino personalizados, acompanha o progresso e
tira dúvidas sobre treino, suplementação básica e recuperação.

Projeto desenvolvido em grupo para a disciplina de Introdução à
Programação, UFCAT.

## Funcionalidades

- **Chat com IA**: conversa natural para coletar dados do usuário (idade,
  peso, altura, objetivo, local de treino, limitações físicas) e montar um
  plano de treino sob medida
- **Catálogo de exercícios**: mais de 60 exercícios, separados entre
  treino em academia e treino em casa, cada um com vídeo de referência no
  YouTube
- **Planos organizados por letra**: A, B, C... conforme a quantidade de
  dias disponíveis na semana (de 2 a 5 dias)
- **Registro de treinos**: o usuário marca quando conclui um treino e dá
  uma nota de 1 a 5
- **Painel de progresso**: total de treinos realizados, semanas ativas,
  nota média e gráfico de frequência semanal
- **Perfil do usuário**: tela dedicada para editar dados, com upload de
  foto de perfil
- **Orientações básicas**: dicas sobre suplementação (creatina, whey,
  cafeína, BCAA), descanso/recuperação e alimentação pré e pós-treino,
  sempre recomendando um profissional para planos detalhados
- **Limites claros de domínio**: o assistente não substitui nutricionista
  nem médico, e redireciona perguntas fora da sua área

## Tecnologias utilizadas

- **Python** com **Flask** (backend e rotas da aplicação)
- **HTML, CSS e JavaScript** (interface do usuário)
- **API da OpenAI** (geração das respostas do assistente)
- **JSON** para armazenamento local dos dados de cada usuário

## Como rodar o projeto localmente

### Pré-requisitos
- Python 3.10 ou superior instalado
- Uma chave de API da OpenAI (platform.openai.com)

### Passo a passo

1. Clone o repositório:
```bash
   git clone https://github.com/emanuelmoretticosta-netizen/academIA-chatbot.git
   cd academia-chatbot
```

2. Crie um ambiente virtual:
```bash
   python -m venv venv
```

3. Ative o ambiente virtual:
```bash
   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
```

4. Instale as dependências:
```bash
   pip install flask openai python-dotenv requests werkzeug
```

5. Crie o arquivo `.env` a partir do exemplo:
```bash
   # Windows
   copy .env.example .env

   # Mac/Linux
   cp .env.example .env
```

6. Abra o `.env` e preencha com seus próprios valores:
OPENAI_API_KEY=sua_chave_aqui
FLASK_SECRET_KEY=uma_chave_secreta_aleatoria_aqui


7. Rode o servidor:
```bash
   python app.py
```

8. Abra o navegador em `http://127.0.0.1:5001`

## Estrutura do projeto

academia-chatbot/
├── app.py # Rotas Flask e lógica principal do servidor
├── bot.py # Lógica de conversa com a IA (OpenAI)
├── database.py # Leitura e escrita dos dados em data/usuarios.json
├── estatisticas.py # Cálculo do resumo de progresso e gráfico semanal
├── exercicios.py # Catálogo de exercícios (academia e casa)
├── prompts.py # Personalidade e regras do assistente
├── index.html # Interface do usuário
├── .env.example # Modelo das variáveis de ambiente necessárias
├── .gitignore # Arquivos e pastas ignorados pelo Git
└── data/ # Dados dos usuários, gerado automaticamente (não versionado)


## Possíveis melhorias futuras

- [ ] Autenticação mais robusta (senha, não só nome de usuário)
- [ ] Exportar plano de treino em PDF
- [ ] Notificações para lembrar o usuário de treinar
- [ ] Testes automatizados

## Autores

- Emanuel Moretti Costa
- Ana Luiza
- Maríllya Gabriella
- Geovana Novais

## Aviso

Este projeto é um trabalho acadêmico. As orientações sobre treino e
suplementação são de caráter geral e não substituem acompanhamento de
profissionais de educação física, nutrição ou medicina.