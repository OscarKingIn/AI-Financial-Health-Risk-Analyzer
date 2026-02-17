# FlowTrack AI | Financial Health & Risk Analyzer

FlowTrack AI is a production-ready SaaS application designed to analyze bank transaction data using AI, calculate risk scores, and generate professional financial reports.

## 🚀 Features

- **AI Categorization**: OpenAI-powered transaction classifier.
- **Fintech Risk Engine**: Proprietary logic for financial health scoring (0-100).
- **Secure Payments**: Stripe integration for report unlocking.
- **Professional Reports**: Detailed PDF exports with category breakdowns and AI recommendations.
- **Modern UI**: Clean, responsive dashboard with Dark/Light mode support.

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.11+)
- **Database**: SQLite (SQLAlchemy)
- **AI**: OpenAI API
- **Payments**: Stripe
- **PDF**: ReportLab
- **Frontend**: Tailwind CSS

## ⚙️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/OscarKingIn/AI-Financial-Health-Risk-Analyzer.git
   cd AI-Financial-Health-Risk-Analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## 📄 Deployment

This application is ready for deployment on **Render** or **Railway**. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🛡️ Security

- **Environment Variables**: All secrets (OpenAI, Stripe) are managed via `.env`.
- **Data Privacy**: Transactions are processed and discarded after report generation (if configured).

## 📊 Sample Data

A `sample_transactions.csv` is included in the root directory for testing the upload and analysis flow.

---
© 2026 FlowTrack AI. Built for financial clarity.
