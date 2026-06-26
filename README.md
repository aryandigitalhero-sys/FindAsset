# AI Asset Finder

An intelligent creative assistant designed for video editors and content creators. It automates the tedious process of finding visual assets for short-form videos like Reels and YouTube Shorts by analyzing your script, breaking it down into scenes, and fetching the perfect b-roll, images, and GIFs.



## 🚀 Functionality

- **Intelligent Scene Splitting**: Paste your video script and our AI agent (powered by Groq & LLaMA 3) logically breaks it down into individual, coherent scenes.
- **Visual Planning**: For each scene, the AI extracts visual intent, emotional tone, and generates highly optimized search keywords.
- **Parallel Asset Search**: The backend simultaneously queries multiple free asset providers (Pexels, Pixabay, Unsplash, Giphy) to bring back high-quality videos, images, and GIFs with minimal latency.
- **AI Background Eraser**: Built-in background removal using `rembg` allows you to instantly isolate subjects and icons directly within the app before downloading them for your edits.
- **Premium Minimalist UI**: A stunning, Apple-esque dark mode interface built with React, Tailwind CSS, and Framer Motion.

## 💻 Tech Stack

### Frontend
- **Framework**: React (via Vite)
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Routing**: React Router DOM
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python)
- **AI/LLM**: Groq API (`llama3-70b-8192`)
- **Computer Vision**: `rembg` & ONNX Runtime (AI Background Removal)
- **Concurrency**: `httpx` (async HTTP client), `asyncio`
- **Resilience**: `tenacity` (retries), `aiolimiter` (rate limiting)

## 📐 Architecture

The project is structured as a decoupled monorepo:

1. **Vite/React Client (`/frontend`)**: Handles the user interface, state management, and asset presentation. It sends the raw script to the backend and displays the resulting scene-by-scene breakdown.
2. **FastAPI Server (`/backend`)**: The orchestration layer. It receives the script, queries the Groq API to analyze and split the text into JSON structured scenes, and then fans out asynchronous API calls to 4 different asset providers (Pexels, Pixabay, Unsplash, Giphy) concurrently. It also exposes an endpoint that processes images through a deep learning model (`rembg`) to remove backgrounds on the fly.
3. **Deployment**:
   - **Frontend**: Pre-configured for seamless deployment on Vercel (`vercel.json` provided).
   - **Backend**: Pre-configured for deployment on Render or Railway via Docker (`Dockerfile` and `render.yaml` provided), isolating the heavy AI models from strict serverless limitations.

## 🛠 Setup & Installation

### Prerequisites
- Node.js (v18+)
- Python 3.10+
- API Keys for: [Groq](https://console.groq.com/), [Pexels](https://www.pexels.com/api/), [Pixabay](https://pixabay.com/api/docs/), [Unsplash](https://unsplash.com/developers), and [Giphy](https://developers.giphy.com/).

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-asset-finder.git
cd ai-asset-finder
```

### 2. Setup the Backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
GROQ_API_KEY=your_groq_api_key
PEXELS_API_KEY=your_pexels_key
PIXABAY_API_KEY=your_pixabay_key
UNSPLASH_ACCESS_KEY=your_unsplash_key
GIPHY_API_KEY=your_giphy_key
```

Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Setup the Frontend
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

The app will now be running at `http://localhost:5173`.
