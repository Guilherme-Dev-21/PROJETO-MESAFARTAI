# Relatório de Execução – Fase 1 / Etapa 2 (AC-3)

**Projeto:** MESAFARTAI – Logística e Inteligência Assistiva no Combate à Fome
**Módulo:** `src/nlu.py` – Motor NLU com TF-IDF + Random Forest e Trava de Threshold

## 1. Número de árvores utilizadas no motor NLU

Foram utilizadas **80 árvores de decisão** (`RandomForestClassifier(n_estimators=80, random_state=42)`).

## 2. Valor de threshold utilizado no limiar de confiança

O limiar de confiança foi **0.60 (60%)** (`MotorNLU(limiar_threshold=0.60)`). Toda mensagem com confiança máxima abaixo de 0.60, ou classificada como `fora_de_escopo`, cai no fallback e o usuário é convidado a reformular o pedido.

## 3. Resultado da primeira execução

Comando executado: `python src/nlu.py`

```
 [NLU] Modelo Random Forest e Vetorizador TF-IDF treinados com sucesso!

--- BATERIA DE TESTES DE ESTRESSE NLU ---

Entrada: 'Tenho 30 kg de banana para doar'
Intenção: cadastrar_doacao | Confiança: 0.93
Retorno: Intenção 'cadastrar_doacao' identificada com 92.5% de confiança.

Entrada: 'Nossa instituição precisa de mantimentos'
Intenção: fallback | Confiança: 0.41
Retorno: Desculpe, não consegui entender com clareza o seu pedido.
Você pode refazer a mensagem informando se deseja **doar alimentos** ou **solicitar doações para uma ONG**?

Entrada: 'Qual é a receita de bolo de cenoura?'
Intenção: fallback | Confiança: 0.49
Retorno: Desculpe, não consegui entender com clareza o seu pedido.
Você pode refazer a mensagem informando se deseja **doar alimentos** ou **solicitar doações para uma ONG**?

Entrada: 'coisa comida doar la'
Intenção: fallback | Confiança: 0.42
Retorno: Desculpe, não consegui entender com clareza o seu pedido.
Você pode refazer a mensagem informando se deseja **doar alimentos** ou **solicitar doações para uma ONG**?
```

### Análise dos resultados

| Frase de teste | Resultado | Avaliação |
|---|---|---|
| Tenho 30 kg de banana para doar | `cadastrar_doacao` (0.93) | Correto. A frase está na base de treino. |
| Nossa instituição precisa de mantimentos | fallback (0.41) | Seguro, mas não ideal. É um pedido válido de `solicitar_alimentos`. |
| Qual é a receita de bolo de cenoura? | fallback (0.49) | Correto. A frase está fora de escopo. |
| coisa comida doar la | fallback (0.42) | Correto. A frase é ambígua. |

Ao inspecionar as probabilidades de cada classe, nos três casos de fallback a classe com maior probabilidade era `cadastrar_doacao` (0.41, 0.49 e 0.42). Ou seja, sem a trava de threshold o sistema teria registrado três doações inexistentes. A trava cumpriu seu papel de impedir decisões erradas quando o modelo não tem certeza.

Na frase "Nossa instituição precisa de mantimentos", a classe correta (`solicitar_alimentos`) ficou em segundo lugar com 0.31. As palavras "instituição" e "mantimentos" não aparecem em nenhuma frase de treino, então o modelo não tinha vocabulário para reconhecer o pedido.

## 4. Como melhorar os resultados e aumentar a confiança

- **Aumentar e equilibrar a base de treino.** Hoje são apenas 21 frases, com 8 de `cadastrar_doacao` e 4 de `consultar_status`. O modelo tende a "chutar" a classe com mais exemplos. O ideal é ter dezenas de frases por intenção, em quantidade parecida.
- **Variar o vocabulário com sinônimos.** Incluir termos como "instituição", "mantimentos", "cesta básica", "entidade", "doar", "contribuir", "ceder", além de gírias e erros de digitação comuns em chat.
- **Pré-processar o texto.** Converter para minúsculas, remover acentos e stopwords ("de", "para", "o") e aplicar stemming ou lematização (ex.: spaCy), para que "doação", "doar" e "doando" sejam tratados como a mesma ideia.
- **Usar n-gramas de caracteres.** `TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))` reconhece pedaços de palavras e lida melhor com palavras novas e erros de grafia.
- **Ajustar os hiperparâmetros do Random Forest.** Testar mais árvores (`n_estimators` entre 200 e 500), `class_weight="balanced"` e outros valores de `max_depth`, com validação cruzada (`GridSearchCV`).
- **Calibrar o threshold com dados reais.** Medir acertos e erros com um conjunto de teste separado e escolher o limiar que equilibra "fallback desnecessário" e "intenção errada aceita".
- **Aprender com o uso.** Registrar as mensagens que caíram no fallback, rotular manualmente e incluí-las no treino periodicamente.

## 5. Por que o Random Forest foi o melhor método para esta fase

- **Fornece probabilidades por classe** (`predict_proba`), o que viabiliza diretamente a trava de threshold e o fallback, requisito central desta etapa.
- **Combina várias árvores por votação**, o que reduz o risco de overfitting em comparação com uma única árvore de decisão, algo importante com uma base de treino pequena.
- **Funciona bem com poucos dados e com a matriz esparsa do TF-IDF**, sem exigir normalização dos dados nem o grande volume que redes neurais e modelos de linguagem exigiriam.
- **Treina em frações de segundo e é fácil de explicar**, o que permite retreinar o modelo sempre que novas frases forem adicionadas.
- **É estável e reproduzível** com `random_state=42`, então todos os integrantes obtêm os mesmos resultados ao rodar o projeto.
- **Faz parte do modelo híbrido da disciplina:** o Random Forest descobre a intenção da mensagem, e nas próximas etapas o Regex extrai as entidades e o KNN faz o matchmaking com a ONG mais próxima.
