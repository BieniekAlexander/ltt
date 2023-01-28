// imports
import React, { useState } from 'react';
import './App.css';
import Navbar from './components/NavBar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomeBody from './pages';
import AboutBody from './pages/about';
import AnnotationsBody from './pages/Annotations';
import InflectionsBody from './pages/Inflections';
import VocabularyBody from './pages/Vocabulary';
import SignUpBody from './pages/sign-up';
import LogInBody from './pages/log-in';
import { useAuth, AuthProvider } from './auth/AuthProvider'

var cors = require('cors');
console.log(process.env.REACT_APP_BACKEND_URL)


export default function App() {
    const { auth } = useAuth();

    return (
        <AuthProvider>
            <div className="background">
                <Router>
                    <Navbar />
                    <Routes>
                        <Route path="/" element={<HomeBody />} />
                        <Route path="/about" element={<AboutBody />} />

                        {/* TODO clean up navbar with auth stuff */}
                        if (!auth) {
                            <Route path="/log-in" element={<LogInBody />} />
                        }
                        <Route path="/sign-up" element={<SignUpBody />} />

                        <Route path="/annotations" element={<AnnotationsBody />} />
                        <Route path="/inflections" element={<InflectionsBody />} />
                        <Route path="/vocabulary" element={<VocabularyBody />} />
                    </Routes>
                </Router>
            </div>
        </AuthProvider> 
    );
}