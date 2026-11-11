import json
from datetime import datetime, timezone
import yfinance as yf
import feedparser

def obter_noticias():
    url_feed = "https://finance.yahoo.com/news/rssindex"
    feed = feedparser.parse(url_feed)
    noticias = []
    
    for item in feed.entries[:10]:
        noticias.append({
            "d": datetime.now().strftime("%d %b").lower(),
            "s": "Yahoo Finance",
            "c": "Mercado",
            "t": item.title,
            "k": [],
            "u": item.link
        })
    return noticias

def obter_movimentacoes():
    tickers = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOGL", "TSLA", "AMD", "INTC"]
    acoes = []
    
    for ticker in tickers:
        try:
            ativo = yf.Ticker(ticker)
            hist = ativo.history(period="2d")
            if len(hist) >= 2:
                fecho_anterior = float(hist['Close'].iloc[-2])
                fecho_atual = float(hist['Close'].iloc[-1])
                variacao = ((fecho_atual - fecho_anterior) / fecho_anterior) * 100
                direcao = "up" if variacao >= 0 else "dn"
                
                acoes.append({
                    "k": ticker,
                    "n": ativo.info.get("shortName", ticker),
                    "d": direcao,
                    "x": f"Variação de {variacao:+.2f}% nas últimas sessões.",
                    "var_abs": abs(variacao)
                })
        except Exception:
            continue
            
    # Ordenar pelas maiores variações usando diretamente o valor numérico
    acoes.sort(key=lambda item: item["var_abs"], reverse=True)
    
    # Limpar a variável auxiliar antes de gravar
    for item in acoes:
        del item["var_abs"]
        
    return acoes[:8]

def main():
    feed_data = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "news": obter_noticias(),
        "stocks": obter_movimentacoes()
    }
    
    with open("feed.json", "w", encoding="utf-8") as f:
        json.dump(feed_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
