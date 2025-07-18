// src/pages/empleado/EmpleadoDashboard.tsx
import useLogout from '../../hooks/useLogout';

const EmpleadoDashboard = () => {
    const logout = useLogout();

    return (
        <div>
            <h2>Dashboard de Empleado</h2>
            <p>Bienvenido empleado</p>
            <button onClick={logout}>Cerrar sesión</button>
        </div>
    );
};

export default EmpleadoDashboard;
