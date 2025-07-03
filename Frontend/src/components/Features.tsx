import '../assets/css/Features.css';  // Cambia la ruta aquí
import { FaCarAlt, FaComments, FaHistory, FaBell, FaClipboardCheck } from 'react-icons/fa'; // Necesitarás instalar react-icons

interface Feature {
    icon: React.ElementType; // Cambié JSX.Element a React.ElementType
    title: string;
    description: string;
}

const Features: React.FC = () => {
    const features: Feature[] = [
        {
            icon: FaCarAlt, // Aquí pasamos el componente en vez de JSX
            title: "Seguimiento del proceso de reparación",
            description: "Los clientes pueden ver el estado de su vehículo en cada etapa del proceso de reparación, ya sea en latonería, pintura, alistamiento interno u otros servicios específicos."
        },
        {
            icon: FaComments,
            title: "Chat en tiempo real",
            description: "Los clientes pueden comunicarse directamente con los empleados del taller a través de un sistema de chat integrado, recibiendo actualizaciones sobre el progreso de la reparación."
        },
        {
            icon: FaHistory,
            title: "Historial completo del vehículo",
            description: "El sistema guarda un registro detallado de todos los trabajos realizados en el vehículo, incluyendo fechas, tipos de reparaciones y detalles de cada servicio."
        },
        {
            icon: FaBell,
            title: "Notificaciones automáticas",
            description: "Los usuarios reciben alertas automáticas sobre cambios importantes en el estado de su vehículo, como la finalización de una etapa del proceso."
        },
        {
            icon: FaClipboardCheck,
            title: "Estado detallado de cada trabajo",
            description: "La plataforma muestra información detallada sobre el avance de cada trabajo, actualizada en tiempo real para mantener al cliente informado."
        }
    ];

    return (
        <section id="caracteristicas" className="features-section">
            <div className="container">
                <div className="section-header">
                    <h2>Características</h2>
                    <p>Descubre todas las herramientas que FPC tiene para mejorar la gestión de tu taller</p>
                </div>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <div className="feature-card" key={index}>
                            <div className="feature-icon">
                                <feature.icon style={{
                                    fontSize: '2rem', color: '#051f57' }} />
                                {/* Usamos <feature.icon /> para renderizar el ícono */}
                            </div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Features;