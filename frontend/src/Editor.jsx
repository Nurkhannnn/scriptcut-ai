import { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from './api';
import { fmt } from './utils';

export default function Editor() {
  const { id } = useParams();
  const video = useRef(null);
  const [project, setProject] = useState(null);
  const [exp, setExp] = useState({ status: 'none' });
  const [save, setSave] = useState('Idle');
  const [error, setError] = useState('');

  useEffect(() => {
    api(`/api/projects/${id}`).then(setProject).catch((e) => setError(e.message));
    api(`/api/projects/${id}/export`).then(setExp).catch(() => {});
  }, [id]);

  useEffect(() => {
    if (exp.status !== 'processing') return undefined;
    const t = setInterval(() => {
      api(`/api/projects/${id}/export`).then(setExp).catch(() => {});
    }, 1000);
    return () => clearInterval(t);
  }, [exp.status, id]);

  const updateLocal = (segId, changes) =>
    setProject((p) => ({ ...p, segments: p.segments.map((s) => (s.id === segId ? { ...s, ...changes } : s)) }));

  async function persist(segId, changes) {
    setSave('Saving…');
    try {
      await api(`/api/projects/${id}/segments/${segId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(changes),
      });
      setSave('Saved');
    } catch (e) {
      setSave('Error');
      setError(e.message);
    }
  }

  function toggleDeleted(seg) {
    updateLocal(seg.id, { deleted: !seg.deleted });
    persist(seg.id, { deleted: !seg.deleted });
  }

  function seek(start) {
    const v = video.current;
    if (!v) return;
    v.currentTime = start;
    v.play().catch(() => {});
  }

  async function cut() {
    setExp({ status: 'processing' });
    try {
      await api(`/api/projects/${id}/cut`, { method: 'POST' });
    } catch (e) {
      setExp({ status: 'failed', error: e.message });
    }
  }

  function download() {
    const a = document.createElement('a');
    a.href = `/api/projects/${id}/export/download`;
    a.download = '';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  if (error && !project) return <p className="error">{error}</p>;
  if (!project) return <p>Loading…</p>;

  const allDeleted = project.segments.every((s) => s.deleted);
  const processing = exp.status === 'processing';

  return (
    <section>
      <h1>{project.name}</h1>
      <video data-testid="video-player" src={`/api/projects/${id}/video`} controls preload="metadata" ref={video} />

      <div className="timeline">
        {project.segments.map((s) => (
          <div
            key={s.id}
            data-testid="timeline-segment"
            data-deleted={String(s.deleted)}
            className={s.deleted ? 'tl deleted' : 'tl'}
            style={{ flex: s.end - s.start }}
            title={`${fmt(s.start)}–${fmt(s.end)}`}
            onClick={() => seek(s.start)}
          />
        ))}
      </div>

      <div className="toolbar">
        <span data-testid="save-status">{save}</span>
        <button data-testid="cut-button" onClick={cut} disabled={allDeleted || processing}>
          Cut video
        </button>
        <span data-testid="cut-status">{exp.status === 'none' ? 'idle' : exp.status}</span>
        <button data-testid="export-button" onClick={download} disabled={exp.status !== 'done'}>
          Export MP4
        </button>
      </div>
      {exp.status === 'failed' && <p className="error">{exp.error}</p>}

      <ol className="segments">
        {project.segments.map((s) => (
          <li key={s.id} data-testid="transcript-segment" data-start={s.start} data-deleted={String(s.deleted)}>
            <span className="time">{fmt(s.start)}</span>
            <textarea
              data-testid="segment-text"
              value={s.text}
              rows={2}
              onChange={(e) => updateLocal(s.id, { text: e.target.value })}
              onBlur={(e) => persist(s.id, { text: e.target.value })}
            />
            <button data-testid="segment-play" onClick={() => seek(s.start)}>
              Play
            </button>
            <button data-testid="segment-delete-toggle" onClick={() => toggleDeleted(s)}>
              {s.deleted ? 'Restore' : 'Delete'}
            </button>
          </li>
        ))}
      </ol>
    </section>
  );
}
