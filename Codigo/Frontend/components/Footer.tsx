import '../assets/css/Footer.css';  // Cambia la ruta aquí
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin, FaEnvelope, FaPhone, FaMapMarkerAlt } from 'react-icons/fa';

const Footer: React.FC = () => {
    return (
        <footer id="contacto" className="footer">
            <div className="container">
                <div className="footer-content">
                    <div className="footer-section about">
                        <h3>FPC</h3>
                        <p>
                            Software de seguimiento de vehículos en taller que permite a los clientes
                            obtener información detallada y en tiempo real sobre el progreso de las
                            reparaciones y servicios que se realizan en sus vehículos.
                        </p>
                        <div className="social-icons">
                            <a href="#"><FaFacebook /></a>
                            <a href="#"><FaTwitter /></a>
                            <a href="#"><FaInstagram /></a>
                            <a href="#"><FaLinkedin /></a>
                        </div>
                    </div>

                    <div className="footer-section links">
                        <h3>Enlaces Rápidos</h3>
                        <ul>
                            <li><a href="#inicio">Inicio</a></li>
                            <li><a href="#caracteristicas">Características</a></li>
                            <li><a href="#funcionamiento">Cómo Funciona</a></li>
                            <li><a href="#beneficios">Beneficios</a></li>
                            <li><a href="/login">Iniciar Sesión</a></li>
                        </ul>
                    </div>

                    <div className="footer-section contact">
                        <h3>Contacto</h3>
                        <div className="contact-info">
                            <p><FaMapMarkerAlt /> Calle Principal #123, Ciudad</p>
                            <p><FaPhone /> +57 300 123 4567</p>
                            <p><FaEnvelope /> info@fpc.com</p>
                        </div>
                    </div>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; {new Date().getFullYear()} FPC - Todos los derechos reservados</p>
            </div>
        </footer>
    );
};

export default Footer;