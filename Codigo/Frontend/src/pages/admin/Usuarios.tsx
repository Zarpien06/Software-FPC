import React, { useState, useEffect } from 'react';
import { apiService, User, Role, UpdateUserData } from '../../api/index';
import '../../assets/css/Admin/Usuarios.css';

const Usuarios: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [formData, setFormData] = useState<UpdateUserData>({
    nombre_completo: '',
    correo: '',
    telefono: '',
    tipo_identificacion: 'cedula',
    numero_identificacion: '',
    estado: 'activo',
    rol_id: 1
  });

  useEffect(() => {
    loadUsers();
    loadRoles();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAllUsers();
      setUsers(response.users);
    } catch (error) {
      console.error('Error loading users:', error);
      alert('Error al cargar usuarios');
    } finally {
      setLoading(false);
    }
  };

  const loadRoles = async () => {
    try {
      const response = await apiService.getAllRoles();
      setRoles(response.roles);
    } catch (error) {
      console.error('Error loading roles:', error);
      alert('Error al cargar roles');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingUser) {
        await apiService.updateUser(editingUser.usuario_id, formData);
        alert('Usuario actualizado correctamente');
      }
      setShowForm(false);
      setEditingUser(null);
      resetForm();
      await loadUsers();
    } catch (error) {
      console.error('Error saving user:', error);
      alert('Error al guardar usuario');
    }
  };

  const resetForm = () => {
    setFormData({
      nombre_completo: '',
      correo: '',
      telefono: '',
      tipo_identificacion: 'cedula',
      numero_identificacion: '',
      estado: 'activo',
      rol_id: 1
    });
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setFormData({
      nombre_completo: user.nombre_completo,
      correo: user.correo,
      telefono: user.telefono,
      tipo_identificacion: user.tipo_identificacion,
      numero_identificacion: user.numero_identificacion,
      estado: user.estado,
      rol_id: user.rol_id
    });
    setShowForm(true);
  };

  const handleDelete = async (userId: number) => {
    if (window.confirm('¿Estás seguro de eliminar este usuario?')) {
      try {
        await apiService.deleteUser(userId);
        alert('Usuario eliminado correctamente');
        await loadUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
        alert('Error al eliminar usuario');
      }
    }
  };

  const handleToggleStatus = async (userId: number) => {
    try {
      await apiService.toggleUserStatus(userId);
      alert('Estado del usuario actualizado');
      await loadUsers();
    } catch (error) {
      console.error('Error toggling user status:', error);
      alert('Error al cambiar estado del usuario');
    }
  };

  if (loading) return <div>Cargando usuarios...</div>;

  return (
    <div>
      <div className="header-usuarios">
        <h2>Gestión de Usuarios</h2>
        <div>
          <span>Total: {users.length}</span>
        </div>
      </div>

      {showForm && (
        <div className="formulario-usuario">
          <h3>{editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}</h3>
          <div className="formulario-grid">
            <div>
              <label>Nombre Completo:</label>
              <input
                type="text"
                value={formData.nombre_completo}
                onChange={(e) => setFormData({...formData, nombre_completo: e.target.value})}
                required
              />
            </div>
            <div>
              <label>Correo:</label>
              <input
                type="email"
                value={formData.correo}
                onChange={(e) => setFormData({...formData, correo: e.target.value})}
                required
              />
            </div>
            <div>
              <label>Teléfono:</label>
              <input
                type="text"
                value={formData.telefono}
                onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                required
              />
            </div>
            <div>
              <label>Tipo Identificación:</label>
              <select
                value={formData.tipo_identificacion}
                onChange={(e) => setFormData({...formData, tipo_identificacion: e.target.value})}
              >
                <option value="cedula">Cédula</option>
                <option value="pasaporte">Pasaporte</option>
                <option value="tarjeta_identidad">Tarjeta de Identidad</option>
              </select>
            </div>
            <div>
              <label>Número Identificación:</label>
              <input
                type="text"
                value={formData.numero_identificacion}
                onChange={(e) => setFormData({...formData, numero_identificacion: e.target.value})}
                required
              />
            </div>
            <div>
              <label>Estado:</label>
              <select
                value={formData.estado}
                onChange={(e) => setFormData({...formData, estado: e.target.value})}
              >
                <option value="activo">Activo</option>
                <option value="inactivo">Inactivo</option>
              </select>
            </div>
            <div>
              <label>Rol:</label>
              <select
                value={formData.rol_id}
                onChange={(e) => setFormData({...formData, rol_id: parseInt(e.target.value)})}
              >
                {roles.map(role => (
                  <option key={role.id} value={role.id}>{role.nombre}</option>
                ))}
              </select>
            </div>
            <div className="botones-formulario">
              <button
                type="button"
                className="btn-cancelar"
                onClick={() => { setShowForm(false); setEditingUser(null); resetForm(); }}
              >
                Cancelar
              </button>
              <button
                type="button"
                className="btn-guardar"
                onClick={(e) => { e.preventDefault(); handleSubmit(e as any); }}
              >
                {editingUser ? 'Actualizar' : 'Crear'}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="tabla-usuarios">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Correo</th>
              <th>Teléfono</th>
              <th>Rol</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.usuario_id}>
                <td>{user.usuario_id}</td>
                <td>{user.nombre_completo}</td>
                <td>{user.correo}</td>
                <td>{user.telefono}</td>
                <td>{user.role.nombre}</td>
                <td className="estado">
                  <span className={user.estado === 'activo' ? 'estado-activo' : 'estado-inactivo'}>
                    {user.estado}
                  </span>
                </td>
                <td>
                  <button className="btn-editar" onClick={() => handleEdit(user)}>Editar</button>
                  <button className="btn-toggle" onClick={() => handleToggleStatus(user.usuario_id)}>Toggle</button>
                  <button className="btn-eliminar" onClick={() => handleDelete(user.usuario_id)}>Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Usuarios;