// ScheduleTable.jsx
import React, { useState } from 'react';
import { Container, Row, Col, Table, Button, Modal } from 'react-bootstrap';
import scheduleData from './scheduleData';
import { useNavigate } from 'react-router';

const ScheduleTable = () => {
  const navigate = useNavigate();
  // Хук для отоборажения окошка с дополнительной информацией о паре
  const [show, setShow] = useState(false);
  const [lesson, setLesson] = useState(null);

  const handleClose = () => setShow(false);

  const handleShow = (lesson) => {
    setLesson(lesson);
    setShow(true);
  };
  
  const navigateToProfile = () => {
    navigate('/profile');
  };

  // Время начала и конца пар
  const timeMarks = [
    { startTime: '9:00 AM', endTime: '11:00 AM' },
    { startTime: '11:00 AM', endTime: '12:00 PM' }
  ];

  // Цвет пары в таблице
  const typeColors = {
    lecture: 'danger',
    practice: 'primary',
    meeting: 'warning'
  };

  return (
    <Container>
	  <Row>
        <Col>
          <Button onClick={() => navigateToProfile()}></Button>
        </Col>
      </Row>
      <Row>
        <Col>
          <h1>Weekly Schedule</h1>
        </Col>
      </Row>
      <Row>
        <Col>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Time</th>
                <th>Monday</th>
                <th>Tuesday</th>
                <th>Wednesday</th>
                <th>Thursday</th>
                <th>Friday</th>
                <th>Saturday</th>
                <th>Sunday</th>
              </tr>
            </thead>
            <tbody>
              {timeMarks.map((timeMark) => (
                <tr key={timeMark.startTime}>
                  <td>{`${timeMark.startTime} - ${timeMark.endTime}`}</td>
                  {scheduleData.map((day) => {
                    const lesson = day.lessons.find((l) => l.startTime === timeMark.startTime);
                    return (
                      <td key={day.day + timeMark.startTime}>
                        {lesson && (
                          <Button variant={typeColors[lesson.type]} onClick={() => handleShow(lesson)}>
                            {lesson.title}
                          </Button>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>
      {/* Modal for displaying lesson info */}
      {lesson && (
        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>{lesson.title}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <p>Type: {lesson.type}</p>
            <p>Time: {lesson.startTime} - {lesson.endTime}</p>
            <p>Additional info: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed hendrerit purus eget urna eleifend tristique. In ac sapien a mi hendrerit tincidunt at ut dolor. Donec eu ultrices metus. Nulla sed turpis ut ipsum euismod egestas vel vel elit.</p>
          </Modal.Body>
        </Modal>
      )}
    </Container>
  );
};

export default ScheduleTable;