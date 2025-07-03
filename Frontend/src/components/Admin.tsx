import { useState } from 'react';
import '../assets/css/admin.css';
import logo from '../assets/logo.png';

interface NavbarProps {
    scrolled: boolean;
}

const AdminNavbar: React.FC<NavbarProps> = ({ scrolled }) => {
    const [menuOpen, setMenuOpen] = useState<boolean>(false);
    const [activeMenu, setActiveMenu] = useState<string>('Dashboard');

    const toggleMenu = (): void => {
        setMenuOpen(!menuOpen);
    };

    const menuItems = [
        { name: 'Dashboard', completed: false },
        { name: 'Usuarios', completed: true },
        { name: 'Roles', completed: false },
        { name: 'Automoviles', completed: false },
        { name: 'Chat', completed: false },
        { name: 'Reportes', completed: false },
        { name: 'Cotizaciones', completed: false },
        { name: 'Process', completed: false },
    ];

    return (
        <nav className={`admin-navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="container">
                <div className="navbar-brand">
                    <img src={logo} alt="Admin Logo" className="logo" />
                    <span className="brand-name">Admin</span>
                </div>

                <div className={`menu-toggle ${menuOpen ? 'active' : ''}`} onClick={toggleMenu}>
                    <div className="hamburger"></div>
                </div>

                <ul className={`navbar-menu ${menuOpen ? 'active' : ''}`}>
                    {menuItems.map((item) => (
                        <li 
                            key={item.name}
                            className={`${activeMenu === item.name ? 'active' : ''} ${item.completed ? 'completed' : ''}`}
                            onClick={() => {
                                setActiveMenu(item.name);
                                setMenuOpen(false);
                            }}
                        >
                            <a href={`#${item.name.toLowerCase()}`}>
                                {item.completed ? '✓ ' : ''}{item.name}
                            </a>
                        </li>
                    ))}
                    <li className="logout-button">
                        <a href="/logout" className="btn btn-logout">Cerrar Sesión</a>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default AdminNavbar;