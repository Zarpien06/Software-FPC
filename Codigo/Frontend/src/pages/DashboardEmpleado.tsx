import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './DashboardEmpleado.css';

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

interface UserFormData {
  nombre_completo: string;
  correo: string;
  password: string;
  telefono: string;
  tipo_identificacion: string;
  numero_identificacion: string;
}

const DashboardEmpleado: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'perfil' | 'usuarios'>('perfil');
  const [users, setUsers] = useState<User[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [showUserModal, setShowUserModal] = useState<boolean>(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);

  // Formulario de usuario
  const [userForm, setUserForm] = useState<UserFormData>({
    nombre_completo: '',
    correo: '',
    password: '',
    telefono: '',
    tipo_identificacion: 'cc',
    numero_identificacion: ''
  });

  // Formulario de perfil
  const [profileForm, setProfileForm] = useState<Partial<User>>({});

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
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        loadCurrentUser(),
        loadUsers(),
        loadRoles()
      ]);
    } catch (error) {
      console.error('Error loading initial data:', error);
      setError('Error al cargar los datos iniciales');
    } finally {
      setLoading(false);
    }
  };

  const loadCurrentUser = async () => {
    try {
      const userData = await apiRequest('/users/me');
      setCurrentUser(userData);
      setProfileForm(userData);
    } catch (error) {
      console.error('Error loading current user:', error);
    }
  };

  const loadUsers = async (page: number = 1, search: string = '') => {
    try {
      const params = new URLSearchParams({
        skip: ((page - 1) * 10).toString(),
        limit: '10',
        ...(search && { search })
      });
      
      const response = await apiRequest(`/users/?${params}`);
      setUsers(response.users);
      setTotalPages(response.total_pages);
    } catch (error) {
      console.error('Error loading users:', error);
      setError('Error al cargar usuarios');
    }
  };

  const loadRoles = async () => {
    try {
      const response = await apiRequest('/roles/');
      setRoles(response.roles);
    } catch (error) {
      console.error('Error loading roles:', error);
    }
  };

  // Manejar búsqueda
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    setCurrentPage(1);
    loadUsers(1, value);
  };

  // Manejar paginación
  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    loadUsers(page, searchTerm);
  };

  // Crear usuario
  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userForm),
      });

      setSuccess('Usuario creado exitosamente');
      setShowUserModal(false);
      setUserForm({
        nombre_completo: '',
        correo: '',
        password: '',
        telefono: '',
        tipo_identificacion: 'cc',
        numero_identificacion: ''
      });
      loadUsers(currentPage, searchTerm);
    } catch (error) {
      setError('Error al crear usuario');
    } finally {
      setLoading(false);
    }
  };

  // Editar usuario
  const handleEditUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingUser) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await apiRequest(`/users/${editingUser.usuario_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          nombre_completo: userForm.nombre_completo,
          correo: userForm.correo,
          telefono: userForm.telefono,
          tipo_identificacion: userForm.tipo_identificacion,
          numero_identificacion: userForm.numero_identificacion,
          estado: editingUser.estado,
          rol_id: editingUser.rol_id
        }),
      });

      setSuccess('Usuario actualizado exitosamente');
      setShowUserModal(false);
      setEditingUser(null);
      loadUsers(currentPage, searchTerm);
    } catch (error) {
      setError('Error al actualizar usuario');
    } finally {
      setLoading(false);
    }
  };

  // Cambiar estado de usuario
  const handleToggleUserStatus = async (userId: number) => {
    setLoading(true);
    try {
      await apiRequest(`/users/${userId}/toggle-status`, {
        method: 'PATCH',
      });
      setSuccess('Estado del usuario actualizado');
      loadUsers(currentPage, searchTerm);
    } catch (error) {
      setError('Error al cambiar estado del usuario');
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
        body: JSON.stringify(profileForm),
      });

      setSuccess('Perfil actualizado exitosamente');
      loadCurrentUser();
    } catch (error) {
      setError('Error al actualizar perfil');
    } finally {
      setLoading(false);
    }
  };

  // Abrir modal para editar usuario
  const openEditModal = (user: User) => {
    setEditingUser(user);
    setUserForm({
      nombre_completo: user.nombre_completo,
      correo: user.correo,
      password: '',
      telefono: user.telefono,
      tipo_identificacion: user.tipo_identificacion,
      numero_identificacion: user.numero_identificacion
    });
    setShowUserModal(true);
  };

  // Cerrar sesión
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
    navigate('/login');
  };

  return (
    <div className="dashboard-empleado">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Dashboard Empleado</h1>
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
          className={activeTab === 'usuarios' ? 'active' : ''}
          onClick={() => setActiveTab('usuarios')}
        >
          Gestión de Usuarios
        </button>
      </div>

      <div className="dashboard-content">
        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {activeTab === 'perfil' && (
          <div className="profile-section">
            <h2>Mi Perfil</h2>
            <form onSubmit={handleUpdateProfile} className="profile-form">
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
              <button type="submit" disabled={loading} className="btn btn-primary">
                {loading ? 'Actualizando...' : 'Actualizar Perfil'}
              </button>
            </form>
          </div>
        )}

        {activeTab === 'usuarios' && (
          <div className="users-section">
            <div className="users-header">
              <h2>Gestión de Usuarios</h2>
              <button 
                onClick={() => setShowUserModal(true)}
                className="btn btn-primary"
              >
                Crear Usuario
              </button>
            </div>

            <div className="users-filters">
              <input
                type="text"
                placeholder="Buscar usuarios..."
                value={searchTerm}
                onChange={handleSearch}
                className="search-input"
              />
            </div>

            <div className="users-table">
              <table>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>Correo</th>
                    <th>Teléfono</th>
                    <th>Identificación</th>
                    <th>Rol</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.usuario_id}>
                      <td>{user.nombre_completo}</td>
                      <td>{user.correo}</td>
                      <td>{user.telefono}</td>
                      <td>{user.numero_identificacion}</td>
                      <td>{user.role?.nombre || 'Sin rol'}</td>
                      <td>
                        <span className={`status ${user.estado.toLowerCase()}`}>
                          {user.estado}
                        </span>
                      </td>
                      <td>
                        <button
                          onClick={() => openEditModal(user)}
                          className="btn btn-small btn-secondary"
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => handleToggleUserStatus(user.usuario_id)}
                          className="btn btn-small btn-warning"
                        >
                          {user.estado === 'ACTIVO' ? 'Desactivar' : 'Activar'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Paginación */}
            <div className="pagination">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => handlePageChange(page)}
                  className={`pagination-btn ${page === currentPage ? 'active' : ''}`}
                >
                  {page}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modal para crear/editar usuario */}
      {showUserModal && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>{editingUser ? 'Editar Usuario' : 'Crear Usuario'}</h3>
              <button 
                onClick={() => {
                  setShowUserModal(false);
                  setEditingUser(null);
                  setUserForm({
                    nombre_completo: '',
                    correo: '',
                    password: '',
                    telefono: '',
                    tipo_identificacion: 'cc',
                    numero_identificacion: ''
                  });
                }}
                className="close-btn"
              >
                ×
              </button>
            </div>
            <form onSubmit={editingUser ? handleEditUser : handleCreateUser}>
              <div className="form-group">
                <label>Nombre Completo</label>
                <input
                  type="text"
                  value={userForm.nombre_completo}
                  onChange={(e) => setUserForm({...userForm, nombre_completo: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Correo Electrónico</label>
                <input
                  type="email"
                  value={userForm.correo}
                  onChange={(e) => setUserForm({...userForm, correo: e.target.value})}
                  required
                />
              </div>
              {!editingUser && (
                <div className="form-group">
                  <label>Contraseña</label>
                  <input
                    type="password"
                    value={userForm.password}
                    onChange={(e) => setUserForm({...userForm, password: e.target.value})}
                    required
                  />
                </div>
              )}
              <div className="form-group">
                <label>Teléfono</label>
                <input
                  type="text"
                  value={userForm.telefono}
                  onChange={(e) => setUserForm({...userForm, telefono: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Tipo de Identificación</label>
                <select
                  value={userForm.tipo_identificacion}
                  onChange={(e) => setUserForm({...userForm, tipo_identificacion: e.target.value})}
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
                  value={userForm.numero_identificacion}
                  onChange={(e) => setUserForm({...userForm, numero_identificacion: e.target.value})}
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="submit" disabled={loading} className="btn btn-primary">
                  {loading ? 'Procesando...' : (editingUser ? 'Actualizar' : 'Crear')}
                </button>
                <button 
                  type="button" 
                  onClick={() => {
                    setShowUserModal(false);
                    setEditingUser(null);
                  }}
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

export default DashboardEmpleado;