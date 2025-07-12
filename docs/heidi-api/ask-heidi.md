# Ask Heidi

---

## Get a Response from the Heidi AI Assistant

- **Method:** `POST`
- **Path:** `/sessions/{session_id}/ask-ai`
- **Description:** Get a streamed AI response from Heidi.

### Request

```
POST /sessions/1234567890/ask-ai HTTP/1.1
Authorization: Bearer <your_token>
Content-Type: application/json
{
  "ai_command_text": "Summarise the following text",
  "content": "My long paragraph of text",
  "content_type": "MARKDOWN"
}
```

#### Parameters

- **`ai_command_text`** *(string, required)*: The instruction for the Heidi AI Assistant.
- **`content`** *(string, required)*: Context for the AI to generate a response.
- **`content_type`** *(string, required)*: Format of the content. Can be `MARKDOWN` or `HTML`.

### Response

The response is streamed as JSON objects containing data chunks:

```
{ "data": "My " }
{ "data": "summary" }
{ "data": " of the " }
{ "data": "text." }
```

---