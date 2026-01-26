import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Home from "./page";

// Mock the API module
vi.mock("@/lib/api", () => ({
  screenStocks: vi.fn().mockResolvedValue({
    stocks: [
      {
        symbol: "JNJ",
        name: "Johnson & Johnson",
        sector: "Healthcare",
        price: 155.5,
        dividend_yield: 3.0,
        pe_ratio: 15.2,
        market_cap: 375.0,
        beta: 0.55,
      },
    ],
    total: 1,
    filters_applied: {},
  }),
  getAvailableSectors: vi.fn().mockResolvedValue(["Healthcare", "Technology"]),
  addToWatchlist: vi.fn().mockResolvedValue({ symbol: "JNJ", is_active: true }),
}));

describe("Home Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the application logo and tagline", () => {
    render(<Home />);
    // Logo renders the text "Stratos"
    expect(screen.getByText("Stratos")).toBeInTheDocument();
    // Tagline about conservative portfolio
    expect(screen.getByText(/conservative portfolio/i)).toBeInTheDocument();
  });

  it("renders the stock screener section", () => {
    render(<Home />);
    expect(
      screen.getByRole("heading", { name: /conservative stock screener/i })
    ).toBeInTheDocument();
  });

  it("displays the investment philosophy before search", () => {
    render(<Home />);
    expect(screen.getAllByText(/long-term/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/stable/i).length).toBeGreaterThan(0);
  });

  it("has filter inputs for screening stocks", () => {
    render(<Home />);
    expect(screen.getByLabelText(/sector/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/min dividend yield/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/max p\/e ratio/i)).toBeInTheDocument();
  });

  it("has a screen stocks button", () => {
    render(<Home />);
    expect(
      screen.getByRole("button", { name: /screen stocks/i })
    ).toBeInTheDocument();
  });

  it("displays results after screening", async () => {
    render(<Home />);

    const screenButton = screen.getByRole("button", { name: /screen stocks/i });
    fireEvent.click(screenButton);

    await waitFor(() => {
      expect(screen.getByText(/results/i)).toBeInTheDocument();
    });
  });

  it("shows stock data in results table", async () => {
    render(<Home />);

    const screenButton = screen.getByRole("button", { name: /screen stocks/i });
    fireEvent.click(screenButton);

    await waitFor(() => {
      expect(screen.getByText("JNJ")).toBeInTheDocument();
      expect(screen.getByText("Johnson & Johnson")).toBeInTheDocument();
    });
  });
});
