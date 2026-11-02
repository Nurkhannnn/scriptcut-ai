import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from './api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api('/api/projects').then(setProjects).catch((e) => setError(e.message));
  }, []);

  async function submit(e) {
    e.preventDefault();
    setError('');
    if (!name.trim()) return setError('Project name is required');
    if (!file) return setError('Please choose a video file');
    const body = new FormData();
    body.append('name', name.trim());
    body.append('video', file);
    setBusy(true);
    try {
      const project = await api('/api/projects', { method: 'POST', body });
      navigate(`/projects/${project.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section>
      <h1>Projects</h1>
      <button data-testid="new-project-button" onClick={() => setShowForm((v) => !v)}>
        New project
      </button>

      {showForm && (
        <form onSubmit={submit} className="card">
          <label>
            Name
            <input data-testid="project-name-input" value={name} onChange={(e) => setName(e.target.value)} />
          </label>
          <label>
            Video
            <input
              data-testid="video-file-input"
              type="file"
              accept="video/*"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
          </label>
          <button data-testid="create-project-submit" type="submit" disabled={busy}>
            {busy ? 'Creating…' : 'Create'}
          </button>
          {error && (
            <p data-testid="form-error" className="error">
              {error}
            </p>
          )}
        </form>
      )}

      {!showForm && error && <p className="error">{error}</p>}

      <ul className="list">
        {projects.map((p) => (
          <li key={p.id} data-testid="project-list-item">
            <Link to={`/projects/${p.id}`}>{p.name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
