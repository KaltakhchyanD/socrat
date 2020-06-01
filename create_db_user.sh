psql -U postgres -c "create user test_user with password 'test_password'"
psql -U postgres -c "ALTER USER test_user CREATEDB"