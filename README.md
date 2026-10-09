# MESAFARTAI – Logística e Inteligência Assistiva no Combate à Fome

![Logo MESAFARTAI](assets/logo_mesafartai.png)

## Sobre o projeto

O MESAFARTAI é uma aplicação conversacional em Python que conecta quem tem alimento sobrando a quem precisa dele. Comerciantes, feirantes, restaurantes e produtores informam a doação em uma mensagem informal de chat; o sistema entende a intenção da mensagem, extrai produto, quantidade e validade e direciona o alimento para a ONG mais próxima.

O problema que o projeto ataca não é a falta de comida, e sim a falta de logística ágil e de comunicação simples entre doadores e instituições.

## Alinhamento com a ODS 2 da ONU

O projeto está alinhado à **ODS 2 – Fome Zero e Agricultura Sustentável**. Ao reduzir o desperdício de alimentos próprios para consumo e encurtar o caminho até ONGs, abrigos e cozinhas comunitárias, a solução contribui para o acesso de famílias em situação de vulnerabilidade a alimentos seguros e suficientes.

## Como funciona

1. **Interface conversacional**: chat com alternância de perfil (Sou Doador | Sou ONG).
2. **Motor de NLU**: classificação de intenções (`cadastrar_doacao`, `solicitar_alimentos`, `consultar_status`, `fora_de_escopo`) com threshold e resposta de fallback para frases ambíguas.
3. **Extração de entidades (Regex)**: quantidades, tipos de alimento e prazos de validade.
4. **Matchmaking logístico (KNN + SQLite3)**: encontra a ONG receptora mais próxima da doação e registra o histórico.

## Tecnologias

- Python 3
- Scikit-Learn / spaCy
- SQLite3
- Streamlit

## Estrutura do repositório

```
PROJETO-MESAFARTAI/
├── README.md
├── assets/
│   └── logo_mesafartai.png
├── docs/
│   ├── regras.txt
│   ├── escopo_projeto.md
│   ├── arquitetura_mesafartai.png
│   └── diag_fluxo_mesafartai.png
└── src/
    └── database.py
```

## Como executar

```bash
python src/database.py
```

O script cria o arquivo `mesafartai.db` com as tabelas `usuarios`, `doacoes` e `matches` e insere os dados iniciais de teste.

## Integrantes

| Nome completo | RGM |
|---|---|
| Guilherme Moreira Frauches Souza | 148960 |
| João Victor Araujo Silva | 158725 |
| Fabio Douglas dos Santos Filho | 160787 |

## Disciplina

Machine Learning & Chatbots
