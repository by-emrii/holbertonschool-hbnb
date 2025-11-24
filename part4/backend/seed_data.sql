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
-- Regular Users for Testing:
-- ==========================
-- User 1: Place Owner (Normal User)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc4',
    'Jane',
    'Smith',
    'jane.smith@example.com',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- password: admin1234
    FALSE
);

-- User 2: Reviewer
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc5',
    'Nana',
    'John',
    'nana.john@example.com',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- password: admin1234
    FALSE
);

-- User 3: Reviewer
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc6',
    'Robert',
    'Brown',
    'robert.brown@example.com',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- password: admin1234
    FALSE
);

-- User 4: Reviewer
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc7',
    'Sylvia',
    'Xie',
    'sylvia.xie@example.com',
    '$2a$12$moBmzGGpareXoBAzBkLj5enYx6gjUtyJnDlCIwGQBakWzA8xVgDby',  -- password: admin1234
    FALSE
);


-- ==========================
-- Dummy Place 1: cozy loft
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
-- Dummy Place 2: forest lodge
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
-- Dummy Place 3: farm hut
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


-- ==========================
-- Amenities:
-- ==========================
INSERT INTO amenities (id, name, description) VALUES 
    ('550e8400-e29b-41d4-a716-446655440001', 'WiFi', 'High-speed wireless internet'),
    ('550e8400-e29b-41d4-a716-446655440003', 'Air Conditioning', 'Climate control'),
    ('550e8400-e29b-41d4-a716-446655440004', 'Kitchen', 'Full kitchen with appliances'),
    ('550e8400-e29b-41d4-a716-446655440005', 'Parking', 'Free parking space'),
    ('550e8400-e29b-41d4-a716-446655440006', 'TV', 'Flat-screen television'),
    ('550e8400-e29b-41d4-a716-446655440007', 'Heating', 'Central heating');


-- ==========================
-- Place-Amenity Associations:
-- ==========================
-- Cozy Loft amenities (WiFi, Air Conditioning, Kitchen, TV, Parking)
INSERT INTO place_amenity (place_id, amenity_id) VALUES 
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7a', '550e8400-e29b-41d4-a716-446655440001'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7a', '550e8400-e29b-41d4-a716-446655440003'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7a', '550e8400-e29b-41d4-a716-446655440004'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7a', '550e8400-e29b-41d4-a716-446655440006'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7a', '550e8400-e29b-41d4-a716-446655440005');

-- Forest Lodge amenities (WiFi, Heating, Kitchen)
INSERT INTO place_amenity (place_id, amenity_id) VALUES 
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '550e8400-e29b-41d4-a716-446655440001'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '550e8400-e29b-41d4-a716-446655440007'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7b', '550e8400-e29b-41d4-a716-446655440004');

-- Farm Hut amenities (WiFi, Parking)
INSERT INTO place_amenity (place_id, amenity_id) VALUES 
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7c', '550e8400-e29b-41d4-a716-446655440001'),
    ('a35837b8-25a2-49be-855d-84c1d0e8fe7c', '550e8400-e29b-41d4-a716-446655440005');

-- ==========================
-- Reviews:
-- ==========================
-- Reviews for Cozy Loft
INSERT INTO reviews (id, user_id, place_id, rating, text) VALUES 
    ('rev-0000-0000-0000-000000000001', 
     '36c9050e-ddd3-4c3b-9731-9f487208bbc5',  -- nana
     'a35837b8-25a2-49be-855d-84c1d0e8fe7a',  -- cozy loft
     5, 
     'Absolutely loved this place! The location is perfect and the amenities are top-notch. Would definitely stay here again!'),
    
    ('rev-0000-0000-0000-000000000002', 
     '36c9050e-ddd3-4c3b-9731-9f487208bbc6',  -- Robert
     'a35837b8-25a2-49be-855d-84c1d0e8fe7a',  -- cozy loft
     4, 
     'Great place overall. Very clean and well-maintained. Only downside was a bit of street noise at night.'),
    
    ('rev-0000-0000-0000-000000000003', 
     '36c9050e-ddd3-4c3b-9731-9f487208bbc7',  -- sylvia
     'a35837b8-25a2-49be-855d-84c1d0e8fe7a',  -- cozy loft
     5, 
     'Perfect for a weekend getaway! The host was very responsive and accommodating.');

-- Reviews for Forest Lodge
INSERT INTO reviews (id, user_id, place_id, rating, text) VALUES 
    ('rev-0000-0000-0000-000000000004', 
     '36c9050e-ddd3-4c3b-9731-9f487208bbc5',  -- nana
     'a35837b8-25a2-49be-855d-84c1d0e8fe7b', 
     5, 
     'Beautiful peaceful retreat! Surrounded by nature, exactly what I needed. Highly recommended!'),
    
    ('rev-0000-0000-0000-000000000005', 
     '36c9050e-ddd3-4c3b-9731-9f487208bbc6',  -- robert
     'a35837b8-25a2-49be-855d-84c1d0e8fe7b', 
     4, 
     'Lovely location and very relaxing. The only issue was the WiFi was a bit slow, but understandable given the remote location.');

-- Reviews for Farm Hut
INSERT INTO reviews (id, user_id, place_id, rating, text) VALUES 
    ('rev-0000-0000-0000-000000000006', 
     '36c9050e-ddd3-4c3b-9731-9f487208bbc7',  -- sylvia
     'a35837b8-25a2-49be-855d-84c1d0e8fe7c', 
     3, 
     'Decent place for the price. The animals are cute but it can get a bit noisy in the morning. Good for a budget stay.');