import React, { useState, useEffect } from 'react';
import { apiService } from '../api/index';
import Usuarios from './admin/Usuarios';
import Roles from './admin/Roles';
import Automoviles from './admin/Automoviles';

const DashboardAdmin: React.FC = () => {
  const [activeModule, setActiveModule] = useState('home');
  const [userInfo, setUserInfo] = useState<any>(null);

  useEffect(() => {
    const user = apiService.getCurrentUserInfo();
    setUserInfo(user);
  }, []);

  const renderModule = () => {
    switch (activeModule) {
      case 'usuarios':
        return <Usuarios />;
      case 'roles':
        return <Roles />;
      case 'automoviles':
        return <Automoviles />;
      default:
        return <HomeModule />;
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <div style={{ width: '250px', backgroundColor: '#2c3e50', color: 'white', padding: '20px' }}>
        <h2>Panel Admin</h2>
        <div style={{ marginBottom: '20px' }}>
          <p>Bienvenido: {userInfo?.nombre_completo}</p>
          <p>Rol: {userInfo?.role?.nombre}</p>
        </div>
        
        <nav>
          <button 
            onClick={() => setActiveModule('home')}
            style={{ 
              width: '100%', 
              padding: '10px', 
              margin: '5px 0', 
              backgroundColor: activeModule === 'home' ? '#3498db' : 'transparent',
              color: 'white',
              border: '1px solid #34495e',
              cursor: 'pointer'
            }}
          >
            Inicio
          </button>
          
          <button 
            onClick={() => setActiveModule('usuarios')}
            style={{ 
              width: '100%', 
              padding: '10px', 
              margin: '5px 0', 
              backgroundColor: activeModule === 'usuarios' ? '#3498db' : 'transparent',
              color: 'white',
              border: '1px solid #34495e',
              cursor: 'pointer'
            }}
          >
            Gestión Usuarios
          </button>
          
          <button 
            onClick={() => setActiveModule('roles')}
            style={{ 
              width: '100%', 
              padding: '10px', 
              margin: '5px 0', 
              backgroundColor: activeModule === 'roles' ? '#3498db' : 'transparent',
              color: 'white',
              border: '1px solid #34495e',
              cursor: 'pointer'
            }}
          >
            Gestión Roles
          </button>
          
          <button 
            onClick={() => setActiveModule('automoviles')}
            style={{ 
              width: '100%', 
              padding: '10px', 
              margin: '5px 0', 
              backgroundColor: activeModule === 'automoviles' ? '#3498db' : 'transparent',
              color: 'white',
              border: '1px solid #34495e',
              cursor: 'pointer'
            }}
          >
            Gestión Automóviles
          </button>
        </nav>
        
        <button 
          onClick={() => {
            apiService.logout();
            window.location.href = '/login';
          }}
          style={{ 
            width: '100%', 
            padding: '10px', 
            marginTop: '20px',
            backgroundColor: '#e74c3c',
            color: 'white',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Cerrar Sesión
        </button>
      </div>
      
      {/* Content Area */}
      <div style={{ flex: 1, padding: '20px', backgroundColor: '#ecf0f1' }}>
        {renderModule()}
      </div>
    </div>
  );
};

// Módulo Home (dentro del mismo archivo por simplicidad)
const HomeModule: React.FC = () => {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [usersResponse, rolesResponse, autoStats] = await Promise.all([
          apiService.getAllUsers(0, 1),
          apiService.getAllRoles(),
          apiService.getAutomovilEstadisticas()
        ]);
        
        setStats({
          totalUsers: usersResponse.total,
          totalRoles: rolesResponse.total,
          totalAutomoviles: autoStats.total_automoviles
        });
      } catch (error) {
        console.error('Error loading stats:', error);
      }
    };
    
    loadStats();
  }, []);

  return (
    <div>
      <h1>Dashboard Administrador</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', marginTop: '20px' }}>
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3>Total Usuarios</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#3498db' }}>{stats?.totalUsers || 0}</p>
        </div>
        
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3>Total Roles</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#27ae60' }}>{stats?.totalRoles || 0}</p>
        </div>
        
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3>Total Automóviles</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#f39c12' }}>{stats?.totalAutomoviles || 0}</p>
        </div>
      </div>
      
      <div style={{ marginTop: '40px' }}>
        <h3>Acciones Rápidas</h3>
        <div style={{ display: 'flex', gap: '15px', marginTop: '15px' }}>
          <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h4>Usuarios</h4>
            <p>Gestiona todos los usuarios del sistema</p>
          </div>
          <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h4>Roles</h4>
            <p>Administra roles y permisos</p>
          </div>
          <div style={{ backgroundColor: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h4>Automóviles</h4>
            <p>Control total de la flota vehicular</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardAdmin;