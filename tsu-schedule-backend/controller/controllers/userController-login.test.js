//const UserController = require('./userController');
//require('dotenv').config();
process.env.JWT_KEY = 'feecdaed6807663b225f40903dff804fa85433990514fded3b1f63f842936f9e';

const fs = require('fs');
const { generateJwt, consumeMessage, produceMessage } = require('./userController');
const UserController = require('./userController');

describe('UserController', () => {
  describe('login', () => {
    it('When a valid email and password are provided, a token should be returned', () => {
      // 模拟请求和响应对象
      const req = { body: { email: 'test@example.com', password: 'test123' } };
      const res = { json: jest.fn() };
      const next = jest.fn();

      // 调用 login 方法
      UserController.login(req, res, next);

      // 断言
      expect(res.json).toHaveBeenCalledTimes(1);
      expect(typeof res.json.mock.calls[0][0].token).toBe('string');
    });

  });
});

