import React, { useState, useEffect } from 'react';
import './App.css';
import HeroSection from './components/HeroSections';
import Features from './components/Features';
import HowItWorks from './components/HowItWorks';
import Benefits from './components/Benefits';
import Footer from './components/Footer';
import Navbar from './components/Navbar';
import { Routes, Route, useLocation, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Registro from './pages/Registro';
import DashboardAdmin from './pages/DashboardAdmin';
import DashboardEmpleado from './pages/DashboardEmpleado';
import DashboardCliente from './pages/DashboardCliente';

const App: React.FC = () => {
  const [scrolled, setScrolled] = useState<boolean>(false);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userRole, setUserRole] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState<boolean>(true);
  const location = useLocation();

  // Función para verificar autenticación
  const checkAuthentication = React.useCallback(() => {
    const token = localStorage.getItem('access_token');
    const userInfo = localStorage.getItem('user_info');
    
    if (token && userInfo) {
      try {
        const parsedUserInfo = JSON.parse(userInfo);
        setIsAuthenticated(true);
        setUserRole(parsedUserInfo.role?.nombre || null);
      } catch (error) {
        console.error('Error parsing user info:', error);
        handleLogout();
      }
    } else {
      setIsAuthenticated(false);
      setUserRole(null);
    }
    setAuthLoading(false);
  }, []);

  // Función para manejar logout
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    setIsAuthenticated(false);
    setUserRole(null);
  };

  // Efecto para verificar autenticación al cargar
  useEffect(() => {
    checkAuthentication();
  }, [checkAuthentication]);

  // Efecto para manejar cambios en localStorage
  useEffect(() => {
    const handleStorageChange = () => {
      checkAuthentication();
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [checkAuthentication]);

  // Efecto para scroll
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

  const hideNavbarFooter = location.pathname === '/login' || 
                          location.pathname === '/registro' ||
                          location.pathname.startsWith('/dashboard');

  // Componente de carga
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Componente para redirección basada en rol
  const RoleBasedRedirect = () => {
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }

    switch (userRole) {
      case 'admin':
        return <Navigate to="/dashboard-admin" replace />;
      case 'empleado':
        return <Navigate to="/dashboard-empleado" replace />;
      case 'cliente':
        return <Navigate to="/dashboard-cliente" replace />;
      default:
        return <Navigate to="/" replace />;
    }
  };

  // Componente para rutas protegidas
  const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode; allowedRoles?: string[] }) => {
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }

    if (allowedRoles && userRole && !allowedRoles.includes(userRole)) {
      return <RoleBasedRedirect />;
    }

    return <>{children}</>;
  };



  return (
    <div className="app">
      {!hideNavbarFooter && <Navbar scrolled={scrolled} />}

      <Routes>
        {/* Página de inicio */}
        <Route 
          path="/" 
          element={
            isAuthenticated ? (
              <RoleBasedRedirect />
            ) : (
              <main>
                <HeroSection />
                <Features />
                <HowItWorks />
                <Benefits />
              </main>
            )
          } 
        />

        {/* Login */}
        <Route 
          path="/login" 
          element={
            isAuthenticated ? (
              <RoleBasedRedirect />
            ) : (
              <Login />
            )
          } 
        />

        {/* Registro */}
        <Route 
          path="/registro" 
          element={
            isAuthenticated ? (
              <RoleBasedRedirect />
            ) : (
              <Registro />
            )
          } 
        />

        {/* Dashboard genérico */}
        <Route path="/dashboard" element={<RoleBasedRedirect />} />

        {/* Dashboards específicos */}
        <Route 
          path="/dashboard-admin" 
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <DashboardAdmin />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/dashboard-empleado" 
          element={
            <ProtectedRoute allowedRoles={['empleado']}>
              <DashboardEmpleado />
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/dashboard-cliente" 
          element={
            <ProtectedRoute allowedRoles={['cliente']}>
              <DashboardCliente />
            </ProtectedRoute>
          } 
        />

        {/* Ruta catch-all */}
        <Route 
          path="*" 
          element={
            isAuthenticated ? <RoleBasedRedirect /> : <Navigate to="/" replace />
          } 
        />
      </Routes>

      {!hideNavbarFooter && <Footer />}
    </div>
  );
};

export default App;