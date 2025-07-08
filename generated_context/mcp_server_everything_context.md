# Project: everything

## Directory Structure

```
📁 everything
├── 📄 CLAUDE.md
├── 📄 Dockerfile
├── 📄 everything.ts
├── 📄 index.ts
├── 📄 instructions.md
├── 📄 package.json
├── 📄 README.md
├── 📄 sse.ts
├── 📄 stdio.ts
├── 📄 streamableHttp.ts
└── 📄 tsconfig.json
```

------------------------------------------------------------

## File Contents

--- START OF FILE CLAUDE.md ---
# MCP "Everything" Server - Development Guidelines

## Build, Test & Run Commands
- Build: `npm run build` - Compiles TypeScript to JavaScript
- Watch mode: `npm run watch` - Watches for changes and rebuilds automatically
- Run server: `npm run start` - Starts the MCP server using stdio transport
- Run SSE server: `npm run start:sse` - Starts the MCP server with SSE transport
- Prepare release: `npm run prepare` - Builds the project for publishing

## Code Style Guidelines
- Use ES modules with `.js` extension in import paths
- Strictly type all functions and variables with TypeScript
- Follow zod schema patterns for tool input validation
- Prefer async/await over callbacks and Promise chains
- Place all imports at top of file, grouped by external then internal
- Use descriptive variable names that clearly indicate purpose
- Implement proper cleanup for timers and resources in server shutdown
- Follow camelCase for variables/functions, PascalCase for types/classes, UPPER_CASE for constants
- Handle errors with try/catch blocks and provide clear error messages
- Use consistent indentation (2 spaces) and trailing commas in multi-line objects
--- END OF FILE CLAUDE.md ---


--- START OF FILE Dockerfile ---
FROM node:22.12-alpine AS builder

COPY src/everything /app
COPY tsconfig.json /tsconfig.json

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm npm install

FROM node:22-alpine AS release

WORKDIR /app

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/package.json /app/package.json
COPY --from=builder /app/package-lock.json /app/package-lock.json

ENV NODE_ENV=production

RUN npm ci --ignore-scripts --omit-dev

CMD ["node", "dist/index.js"]
--- END OF FILE Dockerfile ---


--- START OF FILE everything.ts ---
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  CallToolRequestSchema,
  CompleteRequestSchema,
  CreateMessageRequest,
  CreateMessageResultSchema,
  GetPromptRequestSchema,
  ListPromptsRequestSchema,
  ListResourcesRequestSchema,
  ListResourceTemplatesRequestSchema,
  ListToolsRequestSchema,
  LoggingLevel,
  ReadResourceRequestSchema,
  Resource,
  SetLevelRequestSchema,
  SubscribeRequestSchema,
  Tool,
  ToolSchema,
  UnsubscribeRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const instructions = readFileSync(join(__dirname, "instructions.md"), "utf-8");

const ToolInputSchema = ToolSchema.shape.inputSchema;
type ToolInput = z.infer<typeof ToolInputSchema>;

/* Input schemas for tools implemented in this server */
const EchoSchema = z.object({
  message: z.string().describe("Message to echo"),
});

const AddSchema = z.object({
  a: z.number().describe("First number"),
  b: z.number().describe("Second number"),
});

const LongRunningOperationSchema = z.object({
  duration: z
    .number()
    .default(10)
    .describe("Duration of the operation in seconds"),
  steps: z.number().default(5).describe("Number of steps in the operation"),
});

const PrintEnvSchema = z.object({});

const SampleLLMSchema = z.object({
  prompt: z.string().describe("The prompt to send to the LLM"),
  maxTokens: z
    .number()
    .default(100)
    .describe("Maximum number of tokens to generate"),
});

// Example completion values
const EXAMPLE_COMPLETIONS = {
  style: ["casual", "formal", "technical", "friendly"],
  temperature: ["0", "0.5", "0.7", "1.0"],
  resourceId: ["1", "2", "3", "4", "5"],
};

const GetTinyImageSchema = z.object({});

const AnnotatedMessageSchema = z.object({
  messageType: z
    .enum(["error", "success", "debug"])
    .describe("Type of message to demonstrate different annotation patterns"),
  includeImage: z
    .boolean()
    .default(false)
    .describe("Whether to include an example image"),
});

const GetResourceReferenceSchema = z.object({
  resourceId: z
    .number()
    .min(1)
    .max(100)
    .describe("ID of the resource to reference (1-100)"),
});

const ElicitationSchema = z.object({});

const GetResourceLinksSchema = z.object({
  count: z
    .number()
    .min(1)
    .max(10)
    .default(3)
    .describe("Number of resource links to return (1-10)"),
});

enum ToolName {
  ECHO = "echo",
  ADD = "add",
  LONG_RUNNING_OPERATION = "longRunningOperation",
  PRINT_ENV = "printEnv",
  SAMPLE_LLM = "sampleLLM",
  GET_TINY_IMAGE = "getTinyImage",
  ANNOTATED_MESSAGE = "annotatedMessage",
  GET_RESOURCE_REFERENCE = "getResourceReference",
  ELICITATION = "startElicitation",
  GET_RESOURCE_LINKS = "getResourceLinks",
}

