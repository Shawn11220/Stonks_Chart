from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import yfinance as yf
import matplotlib.pyplot as plt
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import matplotlib.dates as mdates
import os

app = FastAPI(title="Stock Price App")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

CHART_PATH = "static/stock_chart.png"

@app.get("/", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "price": None})

@app.post("/", response_class=HTMLResponse)
def form_post(request: Request, symbol: str = Form(...)):
    symbol = symbol.upper()
    stock = yf.Ticker(symbol)
    data = stock.history(period="7d")

    if data.empty:
        price = "Symbol not found"
        return templates.TemplateResponse("index.html", {"request": request, "price": price})

    price = f"${round(data['Close'].iloc[-1], 2)}"

    # Plot trend
    plt.figure(figsize=(8, 4))
    plt.style.use("seaborn-vcolor")
    plt.plot(data.index, data['Close'], marker='o', color='#007acc', label='Close Price')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)

    plt.title(f"{symbol} - Last 7 Days", fontsize=14, weight='bold')
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    plt.tight_layout()
    plt.savefig("static/stock_chart.png")
    plt.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "price": price,
        "symbol": symbol,
        "show_chart": True
    })

@app.get("/test-image")
def test_image():
    return FileResponse("static/stock_chart.png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

