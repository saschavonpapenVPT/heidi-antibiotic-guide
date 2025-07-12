# Authentication

## Authentication Flow

To authenticate with the Heidi API and use the widget, you will need to generate a JSON Web Token (JWT) using your API key.

The API key provided is unique to your EMR system. (This will actually be one API key per region, e.g. AU, US, EU, UK, etc)

Heidi will use this key in combination with the User's UID and the User's email address to generate a unique EHR integration account for that User.

Once the Widget has been launched, we will ask the User to then sign in to their existing Heidi account, or sign up for new Heidi account.

We then associate this Heidi account with the unique EHR integration account on our database. Any time you authenticate for this User in the future, we will automatically log them into the widget.

Heidi will handle the entire login and subscription flow, as well as all the logic required to link your User's EHR integration account with a Heidi account.

Note: users must be on a Heidi "Together" plan in order to use the integrated Heidi Widget. The above steps will still allow them to be authenticated and allow the widget to open. However we will prompt them to upgrade their account from here.

Heidi offers all integrated users a free 30 day trial of a "Together" subscription (no credit card required).

## Endpoint

| Attribute | Value |
|-----------|-------|
| Endpoint | https://registrar.api.heidihealth.com/api/v2/ml-scribe/open-api/jwt |
| Method | GET |

### Headers

| Parameter | Description |
|-----------|-------------|
| Heidi-Api-Key | Your Heidi API Key. |

### Params

| Parameter | Description |
|-----------|-------------|
| email | The user's email for calling this API. For testing please use test@heidihealth.com |
| third_party_internal_id | The user's internal user_id in your EMR system. For testing, any value may be used. |

## Examples

The examples below assume your user is logged in to your EMR system as test@heidihealth.com and has an internal user ID of 123.

### Request

#### Curl (Linux/MacOS)

```bash
curl -X GET 'https://registrar.api.heidihealth.com/api/v2/ml-scribe/open-api/jwt?email=test@heidihealth.com&third_party_internal_id=123' -H 'Heidi-Api-Key: YOUR_API_KEY'
```

#### Python

```python
import requests
 
url = "https://registrar.api.heidihealth.com/api/v2/ml-scribe/open-api/jwt?email=test@heidihealth.com&third_party_internal_id=123"
 
headers = {
    'Heidi-Api-Key': 'YOUR_API_KEY'
}
 
response = requests.get(url, headers=headers)
 
print(response.json())
```

#### Node.js

```javascript
const axios = require('axios');
 
const url = 'https://registrar.api.heidihealth.com/api/v2/ml-scribe/open-api/jwt?email=test@heidihealth.com&third_party_internal_id=123';
 
const headers = {
  'Heidi-Api-Key': 'YOUR_API_KEY',
};
 
const response = await fetch(url, {
  method: 'GET',
  headers: headers,
});
const data = await response.json();
 
console.log(data);
```

### Response

```json
{
  "token": "JWT_TOKEN",
  "expiration_time": "2024-08-01T00:00:00.000Z"
}
```