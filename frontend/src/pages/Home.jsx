import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowUp, Loader2, Sparkles } from 'lucide-react';
import { generateAssets } from '../api/client';

export default function Home() {
  const [script, setScript] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleGenerate = async () => {
    if (!script.trim()) return;
    
    setLoading(true);
    try {
      const results = await generateAssets(script);
      navigate('/results', { state: { results, script } });
    } catch (error) {
      console.error("Failed to generate assets:", error);
      alert("An error occurred while generating assets.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] w-full max-w-3xl mx-auto text-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full flex flex-col items-center"
      >
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-white/70 text-sm font-medium mb-6 border border-white/20">
          <Sparkles size={16} />
          <span>AI-Powered Asset Discovery</span>
        </div>
        
        <h1 className="text-5xl md:text-6xl italic font-[var(--font-italian)] tracking-tight leading-snug md:leading-[1.2] py-2 mb-6 bg-clip-text text-transparent bg-gradient-to-b from-white via-zinc-200 to-zinc-500">
          Find the perfect assets for <br className="hidden md:block" /> your video script
        </h1>
        
        <p className="text-lg text-white/60 mb-10 max-w-2xl mx-auto">
          Paste your YouTube Shorts or Reel script below. Our AI agent will break it into scenes, understand the visual context, and automatically fetch the best b-roll, images, and GIFs for you.
        </p>
        
        <div className="w-full bg-[#1c1c1c]/80 backdrop-blur-md rounded-[1.5rem] border border-white/5 shadow-2xl flex flex-col overflow-hidden transition-all focus-within:bg-[#222222]/90">
          <textarea
            value={script}
            onChange={(e) => setScript(e.target.value)}
            placeholder="Paste your video script here to find assets..."
            className="w-full min-h-[120px] bg-transparent resize-none outline-none text-white/90 placeholder:text-white/40 text-base p-6 pb-2"
          />
          
          <div className="flex items-center justify-end p-4 pt-2">
            
            <button
              onClick={handleGenerate}
              disabled={loading || !script.trim()}
              className="flex items-center justify-center w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed text-white transition-colors"
            >
              {loading ? (
                <Loader2 size={16} className="animate-spin" />
              ) : (
                <ArrowUp size={16} />
              )}
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
