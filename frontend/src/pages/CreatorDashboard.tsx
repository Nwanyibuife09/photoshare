import { useState } from 'react';
import api from '../services/api';
import { UploadCloud, Image as ImageIcon } from 'lucide-react';

export default function CreatorDashboard() {
  const [title, setTitle] = useState('');
  const [caption, setCaption] = useState('');
  const [location, setLocation] = useState('');
  const [tags, setTags] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<{type: 'success'|'error', text: string} | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedUrl = e.target.files[0];
      setFile(selectedUrl);
      setPreview(URL.createObjectURL(selectedUrl));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage({ type: 'error', text: 'Please select an image file.' });
      return;
    }

    setIsUploading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('caption', caption);
    if (location) formData.append('location', location);
    if (tags) formData.append('tags', tags);
    formData.append('file', file);

    try {
      await api.post('/photos/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setMessage({ type: 'success', text: 'Photo uploaded successfully!' });
      
      // Reset form
      setTitle('');
      setCaption('');
      setLocation('');
      setTags('');
      setFile(null);
      setPreview(null);
      
    } catch (err: any) {
      setMessage({ 
        type: 'error', 
        text: err.response?.data?.detail || 'Failed to upload photo.' 
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="page-container dashboard-container">
      <div className="dashboard-header">
        <h1>Creator Studio</h1>
        <p>Share your vision with the world.</p>
      </div>

      <div className="upload-section glass-card">
        {message && (
          <div className={`alert-${message.type}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="upload-form">
          <div className="form-row">
            <div className="form-column">
              <div className="form-group">
                <label>Photo Title</label>
                <input 
                  type="text" 
                  value={title} 
                  onChange={e => setTitle(e.target.value)} 
                  required 
                  placeholder="A descriptive title"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Caption</label>
                <textarea 
                  value={caption} 
                  onChange={e => setCaption(e.target.value)} 
                  required 
                  placeholder="Tell the story behind this shot..."
                  className="form-control"
                  rows={4}
                />
              </div>

              <div className="form-group">
                <label>Location (Optional)</label>
                <input 
                  type="text" 
                  value={location} 
                  onChange={e => setLocation(e.target.value)} 
                  placeholder="Where was this taken?"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label>Tags (Comma separated)</label>
                <input 
                  type="text" 
                  value={tags} 
                  onChange={e => setTags(e.target.value)} 
                  placeholder="nature, landscape, urban"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-column">
              <div className="file-upload-wrapper">
                <input 
                  type="file" 
                  id="file-upload" 
                  accept="image/jpeg, image/png, image/webp" 
                  onChange={handleFileChange} 
                  className="file-input-hidden"
                />
                <label htmlFor="file-upload" className="file-upload-zone">
                  {preview ? (
                    <img src={preview} alt="Preview" className="image-preview" />
                  ) : (
                    <div className="upload-placeholder">
                      <ImageIcon size={48} className="upload-icon" />
                      <p>Click to browse or drag & drop</p>
                      <span>Supports JPG, PNG, WEBP</span>
                    </div>
                  )}
                </label>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-primary" disabled={isUploading || !file}>
              <UploadCloud size={20} className="icon-left" />
              {isUploading ? 'Uploading...' : 'Publish Photo'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
