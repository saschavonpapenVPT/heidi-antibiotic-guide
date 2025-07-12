# Transcription

---

## Initialise Audio Transcription

- **Method:** `POST`
- **Path:** `/sessions/{session_id}/restful-segment-transcription`
- **Description:** Initialise an audio transcription

### Request

```
POST /sessions/1234567890/restful-segment-transcription HTTP/1.1
Authorization: Bearer <your_token>
```

### Response

```
{
  "recording_id": "123"
}
```

---

## Upload Audio to Transcribe

- **Method:** `POST`
- **Path:** `/sessions/{session_id}/restful-segment-transcription/{recording_id}:transcribe`
- **Description:** Upload an audio chunk to transcribe

**Preferred file types:** `.mp3`, `.ogg`

### Request

```
POST /sessions/1234567890/restful-segment-transcription/123:transcribe HTTP/1.1
Authorization: Bearer <your_token>
Content-Type: multipart/form-data
{
  "file": "audio.mp3",
  "index": "0"
}
```

### Response

```
{
  "is_success": true
}
```

---

## End Audio Transcription

- **Method:** `POST`
- **Path:** `/sessions/{session_id}/restful-segment-transcription/{recording_id}:finish`
- **Description:** Complete an audio transcription

### Request

```
POST /sessions/1234567890/restful-segment-transcription/123:finish HTTP/1.1
Authorization: Bearer <your_token>
```

### Response

```
{
  "is_success": true
}
```

---

## Retrieve Transcript

- **Method:** `GET`
- **Path:** `/sessions/{session_id}/transcript`
- **Description:** Retrieve the transcript for a session.

### Request

```
GET /sessions/1234567890/transcript HTTP/1.1
Authorization: Bearer <your_token>
```

### Response

```
{
  "transcript": "Transcript text..."
}
```
