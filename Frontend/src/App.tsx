import { useState, useEffect } from 'react';
import './App.css';
import HeroSection from './components/HeroSections';
import Features from './components/Features';
import HowItWorks from './components/HowItWorks';
import Benefits from './components/Benefits';
import Footer from './components/Footer';
import Navbar from './components/Navbar';
import Admin from './components/admin';


import { Routes, Route, useLocation, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Registro from './pages/Registro';
import Dashboard from './pages/dashBoard';



const App: React.FC = () => {
  const [scrolled, setScrolled] = useState<boolean>(false);
  const location = useLocation();

  // Función para verificar autenticación
  const isAuthenticated = () => {
    return !!localStorage.getItem('token');
  };

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

  // Oculta Navbar y Footer en páginas de login/registro
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
            <Admin />
          </main>
        } />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route 
          path="/dashboard" 
          element={isAuthenticated() ? <Dashboard /> : <Navigate to="/login" replace />} 
        />
      </Routes>

      {!hideNavbarFooter && <Footer />}
    </div>
  );
};

export default App;