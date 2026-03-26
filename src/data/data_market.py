# data/market_data.py
import yfinance as yf
import pandas as pd
import datetime

def baixar_dados_historicos(ativos: list, anos: int = 3) -> pd.DataFrame:
    """Baixa e limpa os dados históricos de uma lista de ativos."""
    if not ativos:
        return pd.DataFrame()
        
    hoje = datetime.date.today()
    inicio = hoje - datetime.timedelta(days=anos * 365)
    
    data = yf.download(ativos, start=inicio, end=hoje, progress=False)
    if data is None:
        raise ValueError("dataset vazio")
    
    data = data['Close']
    
    # Se for apenas um ativo, o yfinance retorna uma Series. Convertendo para DataFrame:
    if isinstance(data, pd.Series):
        data = data.to_frame()
        
    return data.ffill().dropna()

def extrair_precos_atuais(df_historico: pd.DataFrame) -> pd.Series:
    """Retorna a última cotação válida de cada ativo."""
    if df_historico.empty:
        return pd.Series(dtype=float)
    return df_historico.iloc[-1]