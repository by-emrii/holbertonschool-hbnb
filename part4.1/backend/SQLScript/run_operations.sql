-- ===========================================
-- CRUD TESTS (Create, Read, Update, Delete)
-- ===========================================
SELECT '* List tables in database' AS '** Task 10 Database Tests';
USE task10_sql;
SHOW TABLES;
-- ==========================
-- Create Users: 
-- ==========================
INSERT users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2',
    'Jane',
    'Doe',
    'jane.doe@hbnb.com',
    '$2a$12$QNVEPHOCaFE.gEPmQi7GTueaSlgs8PZ.blOVyjNen7ogEh3ZatMmq',  -- hashed password
    FALSE
);

INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4',
    'Jack',
    'Doe',
    'jack.doe@hbnb.com',
    '$2a$12$kqGA2Gc1Dj1H.qHG7yZXR.f7yhk3tDiDkt05WuEs7LC4JSM0qAzfW',  -- hashed password
    FALSE
);

-- User to be deleted by admin
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc3',
    'John',
    'Doe',
    'john.doe@hbnb.com',
    '$2a$12$DOWRDth4snKhdEzEXXIMN..2vNVwEERZjifDk5kRTvEjUJ4VxtFfO',  -- hashed password
    FALSE
);

-- Verify admin
SELECT '* Admin User:' AS '** User Tests';
SELECT * FROM users WHERE is_admin = TRUE;

-- Retrieve all users
SELECT '* List all users:' AS '';
SELECT * FROM users;

-- Admin updates user's (jane Doe) details
SELECT '* Admin Updates the first and last name of Jane Doe' AS '';
UPDATE users SET first_name = 'Lily', last_name = 'Grey' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc2';

-- Admin deletes user
SELECT '* Delete User John Doe' AS '';
DELETE FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc3';

-- Retrieve all users after deletion
SELECT '* List all users after UPDATE and DELETION:' AS '';
SELECT * FROM users;

-- ==========================
-- Place: create a place
-- ==========================
INSERT INTO places (id, owner_id, title, address, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b', -- id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4', -- owner_id
    'Cozy Loft',
    '14 Holberton St, Melbourne',
    120.0,
    -37.81,
    144.96,
    'A cozy loft near the CBD with modern amenities.'
);

-- Place to be deleted
INSERT INTO places (id, owner_id, title, address, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7c', -- id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2', -- owner_id
    'Haunted House',
    '15 Pennywise St, Melbourne',
    122.0,
    -33.81,
    145.96,
    'A cozy haunted house near the CBD with modern amenities.'
);

-- Retrieve all places
SELECT '* List all places:' AS '** Place Tests';
SELECT * FROM places;

-- Update a Place
UPDATE places Set title = 'Man Cave' WHERE id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b';

-- Retrieve a place by ID after update
SELECT '* Updated the title of a place:' AS '';
SELECT * from places WHERE id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b';

-- Delete a place
SELECT '* Deleted a place named Haunted House' AS '';
DELETE FROM places WHERE id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7c';

-- Retrieve all places after deleting a place
SELECT '* List all places after deletion:' AS '';
SELECT * FROM places;

-- ==========================
-- Amenity: 
-- ==========================

-- Create an amenity
INSERT INTO amenities (id, name) VALUES
('54f0f63a-8c08-45e0-88c9-1824760af8a1', 'Spa');

-- Retrieve all amenities
SELECT '* List all amenities:' AS '** Amenity Tests';
SELECT * FROM amenities;

-- Update an amenity:
SELECT '* Update amenity name of Wifi' AS '';
UPDATE amenities Set name = 'Great Wifi' WHERE name = 'WiFi';

-- Retrieve an amenity by ID
SELECT '* List an amenity by ID after update:' AS '';
SELECT * FROM amenities WHERE id = '54f0f63a-8c08-45e0-88c5-1824760af8a1';

-- Delete amenity
SELECT '* Delete amenity named spa' AS '';
DELETE FROM amenities WHERE id = '54f0f63a-8c08-45e0-88c9-1824760af8a1';

-- Retrieve all amenities
SELECT '* List all amenities after deletion:' AS '';
SELECT * FROM amenities;

-- ==========================
-- Review: create a review
-- ==========================
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc9', -- id
    'Amazing Stay!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2', -- user_id
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b' -- place_id
);

-- Review to be deleted
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc8', -- id
    'Sucks',
    1,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4', -- user_id
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b' -- place_id
);

-- Retrieve all reviews:
SELECT '* List all reviews:' AS '** Review Tests';
SELECT * FROM reviews;

-- Update: 
SELECT '* Update a review text' AS '';
UPDATE reviews Set text = 'Wonderful!' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc9';

-- Retrieve a review by ID
SELECT '* List review by ID:' AS '';
SELECT * FROM reviews WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc9';

-- Delete: 
SELECT '* Delete a review' AS '';
DELETE FROM reviews WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc8';

-- Retrieve all reviews:
SELECT '* List all reviews after deletion:' AS '';
SELECT * FROM reviews;

-- ==========================
-- Link amenity to a place
-- ==========================
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '54f0f63a-8c08-45e0-88c5-1824760af8a1'), -- WiFi
('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '54f0f63a-8c08-45e0-88c6-1824760af8a1'); -- Swimming Pool
-- ('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '54f0f63a-8c08-45e0-88c7-1824760af8a1'); -- Air Conditioning

-- Retrieve amenities for place
SELECT '* List all amenities for a place' AS '** Place Amenity Tests';
SELECT place_amenity.place_id, amenities.name
FROM place_amenity
JOIN amenities ON place_amenity.amenity_id = amenities.id
WHERE place_amenity.place_id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b'; 

-- Adding amenity to place
SELECT '* Add Air Conditioning Amenity to a place' AS '';
INSERT INTO place_amenity (place_id, amenity_id) VALUES ('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '54f0f63a-8c08-45e0-88c7-1824760af8a1');

-- Retrieve all amenities of a place
SELECT '* List all amenities for a place after adding a new amenity' AS '';
SELECT place_amenity.place_id, amenities.name
FROM place_amenity
JOIN amenities ON place_amenity.amenity_id = amenities.id
WHERE place_amenity.place_id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b'; 

-- delete AC amenity from place
SELECT '* Delete Air conditioning amenity from a place' AS '';
DELETE FROM place_amenity WHERE place_id = ('a35837b8-25a2-49be-855d-84c1d0e8fe7b') AND amenity_id = ('54f0f63a-8c08-45e0-88c7-1824760af8a1');

-- Retrieve all amenities of a place
SELECT '* List all amenities for a place after deleting an amenity' AS '';
SELECT place_amenity.place_id, amenities.name
FROM place_amenity
JOIN amenities ON place_amenity.amenity_id = amenities.id
WHERE place_amenity.place_id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b'; 