const scheduleData = [
    {
      day: 'Monday',
      lessons: [
        { startTime: '9:00 AM', endTime: '11:00 AM', type: 'lecture', title: 'Introduction to React' },
        { startTime: '11:00 AM', endTime: '12:00 PM', type: 'practice', title: 'Building a Todo App' },
      ],
    },
    {
      day: 'Tuesday',
      lessons: [
        { startTime: '9:00 AM', endTime: '11:00 PM', type: 'lecture', title: 'React Hooks' },
        { startTime: '11:00 AM', endTime: '12:00 PM', type: 'meeting', title: 'Team Meeting' },
      ],
    },
    // ...and so on for the rest of the week
  ];
  
  export default scheduleData;
  