import { useState } from 'react';
import '../assets/css/FormAuth.css';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';


const Registro: React.FC = () => {
    const [isRegistering, setIsRegistering] = useState<boolean>(true);
    const [form, setForm] = useState({
        nombre: '',
        celular: '',
        tipoId: '',
        numeroId: '',
        correo: '',
        contrasena: '',
        confirmar: '',
    });


    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (isRegistering) {
            if (form.contrasena !== form.confirmar) {
                alert('Las contraseñas no coinciden');
                return;
            }

            // Preparar el body con los nombres de campo que espera tu API
            const body = {
                correo: form.correo,
                nombre_completo: form.nombre,
                numero_identificacion: form.numeroId,
                password: form.contrasena,
                telefono: form.celular,
                tipo_identificacion: form.tipoId.toLowerCase(),
            };

            try {
                const response = await fetch('http://localhost:8000/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(body),
                });

                if (response.status === 201) {
                    alert('Registro exitoso. Ya puedes iniciar sesión.');
                    setIsRegistering(false);
                    setForm({
                        nombre: '',
                        celular: '',
                        tipoId: '',
                        numeroId: '',
                        correo: '',
                        contrasena: '',
                        confirmar: '',
                    });
                } else {
                    // Intentar leer el error JSON
                    let errorMsg = 'Error en el registro.';
                    try {
                        const errorData = await response.json();
                        // El backend puede enviar error como array de detalles
                        if (errorData.detail) {
                            if (Array.isArray(errorData.detail)) {
                                errorMsg = errorData.detail.map((d: any) => d.msg).join(', ');
                            } else if (typeof errorData.detail === 'string') {
                                errorMsg = errorData.detail;
                            }
                        }
                    } catch {
                        // No JSON, ignorar
                    }
                    alert(errorMsg);
                }
            } catch (error) {
                console.error('Error en el registro:', error);
                alert('Ocurrió un error al conectar con el servidor.');
            }
        } else {
            // Aquí podrías implementar login o redirigir al login real
            alert('Por favor, utiliza el formulario de login para iniciar sesión.');
        }
    };

    const toggleMode = () => {
        setIsRegistering(!isRegistering);
        setForm({
            nombre: '',
            celular: '',
            tipoId: '',
            numeroId: '',
            correo: '',
            contrasena: '',
            confirmar: '',
        });
    };

    return (
        <>
            <Navbar scrolled={false} />
            <div className="form-container">
                <h2>{isRegistering ? 'Registrarse' : 'Iniciar Sesión'}</h2>
                <form onSubmit={handleSubmit}>
                    {isRegistering && (
                        <>
                            <input
                                name="nombre"
                                type="text"
                                placeholder="Nombre completo"
                                value={form.nombre}
                                onChange={handleChange}
                                required
                            />
                            <input
                                name="celular"
                                type="tel"
                                placeholder="Número de celular"
                                value={form.celular}
                                onChange={handleChange}
                                required
                            />
                            <select
                                name="tipoId"
                                value={form.tipoId}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Tipo de identificación</option>
                                <option value="CC">Cédula</option>
                                <option value="TI">Tarjeta de Identidad</option>
                                <option value="CE">Cédula de Extranjería</option>
                            </select>
                            <input
                                name="numeroId"
                                type="text"
                                placeholder="Número de identificación"
                                value={form.numeroId}
                                onChange={handleChange}
                                required
                            />
                        </>
                    )}
                    <input
                        name="correo"
                        type="email"
                        placeholder="Correo electrónico"
                        value={form.correo}
                        onChange={handleChange}
                        required
                    />
                    <input
                        name="contrasena"
                        type="password"
                        placeholder="Contraseña"
                        value={form.contrasena}
                        onChange={handleChange}
                        required
                    />
                    {isRegistering && (
                        <input
                            name="confirmar"
                            type="password"
                            placeholder="Confirmar contraseña"
                            value={form.confirmar}
                            onChange={handleChange}
                            required
                        />
                    )}
                    <button type="submit">{isRegistering ? 'Registrarse' : 'Iniciar Sesión'}</button>
                </form>

                <div className="toggle-auth">
                    {isRegistering ? (
                        <p>
                            ¿Ya tienes una cuenta?{' '}
                            <button type="button" onClick={toggleMode}>
                                Inicia sesión
                            </button>
                        </p>
                    ) : (
                        <p>
                            ¿No tienes una cuenta?{' '}
                            <button type="button" onClick={toggleMode}>
                                Regístrate
                            </button>
                        </p>
                    )}
                </div>
            </div>
            <Footer />
        </>
    );
};

export default Registro;
