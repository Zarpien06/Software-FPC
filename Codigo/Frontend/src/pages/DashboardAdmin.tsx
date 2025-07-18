import React, { useState, useEffect } from 'react';
import { Users, Settings, Car, Home, LogOut, BarChart3, Shield, UserCheck } from 'lucide-react';
import Usuarios from '../pages/admin/Usuarios';
import Roles from '../pages/admin/Roles';
import Automoviles from '../pages/admin/Automoviles';
import { apiService } from '../api';
import '../assets/css/Admin/DashboardAdmin.css';

const DashboardAdmin = () => {
  const [moduloActual, setModuloActual] = useState('home');
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    const user = apiService.getCurrentUserInfo();
    setUserInfo(user);
  }, []);

  const renderModule = () => {
    switch (moduloActual) {
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

  const menuItems = [
    { id: 'home', label: 'Inicio', icon: Home },
    { id: 'usuarios', label: 'Usuarios', icon: Users },
    { id: 'roles', label: 'Roles', icon: Shield },
    { id: 'automoviles', label: 'Automóviles', icon: Car },
  ];

  return (
    <div className="dashboard-container">
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <BarChart3 size={32} />
            <span>AdminPanel</span>
          </div>
        </div>

        <div className="user-profile">
          <div className="user-avatar">
            <UserCheck size={24} />
          </div>
          <div className="user-details">
            <h3>{userInfo?.nombre_completo}</h3>
            <p>{userInfo?.role?.nombre}</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setModuloActual(item.id)}
                className={`nav-item ${moduloActual === item.id ? 'active' : ''}`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <button
          onClick={() => {
            apiService.logout();
            window.location.href = '/login';
          }}
          className="logout-btn"
        >
          <LogOut size={20} />
          <span>Cerrar Sesión</span>
        </button>
      </aside>

      <main className="dashboard-content">
        
        <div className="content-wrapper">
          {renderModule()}
        </div>
      </main>
    </div>
  );
};

const HomeModule = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [usersResponse, rolesResponse, autoStats] = await Promise.all([
          apiService.getAllUsers(0, 1),
          apiService.getAllRoles(),
          apiService.getAutomovilEstadisticas(),
        ]);

        setStats({
          totalUsers: usersResponse.total,
          totalRoles: rolesResponse.total,
          totalAutomoviles: autoStats.total_automoviles,
        });
      } catch (error) {
        console.error('Error al cargar estadísticas:', error);
      }
    };

    loadStats();
  }, []);

  const statCards = [
    {
      title: 'Total Usuarios',
      value: stats?.totalUsers || 0,
      icon: Users,
      color: 'blue',
      trend: '+12%'
    },
    {
      title: 'Total Roles',
      value: stats?.totalRoles || 0,
      icon: Shield,
      color: 'green',
      trend: '+5%'
    },
    {
      title: 'Total Automóviles',
      value: stats?.totalAutomoviles || 0,
      icon: Car,
      color: 'orange',
      trend: '+8%'
    }
  ];

  return (
    <div className="home-module">
      <div className="welcome-section">
        <h2>Bienvenido al Dashboard</h2>
        <p>Gestiona eficientemente todos los aspectos de tu sistema</p>
      </div>

      <div className="stats-grid">
        {statCards.map((card, index) => {
          const Icon = card.icon;
          return (
            <div key={index} className={`stat-card ${card.color}`}>
              <div className="stat-icon">
                <Icon size={24} />
              </div>
              <div className="stat-content">
                <h3>{card.title}</h3>
                <div className="stat-value">{card.value}</div>
                <div className="stat-trend">{card.trend}</div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="quick-actions">
        <h3>Acciones Rápidas</h3>
        <div className="actions-grid">
          <div className="action-card" onClick={() => setModuloActual('usuarios')}>
            <Users size={32} />
            <h4>Gestionar Usuarios</h4>
            <p>Administra perfiles y permisos de usuarios</p>
          </div>
          <div className="action-card" onClick={() => setModuloActual('roles')}>
            <Shield size={32} />
            <h4>Configurar Roles</h4>
            <p>Define y asigna roles del sistema</p>
          </div>
          <div className="action-card" onClick={() => setModuloActual('automoviles')}>
            <Car size={32} />
            <h4>Control de Flota</h4>
            <p>Supervisa y mantiene la flota vehicular</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardAdmin;
