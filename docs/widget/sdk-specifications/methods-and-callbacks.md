Recommended use
```javascript
// open the widget
document.getElementById('heidi-button').addEventListener('click', () => {
  Heidi.open({
    patient: {
      id: '123',
      name: 'John Doe',
      gender: 'Male',
      dob: '1990-01-01',
    },
  });
});
 
// open the widget with a custom template
document.getElementById('heidi-button').addEventListener('click', () => {
  Heidi.open({
    template: templateData, //templateData is your custom template object
    patient: {
      id: '123',
      name: 'John Doe',
      gender: 'Male',
      dob: '1990-01-01',
    },
  });
});
```

## All methods and callbacks

### Heidi.open(params?)
Opens Heidi and starts a new session.

If a sessionId is specified, the widget will open that session.
If startNewSession is set to true, the widget will create a new session, regardless of whether a sessionId is provided.
The Heidi.open() method accepts an optional params object with the following properties:

| Attribute | Type | Description |
|-----------|------|-------------|
| patient | PatientInfo | Patient information as defined in Patient Information |
| sessionId | string | A valid Heidi Session ID, obtained from Heidi.onSessionStarted |
| template | Template | Custom template to use for the session. See Custom Templates for more info on the data structure. |
| startNewSession | boolean | Whether to start a new session, regardless of whether a sessionId is provided. |
| context | string | Set context information for the session, if no context was set before. This can be used to set Medications, Allergies and any other patient info to enrich Heidi's notes. |

#### Using a custom template
If you specify a custom template, then after transcription, Heidi will generate answers to all the questions in this template.

When Heidi.onPushData(callback) is triggered, Heidi will send back a JSON template with all the answers included. These answers can then be placed back into the relevant fields in your EHR.

Note that these templates are passed when widget is launched. It is a dynamic process that will require you to take the active EHR template and transform it into a JSON format that widget can accept.

### Heidi.close(params?)
Close Heidi.

```javascript
params?: {
  keepSession? : boolean,
  force? : boolean
}
```

Set force to true to close Heidi skipping the confirmation step.
If keepSession is true and force is true, then Heidi will store the current session ID and re-open it when triggered next.

### Heidi.onPushData(callback)
Triggered when a user clicks Push Note in the widget.

callback(data): a function called when the user chooses to push notes from the Heidi library to your EHR:

```javascript
data: {
  notesData: string | Template,
  transcript: string, // only included if `result.includeTrascript` is `true` in the initialisation options
  sessionId: string, // the Heidi session this note is from
  patientInfo: PatientInfo // the patient information provided in Heidi.open()
}
```

notesData contains the note data as a string, if a template was not provided, or following the Template interface.

Note: If this callback is not set, the Push Note button will not be available on the UI.

### Heidi.onPushDocument(callback)
Triggered when a user clicks Push Document in the widget.

callback(data): a function called when the user chooses to push notes from the Heidi library to your EHR:

```javascript
data: {
  title: string, // the document's title
  content: string, // the document's content
  sessionId: string, // the Heidi session this note is from
  patientInfo: PatientInfo // the patient information provided in Heidi.open()
}
```

Note: If this callback is not set, the Push Document button will not be available on the UI.

### Heidi.onSessionStarted(callback)
Called with a new Heidi session is started.

callback(sessionId): a function called when a new Heidi Session is created. sessionId is a string containing the current Heidi session ID.

### Heidi.onTokenExpired(callback)
When called, use this callback to generate a new token and provide it to the widget via Heidi.setToken.

### Heidi.setToken(token)
Update the current token used by Heidi.

### Heidi.onOpen(callback)
Called when the widget is opened.

### Heidi.onClose(callback)
Called when the widget is closed.

### Heidi.setPatient(patientInfo)
Update the patient information for the current session.

Update patient information for the current session.

### Heidi.setContext({ context: string })
Set context information for the session, if no context was set before. This can be used to set:

- Medications,
- Allergies and,
- any other patient info to enrich Heidi's notes.

Note: we recommend using a string and not structured data as this will be displayed to the practitioners within the widget.

### Heidi.onResize(callback)
Called when the user resizes(expands or collapses) the widget.

callback(expanded: boolean): a function called when the user resizes the widget. expanded is a boolean indicating whether the widget is expanded or not.

### Heidi.onRecordingStarted(callback)
Called when the user starts a recording.

### Heidi.onRecordingPaused(callback)
Called when the user pauses a recording.

### Heidi.onRecordingStopped(callback)
Called when the user stops a recording.

### Heidi.onRecordingStatusChange(callback)
Called when the recording status changes in the Heidi widget.

callback(status: HeidiRecordingStatus): Invoked whenever the recording status updates, receiving the new status.

```typescript
export type HeidiRecordingStatus = 'RECORDING' | 'NOT_STARTED' | 'PAUSED' | 'STOPPED';
```