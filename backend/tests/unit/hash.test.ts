import { hashPassword, comparePassword } from '../../src/utils/hash';

describe('hash utility', () => {
  it('should correctly hash a password', async () => {
    const password = 'mySecurePassword';
    const hashedPassword = await hashPassword(password);
    expect(hashedPassword).toBeDefined();
    expect(hashedPassword).not.toBe(password);
    expect(hashedPassword.length).toBeGreaterThan(10); // bcrypt hashes are long
  });

  it('should correctly compare a password with its hash', async () => {
    const password = 'mySecurePassword';
    const hashedPassword = await hashPassword(password);
    const isMatch = await comparePassword(password, hashedPassword);
    expect(isMatch).toBe(true);
  });

  it('should return false for incorrect password comparison', async () => {
    const password = 'mySecurePassword';
    const wrongPassword = 'wrongPassword';
    const hashedPassword = await hashPassword(password);
    const isMatch = await comparePassword(wrongPassword, hashedPassword);
    expect(isMatch).toBe(false);
  });
});
