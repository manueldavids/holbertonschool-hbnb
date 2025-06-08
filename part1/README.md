# HBnB Project Technical Architecture

**Author:** Manuel D. Santana  
**Date:** June 8, 2025

## 1. Introduction

This document outlines the architecture and design of the HBnB Evolution project. It includes diagrams, core logic, and API flow explanations to support implementation and maintenance. The architecture follows a three-tier structure, emphasizing modularity and scalability.

## 2. High-Level Architecture

**Architecture Overview**  
Three-tier system using the **Facade Pattern** for separation of concerns.

### Presentation Layer

**Responsibilities:** Handles API requests and routes user input.

**Components:**
- `APIService`: Handles routing and general API functions
- `UserController`: Manages user-related endpoints
- `PlaceController`: Manages place-related endpoints

### Business Logic Layer

**Responsibilities:** Contains core application rules and validations.

**Core Classes:**
- `User`
- `Place`
- `Review`
- `Amenity`

### Persistence Layer

**Responsibilities:** Manages data access and interactions with the database.

**Components:**
- `StorageBackend`: Handles DB operations and fallback mechanisms

**Design Pattern:**  
**Facade Pattern** – Example: `UserServiceFacade.register_user()` hides validation, persistence, and notification logic behind a single interface.

## 3. Business Logic Layer

### Key Entities & Relationships

#### BaseModel
- Attributes: `id`, `created_at`, `updated_at`
- Methods: `save()`, `to_dict()`

#### User
- Attributes: `email`, `first_name`, `password`
- Relationships: Owns many Places, writes many Reviews

#### Place
- Attributes: `name`, `location`, `price`, `capacity`
- Relationships: Belongs to User, has many Reviews, linked to many Amenities

#### Review
- Attribute: `text`
- Relationships: Connected to one User and one Place

#### Amenity
- Examples: WiFi, Air Conditioning
- Relationships: Many-to-many with Place via join table

### Summary of Relationships
- `User → Place`: One-to-many  
- `User → Review`: One-to-many  
- `Place → Review`: One-to-many  
- `Place ←→ Amenity`: Many-to-many  
- `Review → User`: One-to-one  
- `Review → Place`: One-to-one  

## 4. API Interaction Flow

### 4.1 User Registration

**Endpoint:** `POST /api/v1/users`

**Flow:**
1. User submits registration data  
2. API forwards to business logic  
3. `UserModel` validates and formats  
4. Insert into DB  
5. Return `201 Created` or error

**Participants:** User → API → UserModel → DB

### 4.2 Place Creation

**Endpoint:** `POST /api/v1/places`

**Flow:**
1. Authenticated user submits place data  
2. API forwards to `PlaceModel`  
3. Validation and user association  
4. Insert into DB  
5. Return `201 Created`

**Participants:** Authenticated User → API → PlaceModel → DB

### 4.3 Retrieve Places by City

**Endpoint:** `GET /api/places?city_id=x`

**Flow:**
1. User queries by `city_id`  
2. API forwards to business logic  
3. `PlaceModel` builds SQL query  
4. DB returns results  
5. API formats and returns response

**Participants:** User → API → PlaceModel → DB → API

### 4.4 Submit a Review

**Endpoint:** `POST /api/v1/places/:id/reviews`

**Flow:**
1. User submits review  
2. API forwards to `ReviewModel`  
3. Create and persist review  
4. Return `201 Created`

**Participants:** User → API → ReviewModel → DB

## 5. Conclusion

This document defines a clean and modular architecture for the HBnB project, with a clear separation between the API layer, business logic, and persistence. It follows established patterns to ensure maintainability, scalability, and clarity across the development lifecycle.