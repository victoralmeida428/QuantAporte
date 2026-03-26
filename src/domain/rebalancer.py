# domain/rebalancer.py
import pandas as pd

def gerar_ordens_compra(carteira_atual: dict, pesos_alvo: dict, precos_atuais: pd.Series, aporte_valor: float) -> tuple:
    """Calcula a quantidade de cotas inteiras a comprar sem estourar o orçamento."""
    patrimonio_futuro = sum(carteira_atual.values()) + aporte_valor
    dinheiro_restante = aporte_valor
    ordens = []
    
    # 1. Identificar déficits
    deficits = {}
    for ativo, peso_ideal in pesos_alvo.items():
        if ativo not in precos_atuais.index:
            continue
            
        valor_ideal = patrimonio_futuro * peso_ideal
        valor_atual = carteira_atual.get(ativo, 0.0)
        
        if valor_ideal > valor_atual:
            deficits[ativo] = valor_ideal - valor_atual
            
    # 2. Priorizar compras
    ativos_ordenados = sorted(deficits.items(), key=lambda x: x[1], reverse=True)
    
    # 3. Executar lógica de arredondamento financeiro
    for ativo, buraco in ativos_ordenados:
        preco = precos_atuais[ativo]
        if preco <= 0:
            continue
            
        qtd_cotas = int(min(buraco, dinheiro_restante) // preco)
        
        if qtd_cotas > 0:
            valor_gasto = qtd_cotas * preco
            ordens.append({
                "Ativo": ativo, 
                "Qtd": qtd_cotas, 
                "Preço": preco, 
                "Total": valor_gasto
            })
            dinheiro_restante -= valor_gasto
            
    return pd.DataFrame(ordens), dinheiro_restante