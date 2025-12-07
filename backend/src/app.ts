import express from 'express';
import cors from 'cors'; // Import cors
import authRoutes from './routes/auth.routes';

const app = express();

app.use(cors()); // Use cors middleware
app.use(express.json()); // Enable JSON body parsing

// Basic route for health check or root
app.get('/', (req, res) => {
  res.send('Auth Service is running!');
});

// Auth routes
app.use('/api/auth', authRoutes);

// Basic error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

export default app;