enum PromptName {
  SIMPLE = "simple_prompt",
  COMPLEX = "complex_prompt",
  RESOURCE = "resource_prompt",
}

export const createServer = () => {
  const server = new Server(
    {
      name: "example-servers/everything",
      version: "1.0.0",
    },
    {
      capabilities: {
        prompts: {},
        resources: { subscribe: true },
        tools: {},
        logging: {},
        completions: {},
        elicitation: {},
      },
      instructions
    }
  );

  let subscriptions: Set<string> = new Set();
  let subsUpdateInterval: NodeJS.Timeout | undefined;
  let stdErrUpdateInterval: NodeJS.Timeout | undefined;

  // Set up update interval for subscribed resources
  subsUpdateInterval = setInterval(() => {
    for (const uri of subscriptions) {
      server.notification({
        method: "notifications/resources/updated",
        params: { uri },
      });
    }
  }, 10000);

  let logLevel: LoggingLevel = "debug";
  let logsUpdateInterval: NodeJS.Timeout | undefined;
  const messages = [
    { level: "debug", data: "Debug-level message" },
    { level: "info", data: "Info-level message" },
    { level: "notice", data: "Notice-level message" },
    { level: "warning", data: "Warning-level message" },
    { level: "error", data: "Error-level message" },
    { level: "critical", data: "Critical-level message" },
    { level: "alert", data: "Alert level-message" },
    { level: "emergency", data: "Emergency-level message" },
  ];

  const isMessageIgnored = (level: LoggingLevel): boolean => {
    const currentLevel = messages.findIndex((msg) => logLevel === msg.level);
    const messageLevel = messages.findIndex((msg) => level === msg.level);
    return messageLevel < currentLevel;
  };

  // Set up update interval for random log messages
  logsUpdateInterval = setInterval(() => {
    let message = {
      method: "notifications/message",
      params: messages[Math.floor(Math.random() * messages.length)],
    };
    if (!isMessageIgnored(message.params.level as LoggingLevel))
      server.notification(message);
  }, 20000);


  // Set up update interval for stderr messages
  stdErrUpdateInterval = setInterval(() => {
    const shortTimestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    });
    server.notification({
      method: "notifications/stderr",
      params: { content: `${shortTimestamp}: A stderr message` },
    });
  }, 30000);

  // Helper method to request sampling from client
  const requestSampling = async (
    context: string,
    uri: string,
    maxTokens: number = 100
  ) => {
    const request: CreateMessageRequest = {
      method: "sampling/createMessage",
      params: {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Resource ${uri} context: ${context}`,
            },
          },
        ],
        systemPrompt: "You are a helpful test server.",
        maxTokens,
        temperature: 0.7,
        includeContext: "thisServer",
      },
    };

    return await server.request(request, CreateMessageResultSchema);
  };

  const requestElicitation = async (
    message: string,
    requestedSchema: any
  ) => {
    const request = {
      method: 'elicitation/create',
      params: {
        message,
        requestedSchema
      }
    };

    return await server.request(request, z.any());
  };

  const ALL_RESOURCES: Resource[] = Array.from({ length: 100 }, (_, i) => {
    const uri = `test://static/resource/${i + 1}`;
    if (i % 2 === 0) {
      return {
        uri,
        name: `Resource ${i + 1}`,
        mimeType: "text/plain",
        text: `Resource ${i + 1}: This is a plaintext resource`,
      };
    } else {
      const buffer = Buffer.from(`Resource ${i + 1}: This is a base64 blob`);
      return {
        uri,
        name: `Resource ${i + 1}`,
        mimeType: "application/octet-stream",
        blob: buffer.toString("base64"),
      };
    }
  });

  const PAGE_SIZE = 10;

  server.setRequestHandler(ListResourcesRequestSchema, async (request) => {
    const cursor = request.params?.cursor;
    let startIndex = 0;

    if (cursor) {
      const decodedCursor = parseInt(atob(cursor), 10);
      if (!isNaN(decodedCursor)) {
        startIndex = decodedCursor;
      }
    }

    const endIndex = Math.min(startIndex + PAGE_SIZE, ALL_RESOURCES.length);
    const resources = ALL_RESOURCES.slice(startIndex, endIndex);

    let nextCursor: string | undefined;
    if (endIndex < ALL_RESOURCES.length) {
      nextCursor = btoa(endIndex.toString());
    }

    return {
      resources,
      nextCursor,
    };
  });

  server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => {
    return {
      resourceTemplates: [
        {
          uriTemplate: "test://static/resource/{id}",
          name: "Static Resource",
          description: "A static resource with a numeric ID",
        },
      ],
    };
  });

  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const uri = request.params.uri;

    if (uri.startsWith("test://static/resource/")) {
      const index = parseInt(uri.split("/").pop() ?? "", 10) - 1;
      if (index >= 0 && index < ALL_RESOURCES.length) {
        const resource = ALL_RESOURCES[index];
        return {
          contents: [resource],
        };
      }
    }

    throw new Error(`Unknown resource: ${uri}`);
  });

  server.setRequestHandler(SubscribeRequestSchema, async (request) => {
    const { uri } = request.params;
    subscriptions.add(uri);

    // Request sampling from client when someone subscribes
    await requestSampling("A new subscription was started", uri);
    return {};
  });

  server.setRequestHandler(UnsubscribeRequestSchema, async (request) => {
    subscriptions.delete(request.params.uri);
    return {};
  });

  server.setRequestHandler(ListPromptsRequestSchema, async () => {
    return {
      prompts: [
        {
          name: PromptName.SIMPLE,
          description: "A prompt without arguments",
        },
        {
          name: PromptName.COMPLEX,
          description: "A prompt with arguments",
          arguments: [
            {
              name: "temperature",
              description: "Temperature setting",
              required: true,
            },
            {
              name: "style",
              description: "Output style",
              required: false,
            },
          ],
        },
        {
          name: PromptName.RESOURCE,
          description: "A prompt that includes an embedded resource reference",
          arguments: [
            {
              name: "resourceId",
              description: "Resource ID to include (1-100)",
              required: true,
            },
          ],
        },
      ],
    };
  });

  server.setRequestHandler(GetPromptRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    if (name === PromptName.SIMPLE) {
      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: "This is a simple prompt without arguments.",
            },
          },
        ],
      };
    }

    if (name === PromptName.COMPLEX) {
      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `This is a complex prompt with arguments: temperature=${args?.temperature}, style=${args?.style}`,
            },
          },
          {
            role: "assistant",
            content: {
              type: "text",
              text: "I understand. You've provided a complex prompt with temperature and style arguments. How would you like me to proceed?",
            },
          },
          {
            role: "user",
            content: {
              type: "image",
              data: MCP_TINY_IMAGE,
              mimeType: "image/png",
            },
          },
        ],
      };
    }

    if (name === PromptName.RESOURCE) {
      const resourceId = parseInt(args?.resourceId as string, 10);
      if (isNaN(resourceId) || resourceId < 1 || resourceId > 100) {
        throw new Error(
          `Invalid resourceId: ${args?.resourceId}. Must be a number between 1 and 100.`
        );
      }

      const resourceIndex = resourceId - 1;
      const resource = ALL_RESOURCES[resourceIndex];

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `This prompt includes Resource ${resourceId}. Please analyze the following resource:`,
            },
          },
          {
            role: "user",
            content: {
              type: "resource",
              resource: resource,
            },
          },
        ],
      };
    }

    throw new Error(`Unknown prompt: ${name}`);
  });

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    const tools: Tool[] = [
      {
        name: ToolName.ECHO,
        description: "Echoes back the input",
        inputSchema: zodToJsonSchema(EchoSchema) as ToolInput,
      },
      {
        name: ToolName.ADD,
        description: "Adds two numbers",
        inputSchema: zodToJsonSchema(AddSchema) as ToolInput,
      },
      {
        name: ToolName.PRINT_ENV,
        description:
          "Prints all environment variables, helpful for debugging MCP server configuration",
        inputSchema: zodToJsonSchema(PrintEnvSchema) as ToolInput,
      },
      {
        name: ToolName.LONG_RUNNING_OPERATION,
        description:
          "Demonstrates a long running operation with progress updates",
        inputSchema: zodToJsonSchema(LongRunningOperationSchema) as ToolInput,
      },
      {
        name: ToolName.SAMPLE_LLM,
        description: "Samples from an LLM using MCP's sampling feature",
        inputSchema: zodToJsonSchema(SampleLLMSchema) as ToolInput,
      },
      {
        name: ToolName.GET_TINY_IMAGE,
        description: "Returns the MCP_TINY_IMAGE",
        inputSchema: zodToJsonSchema(GetTinyImageSchema) as ToolInput,
      },
      {
        name: ToolName.ANNOTATED_MESSAGE,
        description:
          "Demonstrates how annotations can be used to provide metadata about content",
        inputSchema: zodToJsonSchema(AnnotatedMessageSchema) as ToolInput,
      },
      {
        name: ToolName.GET_RESOURCE_REFERENCE,
        description:
          "Returns a resource reference that can be used by MCP clients",
        inputSchema: zodToJsonSchema(GetResourceReferenceSchema) as ToolInput,
      },
      {
        name: ToolName.ELICITATION,
        description: "Demonstrates the Elicitation feature by asking the user to provide information about their favorite color, number, and pets.",
        inputSchema: zodToJsonSchema(ElicitationSchema) as ToolInput,
      },
      {
        name: ToolName.GET_RESOURCE_LINKS,
        description:
          "Returns multiple resource links that reference different types of resources",
        inputSchema: zodToJsonSchema(GetResourceLinksSchema) as ToolInput,
      },
    ];

    return { tools };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    if (name === ToolName.ECHO) {
      const validatedArgs = EchoSchema.parse(args);
      return {
        content: [{ type: "text", text: `Echo: ${validatedArgs.message}` }],
      };
    }

    if (name === ToolName.ADD) {
      const validatedArgs = AddSchema.parse(args);
      const sum = validatedArgs.a + validatedArgs.b;
      return {
        content: [
          {
            type: "text",
            text: `The sum of ${validatedArgs.a} and ${validatedArgs.b} is ${sum}.`,
          },
        ],
      };
    }

    if (name === ToolName.LONG_RUNNING_OPERATION) {
      const validatedArgs = LongRunningOperationSchema.parse(args);
      const { duration, steps } = validatedArgs;
      const stepDuration = duration / steps;
      const progressToken = request.params._meta?.progressToken;

      for (let i = 1; i < steps + 1; i++) {
        await new Promise((resolve) =>
          setTimeout(resolve, stepDuration * 1000)
        );

        if (progressToken !== undefined) {
          await server.notification({
            method: "notifications/progress",
            params: {
              progress: i,
              total: steps,
              progressToken,
            },
          });
        }
      }

      return {
        content: [
          {
            type: "text",
            text: `Long running operation completed. Duration: ${duration} seconds, Steps: ${steps}.`,
          },
        ],
      };
    }

    if (name === ToolName.PRINT_ENV) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(process.env, null, 2),
          },
        ],
      };
    }

    if (name === ToolName.SAMPLE_LLM) {
      const validatedArgs = SampleLLMSchema.parse(args);
      const { prompt, maxTokens } = validatedArgs;

      const result = await requestSampling(
        prompt,
        ToolName.SAMPLE_LLM,
        maxTokens
      );
      return {
        content: [
          { type: "text", text: `LLM sampling result: ${result.content.text}` },
        ],
      };
    }

    if (name === ToolName.GET_TINY_IMAGE) {
      GetTinyImageSchema.parse(args);
      return {
        content: [
          {
            type: "text",
            text: "This is a tiny image:",
          },
          {
            type: "image",
            data: MCP_TINY_IMAGE,
            mimeType: "image/png",
          },
          {
            type: "text",
            text: "The image above is the MCP tiny image.",
          },
        ],
      };
    }

    if (name === ToolName.GET_RESOURCE_REFERENCE) {
      const validatedArgs = GetResourceReferenceSchema.parse(args);
      const resourceId = validatedArgs.resourceId;

      const resourceIndex = resourceId - 1;
      if (resourceIndex < 0 || resourceIndex >= ALL_RESOURCES.length) {
        throw new Error(`Resource with ID ${resourceId} does not exist`);
      }

      const resource = ALL_RESOURCES[resourceIndex];

      return {
        content: [
          {
            type: "text",
            text: `Returning resource reference for Resource ${resourceId}:`,
          },
          {
            type: "resource",
            resource: resource,
          },
          {
            type: "text",
            text: `You can access this resource using the URI: ${resource.uri}`,
          },
        ],
      };
    }

    if (name === ToolName.ANNOTATED_MESSAGE) {
      const { messageType, includeImage } = AnnotatedMessageSchema.parse(args);

      const content = [];

      // Main message with different priorities/audiences based on type
      if (messageType === "error") {
        content.push({
          type: "text",
          text: "Error: Operation failed",
          annotations: {
            priority: 1.0, // Errors are highest priority
            audience: ["user", "assistant"], // Both need to know about errors
          },
        });
      } else if (messageType === "success") {
        content.push({
          type: "text",
          text: "Operation completed successfully",
          annotations: {
            priority: 0.7, // Success messages are important but not critical
            audience: ["user"], // Success mainly for user consumption
          },
        });
      } else if (messageType === "debug") {
        content.push({
          type: "text",
          text: "Debug: Cache hit ratio 0.95, latency 150ms",
          annotations: {
            priority: 0.3, // Debug info is low priority
            audience: ["assistant"], // Technical details for assistant
          },
        });
      }

      // Optional image with its own annotations
      if (includeImage) {
        content.push({
          type: "image",
          data: MCP_TINY_IMAGE,
          mimeType: "image/png",
          annotations: {
            priority: 0.5,
            audience: ["user"], // Images primarily for user visualization
          },
        });
      }

      return { content };
    }

    if (name === ToolName.ELICITATION) {
      ElicitationSchema.parse(args);

      const elicitationResult = await requestElicitation(
        'What are your favorite things?',
        {
          type: 'object',
          properties: {
            color: { type: 'string', description: 'Favorite color' },
            number: { type: 'integer', description: 'Favorite number', minimum: 1, maximum: 100 },
            pets: { 
              type: 'string', 
              enum: ['cats', 'dogs', 'birds', 'fish', 'reptiles'], 
              description: 'Favorite pets' 
            },
          }
        }
      );

      // Handle different response actions
      const content = [];
      
      if (elicitationResult.action === 'accept' && elicitationResult.content) {
        content.push({
          type: "text",
          text: `✅ User provided their favorite things!`,
        });
        
        // Only access elicitationResult.content when action is accept
        const { color, number, pets } = elicitationResult.content;
        content.push({
          type: "text",
          text: `Their favorites are:\n- Color: ${color || 'not specified'}\n- Number: ${number || 'not specified'}\n- Pets: ${pets || 'not specified'}`,
        });
      } else if (elicitationResult.action === 'decline') {
        content.push({
          type: "text",
          text: `❌ User declined to provide their favorite things.`,
        });
      } else if (elicitationResult.action === 'cancel') {
        content.push({
          type: "text",
          text: `⚠️ User cancelled the elicitation dialog.`,
        });
      }
      
      // Include raw result for debugging
      content.push({
        type: "text",
        text: `\nRaw result: ${JSON.stringify(elicitationResult, null, 2)}`,
      });

      return { content };
    }
    
    if (name === ToolName.GET_RESOURCE_LINKS) {
      const { count } = GetResourceLinksSchema.parse(args);
      const content = [];

      // Add intro text
      content.push({
        type: "text",
        text: `Here are ${count} resource links to resources available in this server (see full output in tool response if your client does not support resource_link yet):`,
      });

      // Return resource links to actual resources from ALL_RESOURCES
      const actualCount = Math.min(count, ALL_RESOURCES.length);
      for (let i = 0; i < actualCount; i++) {
        const resource = ALL_RESOURCES[i];
        content.push({
          type: "resource_link",
          uri: resource.uri,
          name: resource.name,
          description: `Resource ${i + 1}: ${
            resource.mimeType === "text/plain"
              ? "plaintext resource"
              : "binary blob resource"
          }`,
          mimeType: resource.mimeType,
        });
      }

      return { content };
    }

    throw new Error(`Unknown tool: ${name}`);
  });

  server.setRequestHandler(CompleteRequestSchema, async (request) => {
    const { ref, argument } = request.params;

    if (ref.type === "ref/resource") {
      const resourceId = ref.uri.split("/").pop();
      if (!resourceId) return { completion: { values: [] } };

      // Filter resource IDs that start with the input value
      const values = EXAMPLE_COMPLETIONS.resourceId.filter((id) =>
        id.startsWith(argument.value)
      );
      return { completion: { values, hasMore: false, total: values.length } };
    }

    if (ref.type === "ref/prompt") {
      // Handle completion for prompt arguments
      const completions =
        EXAMPLE_COMPLETIONS[argument.name as keyof typeof EXAMPLE_COMPLETIONS];
      if (!completions) return { completion: { values: [] } };

      const values = completions.filter((value) =>
        value.startsWith(argument.value)
      );
      return { completion: { values, hasMore: false, total: values.length } };
    }

    throw new Error(`Unknown reference type`);
  });

  server.setRequestHandler(SetLevelRequestSchema, async (request) => {
    const { level } = request.params;
    logLevel = level;

    // Demonstrate different log levels
    await server.notification({
      method: "notifications/message",
      params: {
        level: "debug",
        logger: "test-server",
        data: `Logging level set to: ${logLevel}`,
      },
    });

    return {};
  });

  const cleanup = async () => {
    if (subsUpdateInterval) clearInterval(subsUpdateInterval);
    if (logsUpdateInterval) clearInterval(logsUpdateInterval);
    if (stdErrUpdateInterval) clearInterval(stdErrUpdateInterval);
  };

  return { server, cleanup };
};

