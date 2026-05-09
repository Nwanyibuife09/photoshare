import { useState, useEffect } from 'react';
import api from '../services/api';
import PhotoCard from '../components/PhotoCard';
import { Search } from 'lucide-react';

interface Photo {
  id: number;
  title: string;
  caption: string;
  location?: string;
  s3_path: string;
  thumbnail_path?: string;
}

export default function Home() {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const fetchPhotos = async (searchQuery = '') => {
    setIsLoading(true);
    try {
      const res = await api.get('/photos/', {
        params: { search: searchQuery }
      });
      setPhotos(res.data);
    } catch (err) {
      console.error('Error fetching photos', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPhotos();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchPhotos(search);
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Discover Perspectives</h1>
        <p>Explore stunning photography from creators worldwide.</p>
        
        <form onSubmit={handleSearch} className="search-bar">
          <input
            type="text"
            placeholder="Search by title, location, or tag..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn" title="Search">
            <Search size={20} />
          </button>
        </form>
      </header>

      {isLoading ? (
        <div className="loader">Loading...</div>
      ) : photos.length > 0 ? (
        <div className="photo-grid">
          {photos.map(photo => (
            <PhotoCard key={photo.id} photo={photo} />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <h3>No photos found</h3>
          <p>Try adjusting your search criteria.</p>
        </div>
      )}
    </div>
  );
}
