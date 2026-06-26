import { useLocation, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import SceneCard from '../components/SceneCard';

export default function Results() {
  const location = useLocation();
  const results = location.state?.results || [];

  if (!results.length) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <p className="text-xl text-white/50 mb-4">No results found or page accessed directly.</p>
        <Link to="/" className="text-white/70 hover:text-white flex items-center gap-2">
          <ArrowLeft size={16} /> Go back home
        </Link>
      </div>
    );
  }

  return (
    <>
      <div className="fixed inset-0 bg-gradient-to-b from-[#1a2e21] via-[#050906] to-black -z-10" />
      <div className="max-w-6xl mx-auto pb-20 relative z-10">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Generated Assets</h1>
            <p className="text-white/60">We analyzed your script and found these assets.</p>
          </div>
          <Link to="/" className="px-4 py-2 rounded-lg glass-panel hover:bg-white/5 transition-colors text-sm font-medium">
            New Script
          </Link>
        </div>

        <div className="space-y-8">
          {results.map((scene, index) => (
            <motion.div
              key={scene.scene}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <SceneCard data={scene} />
            </motion.div>
          ))}
        </div>
      </div>
    </>
  );
}
