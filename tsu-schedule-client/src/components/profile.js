import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button, Card, Form } from 'react-bootstrap';
import { Container, Row, Col, Table, Modal } from 'react-bootstrap';

const openCloseAlerts = () => {
    alert("Здесь меняется значение");
  };

function Login() {
  return (
    <Card className="w-50 mx-auto mt-5">
      <Card.Body>
		<h2 className="text-center mb-4">Профиль</h2>
		<Row>
			<Col>
			  <h4 className="text-right mb-4">ФИО:</h4>
			</Col>
			<Col>
			  <h4 className="text-right mb-4">значение ФИО</h4>
			</Col>
		</Row>
		<Row>
			<Col>
			  <h4 className="text-right mb-4">Направление:</h4>
			</Col>
			<Col>
			  <h4 className="text-right mb-4">значение направления</h4>
			</Col>
		</Row>
		<Row>
			<Col>
			  <h4 className="text-right mb-4">Группа:</h4>
			</Col>
			<Col>
			  <h4 className="text-right mb-4">значение группы</h4>
			</Col>
		</Row>
		<Row>
			<Col>
			  <h4 className="text-right mb-4">Уведомления:</h4>
			</Col>
			<Col>
			  <h4 className="text-right mb-4">вкл/выкл</h4>
			</Col>
			<Col>
			  <Button onClick={() => openCloseAlerts()}> выключить/включить </Button>
			</Col>
		</Row>
      </Card.Body>
    </Card>
  );
}

export default Login;