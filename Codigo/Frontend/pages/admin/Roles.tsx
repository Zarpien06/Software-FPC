import React, { useState, useEffect } from 'react';
import { apiService, Role, CreateRoleData } from '../../api/index';

const Roles: React.FC = () => {
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingRole, setEditingRole] = useState<Role | null>(null);
  const [formData, setFormData] = useState<CreateRoleData>({ nombre: '' });

  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAllRoles();
      setRoles(response.roles);
    } catch (error) {
      console.error('Error loading roles:', error);
      alert('Error al cargar roles');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingRole) {
        await apiService.updateRole(editingRole.id, formData);
        alert('Rol actualizado correctamente');
      } else {
        await apiService.createRole(formData);
        alert('Rol creado correctamente');
      }
      setShowForm(false);
      setEditingRole(null);
      setFormData({ nombre: '' });
      await loadRoles();
    } catch (error) {
      console.error('Error saving role:', error);
      alert('Error al guardar rol');
    }
  };

  const handleEdit = (role: Role) => {
    setEditingRole(role);
    setFormData({ nombre: role.nombre });
    setShowForm(true);
  };

  const handleDelete = async (roleId: number) => {
    if (window.confirm('¿Estás seguro de eliminar este rol?')) {
      try {
        await apiService.deleteRole(roleId);
        alert('Rol eliminado correctamente');
        await loadRoles();
      } catch (error) {
        console.error('Error deleting role:', error);
        alert('Error al eliminar rol');
      }
    }
  };

  const resetForm = () => {
    setFormData({ nombre: '' });
    setEditingRole(null);
    setShowForm(false);
  };

  if (loading) return <div>Cargando roles...</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Gestión de Roles</h2>
        <div>
          <button 
            onClick={() => setShowForm(true)}
            style={{ padding: '10px 20px', backgroundColor: '#27ae60', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          >
            Nuevo Rol
          </button>
          <span style={{ marginLeft: '15px' }}>Total: {roles.length}</span>
        </div>
      </div>

      {showForm && (
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h3>{editingRole ? 'Editar Rol' : 'Nuevo Rol'}</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'flex', gap: '15px', alignItems: 'end' }}>
              <div style={{ flex: 1 }}>
                <label>Nombre del Rol:</label>
                <input
                  type="text"
                  placeholder="Ingrese el nombre del rol"
                  value={formData.nombre}
                  onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
                  required
                  style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}
                />
              </div>

              <button 
                type="submit"
                style={{ padding: '10px 20px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                {editingRole ? 'Actualizar' : 'Crear'}
              </button>

              <button 
                type="button"
                onClick={resetForm}
                style={{ padding: '10px 20px', backgroundColor: '#95a5a6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      <div style={{ backgroundColor: 'white', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead style={{ backgroundColor: '#f8f9fa' }}>
            <tr>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>ID</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Nombre</th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {roles.map(role => (
              <tr key={role.id}>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{role.id}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>{role.nombre}</td>
                <td style={{ padding: '12px', borderBottom: '1px solid #eee' }}>
                  <button 
                    onClick={() => handleEdit(role)}
                    style={{ marginRight: '10px', padding: '6px 12px', backgroundColor: '#f1c40f', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                  >
                    Editar
                  </button>
                  <button 
                    onClick={() => handleDelete(role.id)}
                    style={{ padding: '6px 12px', backgroundColor: '#e74c3c', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
            {roles.length === 0 && (
              <tr>
                <td colSpan={3} style={{ padding: '12px', textAlign: 'center', color: '#999' }}>No hay roles registrados.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Roles;
