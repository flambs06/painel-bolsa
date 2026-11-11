import json
import urllib.request
from datetime import datetime, timezone
import yfinance as yf
import feedparser

def obter_noticias():
    # Feed de Mercados e Economia em Português de Portugal (sem bloqueios)
    url_feed = "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=pt-PT&gl=PT&ceid=PT:pt-150"
    
    req = urllib.request.Request(
        url_feed,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    
    noticias = []
    try:
        conteudo = urllib.request.urlopen(req, timeout=10).read()
        feed = feedparser.parse(conteudo)
        
        for item in feed.entries[:8]:
            # Separar o título da fonte
            partes = item.title.rsplit(" - ", 1)
            titulo = partes[0]
            fonte = partes[1] if len(partes) > 1 else "Mercado"
            
            noticias.append({
                "d": datetime.now().strftime("%d %b").lower(),
                "s": fonte,
                "c": "Mercado",
                "t": titulo,
                "k": [],
                "u": item.link
            })
    except Exception as e:
        print(f"Erro ao carregar notícias: {e}")
        
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
            
    acoes.sort(key=lambda item: item["var_abs"], reverse=True)
    
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
