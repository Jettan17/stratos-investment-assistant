# Stratos Investment Assistant

A conservative long-term investment assistant that helps users identify stable stocks suitable for a 10+ year investment horizon.

## Features

- **Stock Screener** - Filter stocks by dividend yield, P/E ratio, market cap, beta, and debt/equity
- **AI-Powered Analysis** - Get buy/hold/sell recommendations with confidence scores
- **Portfolio Tracking** - Track holdings with real-time values and gain/loss calculations
- **Price Alerts** - Set alerts for when stocks hit your target prices
- **Conservative Focus** - Curated universe of 33 blue-chip dividend-paying stocks

## Live Demo

| Service | URL |
|---------|-----|
| **Frontend** | [stratos-investment-assistant.vercel.app](https://stratos-investment-assistant.vercel.app) |
| **Backend API** | [stratos-backend-production-273d.up.railway.app](https://stratos-backend-production-273d.up.railway.app) |
| **API Docs** | [stratos-backend-production-273d.up.railway.app/docs](https://stratos-backend-production-273d.up.railway.app/docs) |

## Tech Stack

| Layer | Technology | Hosting |
|-------|------------|---------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS | Vercel |
| Backend | FastAPI, Python 3.11, SQLAlchemy | Railway |
| Database | SQLite (dev), PostgreSQL (prod) | - |
| Data Source | yfinance (Yahoo Finance API) | - |

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

API available at http://localhost:8000
API docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at http://localhost:3000

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/stocks/screen` | Screen stocks with filters |
| `GET /api/v1/stocks/{symbol}` | Get stock details |
| `GET /api/v1/analysis/quick/{symbol}` | Get AI analysis |
| `GET /api/v1/portfolio/` | Get portfolio with values |
| `POST /api/v1/portfolio/holdings` | Add portfolio holding |
| `GET /api/v1/alerts/` | Get price alerts |
| `POST /api/v1/alerts/` | Create price alert |
| `GET /api/v1/alerts/check/all` | Check all alerts |

## Conservative Stock Universe

33 blue-chip stocks across sectors:

| Sector | Stocks |
|--------|--------|
| Healthcare | JNJ, PFE, ABBV, MRK, UNH |
| Consumer Staples | PG, KO, PEP, WMT, COST |
| Financials | JPM, BRK-B, V, MA, BAC |
| Technology | MSFT, AAPL, CSCO, IBM, INTC |
| Utilities | NEE, DUK, SO, D, AEP |
| Industrials | MMM, HON, CAT, UPS, RTX |
| Energy | XOM, CVX, COP |
| REITs | O, SPG, AMT |

## Default Screening Criteria

| Metric | Target |
|--------|--------|
| Dividend Yield | > 2% |
| P/E Ratio | < 25 |
| Market Cap | > $10B |
| Beta | < 1.0 |
| Debt/Equity | < 0.5 |

## Project Structure

```
stratos-investment-assistant/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── stocks.py      # Stock screening
│   │   │   ├── analysis.py    # AI recommendations
│   │   │   ├── portfolio.py   # Portfolio tracking
│   │   │   ├── alerts.py      # Price alerts
│   │   │   └── preferences.py # User preferences
│   │   └── main.py
│   ├── models/
│   │   ├── database.py        # SQLAlchemy setup
│   │   └── preferences.py     # Data models
│   ├── services/
│   │   ├── stock_service.py   # yfinance integration
│   │   └── ai_service.py      # AI analysis
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx       # Main screener
│   │   │   └── portfolio/     # Portfolio page
│   │   ├── components/
│   │   │   ├── Logo.tsx
│   │   │   ├── ScreenerForm.tsx
│   │   │   ├── StockTable.tsx
│   │   │   ├── StockAnalysisCard.tsx
│   │   │   ├── PortfolioCard.tsx
│   │   │   └── AlertsCard.tsx
│   │   └── lib/
│   │       └── api.ts         # API client
│   └── tests/
└── docs/
    ├── 01-project-overview.md
    └── checkpoints/
```

## Running Tests

```bash
# Backend
cd backend
python -m pytest tests/ -v

# Frontend
cd frontend
npm run test
```

## Screenshots

### Stock Screener
Filter conservative stocks by your criteria and get instant results with color-coded metrics.

### Portfolio Tracker
Track your holdings with real-time prices, gain/loss calculations, and performance metrics.

### Price Alerts
Set price targets and get notified when stocks hit your levels.

## Development Status

- [x] Phase 1: Project setup, basic UI, TDD infrastructure
- [x] Phase 2: Real stock data, database, frontend integration
- [x] Phase 3: AI analysis, portfolio tracking, price alerts
- [ ] Phase 4: Historical charts, diversification analysis, exports

## License

MIT
