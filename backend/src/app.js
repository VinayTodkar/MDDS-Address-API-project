require('dotenv').config();

const express = require('express');
const cors = require('cors');

const healthRoutes = require('./routes/health.routes');
const addressRoutes = require('./routes/address.routes');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/v1/health', healthRoutes);
app.use('/api/v1/address', addressRoutes);

app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found'
  });
});

module.exports = app;
