import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './DashboardCliente.css';

// Interfaces
interface Role {
  id: number;
  nombre: string;
}

interface User {
  usuario_id: number;
  nombre_completo: string;
  correo: string;
  telefono: string;
  tipo_identificacion: string;
  numero_identificacion: string;
  estado: string;
  fecha_registro: string;
  foto_perfil: string;
  rol_id: number;
  role: Role;
  tipo_identificacion_info: {
    descripcion: string;
    tipo_id: string;
  };
}

const DashboardCliente: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'perfil' | 'historial' | 'notificaciones'>('perfil');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [showEditModal, setShowEditModal] = useState<boolean>(false);
  const [showPasswordModal, setShowPasswordModal] = useState<boolean>(false);

  // Formulario de perfil
  const [profileForm, setProfileForm] = useState<Partial<User>>({});
  
  // Formulario de contraseña
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  // Datos simulados para historial y notificaciones
  const [historialServicios] = useState([
    {
      id: 1,
      servicio: 'Pintura completa',
      fecha: '2024-01-15',
      estado: 'Completado',
      total: 450000,
      vehiculo: 'Toyota Corolla 2018'
    },
    {
      id: 2,
      servicio: 'Reparación de rayones',
      fecha: '2024-02-10',
      estado: 'En proceso',
      total: 180000,
      vehiculo: 'Honda Civic 2020'
    },
    {
      id: 3,
      servicio: 'Pulido y encerado',
      fecha: '2024-03-05',
      estado: 'Pendiente',
      total: 120000,
      vehiculo: 'Mazda 3 2019'
    }
  ]);

  const [notificaciones] = useState([
    {
      id: 1,
      titulo: 'Servicio completado',
      mensaje: 'Su vehículo Toyota Corolla ha sido completado exitosamente.',
      fecha: '2024-01-15',
      leido: true,
      tipo: 'success'
    },
    {
      id: 2,
      titulo: 'Recordatorio de cita',
      mensaje: 'Tiene una cita programada para mañana a las 10:00 AM.',
      fecha: '2024-01-20',
      leido: false,
      tipo: 'info'
    },
    {
      id: 3,
      titulo: 'Promoción especial',
      mensaje: '20% de descuento en servicios de pintura durante este mes.',
      fecha: '2024-01-18',
      leido: false,
      tipo: 'promotion'
    }
  ]);

  // Función para obtener el token
  const getToken = (): string | null => {
    return localStorage.getItem('access_token');
  };

  // Función para hacer peticiones a la API
  const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
    const token = getToken();
    const baseUrl = 'http://localhost:8000';
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      ...options,
    };

    try {
      const response = await fetch(`${baseUrl}${endpoint}`, defaultOptions);
      
      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem('access_token');
          localStorage.removeItem('user_info');
          navigate('/login');
          return;
        }
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  };

  // Cargar datos iniciales
  useEffect(() => {
    loadCurrentUser();
  }, []);

  const loadCurrentUser = async () => {
    setLoading(true);
    try {
      const userData = await apiRequest('/users/me');
      setCurrentUser(userData);
      setProfileForm(userData);
    } catch (error) {
      console.error('Error loading current user:', error);
      setError('Error al cargar información del usuario');
    } finally {
      setLoading(false);
    }
  };

  // Actualizar perfil
  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await apiRequest('/users/me', {
        method: 'PUT',
        body: JSON.stringify({
          nombre_completo: profileForm.nombre_completo,
          correo: profileForm.correo,
          telefono: profileForm.telefono,
          tipo_identificacion: profileForm.tipo_identificacion,
          numero_identificacion: profileForm.numero_identificacion
        }),
      });

      setSuccess('Perfil actualizado exitosamente');
      setShowEditModal(false);
      loadCurrentUser();
    } catch (error) {
      setError('Error al actualizar perfil');
    } finally {
      setLoading(false);
    }
  };

  // Cambiar contraseña (simulado)
  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setError('Las contraseñas no coinciden');
      setLoading(false);
      return;
    }

    if (passwordForm.new_password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      setLoading(false);
      return;
    }

    try {
      // Simulación de cambio de contraseña
      setTimeout(() => {
        setSuccess('Contraseña cambiada exitosamente');
        setShowPasswordModal(false);
        setPasswordForm({
          current_password: '',
          new_password: '',
          confirm_password: ''
        });
        setLoading(false);
      }, 1000);
    } catch (error) {
      setError('Error al cambiar la contraseña');
      setLoading(false);
    }
  };

  // Formatear fecha
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  // Formatear moneda
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(amount);
  };

  // Cerrar sesión
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    navigate('/login');
  };

  const openEditModal = () => {
    setProfileForm(currentUser);
    setShowEditModal(true);
  };

  return (
    <div className="dashboard-cliente">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Mi Dashboard</h1>
          <div className="header-actions">
            <span className="user-info">
              Bienvenido, {currentUser?.nombre_completo}
            </span>
            <button onClick={handleLogout} className="logout-btn">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-nav">
        <button 
          className={activeTab === 'perfil' ? 'active' : ''}
          onClick={() => setActiveTab('perfil')}
        >
          Mi Perfil
        </button>
        <button 
          className={activeTab === 'historial' ? 'active' : ''}
          onClick={() => setActiveTab('historial')}
        >
          Historial de Servicios
        </button>
        <button 
          className={activeTab === 'notificaciones' ? 'active' : ''}
          onClick={() => setActiveTab('notificaciones')}
        >
          Notificaciones
        </button>
      </div>

      <div className="dashboard-content">
        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {activeTab === 'perfil' && (
          <div className="profile-section">
            <div className="profile-header">
              <h2>Mi Información Personal</h2>
              <div className="profile-actions">
                <button onClick={openEditModal} className="btn btn-primary">
                  Editar Perfil
                </button>
                <button 
                  onClick={() => setShowPasswordModal(true)} 
                  className="btn btn-secondary"
                >
                  Cambiar Contraseña
                </button>
              </div>
            </div>

            <div className="profile-info">
              <div className="info-card">
                <div className="info-item">
                  <label>Nombre Completo:</label>
                  <span>{currentUser?.nombre_completo}</span>
                </div>
                <div className="info-item">
                  <label>Correo Electrónico:</label>
                  <span>{currentUser?.correo}</span>
                </div>
                <div className="info-item">
                  <label>Teléfono:</label>
                  <span>{currentUser?.telefono || 'No especificado'}</span>
                </div>
                <div className="info-item">
                  <label>Tipo de Identificación:</label>
                  <span>{currentUser?.tipo_identificacion_info?.descripcion}</span>
                </div>
                <div className="info-item">
                  <label>Número de Identificación:</label>
                  <span>{currentUser?.numero_identificacion}</span>
                </div>
                <div className="info-item">
                  <label>Estado:</label>
                  <span className={`status ${currentUser?.estado.toLowerCase()}`}>
                    {currentUser?.estado}
                  </span>
                </div>
                <div className="info-item">
                  <label>Fecha de Registro:</label>
                  <span>{currentUser?.fecha_registro ? formatDate(currentUser.fecha_registro) : 'No disponible'}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'historial' && (
          <div className="historial-section">
            <h2>Historial de Servicios</h2>
            <div className="services-grid">
              {historialServicios.map((servicio) => (
                <div key={servicio.id} className="service-card">
                  <div className="service-header">
                    <h3>{servicio.servicio}</h3>
                    <span className={`service-status ${servicio.estado.toLowerCase().replace(' ', '-')}`}>
                      {servicio.estado}
                    </span>
                  </div>
                  <div className="service-details">
                    <p><strong>Vehículo:</strong> {servicio.vehiculo}</p>
                    <p><strong>Fecha:</strong> {formatDate(servicio.fecha)}</p>
                    <p><strong>Total:</strong> {formatCurrency(servicio.total)}</p>
                  </div>
                  <div className="service-actions">
                    <button className="btn btn-small btn-outline">Ver Detalles</button>
                    {servicio.estado === 'Completado' && (
                      <button className="btn btn-small btn-primary">Descargar Factura</button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'notificaciones' && (
          <div className="notifications-section">
            <h2>Notificaciones</h2>
            <div className="notifications-list">
              {notificaciones.map((notificacion) => (
                <div key={notificacion.id} className={`notification-item ${notificacion.leido ? 'read' : 'unread'}`}>
                  <div className={`notification-icon ${notificacion.tipo}`}>
                    {notificacion.tipo === 'success' && '✓'}
                    {notificacion.tipo === 'info' && 'i'}
                    {notificacion.tipo === 'promotion' && '%'}
                  </div>
                  <div className="notification-content">
                    <h4>{notificacion.titulo}</h4>
                    <p>{notificacion.mensaje}</p>
                    <small>{formatDate(notificacion.fecha)}</small>
                  </div>
                  {!notificacion.leido && <div className="unread-indicator"></div>}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modal para editar perfil */}
      {showEditModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Editar Perfil</h3>
              <button 
                onClick={() => setShowEditModal(false)}
                className="close-btn"
              >
                ×
              </button>
            </div>
            <form onSubmit={handleUpdateProfile}>
              <div className="form-group">
                <label>Nombre Completo</label>
                <input
                  type="text"
                  value={profileForm.nombre_completo || ''}
                  onChange={(e) => setProfileForm({...profileForm, nombre_completo: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Correo Electrónico</label>
                <input
                  type="email"
                  value={profileForm.correo || ''}
                  onChange={(e) => setProfileForm({...profileForm, correo: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Teléfono</label>
                <input
                  type="text"
                  value={profileForm.telefono || ''}
                  onChange={(e) => setProfileForm({...profileForm, telefono: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Tipo de Identificación</label>
                <select
                  value={profileForm.tipo_identificacion || ''}
                  onChange={(e) => setProfileForm({...profileForm, tipo_identificacion: e.target.value})}
                  required
                >
                  <option value="cc">Cédula de Ciudadanía</option>
                  <option value="ti">Tarjeta de Identidad</option>
                  <option value="ce">Cédula de Extranjería</option>
                  <option value="pp">Pasaporte</option>
                </select>
              </div>
              <div className="form-group">
                <label>Número de Identificación</label>
                <input
                  type="text"
                  value={profileForm.numero_identificacion || ''}
                  onChange={(e) => setProfileForm({...profileForm, numero_identificacion: e.target.value})}
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="submit" disabled={loading} className="btn btn-primary">
                  {loading ? 'Actualizando...' : 'Actualizar'}
                </button>
                <button 
                  type="button" 
                  onClick={() => setShowEditModal(false)}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para cambiar contraseña */}
      {showPasswordModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Cambiar Contraseña</h3>
              <button 
                onClick={() => setShowPasswordModal(false)}
                className="close-btn"
              >
                ×
              </button>
            </div>
            <form onSubmit={handleChangePassword}>
              <div className="form-group">
                <label>Contraseña Actual</label>
                <input
                  type="password"
                  value={passwordForm.current_password}
                  onChange={(e) => setPasswordForm({...passwordForm, current_password: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Nueva Contraseña</label>
                <input
                  type="password"
                  value={passwordForm.new_password}
                  onChange={(e) => setPasswordForm({...passwordForm, new_password: e.target.value})}
                  required
                  minLength={8}
                />
              </div>
              <div className="form-group">
                <label>Confirmar Nueva Contraseña</label>
                <input
                  type="password"
                  value={passwordForm.confirm_password}
                  onChange={(e) => setPasswordForm({...passwordForm, confirm_password: e.target.value})}
                  required
                  minLength={8}
                />
              </div>
              <div className="modal-actions">
                <button type="submit" disabled={loading} className="btn btn-primary">
                  {loading ? 'Cambiando...' : 'Cambiar Contraseña'}
                </button>
                <button 
                  type="button" 
                  onClick={() => setShowPasswordModal(false)}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardCliente;