import { Request, Response } from 'express';
import { validationResult } from 'express-validator';
import * as authService from '../services/auth.service';

export async function signupController(req: Request, res: Response) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { name, email, password } = req.body;

  try {
    const user = await authService.signup(name, email, password);
    res.status(201).json(user);
  } catch (error: any) {
    if (error.message === 'Email already in use.') {
      return res.status(409).json({ message: error.message });
    }
    res.status(500).json({ message: 'Failed to register user.' }); // Generic error
  }
}

export async function loginController(req: Request, res: Response) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { email, password } = req.body;

  try {
    const { token } = await authService.login(email, password);
    res.status(200).json({ token });
  } catch (error: any) {
    if (error.message === 'Invalid credentials') {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
    res.status(500).json({ message: 'Failed to log in.' }); // Generic error
  }
}
