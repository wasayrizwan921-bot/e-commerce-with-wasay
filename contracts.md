# API Contracts - E-commerce with Wasay

## Current Mock Data (mock.js)
- **services**: Array of 3 service objects (Amazon, eBay, Etsy)
- **packages**: Array of 3 package objects (Starter, Professional, Enterprise)
- **testimonials**: Array of 3 testimonial objects
- **stats**: Array of 4 stat objects

**Decision**: Keep services, packages, testimonials, and stats as static data in mock.js (no DB needed for these)

## Backend Implementation

### 1. Contact Inquiry API

**Endpoint**: `POST /api/inquiries/contact`

**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "phone": "string (optional)",
  "message": "string (required)"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Thank you! We'll contact you soon.",
  "inquiry_id": "string"
}
```

**MongoDB Collection**: `inquiries`
**Document Schema**:
```json
{
  "_id": "ObjectId",
  "type": "contact",
  "name": "string",
  "email": "string",
  "phone": "string",
  "message": "string",
  "created_at": "datetime",
  "status": "pending" // pending, contacted, resolved
}
```

---

### 2. Package Inquiry API

**Endpoint**: `POST /api/inquiries/package`

**Request Body**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "phone": "string (optional)",
  "package_name": "string (required)", // Starter, Professional, Enterprise
  "message": "string (optional)"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Thank you for your interest! We'll send you a custom quote soon.",
  "inquiry_id": "string"
}
```

**MongoDB Collection**: `inquiries`
**Document Schema**:
```json
{
  "_id": "ObjectId",
  "type": "package",
  "name": "string",
  "email": "string",
  "phone": "string",
  "package_name": "string",
  "message": "string",
  "created_at": "datetime",
  "status": "pending"
}
```

---

### 3. Get All Inquiries API (Admin)

**Endpoint**: `GET /api/inquiries`

**Query Parameters**:
- `type`: filter by type (contact | package | all) - default: all
- `status`: filter by status (pending | contacted | resolved | all) - default: all
- `limit`: number of records - default: 50

**Response**:
```json
{
  "success": true,
  "count": 10,
  "inquiries": [
    {
      "id": "string",
      "type": "string",
      "name": "string",
      "email": "string",
      "phone": "string",
      "message": "string",
      "package_name": "string", // only for package type
      "created_at": "datetime",
      "status": "string"
    }
  ]
}
```

---

## Frontend Integration Plan

### Changes Needed:

1. **Contact Section** (App.js):
   - Add contact form with fields: Name, Email, Phone, Message
   - Replace or complement existing WhatsApp/Email buttons
   - Add form validation
   - Show success toast on submission
   - Use shadcn form components

2. **Package Cards** (App.js):
   - "Get Quote" button should open modal/dialog with inquiry form
   - Pre-fill package_name in the form
   - Fields: Name, Email, Phone, Message (optional)
   - Show success toast on submission

3. **Remove mock.js dependency**:
   - Keep mock.js for services, packages, testimonials, stats (static content)
   - No changes needed for these as they don't require backend

4. **API Integration**:
   - Use axios for API calls
   - Base URL: `${REACT_APP_BACKEND_URL}/api`
   - Add loading states during form submission
   - Add error handling with user-friendly messages

---

## Implementation Steps:

### Backend:
1. Create MongoDB model for inquiries
2. Create inquiry routes: POST /api/inquiries/contact, POST /api/inquiries/package, GET /api/inquiries
3. Add validation middleware (email format, required fields)
4. Add error handling
5. Test APIs with curl

### Frontend:
1. Create ContactForm component with shadcn form components
2. Create PackageInquiryDialog component
3. Integrate forms in App.js
4. Add form validation with zod
5. Implement API calls with axios
6. Add toast notifications for success/error
7. Add loading states

---

## Error Handling:

**Backend Errors**:
- 400: Validation error (missing/invalid fields)
- 500: Server error

**Frontend Handling**:
- Show error toast with appropriate message
- Keep form data if submission fails
- Clear form on success

---

## Notes:
- No authentication needed (public inquiry forms)
- Admin endpoint (/api/inquiries) can be unprotected for MVP or add basic auth later
- Email notifications can be added later if needed
- WhatsApp and direct email buttons remain as alternative contact methods
