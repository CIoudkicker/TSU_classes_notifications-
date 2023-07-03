const UserController  = require('./userController.js');

const { Kafka } = require('kafkajs');
const fs = require('fs');

test('getSchedulestat method should read JSON file and send response', async () => {
  const req = {};
  const res = { json: jest.fn() };
  const next = jest.fn();

  const readFileSyncMock = jest.spyOn(fs, 'readFileSync').mockReturnValue('{"message": "Hello"}');

  await UserController.getSchedulestat(req, res, next);

  expect(readFileSyncMock).toHaveBeenCalledWith(expect.stringContaining('file.json'), 'utf-8');
  expect(res.json).toHaveBeenCalledWith({ message: 'Hello' });
  expect(next).not.toHaveBeenCalled();

  readFileSyncMock.mockRestore();
});


