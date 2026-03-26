# =====================================================================
# MAKEFILE - ALPHA TERMINAL (Powered by UV)
# =====================================================================

.PHONY: help setup run clean

help:
	@echo "Comandos disponíveis na Mesa de Operações:"
	@echo "  make setup  - Cria o ambiente virtual e instala dependências voando com UV"
	@echo "  make run    - Inicia o terminal Streamlit isolado no ambiente"
	@echo "  make clean  - Limpa arquivos de cache e lixo temporário"

setup:
	@echo "⚡ Acionando motor de alta frequência (UV)..."
	uv sync
	@echo "✅ Setup concluído."

run:
	@echo "🚀 Iniciando o AlphaTerminal..."
	streamlit run ./src/app.py

clean:
	@echo "🧹 Varrendo o pregão (limpando cache)..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f alocacao_final_carteira.png
	@echo "✨ Terminal limpo."