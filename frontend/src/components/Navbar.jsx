import { Link } from 'react-router-dom';
import { Film } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="glass border-b border-white/10 px-6 py-4 sticky top-0 z-50">
      <div className="container mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="bg-white/10 border border-white/20 p-2 rounded-xl group-hover:bg-white/20 transition-all">
            <Film size={24} className="text-white" />
          </div>
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
            AI Asset Finder
          </span>
        </Link>
        
        <div className="flex items-center gap-6">
          <Link to="/" className="text-sm font-medium text-white/70 hover:text-white transition-colors">
            Home
          </Link>
          <Link to="/about" className="text-sm font-medium text-white/70 hover:text-white transition-colors">
            About
          </Link>
        </div>
      </div>
    </nav>
  );
}
