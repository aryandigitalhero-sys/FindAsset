import { useState } from 'react';
import { Tag } from 'lucide-react';
import AssetGallery from './AssetGallery';

export default function SceneCard({ data }) {
  const [activeTab, setActiveTab] = useState('videos');

  const tabs = [
    { id: 'videos', label: `Videos (${data.assets.videos.length})` },
    { id: 'images', label: `Images (${data.assets.images.length})` },
    { id: 'gifs', label: `GIFs (${data.assets.gifs.length})` },
    { id: 'icons', label: `Icons (${data.assets.icons.length})` },
  ];

  return (
    <div className="glass-panel rounded-2xl overflow-hidden">
      <div className="p-6 border-b border-white/5">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 bg-white/10 text-white rounded-xl flex items-center justify-center font-bold text-xl border border-white/20">
            {data.scene}
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-medium mb-3 text-white/90">"{data.text}"</h3>
            <div className="flex flex-wrap gap-2">
              {data.keywords.map((kw, i) => (
                <span key={i} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-xs font-medium text-white/70">
                  <Tag size={12} />
                  {kw}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-black/20">
        <div className="flex border-b border-white/5 px-4 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-4 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-white text-white'
                  : 'border-transparent text-white/50 hover:text-white/80'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
        
        <div className="p-6">
          <AssetGallery assets={data.assets[activeTab]} type={activeTab} />
        </div>
      </div>
    </div>
  );
}
