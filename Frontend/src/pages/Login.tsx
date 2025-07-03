import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/css/FormAuth.css';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!email || !password) {
            alert('Por favor, complete todos los campos.');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/auth/login-json', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Quitar 'credentials: include' si no usas cookies
                body: JSON.stringify({
                    correo: email,
                    password
                }),
            });

            if (!response.ok) {
                // Si la respuesta no es JSON válido, captura el error general
                let errorMsg = 'No se pudo iniciar sesión.';
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.detail || errorMsg;
                } catch {
                    // Ignorar error parseando JSON
                }
                alert(`Error: ${errorMsg}`);
                return;
            }

            const data = await response.json();
            console.log('Login exitoso:', data);

            // Guardar token para usar en futuras peticiones
            if (data.access_token) {
                localStorage.setItem('token', data.access_token);
            }

            // Redirigir tras login exitoso
            navigate('/dashboard');
        } catch (error) {
            console.error('Error al iniciar sesión:', error);
            alert('Ocurrió un error al conectar con el servidor.');
        }
    };

    return (
        <>
            <Navbar scrolled={false} />
            <div className="form-container">
                <h2>Iniciar Sesión</h2>
                <form onSubmit={handleLogin}>
                    <input
                        type="email"
                        placeholder="Correo electrónico"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Contraseña"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit">Entrar</button>
                </form>

                <div className="toggle-auth">
                    <p>
                        ¿No tienes una cuenta?{' '}
                        <button type="button" onClick={() => navigate('/registro')}>
                            Regístrate
                        </button>
                    </p>
                </div>
            </div>
            <Footer />
        </>
    );
};

export default Login;
