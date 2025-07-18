import '../assets/css/HowItWorks.css';  // Cambia la ruta aquí
import { FaCarSide, FaTools, FaComment, FaCheckCircle } from 'react-icons/fa';

// Cambié JSX.Element por React.ElementType
interface Step {
    icon: React.ElementType; // Uso React.ElementType para un componente
    title: string;
    description: string;
}

const HowItWorks: React.FC = () => {
    const steps: Step[] = [
        {
            icon: FaCarSide, // Paso el componente directamente, no JSX
            title: "Ingreso del vehículo al taller",
            description: "Cuando un vehículo llega al taller, el cliente ingresa la información básica del vehículo (modelo, año, tipo de reparación, etc.) en la plataforma FPC."
        },
        {
            icon: FaTools,
            title: "Seguimiento del estado de la reparación",
            description: "A medida que los empleados trabajan en el vehículo, se actualiza el estado de la reparación en el sistema, permitiendo que el cliente vea en qué etapa se encuentra el trabajo."
        },
        {
            icon: FaComment,
            title: "Interacción en tiempo real",
            description: "A través del chat en vivo, el cliente puede comunicarse directamente con los empleados para recibir actualizaciones, hacer preguntas o resolver cualquier duda sobre el proceso de reparación."
        },
        {
            icon: FaCheckCircle,
            title: "Notificación de finalización",
            description: "Una vez que el trabajo en el vehículo está completo, el cliente recibe una notificación y puede revisar un informe detallado de las reparaciones realizadas."
        }
    ];

    return (
        <section id="funcionamiento" className="how-it-works-section">
            <div className="container">
                <div className="section-header">
                    <h2>¿Cómo Funciona?</h2>
                    <p>Conoce el proceso de uso de nuestra plataforma FPC</p>
                </div>

                <div className="steps-container">
                    {steps.map((step, index) => (
                        <div className="step" key={index}>
                            <div className="step-number">{index + 1}</div>
                            <div className="step-content">
                                <div className="step-icon">
                                    {/* Uso del componente aquí */}
                                    <step.icon style={{ fontSize: '2rem', color: '#051f57' }} />
                                </div>
                                <h3>{step.title}</h3>
                                <p>{step.description}</p>
                            </div>
                            {index < steps.length - 1 && <div className="connector"></div>}
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default HowItWorks;