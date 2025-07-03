import { useState } from 'react';
import '../assets/css/Navbar.css';  // Cambia la ruta aquí
import logo from '../assets/logo.png'; // Asegúrate de tener un logo en esta ruta

interface NavbarProps {
    scrolled: boolean;
}

const Navbar: React.FC<NavbarProps> = ({ scrolled }) => {
    const [menuOpen, setMenuOpen] = useState<boolean>(false);

    const toggleMenu = (): void => {
        setMenuOpen(!menuOpen);
    };

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="container">
                <div className="navbar-brand">
                    <img src={logo} alt="FPC Logo" className="logo" />
                    <span className="brand-name">FPC</span>
                </div>

                <div className={`menu-toggle ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
                    <div className="hamburger"></div>
                </div>

                <ul className={`navbar-menu ${menuOpen ? 'active' : ''}`}>
                    <li><a href="#inicio" onClick={() => setMenuOpen(false)}>Inicio</a></li>
                    <li><a href="#caracteristicas" onClick={() => setMenuOpen(false)}>Características</a></li>
                    <li><a href="#funcionamiento" onClick={() => setMenuOpen(false)}>Cómo Funciona</a></li>
                    <li><a href="#beneficios" onClick={() => setMenuOpen(false)}>Beneficios</a></li>
                    <li className="login-button">
                        <a href="/login" className="btn btn-login">Iniciar Sesión</a>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
