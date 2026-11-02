import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import Dashboard from './Dashboard.jsx';
import Editor from './Editor.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <header className="top">
        <Link to="/">ScriptCut AI</Link>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects/:id" element={<Editor />} />
        </Routes>
      </main>
    </BrowserRouter>
  </React.StrictMode>,
);
