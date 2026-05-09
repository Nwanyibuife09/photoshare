import { Link } from 'react-router-dom';
import { Heart, MessageCircle, MapPin } from 'lucide-react';

interface PhotoProps {
  photo: {
    id: number;
    title: string;
    caption: string;
    location?: string;
    s3_path: string;
    thumbnail_path?: string;
  };
}

export default function PhotoCard({ photo }: PhotoProps) {
  const imageUrl = photo.thumbnail_path 
    ? `http://localhost:8000${photo.thumbnail_path}` 
    : `http://localhost:8000${photo.s3_path}`;

  return (
    <Link to={`/photo/${photo.id}`} className="photo-card">
      <div className="photo-card-image-wrap">
        <img src={imageUrl} alt={photo.title} className="photo-card-image" loading="lazy" />
        <div className="photo-card-overlay">
          <div className="photo-card-actions">
            <span className="action"><Heart size={20} /></span>
            <span className="action"><MessageCircle size={20} /></span>
          </div>
        </div>
      </div>
      <div className="photo-card-content">
        <h3 className="photo-card-title">{photo.title}</h3>
        {photo.location && (
          <div className="photo-card-location">
            <MapPin size={14} />
            <span>{photo.location}</span>
          </div>
        )}
      </div>
    </Link>
  );
}
