import '../assets/css/Benefits.css';  // Cambia la ruta aquí
import { FaHandshake, FaCommentDots, FaTasks, FaUserCog } from 'react-icons/fa';

// Cambié JSX.Element por React.ElementType
interface Benefit {
    icon: React.ElementType; // Usamos React.ElementType para el ícono
    title: string;
    description: string;
}

const Benefits: React.FC = () => {
    const benefits: Benefit[] = [
        {
            icon: FaHandshake,  // Pasamos el componente directamente
            title: "Transparencia y confianza",
            description: "Los clientes pueden ver el progreso detallado de la reparación de su vehículo, lo que mejora la confianza en el taller y reduce la incertidumbre."
        },
        {
            icon: FaCommentDots,
            title: "Mejora en la comunicación",
            description: "El chat en tiempo real permite que los clientes se comuniquen de manera rápida y directa con el personal del taller, facilitando la resolución de dudas."
        },
        {
            icon: FaTasks,
            title: "Gestión eficiente de reparaciones",
            description: "El sistema ayuda a los talleres a gestionar mejor el flujo de trabajo y a mantener a los clientes informados en todo momento, reduciendo la carga administrativa."
        },
        {
            icon: FaUserCog,
            title: "Experiencia personalizada",
            description: "Gracias a las notificaciones y actualizaciones constantes, el cliente tiene una experiencia más personalizada y controlada sobre el proceso de reparación."
        }
    ];

    return (
        <section id="beneficios" className="benefits-section">
            <div className="container">
                <div className="section-header">
                    <h2>Beneficios</h2>
                    <p>Descubre cómo FPC mejora la experiencia tanto para talleres como para clientes</p>
                </div>

                <div className="benefits-container">
                    {benefits.map((benefit, index) => (
                        <div className="benefit-card" key={index}>
                            <div className="benefit-icon">
                                {/* Usamos el componente directamente */}
                                <benefit.icon style={{ fontSize: '2rem', color: '#051f57' }} />
                            </div>
                            <div className="benefit-content">
                                <h3>{benefit.title}</h3>
                                <p>{benefit.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Benefits;