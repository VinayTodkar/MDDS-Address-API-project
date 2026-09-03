require('dotenv').config();

const { PrismaClient } = require('@prisma/client');
const { PrismaPg } = require('@prisma/adapter-pg');

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL
});

const prisma = new PrismaClient({
  adapter
});

async function main() {
  console.log('Connecting to Neon PostgreSQL...');

  const countries = await prisma.countries.findMany({
    take: 5
  });

  console.log('Connection successful!');
  console.log('Countries found:', countries.length);

  for (const country of countries) {
    console.log(country);
  }
}

main()
  .catch((error) => {
    console.error('Database test failed:');
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
