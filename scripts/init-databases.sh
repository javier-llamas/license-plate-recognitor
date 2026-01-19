#!/bin/bash
# Idempotent database initialization script
# Creates DBOS system database if it doesn't exist

set -e

echo "Starting database initialization..."

# Database connection parameters
DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_USER="${POSTGRES_USER:-lpr_user}"
DB_PASSWORD="${POSTGRES_PASSWORD:-lpr_password}"
DJANGO_DB="${POSTGRES_DB:-license_plate_db}"
DBOS_DB="dbos_system"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d postgres -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Function to check if database exists
database_exists() {
    local db_name=$1
    PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$db_name'" | grep -q 1
}

# Create Django database if it doesn't exist
if database_exists "$DJANGO_DB"; then
    echo "Django database '$DJANGO_DB' already exists"
else
    echo "Creating Django database '$DJANGO_DB'..."
    PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d postgres -c "CREATE DATABASE $DJANGO_DB;"
    echo "Django database '$DJANGO_DB' created successfully"
fi

# Create DBOS system database if it doesn't exist
if database_exists "$DBOS_DB"; then
    echo "DBOS system database '$DBOS_DB' already exists"
else
    echo "Creating DBOS system database '$DBOS_DB'..."
    PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d postgres -c "CREATE DATABASE $DBOS_DB;"
    echo "DBOS system database '$DBOS_DB' created successfully"
fi

echo "Database initialization complete!"