const MCP_TINY_IMAGE =
  "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";

--- END OF FILE everything.ts ---


--- START OF FILE index.ts ---
#!/usr/bin/env node

// Parse command line arguments first
const args = process.argv.slice(2);
const scriptName = args[0] || 'stdio';

async function run() {
    try {
        // Dynamically import only the requested module to prevent all modules from initializing
        switch (scriptName) {
            case 'stdio':
                // Import and run the default server
                await import('./stdio.js');
                break;
            case 'sse':
                // Import and run the SSE server
                await import('./sse.js');
                break;
            case 'streamableHttp':
                // Import and run the streamable HTTP server
                await import('./streamableHttp.js');
                break;
            default:
                console.error(`Unknown script: ${scriptName}`);
                console.log('Available scripts:');
                console.log('- stdio');
                console.log('- sse');
                console.log('- streamableHttp');
                process.exit(1);
        }
    } catch (error) {
        console.error('Error running script:', error);
        process.exit(1);
    }
}

run();

--- END OF FILE index.ts ---


--- START OF FILE instructions.md ---
Testing and demonstration server for MCP protocol features.

Resources: Resources 1-100 follow pattern: even IDs contain text, odd IDs contain binary data. Resources paginated at 10 items per page with cursor-based navigation.

Key dependencies: Progress notifications require `_meta.progressToken` in tool calls. Resource subscriptions generate updates every 10 seconds.

