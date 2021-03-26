# Chat bot plan

- The user has a conversation with it as opposed to just asking questions.
- The chat bot has a specific background and might be a character. This ensures that it's easier to anticipate the conversation.
- Persona:
  - A wise and old human (male) wizard by the name of Ogekron.
  - Has slain a dragon before.
  - He comes from the city of Clistead, but now lives in a wizard tower.
  - His alignment is NG and he likes to tell stories about courage and bravery.

## Architecture

- All anticipated responses to questions are found in `responses.json`.
- In this file, there are mappings from tokens (such as `tower` and `wizard`) to responses. Each token also has a weight, which helps determine the most likely response.
- Tokens also have conditions, such as what words must come before them in order for their weights to count.
- There are a number of generic responses that are activated if no tokens match.
- When the user asks a question or makes a comment, the input is first tokenized and each word is normalized with the help of NLTK.
- The normalized values are then compared to the responses. For each response, all matching tokens (which conform to their specified conditions) are added to a total. The response with the highest total is printed.
- The system also keeps a stack with the most current tokens. A new token is added to the top of the stack. A token that already appeared is moved to the top of the stack. Once the stack reaches its alloted size, every time a token is added, the one at the end is discarded. Tokens in a response also found in the stack have a bonus added to the total. This ensures that the system understands the current context.
- When the system starts, the user is prompted with an introduction. The user inputs a response and gets a response from the wizard. This cycle continues until the system is terminated.

### Database

- The database (which includes responses as well as mappings) is found in a file called `responses.json`.
- Keywords (tokens) are mapped to responses in this file.

The database schema for V1 is the following:

```json
{
  "version": 1,
  // Here are the responses
  "data": [
    // Each response is an object
    {
      // The actual response
      "value": "This is a response",
      // The list of tokens that trigger the response
      "tokens": {
        // A sample token. 2 is the weight
        "token_value": {
            "weight": 2,
            // This token must be after another_token
            "after": ["another_token"]
        }
        // A second token
        "another_token": {"weight": 7}
      }
    }
  ],
  // Generic responses
  "generics": ["Oh no!"]
}
```