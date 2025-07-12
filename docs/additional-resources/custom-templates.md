Implemented custom templates with our deprecated version? See documentation.

## Custom templates

We recognise that many EHRs allow users to create custom templates that have a diverse set of fields and question types.

## JSON template schema

### `questions` (array of objects)

• Description: An array of question objects, each representing a question that the client can ask as part of their template. Each question can have nested child questions to handle more complex hierarchical questioning structures.

Each question object has the following fields:

• `questionId` (string): Unique identifier for the question.

• `question` (string): The text of the question being asked.

• `dateFormat` (string): The format of date required, only for `"DateResponse"` questions.

**View possible values**
  • `"D MMM YYYY"`
  • `"DD/MM/YYYY"`
  • `"MM/DD/YYYY"`
  • `"MMMM DD YYYY"`
  • `"MMM DD YYYY"`
  • `"YYYY/MM/DD"`

• `answerType` (string): Specifies the type of response expected.

**View possible values**
  • `"SingleResponse"` - For single-option answers
  • `"MultipleResponse"` - For questions allowing multiple selections
  • `"TextArea"` - For free-text responses
  • `"DateResponse"` - For date-based answers

• `answerOptions` (array of objects): A list of possible answers if the question is of type `"SingleResponse"` or `"MultipleResponse"`.

  • `value`: value of the answer
  • `metadata`: a json format that can provide any metadata to the answer option.

**Sample**
```json
{
  "answerOptions": [{
    "value": "mg",
    "metadata": {
      "unit": "milligrams",
      "description": "xxxx"
    }
  }]
}
```

• `description` (string): Introduction to this question. Some additional information or explanations can be provided through this field.

• `repeatable` (boolean): whether this question can be repeated.

• `childQuestions` (array of objects): Nested sub-questions that are dependent on the answer to the current question. This structure allows for deep nesting of questions to handle complex dependencies.

  • Note: The recommended maximum child question depth is `5`, as the question structure becomes more complex, it may take longer for the widget to process.

### `template` (string)

• Description: The template field allows the client to provide a pre-defined structure that will be used for generating the final note. This may include formatting, placeholders, or any text that should appear in the final output.

### `summaryRequired` (boolean)

• Description: Specifies whether the final note/answer generation requires a summary.

### `metadata` (array of string)

• Description: This field allows clients to provide additional details or context that might not be directly tied to the template or the questions but could be useful in generating the final note or answers. Each item in the array represents a separate piece of additional information.

## TypeScript Interface

```typescript
type AnswerType = 'SingleResponse' | 'MultipleResponse' | 'TextArea' | 'DateResponse';
 
interface StructuredTemplateQuestionAnswerOption {
  value: string;
  metadata?: {
    [key: string]: string;
  };
}
 
interface StructuredTemplateQuestionAnswer {
  value?: string;
  additionalDetails?: string;
}
 
interface StructuredTemplateQuestion {
  questionId: string;
  question: string;
  description: string;
  answerType: AnswerType;
  answerOptions?: StructuredTemplateQuestionAnswerOption[];
  answer?: StructuredTemplateQuestionAnswer[];
  dateFormat?: string;
  repeatable: boolean;
  childQuestions?: StructuredTemplateQuestion[];
}
 
interface StructuredTemplateRequest {
  template: string;
  questions: StructuredTemplateQuestion[];
  summaryRequired: boolean;
  metadata: string[] | null;
}
 
interface StructuredTemplateResponse {
    content?: string | null;
    questionAnswers: StructuredTemplateQuestion[];
    summary?: string | null;
}
```