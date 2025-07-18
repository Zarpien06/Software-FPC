// api/index.ts
const API_BASE_URL = 'http://localhost:8000';

// Interfaces existentes
export interface User {
  usuario_id: number;
  correo: string;
  nombre_completo: string;
  numero_identificacion: string;
  telefono: string;
  tipo_identificacion: string;
  estado: string;
  rol_id: number;
  fecha_registro: string;
  foto_perfil: string;
  role: {
    id: number;
    nombre: string;
  };
  tipo_identificacion_info: {
    descripcion: string;
    tipo_id: string;
  };
}

export interface Role {
  id: number;
  nombre: string;
}

export interface LoginResponse {
  access_token: string;
  expires_in: number;
  token_type: string;
  user_info: {
    correo: string;
    nombre_completo: string;
    role: Role;
    usuario_id: number;
  };
}

export interface RegisterData {
  correo: string;
  nombre_completo: string;
  numero_identificacion: string;
  password: string;
  telefono: string;
  tipo_identificacion: string;
}

export interface LoginData {
  correo: string;
  password: string;
}

export interface UpdateUserData {
  nombre_completo?: string;
  correo?: string;
  telefono?: string;
  tipo_identificacion: string;
  numero_identificacion?: string;
  estado?: string;
  rol_id?: number;
  foto_perfil?: string;
}

export interface CreateRoleData {
  nombre: string;
}

export interface AssignRoleData {
  user_id: number;
  role_id: number;
}

export interface UsersResponse {
  page: number;
  size: number;
  total: number;
  total_pages: number;
  users: User[];
}

export interface RolesResponse {
  roles: Role[];
  total: number;
}

// Interfaces para Automóviles
export interface Automovil {
  id: number;
  placa: string;
  vin?: string;
  marca: string;
  modelo: string;
  año: number;
  color: string;
  cilindraje?: number;
  numero_motor?: string;
  tipo_combustible: 'gasolina' | 'diesel' | 'gas' | 'electrico' | 'hibrido';
  tipo_transmision: 'manual' | 'automatica' | 'semiautomatica';
  kilometraje_actual: number;
  kilometraje_ingreso?: number;
  estado: 'activo' | 'en_servicio' | 'inactivo' | 'fuera_de_servicio';
  observaciones?: string;
  numero_puertas?: number;
  capacidad_pasajeros?: number;
  fecha_matricula?: string;
  fecha_soat?: string;
  fecha_tecnomecanica?: string;
  created_at: string;
  updated_at: string;
  propietario_id: number;
  propietario: {
    id: number;
    nombre_completo: string;
    correo: string;
    telefono: string;
  };
}

export interface CreateAutomovilData {
  placa: string;
  vin?: string;
  marca: string;
  modelo: string;
  año: number;
  color: string;
  cilindraje?: number;
  numero_motor?: string;
  tipo_combustible?: 'gasolina' | 'diesel' | 'gas' | 'electrico' | 'hibrido';
  tipo_transmision?: 'manual' | 'automatica' | 'semiautomatica';
  kilometraje_actual?: number;
  kilometraje_ingreso?: number;
  estado?: 'activo' | 'en_servicio' | 'inactivo' | 'fuera_de_servicio';
  observaciones?: string;
  numero_puertas?: number;
  capacidad_pasajeros?: number;
  fecha_matricula?: string;
  fecha_soat?: string;
  fecha_tecnomecanica?: string;
  propietario_id: number;
}

export interface UpdateAutomovilData {
  placa?: string;
  vin?: string;
  marca?: string;
  modelo?: string;
  año?: number;
  color?: string;
  cilindraje?: number;
  numero_motor?: string;
  tipo_combustible?: 'gasolina' | 'diesel' | 'gas' | 'electrico' | 'hibrido';
  tipo_transmision?: 'manual' | 'automatica' | 'semiautomatica';
  kilometraje_actual?: number;
  kilometraje_ingreso?: number;
  estado?: 'activo' | 'en_servicio' | 'inactivo' | 'fuera_de_servicio';
  observaciones?: string;
  numero_puertas?: number;
  capacidad_pasajeros?: number;
  fecha_matricula?: string;
  fecha_soat?: string;
  fecha_tecnomecanica?: string;
  propietario_id?: number;
}

export interface AutomovilesResponse {
  items: Automovil[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface AutomovilEstadisticas {
  total_automoviles: number;
  por_estado: Record<string, number>;
  por_marca: Record<string, number>;
  por_año: Record<string, number>;
  por_combustible: Record<string, number>;
  por_transmision: Record<string, number>;
  promedio_kilometraje: number;
  automoviles_proximos_mantenimiento: number;
  automoviles_documentos_vencidos: number;
}

class ApiService {
  private getAuthHeaders(): Record<string, string> {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Error del servidor' }));
      throw new Error(error.detail || `Error ${response.status}`);
    }
    return response.json();
  }

  // AUTH ENDPOINTS
  async register(userData: RegisterData): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return this.handleResponse<User>(response);
  }

  async login(credentials: LoginData): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login-json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    const data = await this.handleResponse<LoginResponse>(response);
    
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user_info', JSON.stringify(data.user_info));
    
