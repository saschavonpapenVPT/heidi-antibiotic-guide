# Authentication

## Authentication Flow

To authenticate with the Heidi API and use the widget, you will need to generate a JSON Web Token (JWT) using your API key.

- The API key provided is unique to your EHR system.
- Heidi uses your API key in combination with your EHR User UID and email address to generate a unique account for the EHR User making the request.

---

## Authenticate with the API

- **Method:** `GET`
- **Path:** `/jwt`
- **Description:** Get a JWT token for authenticating with the API.

### Request

```
GET /jwt?email=test@heidihealth.com&third_party_internal_id=123 HTTP/1.1
Heidi-Api-Key: <heidi_api_key>
```

### Response
```
{
  "token": "JWT_TOKEN",
  "expiration_time": "2024-08-01T00:00:00.000Z"
}
```
