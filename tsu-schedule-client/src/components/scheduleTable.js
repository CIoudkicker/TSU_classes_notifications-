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
    { startTime: '8:45', endTime: '10:20' },
    { startTime: '10:35', endTime: '12:10' },
	{ startTime: '12:25', endTime: '14:00' },
	{ startTime: '14:45', endTime: '16:20' },
	{ startTime: '16:35', endTime: '18:10' },
	{ startTime: '18:25', endTime: '20:00' },
	{ startTime: '20:15', endTime: '21:50' }
  ];

  // Цвет пары в таблице
  const typeColors = {
    lecture: 'danger',
    practice: 'primary',
    meeting: 'warning',
	laboratory: 'info'
  };
  
  return (
    <Container>
	  <Row>
        <Col>
          <Button onClick={() => navigateToProfile()}> Профиль </Button>
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
            <p>Link: </p><a href={lesson.lessonLink}>{lesson.lessonLink}</a>
          </Modal.Body>
        </Modal>
      )}
    </Container>
  );
};

async function fillScedule (){
	
}

export default ScheduleTable;