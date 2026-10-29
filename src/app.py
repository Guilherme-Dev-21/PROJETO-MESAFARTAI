import os
import sqlite3

import pandas as pd
import streamlit as st

from nlu import MotorNLU
from entities import ExtratorEntidades
from matchmaking import MotorMatchmaking

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mesafartai.db")

LAT_DOADOR, LONG_DOADOR = -23.615, -46.785

REFEICOES_POR_KG = 2

st.set_page_config(
    page_title="MESAFARTAI - Combate à Fome",
    page_icon="🍽️",
    layout="wide"
)


@st.cache_resource
def carregar_motores():
    return MotorNLU(), ExtratorEntidades(), MotorMatchmaking(db_path=DB_PATH)


nlu, extrator, matchmaker = carregar_motores()


def registrar_doacao(entidades, match):
    """Grava a doação e o match logístico no SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doacoes (doador_id, descricao_alimento, quantidade_kg, data_validade, status)
        VALUES (NULL, ?, ?, ?, ?)
    """, (
        entidades["alimento"],
        entidades["quantidade_kg"],
        entidades["data_validade"],
        "ENCAMINHADA" if match else "DISPONIVEL"
    ))
    doacao_id = cursor.lastrowid
    if match:
        cursor.execute("""
            INSERT INTO matches (doacao_id, ong_id, distancia_km)
            VALUES (?, ?, ?)
        """, (doacao_id, match["ong_id"], match["distancia_estimada"]))
    conn.commit()
    conn.close()


st.title("🍽️ MESAFARTAI")
st.caption("Inteligência Artificial conectando doadores de alimentos a ONGs • ODS 2 - Fome Zero")

aba_chat, aba_dashboard = st.tabs(["💬 Chatbot de Doações", "📊 Dashboard de Impacto Social"])

with aba_chat:
    st.subheader("Conversar com o Assistente de Doações")

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = [
            {
                "role": "assistant",
                "content": "Olá! 👋 Sou o assistente do **MESAFARTAI**. "
                           "Conte o que você deseja **doar** (alimento, quantidade em kg e validade) "
                           "ou se sua ONG precisa **solicitar alimentos**."
            }
        ]

    for msg in st.session_state.mensagens:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ex: Tenho 20 kg de arroz para doar hoje no centro"):
        st.session_state.mensagens.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        resultado = nlu.processar_mensagem(prompt)
        intencao, confianca = resultado["intencao"], resultado["confianca"]

        if intencao == "cadastrar_doacao":
            entidades = extrator.processar_texto(prompt)
            match = matchmaker.encontrar_ong_mais_proxima(LAT_DOADOR, LONG_DOADOR)
            registrar_doacao(entidades, match)

            resposta = f"**Doação Registrada com Sucesso!**\n\n" \
                       f"• **Item:** {entidades['alimento']}  \n" \
                       f"• **Quantidade:** {entidades['quantidade_kg']} kg  \n" \
                       f"• **Validade Estimada:** {entidades['data_validade']}\n\n"

            if match:
                resposta += f"**Match Logístico (KNN):** Encaminhado para **{match['ong_nome']}** " \
                            f"(~{match['distancia_estimada']} km)."

        elif intencao == "solicitar_alimentos":
            resposta = "Entendemos seu pedido. Estamos buscando doações disponíveis próximas a você no banco de dados."
        elif intencao == "consultar_status":
            resposta = "Você pode acompanhar as doações e os matches realizados na aba **📊 Dashboard de Impacto Social**."
        else:
            resposta = "Desculpe, não entendi perfeitamente sua mensagem. Poderia informar o alimento e a quantidade em kg?"

        resposta += f"\n\n_Intenção: `{intencao}` • Confiança: {confianca * 100:.1f}%_"

        st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        st.chat_message("assistant").write(resposta)

with aba_dashboard:
    st.subheader("Indicadores Logísticos e Sociais em Tempo Real")

    conn = sqlite3.connect(DB_PATH)
    df_ongs = pd.read_sql_query("SELECT * FROM usuarios WHERE tipo = 'ONG'", conn)
    df_doacoes = pd.read_sql_query("""
        SELECT d.id, d.descricao_alimento AS alimento, d.quantidade_kg, d.data_validade,
               d.status, u.nome AS ong_destino, m.distancia_km
        FROM doacoes d
        LEFT JOIN matches m ON m.doacao_id = d.id
        LEFT JOIN usuarios u ON u.id = m.ong_id
        ORDER BY d.id DESC
    """, conn)
    conn.close()

    total_kg = float(df_doacoes["quantidade_kg"].sum()) if not df_doacoes.empty else 0.0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de ONGs Ativas", len(df_ongs))
    col2.metric("Alimentos Arrecadados (kg)", f"{total_kg:,.1f} kg", f"{len(df_doacoes)} doações")
    col3.metric("Refeições Estimadas Proporcionadas", f"~{int(total_kg * REFEICOES_POR_KG):,} refeições", "ODS 2")

    st.markdown("---")
    st.write("### 🏠 Unidades de Atendimento Cadastradas")
    st.dataframe(df_ongs[["id", "nome", "latitude", "longitude"]], width="stretch")

    st.write("### 📦 Doações Registradas")
    if df_doacoes.empty:
        st.info("Nenhuma doação registrada ainda. Use o chatbot para cadastrar a primeira!")
    else:
        st.bar_chart(df_doacoes.groupby("alimento")["quantidade_kg"].sum())
        st.dataframe(df_doacoes, width="stretch")
