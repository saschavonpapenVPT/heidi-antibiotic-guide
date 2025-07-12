# Sessions

A Heidi session is a collection of notes, documents, and other data that is created by a user.  
Sessions are the equivalent of a consultation in the clinical workflow.

---

## Create a New Session

- **Method:** `POST`  
- **Path:** `/sessions`  
- **Description:** Creates a new session.

### Request

```
POST /sessions HTTP/1.1
Authorization: Bearer <your_token>
```

### Response

```
{
  "session_id": "1234567890"
}
```

## Get Session Details
- **Method:** `GET`
- **Path:** `/sessions/{session_id}`
- **Description:** Retrieves detailed information about a specific session.

### Request

```
GET /sessions/1234567890 HTTP/1.1
Authorization: Bearer <your_token>
```

### Response

```
{
  "session": {
    "session_id": "1234567890",
    "session_name": "Session 123",
    "patient": {
      "name": "",
      "gender": null,
      "dob": null
    },
    "audio": [],
    "clinician_notes": [],
    "consult_note": {
      "status": "CREATED",
      "result": "Consult note content...",
      "heading": "Note",
      "brain": "RIGHT",
      "voice_style": null,
      "generation_method": "TEMPLATE",
      "template_id": null,
      "ai_command_id": null,
      "ai_command_text": null,
      "feedback": null,
      "dictation_cleanup_mode": null
    },
    "duration": 16,
    "created_at": "2024-12-11T03:57:57.921000",
    "updated_at": "2024-12-11T23:41:54.138000",
    "language_code": "en",
    "output_language_code": "en",
    "documents": null,
    "ehr_appt_id": null,
    "ehr_provider": "EHR Provider Name",
    "ehr_patient_id": null
  }
}
```

## Update Session Information
- **Method:** `PATCH`
- **Path:** `/sessions/{session_id}`
- **Description:** Updates the details of a session.
  Use this endpoint to update:
  - Session duration
  - Input and output language
  - Patient details
  - Clinician notes
  - Additional context information
  - Linking session to a patient in your system

### Request

```
PATCH /sessions/1234567890 HTTP/1.1
Authorization: Bearer <your_token>
Content-Type: application/json
{
  "duration": 60,
  "language_code": "en",
  "output_language_code": "en",
  "patient": {
    "name": "John Doe",
    "gender": "MALE",
    "dob": "1990-01-01"
  },
  "clinician_notes": [
    "Note 1",
    "Note 2"
  ],
  "generate_output_without_recording": false
}

```

## Response

```
{
  "session": {
    "session_id": "1234567890",
    "session_name": "Session 123",
    "patient": {
      "name": "John Doe",
      "gender": "MALE",
      "dob": "1990-01-01"
    },
    "clinician_notes": [],
    "consult_note": {
      "status": "CREATED",
      "result": "Consult note content...",
      "heading": "Note",
      "brain": "RIGHT",
      "voice_style": null,
      "generation_method": "TEMPLATE",
      "template_id": null,
      "ai_command_id": null,
      "ai_command_text": null,
      "feedback": null,
      "dictation_cleanup_mode": null
    },
    "duration": 60,
    "created_at": "2024-12-11T03:57:57.921000",
    "updated_at": "2024-12-11T23:41:54.138000",
    "language_code": "en",
    "output_language_code": "en",
    "documents": null,
    "ehr_appt_id": null,
    "ehr_provider": "EHR Provider Name",
    "ehr_patient_id": null
  }
}
```