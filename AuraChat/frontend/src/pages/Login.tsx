import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import Window from '../components/layout/Window';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import '../styles/theme.css';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
      // Redirecionamento será feito pelo router após autenticação
    } catch (err) {
      setError('Credenciais inválidas. Por favor, tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="leopard-login-container">
      <div className="leopard-login-logo">
        <img src="/logo.png" alt="Aura" width="80" height="80" />
        <h1 className="leopard-login-title">Aura</h1>
      </div>

      <Window title="Login" width={400} height="auto">
        <form onSubmit={handleSubmit} className="leopard-login-form">
          {error && <div className="leopard-login-error">{error}</div>}
          
          <Input
            type="email"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Seu email"
            required
            icon={<i className="ph ph-envelope"></i>}
          />
          
          <Input
            type="password"
            label="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Sua senha"
            required
            icon={<i className="ph ph-lock"></i>}
          />
          
          <div className="leopard-login-actions">
            <Button
              type="submit"
              variant="primary"
              disabled={isLoading}
              fullWidth
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </Button>
          </div>
          
          <div className="leopard-login-footer">
            <a href="/forgot-password" className="leopard-login-link">
              Esqueceu sua senha?
            </a>
            <a href="/register" className="leopard-login-link">
              Criar uma conta
            </a>
          </div>
        </form>
      </Window>
      
      <div className="leopard-login-footer-info">
        <p>© 2025 Aura. Todos os direitos reservados.</p>
      </div>
    </div>
  );
};

export default Login;
