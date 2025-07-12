# Patient Information
Heidi allows you to provide patient information for the current patient. When providing patient information as params to Heidi.open() or Heidi.setPatient(), you should use this format:

Please note, all fields are optional however providing them will add more contextual information when generating notes

## PatientInfo
| Attribute | Type   | Required |
|-----------|--------|----------|
| id        | string | Yes      |
| name      | string | Yes      |
| gender    | string | Yes      |
| dob       | string | Yes      |

## TypeScript Interface
```typescript
interface PatientInfo {
  id: string;
  name: string;
  gender: string;
  dob: string;
}
```