# 🤖 AI Customer Support Chat Widget

A smart, embeddable AI chat widget that helps businesses handle customer inquiries — like a virtual support employee available 24/7.

Built with:

- 🧠 OpenAI GPT (via API)
- ⚙️ FastAPI backend (Python)
- 💬 React floating chat frontend

## 🚀 Features

- ✨ AI-powered customer support
- 📂 Memory per user (`user_id` based)
- 💬 Floating chat widget for websites
- 🔗 Backend integration with OpenAI
- 🛡️ Environment-safe (no `.env` committed)

## 📆 Tech Stack

| Layer     | Stack              |
| --------- | ------------------ |
| Frontend  | React + Vite       |
| Backend   | FastAPI (Python)   |
| AI Engine | OpenAI API (GPT-4) |

## 💠 How It Works

1. Users interact with a React-based floating widget
2. Messages are sent to a FastAPI backend
3. The backend handles:

   - User session tracking
   - Message history
   - OpenAI GPT responses

4. Responses are streamed back to the frontend

## 🧪 Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
```

Run the API server:

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Make sure your API is accessible at `http://localhost:8000`.

## 🔐 Environment

- `.env` is **ignored by Git**
- Use `.env.example` to share template configs

## 🌍 Deployment

- Deploy backend to **Render**, **Railway**, or **EC2**
- Deploy frontend to **Vercel** or **Netlify**

## 📦 Coming Soon

- Admin dashboard for chat logs
- Chat transfer to human agent
- File upload support
- Business-specific knowledge base

## 📜 License

MIT — free to use, modify, and scale.

---

Made with ❤️ by Femi Atunnise
