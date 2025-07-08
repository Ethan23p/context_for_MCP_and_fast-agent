# Everything Server Summary
A comprehensive test server demonstrating all MCP features.
## Tools
- **echo(message)**: Echoes back the input.
- **add(a, b)**: Adds two numbers.
- **longRunningOperation(duration, steps)**: Simulates a long task with progress updates.
- **printEnv()**: Prints all environment variables.
- **sampleLLM(prompt, maxTokens)**: Requests a completion from the client's LLM.
- **getTinyImage()**: Returns a small test image.
- **annotatedMessage(messageType, includeImage)**: Demonstrates content annotations.
- **getResourceReference(resourceId)**: Returns an embedded resource.
- **getResourceLinks(count)**: Returns multiple resource links.
## Resources
- Provides 100 paginated test resources (even IDs are text, odd IDs are binary). URI: `test://static/resource/{id}`
## Prompts
- **simple_prompt**: A prompt with no arguments.
- **complex_prompt(temperature, [style])**: A prompt with arguments.
- **resource_prompt(resourceId)**: A prompt that embeds a resource.
