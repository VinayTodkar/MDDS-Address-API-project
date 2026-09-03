const express = require('express');
const prisma = require('../config/prisma');

const router = express.Router();

router.get('/', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;

    res.json({
      success: true,
      message: 'MDDS Address API is healthy',
      database: 'connected'
    });
  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      message: 'Database connection failed'
    });
  }
});

module.exports = router;
