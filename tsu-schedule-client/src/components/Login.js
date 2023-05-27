import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button, Card, Form } from 'react-bootstrap';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'password') {
      // processing authorization
	  // processing authorization
      navigate('/schedule');
    } else {
      setError('Неверное имя пользователя или пароль');
    }
  };

  return (
    <Card className="w-50 mx-auto mt-5">
      <Card.Body>
        <h2 className="text-center mb-4">Log In</h2>
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Имя</Form.Label>
            <Form.Control type="text" placeholder="Enter username" value={username} onChange={(e) => setUsername(e.target.value)} />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Пароль</Form.Label>
            <Form.Control type="password" placeholder="Enter password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </Form.Group>

          <Button variant="primary" type="submit" className="w-100 mt-4">
            Log In
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
}

export default Login;