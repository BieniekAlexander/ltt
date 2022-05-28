// imports
import React from 'react';
import './App.css';
import Navbar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomeBody from './pages';
import AboutBody from './pages/about';
import AnnotationsBody from './pages/Annotations';
import InflectionsBody from './pages/Inflections';
import VocabularyBody from './pages/Vocabulary';
var cors = require('cors');

export default function App() {
  return (
    <div className="background">
      <Router>
      <Navbar />
        <Routes>
          <Route path="/" element={<HomeBody/>} />
          <Route path="/about" element={<AboutBody/>} />
          <Route path="/annotations" element={<AnnotationsBody/>} />
          <Route path="/inflections" element={<InflectionsBody/>} />
          <Route path="/vocabulary" element={<VocabularyBody/>} />
        </Routes>
      </Router>
    </div>
  );
}