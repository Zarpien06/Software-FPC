import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/auth/login-json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, password })
      });

      if (response.status === 422) {
        setError('Correo o contraseña inválidos');
        return;
      }

      if (!response.ok) throw new Error('Error en el servidor');

      const data = await response.json();
      const { access_token, user_info } = data;

      console.log('=== LOGIN EXITOSO ===');
      console.log('Token recibido:', access_token);
      console.log('User Info recibido:', user_info);
      console.log('Rol del usuario:', user_info.role);

      // Guardar en localStorage con los mismos nombres que busca App.js
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_info', JSON.stringify(user_info));

      console.log('Datos guardados en localStorage');
      console.log('Token guardado:', localStorage.getItem('access_token'));
      console.log('User info guardado:', localStorage.getItem('user_info'));

      // Verificar que se puede parsear
      try {
        const parsed = JSON.parse(localStorage.getItem('user_info') || '{}');
        console.log('Datos parseados:', parsed);
        console.log('Estructura del rol:', parsed.role);
      } catch (e) {
        console.error('Error parseando:', e);
      }

      // Navegar basado en el rol usando las rutas correctas de App.js
      const roleName = user_info.role?.nombre?.toLowerCase();
      console.log('Rol normalizado:', roleName);

      switch (roleName) {
        case 'administrador':
        case 'admin':
          console.log('Navegando a dashboard admin');
          navigate('/dashboard-admin');
          break;
        case 'empleado':
          console.log('Navegando a dashboard empleado');
          navigate('/dashboard-empleado');
          break;
        case 'cliente':
          console.log('Navegando a dashboard cliente');
          navigate('/dashboard-cliente');
          break;
        default:
          console.log('Rol no reconocido, navegando a dashboard genérico');
          navigate('/dashboard');
      }

    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      setError('Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo más tarde.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <h2>Iniciar Sesión</h2>
        {error && <p className="error-message">{error}</p>}
        <input
          type="email"
          placeholder="Correo electrónico"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Ingresando...' : 'Ingresar'}
        </button>
      </form>
    </div>
  );
};

export default Login;