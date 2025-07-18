import React, { useState, useEffect } from 'react';
import { apiService, User, Role, UpdateUserData } from '../../api/index';

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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Gestión de Usuarios</h2>
        <div>
          <span style={{ marginRight: '10px' }}>Total: {users.length}</span>
        </div>
      </div>

      {showForm && (
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3>{editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
            <div>
              <label>Nombre Completo:</label>
              <input
                type="text"
                value={formData.nombre_completo}
                onChange={(e) => setFormData({...formData, nombre_completo: e.target.value})}
                required
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
              />
            </div>
            
            <div>
              <label>Correo:</label>
              <input
                type="email"
                value={formData.correo}
                onChange={(e) => setFormData({...formData, correo: e.target.value})}
                required
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
              />
            </div>
            
            <div>
              <label>Teléfono:</label>
              <input
                type="text"
                value={formData.telefono}
                onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                required
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
              />
            </div>
            
            <div>
              <label>Tipo Identificación:</label>
              <select
                value={formData.tipo_identificacion}
                onChange={(e) => setFormData({...formData, tipo_identificacion: e.target.value})}
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
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
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
              />
            </div>
            
            <div>
              <label>Estado:</label>
              <select
                value={formData.estado}
                onChange={(e) => setFormData({...formData, estado: e.target.value})}
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
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
                style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
              >
                {roles.map(role => (
                  <option key={role.id} value={role.id}>{role.nombre}</option>
                ))}
              </select>
            </div>
            
            <div style={{ gridColumn: 'span 2', display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
              <button 
                type="button" 
                onClick={() => { setShowForm(false); setEditingUser(null); resetForm(); }}
                style={{ padding: '10px 20px', backgroundColor: '#95a5a6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                Cancelar
              </button>
              <button 
                type="button" 
                onClick={(e) => { e.preventDefault(); handleSubmit(e as any); }}
                style={{ padding: '10px 20px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                {editingUser ? 'Actualizar' : 'Crear'}
              </button>
            </div>
          </div>
        </div>
      )}

      <div style={{ backgroundColor: 'white', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ backgroundColor: '#f8f9fa' }}>
            <tr>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>ID</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Nombre</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Correo</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Teléfono</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Rol</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Estado</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.usuario_id}>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{user.usuario_id}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{user.nombre_completo}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{user.correo}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{user.telefono}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{user.role.nombre}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>
                  <span style={{ 
                    padding: '4px 8px', 
                    borderRadius: '4px', 
                    backgroundColor: user.estado === 'activo' ? '#d4edda' : '#f8d7da',
                    color: user.estado === 'activo' ? '#155724' : '#721c24',
                    fontSize: '12px'
                  }}>
                    {user.estado}
                  </span>
                </td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>
                  <button 
                    onClick={() => handleEdit(user)}
                    style={{ marginRight: '5px', padding: '5px 10px', backgroundColor: '#f39c12', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer', fontSize: '12px' }}
                  >
                    Editar
                  </button>
                  <button 
                    onClick={() => handleToggleStatus(user.usuario_id)}
                    style={{ marginRight: '5px', padding: '5px 10px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer', fontSize: '12px' }}
                  >
                    Toggle
                  </button>
                  <button 
                    onClick={() => handleDelete(user.usuario_id)}
                    style={{ padding: '5px 10px', backgroundColor: '#e74c3c', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer', fontSize: '12px' }}
                  >
                    Eliminar
                  </button>
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