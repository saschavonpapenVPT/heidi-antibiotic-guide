# Consult Notes

Consult notes are clinical documentation generated from session content using Heidi's AI capabilities.

---

## Get Consult Note Templates

- **Method:** `GET`
- **Path:** `/templates/consult-note-templates`
- **Description:** Return a list of Consult Note templates.

### Request

```
GET /templates/consult-note-templates HTTP/1.1
Authorization: Bearer <your_token>
```

### Response

```json
{
  "templates": [
    {
      "id": "659b8042fe093d6592b41ef7",
      "name": "H & P",
      "structure_template": "Template content...",
      "template_category": "CONSULT_NOTE_TEMPLATE",
      "template_html": "Template HTML content, if available...",
      "author_name": "Heidi"
    }
  ]
}
```

---

## Generate Consult Note

- **Method:** `POST`
- **Path:** `/sessions/{session_id}/consult-note`
- **Description:** Generates a consult note using a Heidi template.

### Request

```
POST /sessions/1234567890/consult-note HTTP/1.1
Authorization: Bearer <your_token>
Content-Type: application/json
{
  "generation_method": "TEMPLATE",
  "addition": "",
  "template_id": "659b8042fe093d6592b41ef7",
  "voice_style": "GOLDILOCKS",
  "brain": "LEFT"
}
```

#### Parameters

- **voice_style:** The voice style to use for the generated note. Can be one of `GOLDILOCKS`, `DETAILED`, `BRIEF`, `SUPER_DETAILED`. Refer to the Heidi documentation for more information on voice styles.
- **brain:** Can be one of `LEFT`, `RIGHT`. Refer to the Heidi documentation for more information on brain options.
- **generation_method:** Can be one of `TEMPLATE`, `THIRD_PARTY_TEMPLATE`. Choose `TEMPLATE` in combination with a `template_id` if you're generating a note using a Heidi template, choose `THIRD_PARTY_TEMPLATE` if you're using a custom JSON template.

### Response

This endpoint will return a stream of the generated consult note, in the format:

```json
{
  "data": "Consult note text..."
}
```

---

## Generate Consult Note with Custom Template

- **Method:** `POST`
- **Path:** `/sessions/{session_id}/client-customised-template/response`
- **Description:** Generates a consult note using a custom JSON template.

### Request

```
POST /sessions/1234567890/client-customised-template/response HTTP/1.1
Authorization: Bearer <your_token>
Content-Type: application/json
{
  ...JSON template content
}
```

### Response

This endpoint will return a template JSON response.