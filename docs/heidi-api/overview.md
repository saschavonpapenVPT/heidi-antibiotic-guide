# Heidi Open API

## Overview

The Heidi Open API allows you to transcribe encounters and generate clinical notes and documents. This guide details the API endpoints, parameters, response formats, and examples for using the API effectively.

## Base URL

```
https://registrar.api.heidihealth.com/api/v2/ml-scribe/open-api/
```

---

## API Flow

The following diagram shows the recommended flow for using the Heidi API.

This flow is broken down into several stages:
1. **Authentication**
2. **Session Creation and Management**
3. **Audio Transcription**
4. **Consult Note Generation**
5. **Transcript Retrieval**

---

### 1. Authentication

**Objective**: Secure access to the API using token-based authentication.

- **Request**:
  ```
  POST /authenticate
  ```

- **Response**:
  ```
  {
    "token": "your_authentication_token"
  }
  ```

---

### 2. Session Management

**Objective**: Create and manage the lifecycle of a clinical session.

#### Create a Session

- **Request**:
  ```
  POST /sessions
  ```

- **Response**:
  ```
  {
    "session_id": "uuid"
  }
  ```

#### Retrieve Session Details

- **Request**:
  ```
  GET /sessions/{session_id}
  ```

- **Response**:
  ```
  {
    "session_id": "...",
    "status": "...",
    ...
  }
  ```

#### Update Session

- **Request**:
  ```
  PATCH /sessions/{session_id}
  ```

- **Response**:
  ```
  {
    "session_id": "...",
    "updated": true
  }
  ```

---

### 3. Audio Transcription

**Objective**: Transcribe recorded patient encounters using a restful segment transcription workflow.

#### Initialize a Transcription Session

- **Request**:
  ```
  POST /sessions/{session_id}/restful-segment-transcription
  ```

- **Response**:
  ```
  {
    "recording_id": "uuid"
  }
  ```

#### Stream Audio Chunks (looped)

- **Request**:
  ```
  POST /sessions/{session_id}/restful-segment-transcription/{recording_id}:transcribe
  ```

- **Payload**: Audio chunks (streamed or in batches)

- **Response**:
  ```
  {
    "progress": "xx%",
    "status": "streaming"
  }
  ```

#### Finalize Transcription

- **Request**:
  ```
  POST /sessions/{session_id}/restful-segment-transcription/{recording_id}:finish
  ```

- **Response**:
  ```
  {
    "status": "complete"
  }
  ```

---

### 4. Consult Note Generation

**Objective**: Generate structured consult notes using predefined templates.

#### Retrieve Templates

- **Request**:
  ```
  GET /templates/consult-note-templates
  ```

- **Response**:
  ```
  [
    {
      "template_id": "template_1",
      "name": "General Consult Note"
    },
    ...
  ]
  ```

#### Generate Consult Note

- **Request**:
  ```
  POST /sessions/{session_id}/consult-note
  ```

- **Response**: Returns a stream of the generated consult note.

```
<streamed content>
```

---

### 5. Retrieve Transcript

**Objective**: Retrieve the full transcript of the clinical session.

- **Request**:
  ```
  GET /sessions/{session_id}/transcript
  ```

- **Response**:
  ```
  {
    "transcript": "Full transcription text of the encounter"
  }
  ```

---

## Full API Flow Summary

- Authenticate using `POST /authenticate` and store the returned token.
- Create a session using `POST /sessions`.
- Optionally update or retrieve the session using `PATCH` or `GET`.
- Initiate transcription using `POST /sessions/{session_id}/restful-segment-transcription` to get a `recording_id`.
- Stream audio chunks using `POST /...:transcribe` in a loop.
- Finalize transcription using `POST /...:finish`.
- Retrieve available consult note templates with `GET /templates/consult-note-templates`.
- Generate a consult note using `POST /.../consult-note`.
- Retrieve the full transcript using `GET /.../transcript`.

> Be sure to include the `Authorization: Bearer <token>` header in every API call after authentication.
