import { useState } from 'react';
import '../../assets/css/admin/Navbar.css'; // Estilo para dashboard
import logo from '../../assets/logo.png'; // Usa tu logo actual

const NavbarAdmin = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen(!menuOpen);

  return (
    <nav className="navbar-admin">
      <div className="admin-container">
        <div className="navbar-brand">
          <img src={logo} alt="FPC Logo" className="logo" />
          <span className="brand-name">Panel Admin</span>
        </div>

        <div className={`menu-toggle ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
          <div className="hamburger"></div>
        </div>

        <ul className={`navbar-menu ${menuOpen ? 'active' : ''}`}>
          <li><a href="/admin/dashboard" onClick={() => setMenuOpen(false)}>Inicio</a></li>
          <li><a href="/admin/usuarios" onClick={() => setMenuOpen(false)}>Usuarios</a></li>
          <li><a href="/admin/roles" onClick={() => setMenuOpen(false)}>Roles</a></li>
          <li><a href="/admin/automoviles" onClick={() => setMenuOpen(false)}>Automóviles</a></li>
          <li className="logout-button">
            <a href="/" className="btn btn-logout">Cerrar Sesión</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavbarAdmin;
