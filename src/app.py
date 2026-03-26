# app.py
import streamlit as st
import pandas as pd

# Importando nossos módulos locais
from core.config import PERFIS_RISCO
from data.data_market import baixar_dados_historicos, extrair_precos_atuais
from domain.optimzer import calcular_pesos_alvo_globais
from domain.rebalancer import gerar_ordens_compra
from ui.charts import plotar_alocacao_final


st.set_page_config(page_title="Terminal de Investimentos IA", layout="wide")

st.title("🚀 Terminal de Aporte Inteligente")
st.markdown("---")

# 1. SIDEBAR: Inputs do Usuário
with st.sidebar:
    st.header("⚙️ Configurações de Aporte")
    perfil_selecionado = st.selectbox("Seu Perfil de Risco", list(PERFIS_RISCO.keys()), index=1)
    aporte_valor = st.number_input("Valor do Aporte Mensal (R$)", min_value=0.0, value=1500.0, step=100.0)
    
    st.divider()
    st.write("**Universo de Ativos**")
    acoes_input = st.text_area("Ações (separadas por vírgula)", "ITUB4.SA, PETR4.SA, EGIE3.SA, VALE3.SA")
    fiis_input = st.text_area("FIIs (separados por vírgula)", "HGLG11.SA, BTLG11.SA, VILG11.SA, XPML11.SA, KNCR11.SA")

lista_acoes = [a.strip().upper() for a in acoes_input.split(",")]
lista_fiis = [f.strip().upper() for f in fiis_input.split(",")]
todos_ativos = list(set(lista_acoes + lista_fiis))

# 2. ÁREA CENTRAL: Posição Atual
st.subheader("📋 Sua Posição Atual na Corretora")
df_input = pd.DataFrame({"Ativo": todos_ativos, "Valor_Atual_RS": [0.0] * len(todos_ativos)})
df_posicao = st.data_editor(df_input, use_container_width=True, hide_index=True)

# 3. MOTOR PRINCIPAL
if st.button("🔥 Calcular Otimização e Gerar Ordens", type="primary"):
    with st.spinner("Consultando B3 e processando algoritmos..."):
        try:
            carteira_atual = dict(zip(df_posicao["Ativo"], df_posicao["Valor_Atual_RS"]))
            
            # Etapa 1: Dados
            df_historico = baixar_dados_historicos(todos_ativos)
            if df_historico.empty:
                st.error("Erro crítico: Não foi possível baixar os preços da B3.")
                st.stop()
                
            precos_atuais = extrair_precos_atuais(df_historico)
            
            # Etapa 2: Otimização
            pesos_alvo = calcular_pesos_alvo_globais(
                df_historico, 
                lista_acoes, 
                lista_fiis, 
                PERFIS_RISCO[perfil_selecionado]
            )
            
            # Etapa 3: Rebalanceamento
            df_ordens, sobra_caixa = gerar_ordens_compra(carteira_atual, pesos_alvo, precos_atuais, aporte_valor)
            
            # Etapa 4: Consolidação Visual
            for _, linha in df_ordens.iterrows():
                carteira_atual[linha['Ativo']] += linha['Total']
            carteira_atual['CAIXA'] = sobra_caixa

            # --- EXIBIÇÃO ---
            col1, col2 = st.columns([1, 1])
            with col1:
                st.success("✅ Ordens de Compra Geradas")
                if not df_ordens.empty:
                    st.table(df_ordens.style.format({"Preço": "R$ {:.2f}", "Total": "R$ {:.2f}"}))
                    st.metric("Sobra no Caixa", f"R$ {sobra_caixa:.2f}")
                else:
                    st.warning("Nenhuma ordem necessária para este aporte.")

            with col2:
                st.write("**Alocação Final Consolidada**")
                fig = plotar_alocacao_final(carteira_atual, lista_acoes, lista_fiis)
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Ocorreu um erro inesperado na execução: {e}")