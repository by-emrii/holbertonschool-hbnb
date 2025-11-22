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

-- ==========================
-- Dummy Place 1: 
-- ==========================
INSERT INTO places (id, owner_id, title, address, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7a', -- id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4', -- owner_id
    'Cozy Loft',
    '14 Holberton St, Melbourne',
    95.0,
    -37.81,
    144.96,
    'A cozy loft near the CBD with modern amenities.'
);

-- ==========================
-- Dummy Place 2: 
-- ==========================
INSERT INTO places (id, owner_id, title, address, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b', -- id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4', -- owner_id
    'Forest Lodge',
    '16 Redwood Ave, Melbourne',
    45.0,
    -37.81,
    144.96,
    'Intimate forest lodge surrounded by nature.'
);

-- ==========================
-- Dummy Place 3: 
-- ==========================
INSERT INTO places (id, owner_id, title, address, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7c', -- id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4', -- owner_id
    'Farm Hut',
    '123 McDonald Way, Melbourne',
    5.0,
    -37.81,
    144.96,
    'Remote farm with cute animals.'
);