--Generate SQL Scripts for Table Creation

--Define SQL scripts for each of the following tables:

--User Table

CREATE TABLE IF NOT EXISTS "users" (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

--Place Table:

CREATE TABLE IF NOT EXISTS "places" (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    --if user is deleted, owner_id will be NUU
    CONSTRAINT places_fk FOREIGN KEY (owner_id) REFERENCES users(id)
);

--Review Table:

CREATE TABLE IF NOT EXISTS "reviews" (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36),
    place_id CHAR(36),
    --if author is deleted, their comments will also be deleted? 
    CONSTRAINT reviews_user_fk FOREIGN KEY (user_id), REFERENCES users(id) ON DELETE CASCADE,
    --if place is deleted, all reviews of the place will be deleted also
    CONSTRAINT reviews_place_fk FOREIGN KEY (place_id), REFERENCES place(id) ON DELETE CASCADE,
    --user can only leave one review per place
    CONSTRAINT one_review_per_user_fk UNIQUE (user_id, place_id) 
);

-- Amenity Table:
CREATE TABLE IF NOT EXISTS "amenity" (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
      
--Place_Amenity Table (Many-to-Many relationship):
CREATE TABLE IF NOT EXISTS "place_amenity" (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    --if place is deleted, all data belonging to the place will be deleted
    CONSTRAINT place_fk FOREIGN KEY (place_id), REFERENCES place(id) ON DELETE CASCADE,
    --if amenity is deleted, all data belonging to the amenity will be deleted
    CONSTRAINT amenity_fk FOREIGN KEY (amenity_id) REFERENCES amenity(id) ON DELETE CASCADE
);



--Insert Initial Data

--Insert initial data into the database using SQL INSERT statements:

--User:
import uuid

--Generate SQL Scripts for Table Creation

--Define SQL scripts for each of the following tables:

--User Table

CREATE TABLE IF NOT EXISTS "users" (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

--Place Table:

CREATE TABLE IF NOT EXISTS "places" (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    --if user is deleted, owner_id will be NUU
    CONSTRAINT 'places_fk' FOREIGN KEY ('owner_id') REFERENCES 'users'('id')
);

--Review Table:

CREATE TABLE IF NOT EXISTS "reviews" (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36),
    place_id CHAR(36),
    --if author is deleted, their comments will also be deleted? 
    CONSTRAINT 'reviews_user_fk' FOREIGN KEY ('user_id'), REFERENCES 'users'('id') ON DELETE CASCADE,
    --if place is deleted, all reviews of the place will be deleted also
    CONSTRAINT 'reviews_place_fk' FOREIGN KEY ('place_id'), REFERENCES 'place'('id') ON DELETE CASCADE,
    --user can only leave one review per place
    CONSTRAINT 'one_review_per_user_fk' UNIQUE ('user_id', 'place_id') 
);

-- Amenity Table:
CREATE TABLE IF NOT EXISTS "amenity" (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
      
--Place_Amenity Table (Many-to-Many relationship):
CREATE TABLE IF NOT EXISTS "place_amenity" (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    --if place is deleted, all data belonging to the place will be deleted
    CONSTRAINT 'place_fk' FOREIGN KEY ('place_id'), REFERENCES 'place'('id') ON DELETE CASCADE,
    --if amenity is deleted, all data belonging to the amenity will be deleted
    CONSTRAINT 'amenity_fk' FOREIGN KEY ('amenity_id') REFERENCES 'amenity'('id') ON DELETE CASCADE
);



--Insert Initial Data

--Insert initial data into the database using SQL INSERT statements:

-- Users
INSERT INTO "users" (id, first_name, last_name, email, password, phone_number, profile_img, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$abc123hashedpassword',  -- hashed password
    NULL,
    NULL,
    TRUE
);

-- Place
INSERT INTO "places" (id, owner_id, title, price, address, latitude, longitude, image_url, amenity_ids, description) VALUES (
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b',
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Cozy Loft',
    120.0,
    'Near CBD, 123 King St, Melbourne',
    -37.81,
    144.96,
    'https://picsum.photos/id/1/800/600',
    '["1", "2", "2", "3"]',
    'A cozy loft near the CBD with modern amenities.'
);

-- Amenity
INSERT INTO "amenity" (id, name) VALUES
('54f0f63a-8c08-45e0-88c8-1824760af8a1', 'WiFi'),
('54f0f63a-8c08-45e0-88c8-1824760af8a2', 'Swimming Pool'),
('54f0f63a-8c08-45e0-88c8-1824760af8a3', 'Air Conditioning');

-- Review
INSERT INTO "reviews" (id, text, rating, user_id, place_id, upload_image) VALUES (
    'r1-uuid',
    'Amazing Stay!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', -- user_id
    'a35837b8-25a2-49be-855d-84c1d0e8fe7b', -- place_id
    '["https://picsum.photos/id/1/800/600"]'
);
