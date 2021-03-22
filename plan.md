# Chat bot plan

- The user has a conversation with it as opposed to just asking questions.
- The chat bot has a specific background and might be a character. This ensures that it's easier to anticipate the conversation.
- Persona:
  - A wise and old human (male) wizard by the name of Ogekron.
  - Has slain a dragon before.
  - He comes from the city of Clistead, but now lives in a wizard tower.
  - His alignment is NG and he likes to tell stories about courage and bravery.
  - Wizard's name: NULL

## Architecture
- Start by printing out a background about the wizard.
- Takes a question to begin the conversation.
- Checks for keywords against a database, to launch into a pre-planned answer.
- Perhaps some answers have questions on the end about the user (this would mean it has to detect if a response is a question or an answer to one of the bot's questions).
- Tokens get weights so that if multiple mappings occur it can pick the higher weighted one.

### Database

- The database (which includes responses as well as mappings) is found in a file called `responses.json`.
- Keywords, responses to questions, comments vs questions are mapped to responses.

The database schema for V1 is the following:

```json
{
  "version": 1,
  // Here are the responses
  "data": [
    // Each response is an object
    {
      // The list of tokens that trigger the response
      "tokens": {
        // A sample token. 0.5 is the weight
        "token_value": {"weight": 0.5}
        // You can also specify certain conditions.
        // This means that this token must be after
        // the token 'token_value'
        "another_token": {"after": "token_value"}
      }
    }
  ],
  // Generic responses
  "generics": ["Oh no!"]
}
```