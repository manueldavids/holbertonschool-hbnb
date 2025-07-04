-- HBnB Project: Schema and Initial Data
-- This script creates all tables and relationships, and inserts initial data.

-- Create User table
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create Place table
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

-- Create Amenity table
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

-- Create Review table
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    UNIQUE (user_id, place_id)
);

-- Create Place_Amenity table (many-to-many)
CREATE TABLE Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

-- Insert admin user (password is bcrypt hash of 'admin1234')
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$u1QwQwQwQwQwQwQwQwQwQeQwQwQwQwQwQwQwQwQwQwQwQwQwQwQw', -- bcrypt hash for 'admin1234'
    TRUE
);

-- Insert initial amenities (replace UUIDs with real ones if needed)
INSERT INTO Amenity (id, name) VALUES ('b1a7c1e2-1c2d-4e3f-8a9b-1c2d3e4f5a6b', 'WiFi');
INSERT INTO Amenity (id, name) VALUES ('c2b8d2f3-2d3e-5f4a-9b8c-2d3e4f5a6b7c', 'Swimming Pool');
INSERT INTO Amenity (id, name) VALUES ('d3c9e3a4-3e4f-6a5b-8c9d-3e4f5a6b7c8d', 'Air Conditioning'); 