# AI Financial Health & Risk Analyzer Deployment

This application is ready to be deployed on **Render** or **Railway**.

## Deployment Steps:

1.  **Repository**: Push this codebase to a GitHub repository.
2.  **Web Service**: Create a new Web Service on Render.
3.  **Build Command**: `pip install -r requirements.txt`
4.  **Start Command**: `gunicorn "app:create_app()"`
5.  **Environment Variables**:
    *   `FLASK_APP`: `app.py`
    *   `FLASK_DEBUG`: `False`
    *   `SECRET_KEY`: (Any secure random string)
    *   `DATABASE_URL`: `sqlite:///database.db` (Or provide a PostgreSQL URL)
    *   `OPENAI_API_KEY`: (Your OpenAI Key)
    *   `STRIPE_SECRET_KEY`: (Your Stripe Secret Key)
    *   `STRIPE_WEBHOOK_SECRET`: (Your Stripe Webhook Secret)

## Infrastructure Files:
- `Procfile`: Configured for Gunicorn.
- `requirements.txt`: Includes all production dependencies.
- `runtime.txt`: Specified Python 3.11+.
