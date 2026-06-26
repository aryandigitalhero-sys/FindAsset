import { useState, useRef, useEffect } from 'react';
import { ExternalLink, Download, Video, Image as ImageIcon, Eraser, Loader2 } from 'lucide-react';

function MediaItem({ asset, type }) {
  const [hasError, setHasError] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const containerRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { rootMargin: '200px' } // Load just before scrolling into view
    );
    
    if (containerRef.current) {
      observer.observe(containerRef.current);
    }
    
    return () => {
      observer.disconnect();
    };
  }, []);

  if (hasError) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center bg-white/5 opacity-80 group-hover:opacity-100 transition-opacity text-white/50">
        {type === 'videos' ? <Video size={32} className="mb-2" /> : <ImageIcon size={32} className="mb-2" />}
        <span className="text-xs font-medium text-center px-2">Preview Unavailable</span>
      </div>
    );
  }

  if (!isVisible) {
    // Placeholder while lazy loading
    return <div ref={containerRef} className="w-full h-full bg-white/5 animate-pulse flex items-center justify-center">
       {type === 'videos' ? <Video size={24} className="text-white/20" /> : <ImageIcon size={24} className="text-white/20" />}
    </div>;
  }

  if (type === 'videos') {
    if (asset.preview) {
      return <img src={asset.preview} alt="Video Preview" loading="lazy" onError={() => setHasError(true)} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />;
    } else if (asset.url) {
      return <video src={asset.url} autoPlay muted loop onError={() => setHasError(true)} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />;
    }
  } else if (type === 'icons') {
    return <img src={asset.preview} alt="Icon Preview" loading="lazy" onError={() => setHasError(true)} className="w-16 h-16 object-contain" />;
  } else {
    if (asset.preview) {
      return <img src={asset.preview} alt="Preview" loading="lazy" onError={() => setHasError(true)} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity" />;
    }
  }

  // Fallback if no preview or url is defined at all
  return (
    <div className="w-full h-full flex flex-col items-center justify-center bg-white/5 opacity-80 group-hover:opacity-100 transition-opacity text-white/50">
      {type === 'videos' ? <Video size={32} className="mb-2" /> : <ImageIcon size={32} className="mb-2" />}
      <span className="text-xs font-medium text-center px-2">No Preview</span>
    </div>
  );
}

export default function AssetGallery({ assets, type }) {
  const [bgRemovingIds, setBgRemovingIds] = useState(new Set());

  if (!assets || assets.length === 0) {
    return (
      <div className="py-8 text-center text-white/40">
        <p>No {type} found for this scene.</p>
      </div>
    );
  }

  const handleDownload = async (e, url, id) => {
    e.preventDefault();
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      let ext = url.split('.').pop().split('?')[0];
      if (ext.length > 4) ext = type === 'videos' ? 'mp4' : 'jpg';
      a.download = `${id}.${ext}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.error("Fetch failed, falling back to new tab opening:", err);
      window.open(url, '_blank');
    }
  };

  const handleRemoveBg = async (e, url, id) => {
    e.preventDefault();
    setBgRemovingIds(prev => new Set(prev).add(id));
    try {
      const response = await fetch('http://localhost:8001/api/remove-bg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (!response.ok) throw new Error("Failed to remove background");
      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `${id}_nobg.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.error("Background removal failed:", err);
      alert("Failed to remove background. Please try again.");
    } finally {
      setBgRemovingIds(prev => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {assets.map((asset, index) => {
        const uniqueId = asset.id || `asset-${index}`;
        const isRemoving = bgRemovingIds.has(uniqueId);

        return (
          <div key={uniqueId} className="group relative rounded-xl overflow-hidden bg-white/5 border border-white/10 aspect-video flex items-center justify-center">
            
            <MediaItem asset={asset} type={type} />
            
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
              <div className="flex items-end justify-between">
                <div>
                  <span className="text-xs font-bold px-2 py-1 rounded bg-white/20 backdrop-blur-md">
                    {asset.source}
                  </span>
                  {asset.resolution && (
                    <p className="text-xs text-white/70 mt-1">{asset.resolution}</p>
                  )}
                </div>
                <div className="flex space-x-2">
                  {(type === 'images' || type === 'icons') && (
                    <button
                      onClick={(e) => handleRemoveBg(e, asset.url, uniqueId)}
                      disabled={isRemoving}
                      className="w-8 h-8 rounded-full bg-zinc-800 border border-white/20 flex items-center justify-center hover:bg-zinc-700 transition-colors shadow-lg z-10 disabled:opacity-50"
                      title="Remove Background (AI)"
                    >
                      {isRemoving ? <Loader2 size={14} className="text-white animate-spin" /> : <Eraser size={14} className="text-white" />}
                    </button>
                  )}
                  <button
                    onClick={(e) => handleDownload(e, asset.url, uniqueId)}
                    className="w-8 h-8 rounded-full bg-white flex items-center justify-center hover:bg-zinc-200 transition-colors shadow-lg z-10"
                    title="Download Asset"
                  >
                    <Download size={14} className="text-black" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
