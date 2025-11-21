-- ==========================
-- Administrator User: 
-- ==========================
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- hashed password
    TRUE
);