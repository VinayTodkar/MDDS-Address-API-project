require('dotenv').config();

const app = require('./app');
const prisma = require('./config/prisma');

const PORT = process.env.PORT || 5000;

const server = app.listen(PORT, () => {
  console.log(`MDDS Address API running on http://localhost:${PORT}`);
});

process.on('SIGINT', async () => {
  await prisma.$disconnect();
  server.close(() => {
    console.log('Server stopped');
    process.exit(0);
  });
});

process.on('SIGTERM', async () => {
  await prisma.$disconnect();
  server.close(() => {
    console.log('Server stopped');
    process.exit(0);
  });
});
