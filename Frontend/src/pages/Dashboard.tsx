import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faHome, faUsers, faUserTag, faCar, faComments, 
  faChartBar, faFileInvoiceDollar, faTasks, 
  faSignOutAlt, faBars, faSearch, faBell, 
  faEnvelope, faUserPlus, faFileInvoice, 
  faPaperPlane, faChartLine, faDownload, 
  faEye, faPlus, faEdit, faTrash 
} from '@fortawesome/free-solid-svg-icons';
import '../App.css';

type UserData = {
  nombre: string;
  correo?: string;
  rol?: string;
  avatar?: string;
};

type RecentUser = {
  id: number;
  nombre: string;
  correo: string;
  rol: string;
  avatar: string;
};

type ChatMessage = {
  id: number;
  sender: string;
  avatar: string;
  message: string;
  time: string;
  isSent: boolean;
};

type Report = {
  id: number;
  title: string;
  type: string;
  date: string;
};

type Quotation = {
  id: string;
  client: string;
  date: string;
  amount: string;
  status: 'pending' | 'approved' | 'rejected';
};

const Dashboard = () => {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  // Datos de ejemplo para las secciones del dashboard
  const [recentUsers] = useState<RecentUser[]>([
    { id: 1, nombre: 'Juan Pérez', correo: 'juan@ejemplo.com', rol: 'Admin', avatar: '/api/placeholder/40/40' },
    { id: 2, nombre: 'María López', correo: 'maria@ejemplo.com', rol: 'Usuario', avatar: '/api/placeholder/40/40' },
    { id: 3, nombre: 'Carlos Rodríguez', correo: 'carlos@ejemplo.com', rol: 'Editor', avatar: '/api/placeholder/40/40' },
    { id: 4, nombre: 'Ana Martínez', correo: 'ana@ejemplo.com', rol: 'Usuario', avatar: '/api/placeholder/40/40' },
  ]);

  const [chatMessages] = useState<ChatMessage[]>([
    { id: 1, sender: 'María López', avatar: '/api/placeholder/40/40', message: 'Hola, necesito ayuda con mi cotización #1234', time: 'Hace 10 min', isSent: false },
    { id: 2, sender: 'Admin', avatar: '/api/placeholder/40/40', message: 'Claro, revisaré los detalles y te contactaré pronto.', time: 'Hace 8 min', isSent: true },
    { id: 3, sender: 'Carlos Rodríguez', avatar: '/api/placeholder/40/40', message: '¿Cuándo estará listo el nuevo módulo?', time: 'Hace 5 min', isSent: false },
  ]);

  const [reports] = useState<Report[]>([
    { id: 1, title: 'Reporte de Ventas Abril 2025', type: 'sales', date: '05/04/2025' },
    { id: 2, title: 'Actividad de Usuarios Q1 2025', type: 'users', date: '01/04/2025' },
    { id: 3, title: 'Estado de Procesos Marzo 2025', type: 'processes', date: '31/03/2025' },
  ]);

  const [quotations] = useState<Quotation[]>([
    { id: 'COT-001', client: 'Empresa ABC S.A.', date: '05/04/2025', amount: '$1,500.00', status: 'pending' },
    { id: 'COT-002', client: 'Corporación XYZ', date: '04/04/2025', amount: '$2,750.00', status: 'approved' },
    { id: 'COT-003', client: 'Industrias 123', date: '03/04/2025', amount: '$950.00', status: 'rejected' },
    { id: 'COT-004', client: 'Servicios Omega', date: '02/04/2025', amount: '$3,200.00', status: 'pending' },
  ]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchUserData = async () => {
      try {
        const response = await fetch('http://localhost:8000/auth/user-data', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('No autorizado');
        }

        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error('Error al obtener datos:', error);
        localStorage.removeItem('token');
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  if (!userData) {
    return <div className="dashboard-loading">Cargando...</div>;
  }

  return (
    <div className={`container ${sidebarOpen ? '' : 'sidebar-collapsed'}`}>
      {/* Sidebar */}
      <nav className="sidebar">
        <div className="logo">
          <h2>Admin</h2>
        </div>
        <ul className="menu">
          <li className="active">
            <a href="#">
              <FontAwesomeIcon icon={faHome} /> Dashboard
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faUsers} /> Usuarios
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faUserTag} /> Roles
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faCar} /> Automoviles
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faComments} /> Chat
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faChartBar} /> Reportes
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faFileInvoiceDollar} /> Cotizaciones
            </a>
          </li>
          <li>
            <a href="#">
              <FontAwesomeIcon icon={faTasks} /> Procesos
            </a>
          </li>
        </ul>
        <div className="logout">
          <a onClick={handleLogout}>
            <FontAwesomeIcon icon={faSignOutAlt} /> Cerrar Sesión
          </a>
        </div>
      </nav>

      {/* Main Content */}
      <main className="content">
        {/* Top Header */}
        <header className="header">
          <div className="toggle-menu" onClick={toggleSidebar}>
            <FontAwesomeIcon icon={faBars} />
          </div>
          <div className="search-bar">
            <input 
              type="text" 
              placeholder="Buscar..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button><FontAwesomeIcon icon={faSearch} /></button>
          </div>
          <div className="user-info">
            <div className="notifications">
              <FontAwesomeIcon icon={faBell} />
              <span className="badge">5</span>
            </div>
            <div className="messages">
              <FontAwesomeIcon icon={faEnvelope} />
              <span className="badge">3</span>
            </div>
            <div className="profile">
              <img src={userData.avatar || '/api/placeholder/40/40'} alt="Usuario" />
              <span>{userData.nombre}</span>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="dashboard-content">
          <div className="page-title">
            <h1>Dashboard</h1>
            <p>Bienvenido al panel de administración, {userData.nombre}</p>
          </div>
          
          {/* Stats Cards */}
          <div className="stats-container">
            <div className="stat-card">
              <div className="stat-value">
                <h3>1,254</h3>
                <p>Usuarios Totales</p>
              </div>
              <div className="stat-icon">
                <FontAwesomeIcon icon={faUsers} />
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-value">
                <h3>145</h3>
                <p>Nuevos Usuarios</p>
              </div>
              <div className="stat-icon">
                <FontAwesomeIcon icon={faUserPlus} />
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-value">
                <h3>50</h3>
                <p>Cotizaciones Pendientes</p>
              </div>
              <div className="stat-icon">
                <FontAwesomeIcon icon={faFileInvoice} />
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-value">
                <h3>24</h3>
                <p>Mensajes Nuevos</p>
              </div>
              <div className="stat-icon">
                <FontAwesomeIcon icon={faEnvelope} />
              </div>
            </div>
          </div>

          {/* Widgets Row */}
          <div className="widgets-row">
            {/* Recent Users */}
            <div className="widget">
              <div className="widget-header">
                <h3>Usuarios Recientes</h3>
                <a href="#" className="view-all">Ver Todos</a>
              </div>
              <div className="widget-content">
                <div className="user-list">
                  {recentUsers.map(user => (
                    <div className="user-item" key={user.id}>
                      <img src={user.avatar} alt="Usuario" />
                      <div className="user-info">
                        <h4>{user.nombre}</h4>
                        <p>{user.correo}</p>
                      </div>
                      <span className={`user-role ${user.rol.toLowerCase() === 'admin' ? 'admin' : ''}`}>
                        {user.rol}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Chat Widget */}
            <div className="widget">
              <div className="widget-header">
                <h3>Mensajes Recientes</h3>
                <a href="#" className="view-all">Ver Todos</a>
              </div>
              <div className="widget-content">
                <div className="chat-container">
                  {chatMessages.map(message => (
                    <div className={`chat-message ${message.isSent ? 'sent' : 'received'}`} key={message.id}>
                      {!message.isSent && <img src={message.avatar} alt="Usuario" />}
                      <div className="message-content">
                        <div className="message-info">
                          <h4>{message.sender}</h4>
                          <span>{message.time}</span>
                        </div>
                        <p>{message.message}</p>
                      </div>
                      {message.isSent && <img src={message.avatar} alt="Admin" />}
                    </div>
                  ))}
                </div>
                <div className="chat-input">
                  <input type="text" placeholder="Escribe un mensaje..." />
                  <button><FontAwesomeIcon icon={faPaperPlane} /></button>
                </div>
              </div>
            </div>
          </div>

          {/* Charts and Reports Row */}
          <div className="charts-row">
            {/* Graph Widget */}
            <div className="widget">
              <div className="widget-header">
                <h3>Actividad de Usuarios</h3>
                <div className="widget-actions">
                  <select>
                    <option>Últimos 7 días</option>
                    <option>Último mes</option>
                    <option>Último año</option>
                  </select>
                </div>
              </div>
              <div className="widget-content">
                <div className="chart-container">
                  {/* Aquí iría el gráfico con Chart.js */}
                  <div className="chart-placeholder">
                    <FontAwesomeIcon icon={faChartLine} size="3x" />
                    <p>Gráfico de actividad de usuarios</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Reports Widget */}
            <div className="widget">
              <div className="widget-header">
                <h3>Reportes Recientes</h3>
                <a href="#" className="view-all">Ver Todos</a>
              </div>
              <div className="widget-content">
                <div className="reports-list">
                  {reports.map(report => (
                    <div className="report-item" key={report.id}>
                      <div className="report-icon">
                        <FontAwesomeIcon icon={
                          report.type === 'sales' ? faChartLine : 
                          report.type === 'users' ? faUsers : faTasks
                        } />
                      </div>
                      <div className="report-info">
                        <h4>{report.title}</h4>
                        <p>Generado: {report.date}</p>
                      </div>
                      <div className="report-actions">
                        <button><FontAwesomeIcon icon={faDownload} /></button>
                        <button><FontAwesomeIcon icon={faEye} /></button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Cotizaciones Section */}
          <div className="full-width-section">
            <div className="widget">
              <div className="widget-header">
                <h3>Cotizaciones Recientes</h3>
                <div className="widget-actions">
                  <button className="btn-primary">
                    <FontAwesomeIcon icon={faPlus} /> Nueva Cotización
                  </button>
                </div>
              </div>
              <div className="widget-content">
                <div className="table-responsive">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>#ID</th>
                        <th>Cliente</th>
                        <th>Fecha</th>
                        <th>Monto</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {quotations.map(quotation => (
                        <tr key={quotation.id}>
                          <td>#{quotation.id}</td>
                          <td>{quotation.client}</td>
                          <td>{quotation.date}</td>
                          <td>{quotation.amount}</td>
                          <td>
                            <span className={`status ${quotation.status}`}>
                              {quotation.status === 'pending' ? 'Pendiente' : 
                               quotation.status === 'approved' ? 'Aprobada' : 'Rechazada'}
                            </span>
                          </td>
                          <td>
                            <button className="btn-icon"><FontAwesomeIcon icon={faEye} /></button>
                            <button className="btn-icon"><FontAwesomeIcon icon={faEdit} /></button>
                            <button className="btn-icon"><FontAwesomeIcon icon={faTrash} /></button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;