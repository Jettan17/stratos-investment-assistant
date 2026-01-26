# Stratos Investment Assistant - Project Overview

## Project Settings

| Setting | Value |
|---------|-------|
| Scope | Medium |
| Final Product | Web Application |
| Usage | Personal |
| Connection | Public |
| Visual Style | Modern |

## Objective

Build a conservative long-term investment assistant that helps users identify stable stocks suitable for a 10+ year investment horizon.

## Key Features

### Phase 1 (Complete - Checkpointed 2026-01-26)
- [x] Project structure setup
- [x] Basic stock screener UI
- [x] FastAPI backend with stock endpoints
- [x] TDD test infrastructure
- [x] Checkpoint saved: [2026-01-26-initial-project-setup.md](checkpoints/2026-01-26-initial-project-setup.md)

### Phase 2 (Complete - Checkpointed 2026-01-26)
- [x] Real stock data from yfinance
- [x] Database persistence (SQLite + SQLAlchemy)
- [x] User preferences storage
- [x] Advanced screening filters (beta, debt/equity)
- [x] Frontend connected to backend API
- [x] Stock results table with color-coded metrics
- [x] Checkpoint saved: [2026-01-26-phase2-real-data-integration.md](checkpoints/2026-01-26-phase2-real-data-integration.md)

### Phase 3 (Complete - Checkpointed 2026-01-26)
- [x] AI-powered recommendations (rule-based with OpenAI fallback)
- [x] Portfolio tracking with real-time values
- [x] Price alerts system
- [x] Stratos logo and branding
- [x] Checkpoint saved: [2026-01-26-phase3-ai-and-portfolio.md](checkpoints/2026-01-26-phase3-ai-and-portfolio.md)

### Phase 4 (Future)
- [ ] Brokerage API integration
- [ ] Historical price charts
- [ ] Portfolio diversification analysis
- [ ] Export functionality (CSV/PDF)
- [ ] Email/push notifications

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Next.js 15    │────▶│   FastAPI       │────▶│   yfinance      │
│   Frontend      │     │   Backend       │     │   Stock Data    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │                 │
                        │   SQLite/       │
                        │   PostgreSQL    │
                        │                 │
                        └─────────────────┘
```

## Investment Criteria

For conservative stock selection:

| Metric | Target Range |
|--------|--------------|
| Dividend Yield | > 2% |
| P/E Ratio | < 25 |
| Market Cap | > $10B |
| Beta | < 1.0 |
| Debt/Equity | < 0.5 |

## Data Sources

- **Primary**: yfinance (Yahoo Finance API)
- **Secondary**: Alpha Vantage free tier
- **Future**: Bloomberg, Reuters (premium)
