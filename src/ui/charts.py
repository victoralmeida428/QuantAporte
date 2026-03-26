# ui/charts.py
import matplotlib.pyplot as plt
import pandas as pd

def plotar_alocacao_final(carteira_atual_dict: dict, lista_acoes: list, lista_fiis: list):
    """Gera um gráfico de barras colorizado da posição final consolidada."""
    df_final = pd.Series(carteira_atual_dict).sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    colors = []
    for ticker in df_final.index:
        if ticker in lista_acoes: colors.append('#3498db')      # Azul
        elif ticker in lista_fiis: colors.append('#2ecc71')     # Verde
        elif ticker == 'CAIXA': colors.append('#95a5a6')        # Cinza
        else: colors.append('#f1c40f')                          # Amarelo (Outros)
            
    ax.bar(df_final.index, df_final.values.tolist(), color=colors)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Patrimônio Total (R$)")
    plt.title("Alocação Consolidada Pós-Aporte")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    return fig