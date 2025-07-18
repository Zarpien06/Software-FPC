import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [correo, setCorreo] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/auth/login-json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ correo, password })  // 👈 usa 'correo' como lo espera FastAPI
      });

      if (response.status === 422) {
        setError('Correo o contraseña inválidos');
        return;
      }

      if (!response.ok) throw new Error('Error en el servidor');

      const data = await response.json();
      const { access_token, user_info } = data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user_info));

      switch (user_info.role.nombre.toLowerCase()) {
  case 'administrador':
    navigate('/admin/dashboard');
    break;
  case 'empleado':
    navigate('/empleado/dashboard');
    break;
  case 'cliente':
    navigate('/cliente/dashboard');
    break;
  default:
    navigate('/');
}

    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      setError('Ocurrió un error al iniciar sesión. Por favor, inténtalo de nuevo más tarde.');
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
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
};

export default Login;
