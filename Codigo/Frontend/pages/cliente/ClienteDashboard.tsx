// src/pages/cliente/ClienteDashboard.tsx
import useLogout from '../../hooks/useLogout';

const ClienteDashboard = () => {
    const logout = useLogout();

    return (
        <div>
            <h2>Dashboard de Cliente</h2>
            <p>Bienvenido cliente</p>
            <button onClick={logout}>Cerrar sesión</button>
        </div>
    );
};

export default ClienteDashboard;
