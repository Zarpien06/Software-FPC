import { useState, useEffect } from 'react';
import './App.css';
import HeroSection from './components/HeroSections';
import Features from './components/Features';
import HowItWorks from './components/HowItWorks';
import Benefits from './components/Benefits';
import Footer from './components/Footer';
import Navbar from './components/Navbar';

import { Routes, Route, useLocation } from 'react-router-dom';
import Login from './Pages/Login';
import Registro from './Pages/Registro';

const App: React.FC = () => {
  const [scrolled, setScrolled] = useState<boolean>(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = (): void => {
      const isScrolled = window.scrollY > 10;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [scrolled]);

  // Oculta Navbar y Footer en páginas de login/registro si deseas
  const hideNavbarFooter = location.pathname === '/login' || location.pathname === '/registro';

  return (
    <div className="app">
      {!hideNavbarFooter && <Navbar scrolled={scrolled} />}

      <Routes>
        <Route path="/" element={
          <main>
            <HeroSection />
            <Features />
            <HowItWorks />
            <Benefits />
          </main>
        } />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
      </Routes>

      {!hideNavbarFooter && <Footer />}
    </div>
  );
};

export default App;