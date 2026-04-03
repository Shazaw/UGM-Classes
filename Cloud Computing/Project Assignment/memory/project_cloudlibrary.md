---
name: CloudLibrary project deployment
description: Full-stack cloud library website deployed to DigitalOcean droplet
type: project
---

CloudLibrary is deployed and running at http://157.230.244.123

**Server:** 157.230.244.123 (DigitalOcean, Ubuntu 24.04 LTS)
**Stack:** Node.js 20 + Express + PostgreSQL 16 + Nginx + PM2

**App location:** /var/www/cloudlibrary/
- backend/ — Express API on port 3001
- frontend/public/ — SPA served by Express (static)
- uploads/books/ — Uploaded book files

**Database:** PostgreSQL, db=cloudlibrary, user=cloudlib_user, pw=CloudLib@2024!

**Features built:**
- JWT authentication (register/login)
- 25 pre-seeded public domain books (Project Gutenberg classics)
- Book upload/download (PDF, TXT, EPUB, MOBI, DOC)
- User library, want-to-read list, contributions
- Profile editing with avatar color picker
- Star ratings and reviews
- Search, genre filter, sort, pagination
- 11 genres: Adventure, Classic, Romance, Sci-Fi, Historical Fiction, Horror, Drama, Fantasy, Mystery, Philosophy, Poetry

**Why:** UGM Semester 4 Cloud Computing project assignment.

**How to apply:** When making changes, SSH in as root, files are at /var/www/cloudlibrary. Use `pm2 restart cloudlibrary` after backend changes.
