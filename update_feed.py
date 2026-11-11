import json
from datetime import datetime, timezone
import yfinance as yf
import feedparser

def obter_noticias():
    # Recolhe as notícias mais recentes do Yahoo Finance
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
    # As ações que queres monitorizar
    tickers = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOGL", "TSLA", "AMD", "INTC"]
    acoes = []
    
    for ticker in tickers:
        try:
            ativo = yf.Ticker(ticker)
            hist = ativo.history(period="2d")
            if len(hist) >= 2:
                fecho_anterior = hist['Close'].iloc[-2]
                fecho_atual = hist['Close'].iloc[-1]
                variacao = ((fecho_atual - fecho_anterior) / fecho_anterior) * 100
                direcao = "up" if variacao >= 0 else "dn"
                
                acoes.append({
                    "k": ticker,
                    "n": ativo.info.get("shortName", ticker),
                    "d": direcao,
                    "x": f"Variação de {variacao:+.2f}% nas últimas sessões."
                })
        except Exception:
            continue
            
    acoes.sort(key=lambda x: abs(float(x["x"].split()[1].replace("%", ""))), reverse=True)
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
