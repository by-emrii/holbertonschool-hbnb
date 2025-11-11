-- ==========================
-- HBnB: Schema Creation
-- ==========================
DROP DATABASE IF EXISTS task10_sql;
CREATE DATABASE IF NOT EXISTS task10_sql;
USE task10_sql;

-- ==========================
-- User Table:
-- ==========================
CREATE TABLE IF NOT EXISTS users (
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
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY, -- uuid
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    address VARCHAR(200) NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT  NOT NULL,
    owner_id CHAR(36) NOT NULL,
    -- if user is deleted, all places referecing the user will be deleted
    CONSTRAINT places_fk FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ==========================
-- Review Table:
-- ==========================
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY, -- uuid
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    -- if author is deleted, their comments will also be deleted? 
    CONSTRAINT reviews_user_fk FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- if place is deleted, all reviews of the place will be deleted
    CONSTRAINT reviews_place_fk FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    -- user can only leave one review per place
    CONSTRAINT one_review_per_user_placefk UNIQUE (user_id, place_id) 
);

-- ==========================
-- Amenity Table:
-- ==========================
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY, -- uuid
    name VARCHAR(255) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- ==========================
-- Place_Amenity Table:
-- ==========================      
-- Link table to connect place to amenity. Place_Amenity Table (Many-to-Many relationship):
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    -- if place is deleted, all data belonging to the place will be deleted
    CONSTRAINT place_fk FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    -- if amenity is deleted, all data belonging to the amenity will be deleted
    CONSTRAINT amenity_fk FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);


-- ==========================
-- Administrator User: 
-- ==========================
INSERT users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- hashed password
    TRUE
);

-- ==========================
-- Amenity: 
-- ==========================
INSERT INTO amenities (id, name) VALUES
('54f0f63a-8c08-45e0-88c5-1824760af8a1', 'WiFi'),
('54f0f63a-8c08-45e0-88c6-1824760af8a1', 'Swimming Pool'),
('54f0f63a-8c08-45e0-88c7-1824760af8a1', 'Air Conditioning');