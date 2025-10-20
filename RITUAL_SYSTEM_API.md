# Ritual Reminder System API Documentation

## Overview
Complete API documentation for the Kul Setu Ritual Reminder System that manages all family rituals and ceremonies.

---

## 📋 Ritual Types Supported

1. **Barsi** - Death anniversary rituals
2. **Shraad** - Ancestral worship ceremonies
3. **Marriage** - Wedding ceremonies and rituals
4. **Pooja** - General worship reminders
5. **Worship** - Daily/regular worship activities
6. **Kul Devta** - Family deity worship
7. **Festival** - Festival celebrations (Diwali, Holi, etc.)
8. **Birth** - Birth-related rituals (Namkaran, etc.)
9. **Death** - Death rituals (Asthi Visarjan, etc.)

---

## 🔗 API Endpoints

### 1. Get Ritual Types
Get list of all supported ritual types and configuration options.

**Endpoint:** `GET /rituals/types`

**Response:**
```json
{
  "ritual_types": [
    {
      "value": "barsi",
      "label": "Barsi (Death Anniversary)"
    },
    ...
  ],
  "recurrence_patterns": ["yearly", "monthly", "weekly", "one_time"],
  "pandit_types": ["Purohit", "Acharya", "Pandit", "Guru", "Other"]
}
```

---

### 2. Create Ritual Reminder
Create a new ritual reminder for a family.

**Endpoint:** `POST /rituals/create`

**Request Body:**
```json
{
  "familyId": "F01",                    // Required
  "personId": "P0001",                  // Optional
  "ritualType": "barsi",                // Required
  "ritualName": "Barsi of Grandfather", // Required
  "ritualDate": "15-11-2025",           // Required (DD-MM-YYYY)
  "recurring": true,                    // Optional
  "recurrencePattern": "yearly",        // Optional
  "location": "Family Temple, Delhi",   // Optional
  "panditType": "Purohit",              // Optional
  "kulDevta": "Lord Shiva",             // Optional
  "description": "Annual ceremony...",  // Optional
  "notes": "Invite all family members", // Optional
  "reminderDaysBefore": 15              // Optional (default: 7)
}
```

**Response:**
```json
{
  "success": true,
  "message": "Ritual reminder created successfully",
  "reminderId": "REM0013"
}
```

---

### 3. Get Family Rituals
Get all rituals for a specific family with optional filters.

**Endpoint:** `GET /rituals/{family_id}`

**Query Parameters:**
- `type` - Filter by ritual type (e.g., "barsi", "pooja")
- `showCompleted` - Show completed rituals (default: true)
- `upcomingOnly` - Show only upcoming rituals (default: false)

**Examples:**
```
GET /rituals/F01
GET /rituals/F01?type=barsi
GET /rituals/F01?upcomingOnly=true&showCompleted=false
```

**Response:**
```json
[
  {
    "reminderId": "REM0001",
    "familyId": "F01",
    "personId": "P0001",
    "ritualType": "barsi",
    "ritualName": "Barsi Ceremony for P0001",
    "ritualDate": "2026-01-15",
    "recurring": true,
    "recurrencePattern": "yearly",
    "location": "Family Temple, Delhi",
    "panditType": "Purohit",
    "kulDevta": "Lord Shiva",
    "description": "Annual death anniversary ceremony...",
    "notes": "Invite all family members...",
    "reminderDaysBefore": 15,
    "isCompleted": false,
    "createdAt": "2025-10-20 10:30:00",
    "updatedAt": "2025-10-20 10:30:00"
  }
]
```

---

### 4. Update Ritual Reminder
Update an existing ritual reminder.

**Endpoint:** `PUT /rituals/update/{reminder_id}`

**Request Body:** (All fields optional)
```json
{
  "ritualName": "Updated Ritual Name",
  "ritualDate": "20-12-2025",
  "location": "New Location",
  "notes": "Updated notes",
  "reminderDaysBefore": 20,
  "isCompleted": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Ritual reminder updated successfully"
}
```

---

### 5. Delete Ritual Reminder
Delete a ritual reminder.

**Endpoint:** `DELETE /rituals/delete/{reminder_id}`

**Response:**
```json
{
  "success": true,
  "message": "Ritual reminder deleted successfully"
}
```

---

### 6. Get Upcoming Rituals
Get upcoming rituals across all families or for a specific family.

**Endpoint:** `GET /rituals/upcoming`

**Query Parameters:**
- `familyId` - Filter by family ID (optional)
- `daysAhead` - Number of days to look ahead (default: 30)

**Examples:**
```
GET /rituals/upcoming
GET /rituals/upcoming?familyId=F01
GET /rituals/upcoming?daysAhead=60
```

