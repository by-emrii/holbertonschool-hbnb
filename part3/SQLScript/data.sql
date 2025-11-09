-- ==========================
-- HBnB: Schema Creation
-- ==========================

-- ==========================
-- User Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "users" (
    id CHAR(36) PRIMARY KEY, -- uuid
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

-- ==========================
-- Place Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "places" (
    id CHAR(36) PRIMARY KEY, -- uuid
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    address VARCHAR(200) NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT  NOT NULL,
    owner_id CHAR(36) NOT NULL,
    --if user is deleted, all places referecing the user will be deleted
    CONSTRAINT places_fk FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ==========================
-- Review Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "reviews" (
    id CHAR(36) PRIMARY KEY, -- uuid
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    --if author is deleted, their comments will also be deleted? 
    CONSTRAINT reviews_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    --if place is deleted, all reviews of the place will be deleted
    CONSTRAINT reviews_place_fk FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    --user can only leave one review per place
    CONSTRAINT one_review_per_user_placefk UNIQUE (user_id, place_id) 
);

-- ==========================
-- Amenity Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "amenities" (
    id CHAR(36) PRIMARY KEY, -- uuid
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- ==========================
-- Place_Amenity Table:
-- ==========================      
--Link table to connect place to amenity. Place_Amenity Table (Many-to-Many relationship):
CREATE TABLE IF NOT EXISTS "place_amenity" (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    --if place is deleted, all data belonging to the place will be deleted
    CONSTRAINT place_fk FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    --if amenity is deleted, all data belonging to the amenity will be deleted
    CONSTRAINT amenity_fk FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);



-- ===========================================
-- CRUD TESTS (Create, Read, Update, Delete)
-- ===========================================

-- ==========================
-- Administrator User: 
-- ==========================
INSERT OR IGNORE INTO "users" (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- hashed password
    TRUE
);

-- ==========================
-- Create a User: 
-- ==========================

INSERT INTO "users" (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2',
    'Jane',
    'Doe',
    'jane.doe@hbnb.com',
    '$2a$12$QNVEPHOCaFE.gEPmQi7GTueaSlgs8PZ.blOVyjNen7ogEh3ZatMmq',  -- hashed password
    FALSE
);

INSERT INTO "users" (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4',
    'Jack',
    'Doe',
    'jack.doe@hbnb.com',
    '$2a$12$kqGA2Gc1Dj1H.qHG7yZXR.f7yhk3tDiDkt05WuEs7LC4JSM0qAzfW',  -- hashed password
    FALSE
);

-- User to be deleted by adminn
INSERT INTO "users" (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc3',
    'John',
    'Doe',
    'john.doe@hbnb.com',
    '$2a$12$DOWRDth4snKhdEzEXXIMN..2vNVwEERZjifDk5kRTvEjUJ4VxtFfO',  -- hashed password
    FALSE
);

-- Verify admin
SELECT * FROM users WHERE is_admin = TRUE;

--View all users
SELECT * FROM users;

-- Admin updates user's (jane Doe) details
UPDATE users SET first_name = 'Lily', last_name = 'Grey' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc2';

-- Admin deletes user
DELETE FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc3';


-- ==========================
-- Place: create a place
-- ==========================
INSERT OR IGNORE INTO "places" (id, owner_id, title, address, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b', --id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', --owner_id
    'Cozy Loft',
    '14 Holberton St, Melbourne',
    120.0,
    -37.81,
    144.96,
    'A cozy loft near the CBD with modern amenities.'
);

-- Read
SELECT * FROM places;

-- Place
UPDATE places Set title = 'Man Cave' WHERE id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b';

-- ==========================
-- Amenity: 
-- ==========================
INSERT OR IGNORE INTO "amenities" (id, name) VALUES
('54f0f63a-8c08-45e0-88c5-1824760af8a1', 'WiFi'),
('54f0f63a-8c08-45e0-88c6-1824760af8a1', 'Swimming Pool'),
('54f0f63a-8c08-45e0-88c7-1824760af8a1', 'Air Conditioning');

-- Read 
SELECT * FROM amenities;

-- Update: 
UPDATE amenities Set name = 'Great Wifi' WHERE name = 'WiFi';

-- ==========================
-- Review: create a review
-- ==========================
INSERT INTO "reviews" (id, text, rating, user_id, place_id) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc9', -- id
    'Amazing Stay!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc2', -- user_id
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b' -- place_id
);

-- Review to be deleted
INSERT INTO "reviews" (id, text, rating, user_id, place_id) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc8', -- id
    'Sucks',
    1,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4', -- user_id
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b' -- place_id
);

-- Read:
SELECT * FROM reviews;

-- Update: 
UPDATE reviews Set text = 'Wonderful!' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc9';

-- Delete: 
DELETE FROM reviews WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc8';

-- ==========================
--Link amenity to a place
-- ==========================
INSERT OR IGNORE INTO "place_amenity" (place_id, amenity_id) VALUES
('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '54f0f63a-8c08-45e0-88c5-1824760af8a1'), --WiFi
('54f0f63a-8c08-45e0-88c8-1824760af8a2', '54f0f63a-8c08-45e0-88c6-1824760af8a1'), --Swimming Pool
('54f0f63a-8c08-45e0-88c8-1824760af8a3', '54f0f63a-8c08-45e0-88c7-1824760af8a1'); --Air Conditioning

-- Get amenity for place
SELECT pa.place_id, a.name
FROM place_amenity pa
JOIN amenities a ON pa.amenity_id = a.id
WHERE pa.place_id = 'a35837b8-25a2-49be-855d-84c1d0e8fe7b'; 

-- Adding amenity to place
INSERT OR IGNORE INTO "place_amenity" (place_id, amenity_id) VALUES ('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '54f0f63a-8c08-45e0-88c6-1824760af8a1');

-- delete AC amenity from place
DELETE FROM place_amenity WHERE place_id = ('54f0f63a-8c08-45e0-88c8-1824760af8a3') AND amenity_id = ('54f0f63a-8c08-45e0-88c7-1824760af8a1');