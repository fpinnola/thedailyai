import { Navigate } from 'react-router-dom';

const RequireAuth = ({ children }: { children: any }) => {
  const accessToken = localStorage.getItem('access_token');
  return accessToken ? <Navigate to="/home" replace /> : children;
};