**Response:**
```json
[
  {
    "reminderId": "REM0006",
    "familyId": "F01",
    "personId": null,
    "personName": null,
    "ritualType": "pooja",
    "ritualName": "Satyanarayan Puja",
    "ritualDate": "2025-11-19",
    "location": "Home Temple",
    "panditType": "Purohit",
    "kulDevta": "Lord Vishnu",
    "description": "Monthly Satyanarayan Puja...",
    "reminderDaysBefore": 5
  }
]
```

---

### 7. Get Ritual Statistics
Get statistics about ritual reminders.

**Endpoint:** `GET /rituals/stats`

**Query Parameters:**
- `familyId` - Filter statistics by family (optional)

**Examples:**
```
GET /rituals/stats
GET /rituals/stats?familyId=F01
```

**Response:**
```json
{
  "total": 12,
  "byType": {
    "barsi": 3,
    "shraad": 1,
    "marriage": 1,
    "pooja": 1,
    "worship": 1,
    "kul_devta": 1,
    "festival": 2,
    "birth": 1,
    "death": 1
  },
  "upcoming": 5,
  "completed": 2,
  "pending": 10
}
```

---

### 8. Reload Sample Data
Reload sample ritual data (for testing/demo purposes).

**Endpoint:** `POST /rituals/reload-sample`

**Response:**
```json
{
  "success": true,
  "message": "Sample ritual data reloaded successfully"
}
```

---

## 📊 Sample Data Included

The system comes with 12 pre-configured sample rituals:

1. **3 Barsi Ceremonies** - For deceased family members
2. **1 Shraad Ritual** - Pitru Paksha ceremony
3. **1 Marriage Ceremony** - Wedding planning
4. **1 Pooja Reminder** - Monthly Satyanarayan Puja
5. **1 Worship Ritual** - Daily morning aarti
6. **1 Kul Devta Worship** - Annual temple visit
7. **2 Festival Rituals** - Diwali and Holi celebrations
8. **1 Birth Ritual** - Namkaran ceremony
9. **1 Death Ritual** - Asthi Visarjan

---

## 🔄 Recurrence Patterns

- **yearly** - Annual rituals (Barsi, festivals, etc.)
- **monthly** - Monthly ceremonies (Pooja, etc.)
- **weekly** - Weekly worship
- **daily** - Daily rituals
- **one_time** - One-time events (marriages, specific ceremonies)

---

## 📍 Common Use Cases

### Example 1: Track Barsi (Death Anniversary)
```json
POST /rituals/create
{
  "familyId": "F01",
  "personId": "P0001",
  "ritualType": "barsi",
  "ritualName": "Grandfather's Barsi",
  "ritualDate": "15-01-2026",
  "recurring": true,
  "recurrencePattern": "yearly",
  "location": "Haridwar Ghat",
  "panditType": "Purohit",
  "reminderDaysBefore": 30
}
```

### Example 2: Festival Reminder
```json
POST /rituals/create
{
  "familyId": "F01",
  "ritualType": "festival",
  "ritualName": "Diwali Lakshmi Puja",
  "ritualDate": "24-10-2025",
  "recurring": true,
  "recurrencePattern": "yearly",
  "kulDevta": "Goddess Lakshmi",
  "reminderDaysBefore": 10
}
```

### Example 3: Get This Week's Rituals
```
GET /rituals/upcoming?familyId=F01&daysAhead=7
```

---

## 🚀 Deployment

After pushing to Render, the ritual_reminders table will be automatically created on first initialization.

To initialize with sample data:
```
POST https://kul-setu-backend.onrender.com/init-db
```

---

## 📝 Notes

- All dates should be in **DD-MM-YYYY** format for input
- Dates are returned in **YYYY-MM-DD** format in responses
- The `person_id` field is optional and typically used for person-specific rituals like Barsi
- Reminder notifications can be calculated based on `ritual_date` and `reminder_days_before`
- Foreign key constraints ensure data integrity with family_members table

---

## 🔒 Database Schema

```sql
CREATE TABLE ritual_reminders (
    reminder_id VARCHAR(50) PRIMARY KEY,
    family_id VARCHAR(50) NOT NULL,
    person_id VARCHAR(50),
    ritual_type VARCHAR(50) NOT NULL,
    ritual_name VARCHAR(200) NOT NULL,
    ritual_date DATE NOT NULL,
    recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    location VARCHAR(200),
    pandit_type VARCHAR(100),
    kul_devta VARCHAR(100),
    description TEXT,
    notes TEXT,
    reminder_days_before INTEGER DEFAULT 7,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (family_id) REFERENCES family_members(family_line_id),
    FOREIGN KEY (person_id) REFERENCES family_members(person_id)
);
```

---

**Last Updated:** October 20, 2025  
**Version:** 1.0  
**Backend URL:** https://kul-setu-backend.onrender.com