    return data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<User>(response);
  }

  async refreshToken(): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse<LoginResponse>(response);
    
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('user_info', JSON.stringify(data.user_info));
    
    return data;
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
  }

  // USER ENDPOINTS
  async getAllUsers(skip = 0, limit = 100, search?: string): Promise<UsersResponse> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
      ...(search && { search })
    });
    
    const response = await fetch(`${API_BASE_URL}/users/?${params}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<UsersResponse>(response);
  }

  async getUserById(userId: number): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<User>(response);
  }

  async getMyProfile(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<User>(response);
  }

  async updateMyProfile(userData: UpdateUserData): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(userData)
    });
    return this.handleResponse<User>(response);
  }

  async updateUser(userId: number, userData: UpdateUserData): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(userData)
    });
    return this.handleResponse<User>(response);
  }

  async deleteUser(userId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    });
    await this.handleResponse<void>(response);
  }

  async toggleUserStatus(userId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/toggle-status`, {
      method: 'PATCH',
      headers: this.getAuthHeaders()
    });
    await this.handleResponse<void>(response);
  }

  // ROLE ENDPOINTS
  async getAllRoles(): Promise<RolesResponse> {
    const response = await fetch(`${API_BASE_URL}/roles/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<RolesResponse>(response);
  }

  async getRoleById(roleId: number): Promise<Role> {
    const response = await fetch(`${API_BASE_URL}/roles/${roleId}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<Role>(response);
  }

  async createRole(roleData: CreateRoleData): Promise<Role> {
    const response = await fetch(`${API_BASE_URL}/roles/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(roleData)
    });
    return this.handleResponse<Role>(response);
  }

  async updateRole(roleId: number, roleData: Partial<CreateRoleData>): Promise<Role> {
    const response = await fetch(`${API_BASE_URL}/roles/${roleId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(roleData)
    });
    return this.handleResponse<Role>(response);
  }

  async deleteRole(roleId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/roles/${roleId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    });
    await this.handleResponse<void>(response);
  }

  async assignRoleToUser(userId: number, assignData: AssignRoleData): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/roles/assign/${userId}`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(assignData)
    });
    return this.handleResponse<User>(response);
  }

  // AUTOMOVIL ENDPOINTS
  async createAutomovil(automovilData: CreateAutomovilData): Promise<Automovil> {
    const response = await fetch(`${API_BASE_URL}/automoviles/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(automovilData)
    });
    return this.handleResponse<Automovil>(response);
  }

  async getAllAutomoviles(
    skip = 0,
    limit = 100,
    filters?: {
      placa?: string;
      marca?: string;
      modelo?: string;
      año_min?: number;
      año_max?: number;
      estado?: string;
      propietario_id?: number;
      tipo_combustible?: string;
      tipo_transmision?: string;
    }
  ): Promise<AutomovilesResponse> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
      ...(filters?.placa && { placa: filters.placa }),
      ...(filters?.marca && { marca: filters.marca }),
      ...(filters?.modelo && { modelo: filters.modelo }),
      ...(filters?.año_min && { año_min: filters.año_min.toString() }),
      ...(filters?.año_max && { año_max: filters.año_max.toString() }),
      ...(filters?.estado && { estado: filters.estado }),
      ...(filters?.propietario_id && { propietario_id: filters.propietario_id.toString() }),
      ...(filters?.tipo_combustible && { tipo_combustible: filters.tipo_combustible }),
      ...(filters?.tipo_transmision && { tipo_transmision: filters.tipo_transmision })
    });
    
    const response = await fetch(`${API_BASE_URL}/automoviles/?${params}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<AutomovilesResponse>(response);
  }

  async getAutomovilById(automovilId: number): Promise<Automovil> {
    const response = await fetch(`${API_BASE_URL}/automoviles/${automovilId}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<Automovil>(response);
  }

  async updateAutomovil(automovilId: number, automovilData: UpdateAutomovilData): Promise<Automovil> {
    const response = await fetch(`${API_BASE_URL}/automoviles/${automovilId}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(automovilData)
    });
    return this.handleResponse<Automovil>(response);
  }

  async deleteAutomovil(automovilId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/automoviles/${automovilId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    });
    await this.handleResponse<void>(response);
  }

  async changeAutomovilStatus(
    automovilId: number, 
    estado: 'activo' | 'en_servicio' | 'inactivo' | 'fuera_de_servicio',
    observaciones?: string
  ): Promise<Automovil> {
    const response = await fetch(`${API_BASE_URL}/automoviles/${automovilId}/estado`, {
      method: 'PATCH',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ estado, observaciones })
    });
    return this.handleResponse<Automovil>(response);
  }

  async updateKilometraje(
    automovilId: number, 
    kilometraje_actual: number,
    observaciones?: string
  ): Promise<Automovil> {
    const response = await fetch(`${API_BASE_URL}/automoviles/${automovilId}/kilometraje`, {
      method: 'PATCH',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ kilometraje_actual, observaciones })
    });
    return this.handleResponse<Automovil>(response);
  }

  async getAutomovilHistorial(automovilId: number, skip = 0, limit = 50): Promise<any> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString()
    });
    
    const response = await fetch(`${API_BASE_URL}/automoviles/${automovilId}/historial?${params}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<any>(response);
  }

  async getAutomovilEstadisticas(): Promise<AutomovilEstadisticas> {
    const response = await fetch(`${API_BASE_URL}/automoviles/estadisticas/general`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<AutomovilEstadisticas>(response);
  }

  async buscarAutomoviles(termino: string): Promise<Automovil[]> {
    const response = await fetch(`${API_BASE_URL}/automoviles/buscar/${encodeURIComponent(termino)}`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse<Automovil[]>(response);
  }

  // UTILITY METHODS
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  getCurrentUserInfo(): LoginResponse['user_info'] | null {
    const userInfo = localStorage.getItem('user_info');
    return userInfo ? JSON.parse(userInfo) : null;
  }

  getUserRole(): string | null {
    const userInfo = this.getCurrentUserInfo();
    return userInfo?.role?.nombre || null;
  }

  isAdmin(): boolean {
    return this.getUserRole() === 'admin';
  }

  isEmployee(): boolean {
    return this.getUserRole() === 'empleado';
  }

  isClient(): boolean {
    return this.getUserRole() === 'cliente';
  }
}

export const apiService = new ApiService();