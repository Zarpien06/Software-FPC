// src/components/PrivateRoute.tsx
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface Props {
  children: JSX.Element;
  allowedRoles: string[];
}

const PrivateRoute = ({ children, allowedRoles }: Props): JSX.Element => {
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;
  if (!allowedRoles.includes(user.role.nombre)) return <Navigate to="/" replace />;

  return children;
};

export default PrivateRoute;
