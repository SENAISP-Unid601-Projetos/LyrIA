// src/pages/InitialScreen/index.jsx
import React from 'react';
import Header from '../../components/Header';
import HeroSection from '../../components/HeroSection';
import Footer from '../../components/Footer';
import './styles/styles.css';

function InitialScreen() {
  return (
    <div className="initial-screen">
      <Header />
      <HeroSection />
      <Footer />
    </div>
  );
}

export default InitialScreen;