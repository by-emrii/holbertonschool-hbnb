-- ==========================
-- HBnB: Schema Creation
-- ==========================

-- ==========================
-- User Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "users" (
    id CHAR(36) PRIMARY KEY, -- uuid
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

-- ==========================
-- Place Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "places" (
    id CHAR(36) PRIMARY KEY, -- uuid
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
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
    name VARCHAR(255) NOT NULL UNIQUE
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
INSERT INTO "admin" (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    'admin1234',  -- hashed password
    TRUE
);

-- Verify admin
SELECT * FROM users WHERE is_admin = TRUE;

--View all users
SELECT * FROM users;

-- Admin updates user's (jane Doe) details
UPDATE users SET first_name = 'Lily', last_name = 'Grey' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc2'

-- Admin deletes user
DELETE FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc2';


-- ==========================
-- Place: create a place
-- ==========================
INSERT INTO "places" (id, owner_id, title, price, latitude, longitude, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b', --id
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', --owner_id
    'Cozy Loft',
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
INSERT INTO "amenities" (id, name) VALUES
('54f0f63a-8c08-45e0-88c8-1824760af8a1', 'WiFi'),
('54f0f63a-8c08-45e0-88c8-1824760af8a2', 'Swimming Pool'),
('54f0f63a-8c08-45e0-88c8-1824760af8a3', 'Air Conditioning');

-- Read 
select * FROM amenities;

-- Update: 
UPDATE amenities Set name = 'Great Wifi' WHERE name = 'WiFi';

-- Delete 
DELETE FROM amenities WHERE id = '54f0f63a-8c08-45e0-88c8-1824760af8a2';

-- ==========================
-- Review: create a review
-- ==========================
INSERT INTO "reviews" (id, text, rating, user_id, place_id) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', -- id
    'Amazing Stay!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', -- user_id
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b' -- place_id
);

-- Read:
SELECT * FROM reviews;

-- Update: 
UPDATE reviews Set text = 'Wonderful!' WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Delete: 
DELETE FROM reviews WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1',

-- ==========================
--Link amenity to a place
-- ==========================
INSERT INTO "place_amenity" (place_id, amenity_id) VALUES
('54f0f63a-8c08-45e0-88c8-1824760af8a1', '54f0f63a-8c08-45e0-88c8-1824760af8a1'), --WiFi
('54f0f63a-8c08-45e0-88c8-1824760af8a2', '54f0f63a-8c08-45e0-88c8-1824760af8a1'), --Swimming Pool
('54f0f63a-8c08-45e0-88c8-1824760af8a3', '54f0f63a-8c08-45e0-88c8-1824760af8a1'); --Air Conditioning

-- Get amenity for place
SELECT pa.place_id, a.name
FROM place_amenity pa
JOIN amenities a NO pa.amenity_id = a.id
WHERE pa.place_id = '54f0f63a-8c08-45e0-88c8-1824760af8a3'; 

-- Adding amenity to place
INSERT INTO "place_amenity" (place_id, amenity_id) VALUES ('54f0f63a-8c08-45e0-88c8-1824760af8a3', '54f0f63a-8c08-45e0-88c8-1824760af8a1');

-- change air conditioning to ac
UPDATE place_amenity SET amenity_id = 'acuuid' WHERE place_id '54f0f63a-8c08-45e0-88c8-1824760af8a3' AND amenity_id '54f0f63a-8c08-45e0-88c8-1824760af8a1';

-- delete AC amenity from place
DELET FROM place_amenity WHERE place_id = '54f0f63a-8c08-45e0-88c8-1824760af8a3' AND amenity_id '54f0f63a-8c08-45e0-88c8-1824760af8a1';