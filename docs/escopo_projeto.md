# Escopo do Projeto – MESAFARTAI

## 1. Problema de negócio

Todos os dias, feirantes, supermercados, restaurantes e produtores descartam alimentos próprios para consumo por causa da proximidade da validade, de pequenos defeitos estéticos ou de excesso de estoque. Ao mesmo tempo, ONGs, abrigos e cozinhas comunitárias enfrentam escassez de suprimentos para atender famílias em situação de vulnerabilidade.

O gargalo não é a falta de comida, e sim a falta de logística ágil e de comunicação eficiente. Um comerciante não tem tempo de preencher formulários extensos para doar 30 kg de alimento que vencem em 24 horas, e a doação acaba no lixo.

O MESAFARTAI resolve isso com um chat: o doador escreve uma mensagem informal, o sistema entende a intenção, extrai os dados da doação e indica a ONG mais próxima para a coleta.

## 2. Público-alvo

| Perfil | Quem é | O que precisa | Como usa o sistema |
|---|---|---|---|
| **Doador** | Supermercados, feirantes, restaurantes, padarias e produtores com excedente de alimentos | Doar rápido, sem burocracia, antes do alimento vencer | Informa a doação em uma mensagem de chat e acompanha o status |
| **ONG** | ONGs, abrigos e cozinhas comunitárias | Receber alimentos próximos e dentro da validade | Solicita alimentos, consulta doações disponíveis e o status das coletas |

A alternância entre os perfis é feita na barra lateral da interface (Sou Doador | Sou ONG).

## 3. Escopo das intenções tratadas

| Intenção | Descrição | Exemplo de mensagem |
|---|---|---|
| `cadastrar_doacao` | Doador informa um alimento disponível para doação | "Tenho 30 kg de tomate que vencem amanhã" |
| `solicitar_alimentos` | ONG pede alimentos ou consulta o que está disponível | "Precisamos de arroz e feijão para o almoço de sábado" |
| `consultar_status` | Usuário pergunta sobre uma doação ou coleta já registrada | "Já vieram buscar a minha doação?" |
| `fora_de_escopo` | Mensagem sem relação com doação de alimentos | "Qual a previsão do tempo hoje?" |

Quando a confiança da classificação fica abaixo do threshold (ex.: 0,60), o sistema não assume uma intenção e responde com uma mensagem de fallback amigável, pedindo que o usuário reformule.

## 4. Dados coletados no chat

Extraídos da mensagem por Regex:

- **Tipo de alimento**: tomate, arroz, pão, marmitas etc.
- **Quantidade**: valor e unidade (kg, caixas, unidades).
- **Prazo de validade**: hoje, amanhã, horário (ex.: 18h) ou data.

Vindos do cadastro do usuário:

- Nome, tipo (DOADOR ou ONG), CEP, latitude, longitude e telefone.

Gerados pelo sistema:

- Status da doação (ex.: DISPONIVEL).
- Match logístico: ONG selecionada, distância em km e data do match.

## 5. Fora do escopo

- Pagamentos ou transações financeiras.
- Rastreamento em tempo real do transporte.
- Validação sanitária dos alimentos doados.

## 6. Identidade visual – Logotipo

Arquivo: `assets/logo_mesafartai.png`

Requisito: unir os conceitos de alimento/acolhimento e tecnologia/IA assistiva.

Ferramenta utilizada: Claude (Anthropic)

Prompt exato utilizado:

```
gere uma logo e me manda
```

Observação: o pedido foi feito na mesma conversa em que o Claude montou a documentação do projeto, então ele já tinha o nome MESAFARTAI e o escopo como contexto. A logo foi desenhada em vetor (SVG) e convertida para PNG.
