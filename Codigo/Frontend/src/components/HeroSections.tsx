import React from 'react';
import '../assets/css/HeroSection.css';
import videoBackgroundWebm from '../assets/fpc.webm';

const HeroSection: React.FC = () => {
    return (
        <section id="inicio" className="hero-section">
            <div className="video-container">
                <video autoPlay muted loop playsInline className="background-video">
                    <source src={videoBackgroundWebm} type="video/webm" />
                    Tu navegador no soporta videos HTML5.
                </video>
                <div className="overlay"></div>
            </div>

            <div className="hero-content">
                <h1>FPC - Software de Seguimiento de Vehículos en Taller</h1>
                <p>Plataforma integral para el seguimiento y gestión de vehículos dentro de un taller automotriz</p>
                <div className="hero-buttons">
                    <a href="#caracteristicas" className="btn btn-primary">Conocer más</a>
                    <a href="/Registro" className="btn btn-secondary">Registrarse</a>
                </div>
            </div>
        </section>
    );
};

export default HeroSection;