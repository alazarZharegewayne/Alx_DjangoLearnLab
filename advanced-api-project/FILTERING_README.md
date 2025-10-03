# API Filtering, Searching, and Ordering Documentation

## Overview
This API now includes advanced query capabilities for filtering, searching, and ordering book data.

## Available Features

### Filtering
Filter books using the following query parameters:

- `title`: Filter by book title (case-insensitive contains)
- `author_name`: Filter by author name (case-insensitive contains)  
- `publication_year`: Filter by exact publication year
- `publication_year_min`: Filter books published in or after this year
- `publication_year_max`: Filter books published in or before this year

**Example:**
