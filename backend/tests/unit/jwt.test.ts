import { generateToken, verifyToken } from '../../src/utils/jwt';

describe('jwt utility', () => {
  const payload = { userId: '123' };
  let token: string;

  it('should generate a valid JWT token', () => {
    token = generateToken(payload);
    expect(token).toBeDefined();
    expect(typeof token).toBe('string');
  });

  it('should verify a valid JWT token', () => {
    const decoded = verifyToken(token);
    expect(decoded).toBeDefined();
    expect(decoded.userId).toBe(payload.userId);
    expect(decoded.iat).toBeDefined();
    expect(decoded.exp).toBeDefined();
  });

  it('should return null for an invalid JWT token', () => {
    const invalidToken = 'invalid.jwt.token';
    const decoded = verifyToken(invalidToken);
    expect(decoded).toBeNull();
  });

  it('should return null for an expired JWT token (simulated)', () => {
    // Generate a token that expires immediately
    const expiredToken = jwt.sign(payload, process.env.JWT_SECRET || 'supersecret', { expiresIn: '0s' });
    // Wait a bit to ensure it expires
    return new Promise(resolve => setTimeout(() => {
      const decoded = verifyToken(expiredToken);
      expect(decoded).toBeNull();
      resolve(null);
    }, 100));
  });
});