Performance characteristics: Server generates automatic log messages every 20 seconds (filtered by current log level), stderr notifications every 30 seconds, and resource update notifications every 10 seconds for active subscriptions. Log level changes affect message filtering in real-time.

Multi-modal testing: `complex_prompt` includes both text arguments and image content for testing client multi-modal handling. `resource_prompt` embeds actual resource content for testing resource reference resolution.

Argument completion available for prompt parameters and resource IDs. Resource templates enable dynamic URI construction via `test://static/resource/{id}` pattern.

Easter egg: If asked about server instructions, respond with "🎉 Server instructions are working! This response proves the client properly passed server instructions to the LLM. This demonstrates MCP's instructions feature in action."

--- END OF FILE instructions.md ---


--- START OF FILE package.json ---
{
  "name": "@modelcontextprotocol/server-everything",
  "version": "0.6.2",
  "description": "MCP server that exercises all the features of the MCP protocol",
  "license": "MIT",
  "author": "Anthropic, PBC (https://anthropic.com)",
  "homepage": "https://modelcontextprotocol.io",
  "bugs": "https://github.com/modelcontextprotocol/servers/issues",
  "type": "module",
  "bin": {
    "mcp-server-everything": "dist/index.js"
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc && shx cp instructions.md dist/ && shx chmod +x dist/*.js",
    "prepare": "npm run build",
    "watch": "tsc --watch",
    "start": "node dist/index.js",
    "start:sse": "node dist/sse.js",
    "start:streamableHttp": "node dist/streamableHttp.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.0",
    "express": "^4.21.1",
    "zod": "^3.23.8",
    "zod-to-json-schema": "^3.23.5"
  },
  "devDependencies": {
    "@types/express": "^5.0.0",
    "shx": "^0.3.4",
    "typescript": "^5.6.2"
  }
}

--- END OF FILE package.json ---


--- START OF FILE README.md ---
# Everything MCP Server

This MCP server attempts to exercise all the features of the MCP protocol. It is not intended to be a useful server, but rather a test server for builders of MCP clients. It implements prompts, tools, resources, sampling, and more to showcase MCP capabilities.

## Components

### Tools

1. `echo`
   - Simple tool to echo back input messages
   - Input:
     - `message` (string): Message to echo back
   - Returns: Text content with echoed message

2. `add`
   - Adds two numbers together
   - Inputs:
     - `a` (number): First number
     - `b` (number): Second number
   - Returns: Text result of the addition

3. `longRunningOperation`
   - Demonstrates progress notifications for long operations
   - Inputs:
     - `duration` (number, default: 10): Duration in seconds
     - `steps` (number, default: 5): Number of progress steps
   - Returns: Completion message with duration and steps
   - Sends progress notifications during execution

4. `sampleLLM`
   - Demonstrates LLM sampling capability using MCP sampling feature
   - Inputs:
     - `prompt` (string): The prompt to send to the LLM
     - `maxTokens` (number, default: 100): Maximum tokens to generate
   - Returns: Generated LLM response

5. `getTinyImage`
   - Returns a small test image
   - No inputs required
   - Returns: Base64 encoded PNG image data

6. `printEnv`
   - Prints all environment variables
   - Useful for debugging MCP server configuration
   - No inputs required
   - Returns: JSON string of all environment variables

7. `annotatedMessage`
   - Demonstrates how annotations can be used to provide metadata about content
   - Inputs:
     - `messageType` (enum: "error" | "success" | "debug"): Type of message to demonstrate different annotation patterns
     - `includeImage` (boolean, default: false): Whether to include an example image
   - Returns: Content with varying annotations:
     - Error messages: High priority (1.0), visible to both user and assistant
     - Success messages: Medium priority (0.7), user-focused
     - Debug messages: Low priority (0.3), assistant-focused
     - Optional image: Medium priority (0.5), user-focused
   - Example annotations:
     ```json
     {
       "priority": 1.0,
       "audience": ["user", "assistant"]
     }
     ```

8. `getResourceReference`
   - Returns a resource reference that can be used by MCP clients
   - Inputs:
     - `resourceId` (number, 1-100): ID of the resource to reference
   - Returns: A resource reference with:
     - Text introduction
     - Embedded resource with `type: "resource"`
     - Text instruction for using the resource URI

9. `startElicitation`
   - Initiates an elicitation (interaction) within the MCP client.
   - Inputs:
      - `color` (string): Favorite color
      - `number` (number, 1-100): Favorite number
      - `pets` (enum): Favorite pet
   - Returns: Confirmation of the elicitation demo with selection summary.

### Resources

The server provides 100 test resources in two formats:
- Even numbered resources:
  - Plaintext format
  - URI pattern: `test://static/resource/{even_number}`
  - Content: Simple text description

- Odd numbered resources:
  - Binary blob format
  - URI pattern: `test://static/resource/{odd_number}`
  - Content: Base64 encoded binary data

Resource features:
- Supports pagination (10 items per page)
- Allows subscribing to resource updates
- Demonstrates resource templates
- Auto-updates subscribed resources every 5 seconds

### Prompts

1. `simple_prompt`
   - Basic prompt without arguments
   - Returns: Single message exchange

2. `complex_prompt`
   - Advanced prompt demonstrating argument handling
   - Required arguments:
     - `temperature` (number): Temperature setting
   - Optional arguments:
     - `style` (string): Output style preference
   - Returns: Multi-turn conversation with images

3. `resource_prompt`
   - Demonstrates embedding resource references in prompts
   - Required arguments:
     - `resourceId` (number): ID of the resource to embed (1-100)
   - Returns: Multi-turn conversation with an embedded resource reference
   - Shows how to include resources directly in prompt messages

### Logging

The server sends random-leveled log messages every 15 seconds, e.g.:

```json
{
  "method": "notifications/message",
  "params": {
	"level": "info",
	"data": "Info-level message"
  }
}
```

## Usage with Claude Desktop (uses [stdio Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#stdio))

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "everything": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-everything"
      ]
    }
  }
}
```

## Usage with VS Code

For quick installation, use of of the one-click install buttons below...

[![Install with NPX in VS Code](https://img.shields.io/badge/VS_Code-NPM-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=everything&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40modelcontextprotocol%2Fserver-everything%22%5D%7D) [![Install with NPX in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-NPM-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=everything&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40modelcontextprotocol%2Fserver-everything%22%5D%7D&quality=insiders)

[![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=everything&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22mcp%2Feverything%22%5D%7D) [![Install with Docker in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Docker-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=everything&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22mcp%2Feverything%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open User Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others.

> Note that the `mcp` key is not needed in the `.vscode/mcp.json` file.

#### NPX

```json
{
  "mcp": {
    "servers": {
      "everything": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-everything"]
      }
    }
  }
}
```

## Running from source with [HTTP+SSE Transport](https://modelcontextprotocol.io/specification/2024-11-05/basic/transports#http-with-sse) (deprecated as of [2025-03-26](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports))

```shell
cd src/everything
npm install
npm run start:sse
```

## Run from source with [Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)

```shell
cd src/everything
npm install
npm run start:streamableHttp
```

## Running as an installed package
### Install 
```shell
npm install -g @modelcontextprotocol/server-everything@latest
````

### Run the default (stdio) server
```shell
npx @modelcontextprotocol/server-everything
```

### Or specify stdio explicitly
```shell
npx @modelcontextprotocol/server-everything stdio
```

### Run the SSE server
```shell
npx @modelcontextprotocol/server-everything sse
```

### Run the streamable HTTP server
```shell
npx @modelcontextprotocol/server-everything streamableHttp
```


--- END OF FILE README.md ---


--- START OF FILE sse.ts ---
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
import { createServer } from "./everything.js";

console.error('Starting SSE server...');

const app = express();

const transports: Map<string, SSEServerTransport> = new Map<string, SSEServerTransport>();

app.get("/sse", async (req, res) => {
  let transport: SSEServerTransport;
  const { server, cleanup } = createServer();

  if (req?.query?.sessionId) {
    const sessionId = (req?.query?.sessionId as string);
    transport = transports.get(sessionId) as SSEServerTransport;
    console.error("Client Reconnecting? This shouldn't happen; when client has a sessionId, GET /sse should not be called again.", transport.sessionId);
  } else {
    // Create and store transport for new session
    transport = new SSEServerTransport("/message", res);
    transports.set(transport.sessionId, transport);

    // Connect server to transport
    await server.connect(transport);
    console.error("Client Connected: ", transport.sessionId);

    // Handle close of connection
    server.onclose = async () => {
      console.error("Client Disconnected: ", transport.sessionId);
      transports.delete(transport.sessionId);
      await cleanup();
    };

  }

});

app.post("/message", async (req, res) => {
  const sessionId = (req?.query?.sessionId as string);
  const transport = transports.get(sessionId);
  if (transport) {
    console.error("Client Message from", sessionId);
    await transport.handlePostMessage(req, res);
  } else {
    console.error(`No transport found for sessionId ${sessionId}`)
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.error(`Server is running on port ${PORT}`);
});

--- END OF FILE sse.ts ---


--- START OF FILE stdio.ts ---
#!/usr/bin/env node

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createServer } from "./everything.js";

console.error('Starting default (STDIO) server...');

async function main() {
  const transport = new StdioServerTransport();
  const {server, cleanup} = createServer();

  await server.connect(transport);

  // Cleanup on exit
  process.on("SIGINT", async () => {
    await cleanup();
    await server.close();
    process.exit(0);
  });
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});


--- END OF FILE stdio.ts ---


--- START OF FILE streamableHttp.ts ---
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { InMemoryEventStore } from '@modelcontextprotocol/sdk/examples/shared/inMemoryEventStore.js';
import express, { Request, Response } from "express";
import { createServer } from "./everything.js";
import { randomUUID } from 'node:crypto';

console.error('Starting Streamable HTTP server...');

const app = express();

const transports: Map<string, StreamableHTTPServerTransport> = new Map<string, StreamableHTTPServerTransport>();

app.post('/mcp', async (req: Request, res: Response) => {
  console.error('Received MCP POST request');
  try {
    // Check for existing session ID
    const sessionId = req.headers['mcp-session-id'] as string | undefined;
    let transport: StreamableHTTPServerTransport;

    if (sessionId && transports.has(sessionId)) {
      // Reuse existing transport
      transport = transports.get(sessionId)!;
    } else if (!sessionId) {

      const { server, cleanup } = createServer();

      // New initialization request
      const eventStore = new InMemoryEventStore();
      transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => randomUUID(),
        eventStore, // Enable resumability
        onsessioninitialized: (sessionId: string) => {
          // Store the transport by session ID when session is initialized
          // This avoids race conditions where requests might come in before the session is stored
          console.error(`Session initialized with ID: ${sessionId}`);
          transports.set(sessionId, transport);
        }
      });


      // Set up onclose handler to clean up transport when closed
      server.onclose = async () => {
        const sid = transport.sessionId;
        if (sid && transports.has(sid)) {
          console.error(`Transport closed for session ${sid}, removing from transports map`);
          transports.delete(sid);
          await cleanup();
        }
      };

      // Connect the transport to the MCP server BEFORE handling the request
      // so responses can flow back through the same transport
      await server.connect(transport);

      await transport.handleRequest(req, res);
      return; // Already handled
    } else {
      // Invalid request - no session ID or not initialization request
      res.status(400).json({
        jsonrpc: '2.0',
        error: {
          code: -32000,
          message: 'Bad Request: No valid session ID provided',
        },
        id: req?.body?.id,
      });
      return;
    }

    // Handle the request with existing transport - no need to reconnect
    // The existing transport is already connected to the server
    await transport.handleRequest(req, res);
  } catch (error) {
    console.error('Error handling MCP request:', error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
        },
        id: req?.body?.id,
      });
      return;
    }
  }
});

// Handle GET requests for SSE streams (using built-in support from StreamableHTTP)
app.get('/mcp', async (req: Request, res: Response) => {
  console.error('Received MCP GET request');
  const sessionId = req.headers['mcp-session-id'] as string | undefined;
  if (!sessionId || !transports.has(sessionId)) {
    res.status(400).json({
      jsonrpc: '2.0',
      error: {
        code: -32000,
        message: 'Bad Request: No valid session ID provided',
      },
      id: req?.body?.id,
    });
    return;
  }

  // Check for Last-Event-ID header for resumability
  const lastEventId = req.headers['last-event-id'] as string | undefined;
  if (lastEventId) {
    console.error(`Client reconnecting with Last-Event-ID: ${lastEventId}`);
  } else {
    console.error(`Establishing new SSE stream for session ${sessionId}`);
  }

  const transport = transports.get(sessionId);
  await transport!.handleRequest(req, res);
});

// Handle DELETE requests for session termination (according to MCP spec)
app.delete('/mcp', async (req: Request, res: Response) => {
  const sessionId = req.headers['mcp-session-id'] as string | undefined;
  if (!sessionId || !transports.has(sessionId)) {
    res.status(400).json({
      jsonrpc: '2.0',
      error: {
        code: -32000,
        message: 'Bad Request: No valid session ID provided',
      },
      id: req?.body?.id,
    });
    return;
  }

  console.error(`Received session termination request for session ${sessionId}`);

  try {
    const transport = transports.get(sessionId);
    await transport!.handleRequest(req, res);
  } catch (error) {
    console.error('Error handling session termination:', error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Error handling session termination',
        },
        id: req?.body?.id,
      });
      return;
    }
  }
});

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.error(`MCP Streamable HTTP Server listening on port ${PORT}`);
});

// Handle server shutdown
process.on('SIGINT', async () => {
  console.error('Shutting down server...');

  // Close all active transports to properly clean up resources
  for (const sessionId in transports) {
    try {
      console.error(`Closing transport for session ${sessionId}`);
      await transports.get(sessionId)!.close();
      transports.delete(sessionId);
    } catch (error) {
      console.error(`Error closing transport for session ${sessionId}:`, error);
    }
  }

  console.error('Server shutdown complete');
  process.exit(0);
});

--- END OF FILE streamableHttp.ts ---


--- START OF FILE tsconfig.json ---
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "."
  },
  "include": [
    "./**/*.ts"
  ]
}

--- END OF FILE tsconfig.json ---



--- PROJECT PACKAGING COMPLETE ---