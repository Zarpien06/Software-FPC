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

  // Función para verificar autenticación mejorada
  const checkAuthentication = React.useCallback(() => {
    const token = localStorage.getItem('access_token');
    const userInfo = localStorage.getItem('user_info');
    
    console.log('=== VERIFICANDO AUTENTICACIÓN ===');
    console.log('Token encontrado:', !!token);
    console.log('User Info encontrado:', !!userInfo);
    console.log('Token:', token);
    console.log('User Info:', userInfo);
    
    if (token && userInfo) {
      try {
        const parsedUserInfo = JSON.parse(userInfo);
        console.log('Información del usuario parseada:', parsedUserInfo);
        
        // Verificar diferentes estructuras posibles del rol
        let roleNombre = null;
        
        if (parsedUserInfo.role?.nombre) {
          roleNombre = parsedUserInfo.role.nombre;
        } else if (parsedUserInfo.role?.name) {
          roleNombre = parsedUserInfo.role.name;
        } else if (parsedUserInfo.role_name) {
          roleNombre = parsedUserInfo.role_name;
        } else if (parsedUserInfo.role) {
          roleNombre = parsedUserInfo.role;
        } else if (parsedUserInfo.tipo_usuario) {
          roleNombre = parsedUserInfo.tipo_usuario;
        }
        
        console.log('Rol detectado:', roleNombre);
        
        if (roleNombre) {
          // Normalizar el rol a minúsculas y manejar variaciones
          let normalizedRole = roleNombre.toLowerCase();
          if (normalizedRole === 'administrador') {
            normalizedRole = 'admin';
          }
          
          setIsAuthenticated(true);
          setUserRole(normalizedRole);
          console.log('Autenticación exitosa con rol:', normalizedRole);
        } else {
          console.error('No se pudo determinar el rol del usuario');
          handleLogout();
        }
      } catch (error) {
        console.error('Error parsing user info:', error);
        handleLogout();
      }
    } else {
      console.log('No se encontraron credenciales');
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
      console.log('Cambio detectado en localStorage');
      checkAuthentication();
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [checkAuthentication]);

  // Efecto para verificar autenticación cuando cambia la ruta
  useEffect(() => {
    console.log('Ruta cambiada a:', location.pathname);
    checkAuthentication();
  }, [location.pathname, checkAuthentication]);

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
    console.log('RoleBasedRedirect - isAuthenticated:', isAuthenticated, 'userRole:', userRole);
    
    if (!isAuthenticated) {
      return <Navigate to="/login" replace />;
    }

    switch (userRole) {
      case 'admin':
      case 'administrador':
        console.log('Redirigiendo a dashboard admin');
        return <Navigate to="/dashboard-admin" replace />;
      case 'empleado':
        console.log('Redirigiendo a dashboard empleado');
        return <Navigate to="/dashboard-empleado" replace />;
      case 'cliente':
        console.log('Redirigiendo a dashboard cliente');
        return <Navigate to="/dashboard-cliente" replace />;
      default:
        console.log('No role defined, redirecting to login. Role:', userRole);
        return <Navigate to="/login" replace />;
    }
  };

  // Componente para rutas protegidas
  const ProtectedRoute = ({ children, allowedRoles }: { children: React.ReactNode; allowedRoles?: string[] }) => {
    console.log('ProtectedRoute - Auth:', isAuthenticated, 'Role:', userRole, 'Allowed:', allowedRoles);
    
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
            <ProtectedRoute allowedRoles={['admin', 'administrador']}>
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