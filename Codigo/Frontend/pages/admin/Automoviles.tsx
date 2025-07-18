import React, { useState, useEffect } from 'react';

const Automoviles = () => {
  const [automoviles, setAutomoviles] = useState([]);
  const [formData, setFormData] = useState({ placa: '', vin: '', marca: '', modelo: '', anio: '' });
  const [editandoId, setEditandoId] = useState(null);
  const [busqueda, setBusqueda] = useState('');

  const fetchAutomoviles = async () => {
    try {
      const res = await fetch('http://localhost:8000/automoviles');
      const data = await res.json();
      setAutomoviles(data);
    } catch (error) {
      console.error('Error al obtener automóviles:', error);
    }
  };

  useEffect(() => {
    fetchAutomoviles();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const url = editandoId
        ? `http://localhost:8000/automoviles/${editandoId}`
        : 'http://localhost:8000/automoviles';
      const method = editandoId ? 'PUT' : 'POST';
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (res.ok) {
        fetchAutomoviles();
        setFormData({ placa: '', vin: '', marca: '', modelo: '', anio: '' });
        setEditandoId(null);
      }
    } catch (error) {
      console.error('Error al guardar/editar automóvil:', error);
    }
  };

  const handleEdit = (auto) => {
    setFormData(auto);
    setEditandoId(auto.id);
  };

  const handleDelete = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/automoviles/${id}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        fetchAutomoviles();
      }
    } catch (error) {
      console.error('Error al eliminar automóvil:', error);
    }
  };

  const automovilesFiltrados = automoviles.filter((auto) =>
    Object.values(auto).some((valor) =>
      String(valor).toLowerCase().includes(busqueda.toLowerCase())
    )
  );

  return (
    <div style={{ padding: '20px' }}>
      <h1>Gestión de Automóviles</h1>

      <input
        type="text"
        placeholder="Buscar..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
        style={{ marginBottom: '20px', padding: '5px', width: '300px' }}
      />

      <form onSubmit={handleSubmit} style={{ marginBottom: '30px' }}>
        <input type="text" name="placa" placeholder="Placa" value={formData.placa} onChange={handleChange} required />
        <input type="text" name="vin" placeholder="VIN" value={formData.vin} onChange={handleChange} />
        <input type="text" name="marca" placeholder="Marca" value={formData.marca} onChange={handleChange} required />
        <input type="text" name="modelo" placeholder="Modelo" value={formData.modelo} onChange={handleChange} />
        <input type="number" name="anio" placeholder="Año" value={formData.anio} onChange={handleChange} />
        <button type="submit">{editandoId ? 'Actualizar' : 'Crear'}</button>
      </form>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Placa</th>
            <th>VIN</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Año</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {automovilesFiltrados.map((auto) => (
            <tr key={auto.id}>
              <td>{auto.id}</td>
              <td>{auto.placa}</td>
              <td>{auto.vin}</td>
              <td>{auto.marca}</td>
              <td>{auto.modelo}</td>
              <td>{auto.anio}</td>
              <td>
                <button onClick={() => handleEdit(auto)}>Editar</button>
                <button onClick={() => handleDelete(auto.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Automoviles;
