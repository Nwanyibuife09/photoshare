import { useState, useCallback, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Star, MapPin, Tag, ArrowLeft, Send, Trash2 } from 'lucide-react';

interface Comment {
  id: number;
  text: string;
  author_id: number;
  created_at: string;
}


interface PhotoDetail {
  id: number;
  title: string;
  caption: string;
  location?: string;
  tags?: string;
  s3_path: string;
  thumbnail_path?: string;
  created_at: string;
  owner_id: number;
  comments: Comment[];
  average_rating: number;
  rating_count: number;
}

export default function PhotoDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [photo, setPhoto] = useState<PhotoDetail | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const [comment, setComment] = useState('');
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  const fetchPhoto = useCallback(async () => {
    try {
      const res = await api.get(`/photos/${id}`);
      setPhoto(res.data);
    } catch (err) {
      console.error('Error fetching photo', err);
    } finally {
      setIsLoading(false);
    }
  }, [id]);

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this photo? This action cannot be undone.")) return;
    
    setIsDeleting(true);
    try {
      await api.delete(`/photos/${id}`);
      navigate('/');
    } catch (err) {
      console.error('Error deleting photo', err);
      setIsDeleting(false);
      alert("Failed to delete the photo. Please try again.");
    }
  };



  useEffect(() => {
    fetchPhoto();
  }, [fetchPhoto]);

  const handleComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comment.trim()) return;
    try {
      const formData = new URLSearchParams();
      formData.append('text', comment);
      await api.post(`/photos/${id}/comment`, formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      setComment('');
      fetchPhoto();
    } catch (err) {
      console.error('Error posting comment', err);
    }
  };

  const handleRate = async (score: number) => {
    try {
      const formData = new URLSearchParams();
      formData.append('score', score.toString());
      await api.post(`/photos/${id}/rate`, formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      setRating(score);
      fetchPhoto();
    } catch (err) {
      console.error('Error rating photo', err);
    }
  };

  if (isLoading) return <div className="loader">Loading...</div>;
  if (!photo) return <div className="empty-state"><h3>Photo not found</h3></div>;

  const imageUrl = `http://localhost:8000${photo.s3_path}`;

  return (
    <div className="page-container detail-container">
      <Link to="/" className="back-link">
        <ArrowLeft size={20} /> Back to Gallery
      </Link>

      <div className="detail-layout">
        <div className="detail-image-section">
          <img src={imageUrl} alt={photo.title} className="detail-image" />
        </div>

        <div className="detail-info-section glass-card">
          <h1 className="detail-title">{photo.title}</h1>
          <p className="detail-caption">{photo.caption}</p>

          {photo.location && (
            <div className="detail-meta">
              <MapPin size={16} />
              <span>{photo.location}</span>
            </div>
          )}

          {photo.tags && (
            <div className="detail-meta">
              <Tag size={16} />
              <div className="tag-list">
                {photo.tags.split(',').map((tag: string, i: number) => (
                  <span key={i} className="tag-chip">{tag.trim()}</span>
                ))}
              </div>
            </div>
          )}



          <div className="rating-section">
            <h3>Rating ({photo.average_rating}/5 from {photo.rating_count} votes)</h3>
            {user && (
              <div className="star-rating">
                {[1, 2, 3, 4, 5].map(s => (
                  <button
                    key={s}
                    className={`star-btn ${s <= (hoverRating || rating) ? 'active' : ''}`}
                    onClick={() => handleRate(s)}
                    onMouseEnter={() => setHoverRating(s)}
                    onMouseLeave={() => setHoverRating(0)}
                    title={`Rate ${s} star${s > 1 ? 's' : ''}`}
                  >
                    <Star size={24} />
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="comments-section">
            <h3>Comments ({photo.comments?.length || 0})</h3>

            {user && (
              <form onSubmit={handleComment} className="comment-form">
                <input
                  type="text"
                  value={comment}
                  onChange={e => setComment(e.target.value)}
                  placeholder="Write a comment..."
                  className="form-control"
                />
                <button type="submit" className="btn-primary btn-icon" title="Submit comment">
                  <Send size={18} />
                </button>
              </form>
            )}

            <div className="comment-list">
              {photo.comments?.map((c) => (
                <div key={c.id} className="comment-item">
                  <p>{c.text}</p>
                  <span className="comment-date">
                    {new Date(c.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          {user && photo.owner_id === user.id && (
            <div className="owner-actions">
              <button 
                className="btn-danger" 
                onClick={handleDelete}
                disabled={isDeleting}
              >
                <Trash2 size={18} />
                {isDeleting ? 'Deleting...' : 'Delete Photo'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
