import re

# DESAFIO REGEX - "O Filtro Anti-Desperdício" (AC-3 Final - MESAFARTAI)
# Extrair quantidade, alimento e validade

# Mensagem de teste que o aluno deve processar:
mensagem = "Atenção: estamos doando 35 kg de leite fresco que vence em 2 dias!"

# Limpeza do texto: remove espaços extras
mensagem_limpa = re.sub(r'\s+', ' ', mensagem).strip()

# PADRÕES REGEX:
padrao_qtd = r'(\d+(?:[\.,]\d+)?)\s*(kg|quilos|caixas)'  # Deve capturar 35 kg
padrao_dias = r'(\d+)\s*dias?'                           # Deve capturar 2 dias
padrao_meses = r'(\d+)\s*m[eê]s(?:es)?'                  # Não perecível (validade em meses)
padrao_alimento = r'(?:kg|quilos|caixas)\s+de\s+(\w+)'   # Palavra após "kg de"

# 1. Quantidade e unidade
match_qtd = re.search(padrao_qtd, mensagem_limpa, re.IGNORECASE)
quantidade = float(match_qtd.group(1).replace(',', '.')) if match_qtd else 0.0
unidade = match_qtd.group(2).lower() if match_qtd else ''

# 2. Tipo de alimento
match_alimento = re.search(padrao_alimento, mensagem_limpa, re.IGNORECASE)
alimento = match_alimento.group(1).capitalize() if match_alimento else 'Não identificado'

# 3. Perecível (dias) ou não perecível (meses)
match_dias = re.search(padrao_dias, mensagem_limpa, re.IGNORECASE)
match_meses = re.search(padrao_meses, mensagem_limpa, re.IGNORECASE)

if match_dias:
    urgencia = f"ALTA (Vence em {match_dias.group(1)} dias)"
elif match_meses:
    urgencia = f"BAIXA (Vence em {match_meses.group(1)} meses)"
else:
    urgencia = "Validade não informada"

# Saída esperada no print:
print(f"Alimento: {alimento} | Quantidade: {quantidade} {unidade} | Urgência: {urgencia}")
