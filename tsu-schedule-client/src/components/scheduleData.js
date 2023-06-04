const scheduleData = [
    {
      day: 'Monday',
      lessons: [
        { startTime: '8:45', endTime: '10:20', type: 'lecture', title: 'Introduction to React' },
        { startTime: '10:35', endTime: '12:10', type: 'practice', title: 'Building a Todo App' },
      ],
    },
    {
      day: 'Tuesday',
      lessons: [
        { startTime: '8:45', endTime: '10:20', type: 'lecture', title: 'React Hooks' },
        { startTime: '10:35', endTime: '12:10', type: 'meeting', title: 'Team Meeting' },
      ],
    },
    // ...and so on for the rest of the week
  ];
  
  export default scheduleData;
  