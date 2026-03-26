# domain/optimizer.py
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, expected_returns

def otimizar_classe(df_classe: pd.DataFrame) -> dict:
    """Gera a fronteira eficiente usando covariância robusta (Ledoit-Wolf)."""
    if df_classe.empty or df_classe.shape[1] == 0: 
        return {}
        
    if df_classe.shape[1] == 1: 
        return {df_classe.columns[0]: 1.0}
        
    try:
        mu = expected_returns.mean_historical_return(df_classe)
        S = risk_models.CovarianceShrinkage(df_classe).ledoit_wolf()
        S = risk_models.fix_nonpositive_semidefinite(S)
        
        ef = EfficientFrontier(mu, S)
        
        num_ativos = len(df_classe.columns)
        limite_peso = max(0.35, 1.0 / num_ativos)
        ef.add_constraint(lambda w: w <= limite_peso)
        
        ef.max_sharpe()
        return ef.clean_weights()
    except Exception:
        # Fallback de segurança: pesos iguais
        num_ativos = len(df_classe.columns)
        return {col: 1.0 / num_ativos for col in df_classe.columns}

def calcular_pesos_alvo_globais(df_limpo: pd.DataFrame, lista_acoes: list, lista_fiis: list, macro_alocacao: dict) -> dict:
    """Cruza a otimização individual com o perfil de risco do usuário."""
    acoes_disponiveis = [a for a in lista_acoes if a in df_limpo.columns]
    fiis_disponiveis = [f for f in lista_fiis if f in df_limpo.columns]
    
    pesos_acoes = otimizar_classe(df_limpo[acoes_disponiveis]) if acoes_disponiveis else {}
    pesos_fiis = otimizar_classe(df_limpo[fiis_disponiveis]) if fiis_disponiveis else {}
    
    pesos_alvo = {}
    for ativo, peso in pesos_acoes.items(): 
        pesos_alvo[ativo] = peso * macro_alocacao["acoes"]
        
    for ativo, peso in pesos_fiis.items(): 
        pesos_alvo[ativo] = peso * macro_alocacao["fiis"]
        
    return pesos_alvo