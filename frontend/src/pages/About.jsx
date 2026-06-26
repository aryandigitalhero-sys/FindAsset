export default function About() {
  return (
    <div className="max-w-3xl mx-auto py-12">
      <h1 className="text-4xl font-bold mb-8">About AI Asset Finder</h1>
      
      <div className="bg-[#1c1c1c]/80 backdrop-blur-md border border-white/5 shadow-2xl rounded-3xl p-10 space-y-8">
        <p className="text-lg text-white/80">
          AI Asset Finder is an intelligent creative assistant designed for video editors and content creators. It automates the tedious process of finding visual assets for short-form videos like Reels and YouTube Shorts.
        </p>
        
        <h2 className="text-2xl font-semibold mt-8 mb-4">How it works</h2>
        
        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white text-black flex items-center justify-center font-bold">1</div>
            <div>
              <h3 className="font-semibold text-lg text-white/90">Scene Splitting</h3>
              <p className="text-white/60">Our AI analyzes your script and logically breaks it down into individual scenes.</p>
            </div>
          </div>
          
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white text-black flex items-center justify-center font-bold">2</div>
            <div>
              <h3 className="font-semibold text-lg text-white/90">Visual Planning</h3>
              <p className="text-white/60">For each scene, the AI extracts the visual intent, style, emotion, and generates search keywords.</p>
            </div>
          </div>
          
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white text-black flex items-center justify-center font-bold">3</div>
            <div>
              <h3 className="font-semibold text-lg text-white/90">Parallel Search</h3>
              <p className="text-white/60">The agent searches multiple free asset providers (Pexels, Pixabay, Unsplash, Giphy) simultaneously to bring back the best videos, images, and GIFs.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
