import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Kanban from './pages/Kanban';
import FlowEditor from './pages/FlowEditor';
import AIAssistant from './pages/AIAssistant';
import WhatsApp from './pages/WhatsApp';
import './App.css';
import './styles/theme.css';

// Componente de rota protegida
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div className="leopard-loading">Carregando...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/chat" 
            element={
              <ProtectedRoute>
                <Chat />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/kanban" 
            element={
              <ProtectedRoute>
                <Kanban />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/flow-editor" 
            element={
              <ProtectedRoute>
                <FlowEditor />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/ai-assistant" 
            element={
              <ProtectedRoute>
                <AIAssistant />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/whatsapp" 
            element={
              <ProtectedRoute>
                <WhatsApp />
              </ProtectedRoute>
            } 
          />
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
