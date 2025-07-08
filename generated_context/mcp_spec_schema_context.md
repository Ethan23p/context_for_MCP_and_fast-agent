# Project: draft

## Directory Structure

```
📁 draft
├── 📁 architecture
│   └── 📄 index.mdx
├── 📁 basic
│   ├── 📁 utilities
│   │   ├── 📄 cancellation.mdx
│   │   ├── 📄 ping.mdx
│   │   └── 📄 progress.mdx
│   ├── 📄 authorization.mdx
│   ├── 📄 index.mdx
│   ├── 📄 lifecycle.mdx
│   ├── 📄 security_best_practices.mdx
│   └── 📄 transports.mdx
├── 📁 client
│   ├── 📄 elicitation.mdx
│   ├── 📄 roots.mdx
│   └── 📄 sampling.mdx
├── 📁 server
│   ├── 📁 utilities
│   │   ├── 📄 completion.mdx
│   │   ├── 📄 logging.mdx
│   │   └── 📄 pagination.mdx
│   ├── 📄 index.mdx
│   ├── 📄 prompts.mdx
│   ├── 📄 resource-picker.png
│   ├── 📄 resources.mdx
│   ├── 📄 slash-command.png
│   └── 📄 tools.mdx
├── 📄 changelog.mdx
└── 📄 index.mdx
```

------------------------------------------------------------

## File Contents

--- START OF FILE architecture/index.mdx ---
---
title: Architecture
---

<div id="enable-section-numbers" />

The Model Context Protocol (MCP) follows a client-host-server architecture where each
host can run multiple client instances. This architecture enables users to integrate AI
capabilities across applications while maintaining clear security boundaries and
isolating concerns. Built on JSON-RPC, MCP provides a stateful session protocol focused
on context exchange and sampling coordination between clients and servers.

## Core Components

```mermaid
graph LR
    subgraph "Application Host Process"
        H[Host]
        C1[Client 1]
        C2[Client 2]
        C3[Client 3]
        H --> C1
        H --> C2
        H --> C3
    end

    subgraph "Local machine"
        S1[Server 1<br>Files & Git]
        S2[Server 2<br>Database]
        R1[("Local<br>Resource A")]
        R2[("Local<br>Resource B")]

        C1 --> S1
        C2 --> S2
        S1 <--> R1
        S2 <--> R2
    end

    subgraph "Internet"
        S3[Server 3<br>External APIs]
        R3[("Remote<br>Resource C")]

        C3 --> S3
        S3 <--> R3
    end
```

### Host

The host process acts as the container and coordinator:

- Creates and manages multiple client instances
- Controls client connection permissions and lifecycle
- Enforces security policies and consent requirements
- Handles user authorization decisions
- Coordinates AI/LLM integration and sampling
- Manages context aggregation across clients

### Clients

Each client is created by the host and maintains an isolated server connection:

- Establishes one stateful session per server
- Handles protocol negotiation and capability exchange
- Routes protocol messages bidirectionally
- Manages subscriptions and notifications
- Maintains security boundaries between servers

A host application creates and manages multiple clients, with each client having a 1:1
relationship with a particular server.

### Servers

Servers provide specialized context and capabilities:

- Expose resources, tools and prompts via MCP primitives
- Operate independently with focused responsibilities
- Request sampling through client interfaces
- Must respect security constraints
- Can be local processes or remote services

## Design Principles

MCP is built on several key design principles that inform its architecture and
implementation:

1. **Servers should be extremely easy to build**

   - Host applications handle complex orchestration responsibilities
   - Servers focus on specific, well-defined capabilities
   - Simple interfaces minimize implementation overhead
   - Clear separation enables maintainable code

2. **Servers should be highly composable**

   - Each server provides focused functionality in isolation
   - Multiple servers can be combined seamlessly
   - Shared protocol enables interoperability
   - Modular design supports extensibility

3. **Servers should not be able to read the whole conversation, nor "see into" other
   servers**

   - Servers receive only necessary contextual information
   - Full conversation history stays with the host
   - Each server connection maintains isolation
   - Cross-server interactions are controlled by the host
   - Host process enforces security boundaries

4. **Features can be added to servers and clients progressively**
   - Core protocol provides minimal required functionality
   - Additional capabilities can be negotiated as needed
   - Servers and clients evolve independently
   - Protocol designed for future extensibility
   - Backwards compatibility is maintained

## Capability Negotiation

The Model Context Protocol uses a capability-based negotiation system where clients and
servers explicitly declare their supported features during initialization. Capabilities
determine which protocol features and primitives are available during a session.

- Servers declare capabilities like resource subscriptions, tool support, and prompt
  templates
- Clients declare capabilities like sampling support and notification handling
- Both parties must respect declared capabilities throughout the session
- Additional capabilities can be negotiated through extensions to the protocol

```mermaid
sequenceDiagram
    participant Host
    participant Client
    participant Server

    Host->>+Client: Initialize client
    Client->>+Server: Initialize session with capabilities
    Server-->>Client: Respond with supported capabilities

    Note over Host,Server: Active Session with Negotiated Features

    loop Client Requests
        Host->>Client: User- or model-initiated action
        Client->>Server: Request (tools/resources)
        Server-->>Client: Response
        Client-->>Host: Update UI or respond to model
    end

    loop Server Requests
        Server->>Client: Request (sampling)
        Client->>Host: Forward to AI
        Host-->>Client: AI response
        Client-->>Server: Response
    end

    loop Notifications
        Server--)Client: Resource updates
        Client--)Server: Status changes
    end

    Host->>Client: Terminate
    Client->>-Server: End session
    deactivate Server
```

Each capability unlocks specific protocol features for use during the session. For
example:

- Implemented [server features](/specification/draft/server) must be advertised in the
  server's capabilities
- Emitting resource subscription notifications requires the server to declare
  subscription support
- Tool invocation requires the server to declare tool capabilities
- [Sampling](/specification/draft/client) requires the client to declare support in its
  capabilities

This capability negotiation ensures clients and servers have a clear understanding of
supported functionality while maintaining protocol extensibility.

--- END OF FILE architecture/index.mdx ---


--- START OF FILE basic/utilities/cancellation.mdx ---
---
title: Cancellation
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) supports optional cancellation of in-progress requests
through notification messages. Either side can send a cancellation notification to
indicate that a previously-issued request should be terminated.

## Cancellation Flow

When a party wants to cancel an in-progress request, it sends a `notifications/cancelled`
notification containing:

- The ID of the request to cancel
- An optional reason string that can be logged or displayed

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": "123",
    "reason": "User requested cancellation"
  }
}
```

## Behavior Requirements

1. Cancellation notifications **MUST** only reference requests that:
   - Were previously issued in the same direction
   - Are believed to still be in-progress
2. The `initialize` request **MUST NOT** be cancelled by clients
3. Receivers of cancellation notifications **SHOULD**:
   - Stop processing the cancelled request
   - Free associated resources
   - Not send a response for the cancelled request
4. Receivers **MAY** ignore cancellation notifications if:
   - The referenced request is unknown
   - Processing has already completed
   - The request cannot be cancelled
5. The sender of the cancellation notification **SHOULD** ignore any response to the
   request that arrives afterward

## Timing Considerations

Due to network latency, cancellation notifications may arrive after request processing
has completed, and potentially after a response has already been sent.

Both parties **MUST** handle these race conditions gracefully:

```mermaid
sequenceDiagram
   participant Client
   participant Server

   Client->>Server: Request (ID: 123)
   Note over Server: Processing starts
   Client--)Server: notifications/cancelled (ID: 123)
   alt
      Note over Server: Processing may have<br/>completed before<br/>cancellation arrives
   else If not completed
      Note over Server: Stop processing
   end
```

## Implementation Notes

- Both parties **SHOULD** log cancellation reasons for debugging
- Application UIs **SHOULD** indicate when cancellation is requested

## Error Handling

Invalid cancellation notifications **SHOULD** be ignored:

- Unknown request IDs
- Already completed requests
- Malformed notifications

This maintains the "fire and forget" nature of notifications while allowing for race
conditions in asynchronous communication.

--- END OF FILE basic/utilities/cancellation.mdx ---


--- START OF FILE basic/utilities/ping.mdx ---
---
title: Ping
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol includes an optional ping mechanism that allows either party
to verify that their counterpart is still responsive and the connection is alive.

## Overview

The ping functionality is implemented through a simple request/response pattern. Either
the client or server can initiate a ping by sending a `ping` request.

## Message Format

A ping request is a standard JSON-RPC request with no parameters:

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "method": "ping"
}
```

## Behavior Requirements

1. The receiver **MUST** respond promptly with an empty response:

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "result": {}
}
```

2. If no response is received within a reasonable timeout period, the sender **MAY**:
   - Consider the connection stale
   - Terminate the connection
   - Attempt reconnection procedures

## Usage Patterns

```mermaid
sequenceDiagram
    participant Sender
    participant Receiver

    Sender->>Receiver: ping request
    Receiver->>Sender: empty response
```

## Implementation Considerations

- Implementations **SHOULD** periodically issue pings to detect connection health
- The frequency of pings **SHOULD** be configurable
- Timeouts **SHOULD** be appropriate for the network environment
- Excessive pinging **SHOULD** be avoided to reduce network overhead

## Error Handling

- Timeouts **SHOULD** be treated as connection failures
- Multiple failed pings **MAY** trigger connection reset
- Implementations **SHOULD** log ping failures for diagnostics

--- END OF FILE basic/utilities/ping.mdx ---


--- START OF FILE basic/utilities/progress.mdx ---
---
title: Progress
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) supports optional progress tracking for long-running
operations through notification messages. Either side can send progress notifications to
provide updates about operation status.

## Progress Flow

When a party wants to _receive_ progress updates for a request, it includes a
`progressToken` in the request metadata.

- Progress tokens **MUST** be a string or integer value
- Progress tokens can be chosen by the sender using any means, but **MUST** be unique
  across all active requests.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "some_method",
  "params": {
    "_meta": {
      "progressToken": "abc123"
    }
  }
}
```

The receiver **MAY** then send progress notifications containing:

- The original progress token
- The current progress value so far
- An optional "total" value
- An optional "message" value

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "abc123",
    "progress": 50,
    "total": 100,
    "message": "Reticulating splines..."
  }
}
```

- The `progress` value **MUST** increase with each notification, even if the total is
  unknown.
- The `progress` and the `total` values **MAY** be floating point.
- The `message` field **SHOULD** provide relevant human readable progress information.

## Behavior Requirements

1. Progress notifications **MUST** only reference tokens that:

   - Were provided in an active request
   - Are associated with an in-progress operation

2. Receivers of progress requests **MAY**:
   - Choose not to send any progress notifications
   - Send notifications at whatever frequency they deem appropriate
   - Omit the total value if unknown

```mermaid
sequenceDiagram
    participant Sender
    participant Receiver

    Note over Sender,Receiver: Request with progress token
    Sender->>Receiver: Method request with progressToken

    Note over Sender,Receiver: Progress updates
    loop Progress Updates
        Receiver-->>Sender: Progress notification (0.2/1.0)
        Receiver-->>Sender: Progress notification (0.6/1.0)
        Receiver-->>Sender: Progress notification (1.0/1.0)
    end

    Note over Sender,Receiver: Operation complete
    Receiver->>Sender: Method response
```

## Implementation Notes

- Senders and receivers **SHOULD** track active progress tokens
- Both parties **SHOULD** implement rate limiting to prevent flooding
- Progress notifications **MUST** stop after completion

--- END OF FILE basic/utilities/progress.mdx ---


--- START OF FILE basic/authorization.mdx ---
---
title: Authorization
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

## Introduction

### Purpose and Scope

The Model Context Protocol provides authorization capabilities at the transport level,
enabling MCP clients to make requests to restricted MCP servers on behalf of resource
owners. This specification defines the authorization flow for HTTP-based transports.

### Protocol Requirements

Authorization is **OPTIONAL** for MCP implementations. When supported:

- Implementations using an HTTP-based transport **SHOULD** conform to this specification.
- Implementations using an STDIO transport **SHOULD NOT** follow this specification, and
  instead retrieve credentials from the environment.
- Implementations using alternative transports **MUST** follow established security best
  practices for their protocol.

### Standards Compliance

This authorization mechanism is based on established specifications listed below, but
implements a selected subset of their features to ensure security and interoperability
while maintaining simplicity:

- OAuth 2.1 IETF DRAFT ([draft-ietf-oauth-v2-1-13](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13))
- OAuth 2.0 Authorization Server Metadata
  ([RFC8414](https://datatracker.ietf.org/doc/html/rfc8414))
- OAuth 2.0 Dynamic Client Registration Protocol
  ([RFC7591](https://datatracker.ietf.org/doc/html/rfc7591))
- OAuth 2.0 Protected Resource Metadata ([RFC9728](https://datatracker.ietf.org/doc/html/rfc9728))

## Authorization Flow

### Roles

A protected _MCP server_ acts as an [OAuth 2.1 resource server](https://www.ietf.org/archive/id/draft-ietf-oauth-v2-1-13.html#name-roles),
capable of accepting and responding to protected resource requests using access tokens.

An _MCP client_ acts as an [OAuth 2.1 client](https://www.ietf.org/archive/id/draft-ietf-oauth-v2-1-13.html#name-roles),
making protected resource requests on behalf of a resource owner.

The _authorization server_ is responsible for interacting with the user (if necessary) and issuing access tokens for use at the MCP server.
The implementation details of the authorization server are beyond the scope of this specification. It may be hosted with the
resource server or a separate entity. The [Authorization Server Discovery section](#authorization-server-discovery)
specifies how an MCP server indicates the location of its corresponding authorization server to a client.

### Overview

1. Authorization servers **MUST** implement OAuth 2.1 with appropriate security
   measures for both confidential and public clients.

1. Authorization servers and MCP clients **SHOULD** support the OAuth 2.0 Dynamic Client Registration
   Protocol ([RFC7591](https://datatracker.ietf.org/doc/html/rfc7591)).

1. MCP servers **MUST** implement OAuth 2.0 Protected Resource Metadata ([RFC9728](https://datatracker.ietf.org/doc/html/rfc9728)).
   MCP clients **MUST** use OAuth 2.0 Protected Resource Metadata for authorization server discovery.

1. MCP authorization servers **MUST** provide OAuth 2.0 Authorization
   Server Metadata ([RFC8414](https://datatracker.ietf.org/doc/html/rfc8414)).
   MCP clients **MUST** use the OAuth 2.0 Authorization Server Metadata.

### Authorization Server Discovery

This section describes the mechanisms by which MCP servers advertise their associated
authorization servers to MCP clients, as well as the discovery process through which MCP
clients can determine authorization server endpoints and supported capabilities.

#### Authorization Server Location

MCP servers **MUST** implement the OAuth 2.0 Protected Resource Metadata ([RFC9728](https://datatracker.ietf.org/doc/html/rfc9728))
specification to indicate the locations of authorization servers. The Protected Resource Metadata document returned by the MCP server **MUST** include
the `authorization_servers` field containing at least one authorization server.

The specific use of `authorization_servers` is beyond the scope of this specification; implementers should consult
OAuth 2.0 Protected Resource Metadata ([RFC9728](https://datatracker.ietf.org/doc/html/rfc9728)) for
guidance on implementation details.

Implementors should note that Protected Resource Metadata documents can define multiple authorization servers. The responsibility for selecting which authorization server to use lies with the MCP client, following the guidelines specified in
[RFC9728 Section 7.6 "Authorization Servers"](https://datatracker.ietf.org/doc/html/rfc9728#name-authorization-servers).

MCP servers **MUST** use the HTTP header `WWW-Authenticate` when returning a _401 Unauthorized_ to indicate the location of the resource server metadata URL
as described in [RFC9728 Section 5.1 "WWW-Authenticate Response"](https://datatracker.ietf.org/doc/html/rfc9728#name-www-authenticate-response).

MCP clients **MUST** be able to parse `WWW-Authenticate` headers and respond appropriately to `HTTP 401 Unauthorized` responses from the MCP server.

#### Server Metadata Discovery

MCP clients **MUST** follow the OAuth 2.0 Authorization Server Metadata [RFC8414](https://datatracker.ietf.org/doc/html/rfc8414)
specification to obtain the information required to interact with the authorization server.

#### Sequence Diagram

The following diagram outlines an example flow:

```mermaid
sequenceDiagram
    participant C as Client
    participant M as MCP Server (Resource Server)
    participant A as Authorization Server

    C->>M: MCP request without token
    M-->>C: HTTP 401 Unauthorized with WWW-Authenticate header
    Note over C: Extract resource_metadata<br />from WWW-Authenticate

    C->>M: GET /.well-known/oauth-protected-resource
    M-->>C: Resource metadata with authorization server URL
    Note over C: Validate RS metadata,<br />build AS metadata URL

    C->>A: GET /.well-known/oauth-authorization-server
    A-->>C: Authorization server metadata

    Note over C,A: OAuth 2.1 authorization flow happens here

    C->>A: Token request
    A-->>C: Access token

    C->>M: MCP request with access token
    M-->>C: MCP response
    Note over C,M: MCP communication continues with valid token
```

### Dynamic Client Registration

MCP clients and authorization servers **SHOULD** support the
OAuth 2.0 Dynamic Client Registration Protocol [RFC7591](https://datatracker.ietf.org/doc/html/rfc7591)
to allow MCP clients to obtain OAuth client IDs without user interaction. This provides a
standardized way for clients to automatically register with new authorization servers, which is crucial
for MCP because:

- Clients may not know all possible MCP servers and their authorization servers in advance.
- Manual registration would create friction for users.
- It enables seamless connection to new MCP servers and their authorization servers.
- Authorization servers can implement their own registration policies.

Any authorization servers that _do not_ support Dynamic Client Registration need to provide
alternative ways to obtain a client ID (and, if applicable, client credentials). For one of
these authorization servers, MCP clients will have to either:

1. Hardcode a client ID (and, if applicable, client credentials) specifically for the MCP client to use when
   interacting with that authorization server, or
2. Present a UI to users that allows them to enter these details, after registering an
   OAuth client themselves (e.g., through a configuration interface hosted by the
   server).

### Authorization Flow Steps

The complete Authorization flow proceeds as follows:

```mermaid
sequenceDiagram
    participant B as User-Agent (Browser)
    participant C as Client
    participant M as MCP Server (Resource Server)
    participant A as Authorization Server

    C->>M: MCP request without token
    M->>C: HTTP 401 Unauthorized with WWW-Authenticate header
    Note over C: Extract resource_metadata URL from WWW-Authenticate

    C->>M: Request Protected Resource Metadata
    M->>C: Return metadata

    Note over C: Parse metadata and extract authorization server(s)<br/>Client determines AS to use

    C->>A: GET /.well-known/oauth-authorization-server
    A->>C: Authorization server metadata response

    alt Dynamic client registration
        C->>A: POST /register
        A->>C: Client Credentials
    end

    Note over C: Generate PKCE parameters<br/>Include resource parameter
    C->>B: Open browser with authorization URL + code_challenge + resource
    B->>A: Authorization request with resource parameter
    Note over A: User authorizes
    A->>B: Redirect to callback with authorization code
    B->>C: Authorization code callback
    C->>A: Token request + code_verifier + resource
    A->>C: Access token (+ refresh token)
    C->>M: MCP request with access token
    M-->>C: MCP response
    Note over C,M: MCP communication continues with valid token
```

#### Resource Parameter Implementation

MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html)
to explicitly specify the target resource for which the token is being requested. The `resource` parameter:

1. **MUST** be included in both authorization requests and token requests.
2. **MUST** identify the MCP server that the client intends to use the token with.
3. **MUST** use the canonical URI of the MCP server as defined in [RFC 8707 Section 2](https://www.rfc-editor.org/rfc/rfc8707.html#name-access-token-request).

##### Canonical Server URI

For the purposes of this specification, the canonical URI of an MCP server is defined as the resource identifier as specified in
[RFC 8707 Section 2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2) and aligns with the `resource` parameter in
[RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728).

MCP clients **SHOULD** provide the most specific URI that they can for the MCP server they intend to access, following the guidance in [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707). While the canonical form uses lowercase scheme and host components, implementations **SHOULD** accept uppercase scheme and host components for robustness and interoperability.

Examples of valid canonical URIs:

- `https://mcp.example.com/mcp`
- `https://mcp.example.com`
- `https://mcp.example.com:8443`
- `https://mcp.example.com/server/mcp` (when path component is necessary to identify individual MCP server)

Examples of invalid canonical URIs:

- `mcp.example.com` (missing scheme)
- `https://mcp.example.com#fragment` (contains fragment)

> **Note:** While both `https://mcp.example.com/` (with trailing slash) and `https://mcp.example.com` (without trailing slash) are technically valid absolute URIs according to [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986), implementations **SHOULD** consistently use the form without the trailing slash for better interoperability unless the trailing slash is semantically significant for the specific resource.

For example, if accessing an MCP server at `https://mcp.example.com`, the authorization request would include:

```
&resource=https%3A%2F%2Fmcp.example.com
```

MCP clients **MUST** send this parameter regardless of whether authorization servers support it.

### Access Token Usage

#### Token Requirements

Access token handling when making requests to MCP servers **MUST** conform to the requirements defined in
[OAuth 2.1 Section 5 "Resource Requests"](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5).
Specifically:

1. MCP client **MUST** use the Authorization request header field defined in
   [OAuth 2.1 Section 5.1.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5.1.1):

```
Authorization: Bearer <access-token>
```

Note that authorization **MUST** be included in every HTTP request from client to server,
even if they are part of the same logical session.

2. Access tokens **MUST NOT** be included in the URI query string

Example request:

```http
GET /mcp HTTP/1.1
Host: mcp.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

#### Token Handling

MCP servers, acting in their role as an OAuth 2.1 resource server, **MUST** validate access tokens as described in
[OAuth 2.1 Section 5.2](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5.2).
MCP servers **MUST** validate that access tokens were issued specifically for them as the intended audience,
according to [RFC 8707 Section 2](https://www.rfc-editor.org/rfc/rfc8707.html#section-2).
If validation fails, servers **MUST** respond according to
[OAuth 2.1 Section 5.3](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5.3)
error handling requirements. Invalid or expired tokens **MUST** receive a HTTP 401
response.

MCP clients **MUST NOT** send tokens to the MCP server other than ones issued by the MCP server's authorization server.

Authorization servers **MUST** only accept tokens that are valid for use with their
own resources.

MCP servers **MUST NOT** accept or transit any other tokens.

### Error Handling

Servers **MUST** return appropriate HTTP status codes for authorization errors:

| Status Code | Description  | Usage                                      |
| ----------- | ------------ | ------------------------------------------ |
| 401         | Unauthorized | Authorization required or token invalid    |
| 403         | Forbidden    | Invalid scopes or insufficient permissions |
| 400         | Bad Request  | Malformed authorization request            |

## Security Considerations

Implementations **MUST** follow OAuth 2.1 security best practices as laid out in [OAuth 2.1 Section 7. "Security Considerations"](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#name-security-considerations).

### Token Audience Binding and Validation

[RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html) Resource Indicators provide critical security benefits by binding tokens to their intended
audiences **when the Authorization Server supports the capability**. To enable current and future adoption:

- MCP clients **MUST** include the `resource` parameter in authorization and token requests as specified in the [Resource Parameter Implementation](#resource-parameter-implementation) section
- MCP servers **MUST** validate that tokens presented to them were specifically issued for their use

The [Security Best Practices document](/specification/draft/basic/security_best_practices#token-passthrough)
outlines why token audience validation is crucial and why token passthrough is explicitly forbidden.

### Token Theft

Attackers who obtain tokens stored by the client, or tokens cached or logged on the server can access protected resources with
requests that appear legitimate to resource servers.

Clients and servers **MUST** implement secure token storage and follow OAuth best practices,
as outlined in [OAuth 2.1, Section 7.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-7.1).

Authorization servers **SHOULD** issue short-lived access tokens to reduce the impact of leaked tokens.
For public clients, authorization servers **MUST** rotate refresh tokens as described in [OAuth 2.1 Section 4.3.1 "Token Endpoint Extension"](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-4.3.1).

### Communication Security

Implementations **MUST** follow [OAuth 2.1 Section 1.5 "Communication Security"](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-1.5).

Specifically:

1. All authorization server endpoints **MUST** be served over HTTPS.
1. All redirect URIs **MUST** be either `localhost` or use HTTPS.

### Authorization Code Protection

An attacker who has gained access to an authorization code contained in an authorization response can try to redeem the authorization code for an access token or otherwise make use of the authorization code.
(Further described in [OAuth 2.1 Section 7.5](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-7.5))

To mitigate this, MCP clients **MUST** implement PKCE according to [OAuth 2.1 Section 7.5.2](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-7.5.2).
PKCE helps prevent authorization code interception and injection attacks by requiring clients to create a secret verifier-challenge pair, ensuring that only the original requestor can exchange an authorization code for tokens.

### Open Redirection

An attacker may craft malicious redirect URIs to direct users to phishing sites.

MCP clients **MUST** have redirect URIs registered with the authorization server.

Authorization servers **MUST** validate exact redirect URIs against pre-registered values to prevent redirection attacks.

MCP clients **SHOULD** use and verify state parameters in the authorization code flow
and discard any results that do not include or have a mismatch with the original state.

Authorization servers **MUST** take precautions to prevent redirecting user agents to untrusted URI's, following suggestions laid out in [OAuth 2.1 Section 7.12.2](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-7.12.2)

Authorization servers **SHOULD** only automatically redirect the user agent if it trusts the redirection URI. If the URI is not trusted, the authorization server MAY inform the user and rely on the user to make the correct decision.

### Confused Deputy Problem

Attackers can exploit MCP servers acting as intermediaries to third-party APIs, leading to [confused deputy vulnerabilities](/specification/draft/basic/security_best_practices#confused-deputy-problem).
By using stolen authorization codes, they can obtain access tokens without user consent.

MCP proxy servers using static client IDs **MUST** obtain user consent for each dynamically
registered client before forwarding to third-party authorization servers (which may require additional consent).

### Access Token Privilege Restriction

An attacker can gain unauthorized access or otherwise compromise a MCP server if the server accepts tokens issued for other resources.

This vulnerability has two critical dimensions:

1. **Audience validation failures.** When an MCP server doesn't verify that tokens were specifically intended for it (for example, via the audience claim, as mentioned in [RFC9068](https://www.rfc-editor.org/rfc/rfc9068.html)), it may accept tokens originally issued for other services. This breaks a fundamental OAuth security boundary, allowing attackers to reuse legitimate tokens across different services than intended.
2. **Token passthrough.** If the MCP server not only accepts tokens with incorrect audiences but also forwards these unmodified tokens to downstream services, it can potentially cause the ["confused deputy" problem](#confused-deputy-problem), where the downstream API may incorrectly trust the token as if it came from the MCP server or assume the token was validated by the upstream API. See the [Token Passthrough section](/specification/draft/basic/security_best_practices#token-passthrough) of the Security Best Practices guide for additional details.

MCP servers **MUST** validate access tokens before processing the request, ensuring the access token is issued specifically for the MCP server, and take all necessary steps to ensure no data is returned to unauthorized parties.

A MCP server **MUST** follow the guidelines in [OAuth 2.1 - Section 5.2](https://www.ietf.org/archive/id/draft-ietf-oauth-v2-1-13.html#section-5.2) to validate inbound tokens.

MCP servers **MUST** only accept tokens specifically intended for themselves and **MUST** reject tokens that do not include them in the audience claim or otherwise verify that they are the intended recipient of the token. See the [Security Best Practices Token Passthrough section](/specification/draft/basic/security_best_practices#token-passthrough) for details.

If the MCP server makes requests to upstream APIs, it may act as an OAuth client to them. The access token used at the upstream API is a seperate token, issued by the upstream authorization server. The MCP server **MUST NOT** pass through the token it received from the MCP client.

MCP clients **MUST** implement and use the `resource` parameter as defined in [RFC 8707 - Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707.html)
to explicitly specify the target resource for which the token is being requested. This requirement aligns with the recommendation in
[RFC 9728 Section 7.4](https://datatracker.ietf.org/doc/html/rfc9728#section-7.4). This ensures that access tokens are bound to their intended resources and
cannot be misused across different services.

--- END OF FILE basic/authorization.mdx ---


--- START OF FILE basic/index.mdx ---
---
title: Overview
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol consists of several key components that work together:

- **Base Protocol**: Core JSON-RPC message types
- **Lifecycle Management**: Connection initialization, capability negotiation, and
  session control
- **Authorization**: Authentication and authorization framework for HTTP-based transports
- **Server Features**: Resources, prompts, and tools exposed by servers
- **Client Features**: Sampling and root directory lists provided by clients
- **Utilities**: Cross-cutting concerns like logging and argument completion

All implementations **MUST** support the base protocol and lifecycle management
components. Other components **MAY** be implemented based on the specific needs of the
application.

These protocol layers establish clear separation of concerns while enabling rich
interactions between clients and servers. The modular design allows implementations to
support exactly the features they need.

## Messages

All messages between MCP clients and servers **MUST** follow the
[JSON-RPC 2.0](https://www.jsonrpc.org/specification) specification. The protocol defines
these types of messages:

### Requests

Requests are sent from the client to the server or vice versa, to initiate an operation.

```typescript
{
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: {
    [key: string]: unknown;
  };
}
```

- Requests **MUST** include a string or integer ID.
- Unlike base JSON-RPC, the ID **MUST NOT** be `null`.
- The request ID **MUST NOT** have been previously used by the requestor within the same
  session.

### Responses

Responses are sent in reply to requests, containing the result or error of the operation.

```typescript
{
  jsonrpc: "2.0";
  id: string | number;
  result?: {
    [key: string]: unknown;
  }
  error?: {
    code: number;
    message: string;
    data?: unknown;
  }
}
```

- Responses **MUST** include the same ID as the request they correspond to.
- **Responses** are further sub-categorized as either **successful results** or
  **errors**. Either a `result` or an `error` **MUST** be set. A response **MUST NOT**
  set both.
- Results **MAY** follow any JSON object structure, while errors **MUST** include an
  error code and message at minimum.
- Error codes **MUST** be integers.

### Notifications

Notifications are sent from the client to the server or vice versa, as a one-way message.
The receiver **MUST NOT** send a response.

```typescript
{
  jsonrpc: "2.0";
  method: string;
  params?: {
    [key: string]: unknown;
  };
}
```

- Notifications **MUST NOT** include an ID.

## Auth

MCP provides an [Authorization](/specification/draft/basic/authorization) framework for use with HTTP.
Implementations using an HTTP-based transport **SHOULD** conform to this specification,
whereas implementations using STDIO transport **SHOULD NOT** follow this specification,
and instead retrieve credentials from the environment.

Additionally, clients and servers **MAY** negotiate their own custom authentication and
authorization strategies.

For further discussions and contributions to the evolution of MCP’s auth mechanisms, join
us in
[GitHub Discussions](https://github.com/modelcontextprotocol/specification/discussions)
to help shape the future of the protocol!

## Schema

The full specification of the protocol is defined as a
[TypeScript schema](https://github.com/modelcontextprotocol/specification/blob/main/schema/draft/schema.ts).
This is the source of truth for all protocol messages and structures.

There is also a
[JSON Schema](https://github.com/modelcontextprotocol/specification/blob/main/schema/draft/schema.json),
which is automatically generated from the TypeScript source of truth, for use with
various automated tooling.

### General fields

#### `_meta`

The `_meta` property/parameter is reserved by MCP to allow clients and servers
to attach additional metadata to their interactions.

Certain key names are reserved by MCP for protocol-level metadata, as specified below;
implementations MUST NOT make assumptions about values at these keys.

Additionally, definitions in the [schema](https://github.com/modelcontextprotocol/specification/blob/main/schema/draft/schema.ts)
may reserve particular names for purpose-specific metadata, as declared in those definitions.

**Key name format:** valid `_meta` key names have two segments: an optional **prefix**, and a **name**.

**Prefix:**

- If specified, MUST be a series of labels separated by dots (`.`), followed by a slash (`/`).
  - Labels MUST start with a letter and end with a letter or digit; interior characters can be letters, digits, or hyphens (`-`).
- Any prefix beginning with zero or more valid labels, followed by `modelcontextprotocol` or `mcp`, followed by any valid label,
  is **reserved** for MCP use.
  - For example: `modelcontextprotocol.io/`, `mcp.dev/`, `api.modelcontextprotocol.org/`, and `tools.mcp.com/` are all reserved.

**Name:**

- Unless empty, MUST begin and end with an alphanumeric character (`[a-z0-9A-Z]`).
- MAY contain hyphens (`-`), underscores (`_`), dots (`.`), and alphanumerics in between.

--- END OF FILE basic/index.mdx ---


--- START OF FILE basic/lifecycle.mdx ---
---
title: Lifecycle
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) defines a rigorous lifecycle for client-server
connections that ensures proper capability negotiation and state management.

1. **Initialization**: Capability negotiation and protocol version agreement
2. **Operation**: Normal protocol communication
3. **Shutdown**: Graceful termination of the connection

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Note over Client,Server: Initialization Phase
    activate Client
    Client->>+Server: initialize request
    Server-->>Client: initialize response
    Client--)Server: initialized notification

    Note over Client,Server: Operation Phase
    rect rgb(200, 220, 250)
        note over Client,Server: Normal protocol operations
    end

    Note over Client,Server: Shutdown
    Client--)-Server: Disconnect
    deactivate Server
    Note over Client,Server: Connection closed
```

## Lifecycle Phases

### Initialization

The initialization phase **MUST** be the first interaction between client and server.
During this phase, the client and server:

- Establish protocol version compatibility
- Exchange and negotiate capabilities
- Share implementation details

The client **MUST** initiate this phase by sending an `initialize` request containing:

- Protocol version supported
- Client capabilities
- Client implementation information

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {},
      "elicitation": {}
    },
    "clientInfo": {
      "name": "ExampleClient",
      "title": "Example Client Display Name",
      "version": "1.0.0"
    }
  }
}
```

The server **MUST** respond with its own capabilities and information:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "logging": {},
      "prompts": {
        "listChanged": true
      },
      "resources": {
        "subscribe": true,
        "listChanged": true
      },
      "tools": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "ExampleServer",
      "title": "Example Server Display Name",
      "version": "1.0.0"
    },
    "instructions": "Optional instructions for the client"
  }
}
```

After successful initialization, the client **MUST** send an `initialized` notification
to indicate it is ready to begin normal operations:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

- The client **SHOULD NOT** send requests other than
  [pings](/specification/draft/basic/utilities/ping) before the server has responded to the
  `initialize` request.
- The server **SHOULD NOT** send requests other than
  [pings](/specification/draft/basic/utilities/ping) and
  [logging](/specification/draft/server/utilities/logging) before receiving the `initialized`
  notification.

#### Version Negotiation

In the `initialize` request, the client **MUST** send a protocol version it supports.
This **SHOULD** be the _latest_ version supported by the client.

If the server supports the requested protocol version, it **MUST** respond with the same
version. Otherwise, the server **MUST** respond with another protocol version it
supports. This **SHOULD** be the _latest_ version supported by the server.

If the client does not support the version in the server's response, it **SHOULD**
disconnect.

<Note>
If using HTTP, the client **MUST** include the `MCP-Protocol-Version:
<protocol-version>` HTTP header on all subsequent requests to the MCP
server.
For details, see [the Protocol Version Header section in Transports](/specification/draft/basic/transports#protocol-version-header).
</Note>

#### Capability Negotiation

Client and server capabilities establish which optional protocol features will be
available during the session.

Key capabilities include:

| Category | Capability     | Description                                                                          |
| -------- | -------------- | ------------------------------------------------------------------------------------ |
| Client   | `roots`        | Ability to provide filesystem [roots](/specification/draft/client/roots)             |
| Client   | `sampling`     | Support for LLM [sampling](/specification/draft/client/sampling) requests            |
| Client   | `elicitation`  | Support for server [elicitation](/specification/draft/client/elicitation) requests   |
| Client   | `experimental` | Describes support for non-standard experimental features                             |
| Server   | `prompts`      | Offers [prompt templates](/specification/draft/server/prompts)                       |
| Server   | `resources`    | Provides readable [resources](/specification/draft/server/resources)                 |
| Server   | `tools`        | Exposes callable [tools](/specification/draft/server/tools)                          |
| Server   | `logging`      | Emits structured [log messages](/specification/draft/server/utilities/logging)       |
| Server   | `completions`  | Supports argument [autocompletion](/specification/draft/server/utilities/completion) |
| Server   | `experimental` | Describes support for non-standard experimental features                             |

Capability objects can describe sub-capabilities like:

- `listChanged`: Support for list change notifications (for prompts, resources, and
  tools)
- `subscribe`: Support for subscribing to individual items' changes (resources only)

### Operation

During the operation phase, the client and server exchange messages according to the
negotiated capabilities.

Both parties **SHOULD**:

- Respect the negotiated protocol version
- Only use capabilities that were successfully negotiated

### Shutdown

During the shutdown phase, one side (usually the client) cleanly terminates the protocol
connection. No specific shutdown messages are defined—instead, the underlying transport
mechanism should be used to signal connection termination:

#### stdio

For the stdio [transport](/specification/draft/basic/transports), the client **SHOULD** initiate
shutdown by:

1. First, closing the input stream to the child process (the server)
2. Waiting for the server to exit, or sending `SIGTERM` if the server does not exit
   within a reasonable time
3. Sending `SIGKILL` if the server does not exit within a reasonable time after `SIGTERM`

The server **MAY** initiate shutdown by closing its output stream to the client and
exiting.

#### HTTP

For HTTP [transports](/specification/draft/basic/transports), shutdown is indicated by closing the
associated HTTP connection(s).

## Timeouts

Implementations **SHOULD** establish timeouts for all sent requests, to prevent hung
connections and resource exhaustion. When the request has not received a success or error
response within the timeout period, the sender **SHOULD** issue a [cancellation
notification](/specification/draft/basic/utilities/cancellation) for that request and stop waiting for
a response.

SDKs and other middleware **SHOULD** allow these timeouts to be configured on a
per-request basis.

Implementations **MAY** choose to reset the timeout clock when receiving a [progress
notification](/specification/draft/basic/utilities/progress) corresponding to the request, as this
implies that work is actually happening. However, implementations **SHOULD** always
enforce a maximum timeout, regardless of progress notifications, to limit the impact of a
misbehaving client or server.

## Error Handling

Implementations **SHOULD** be prepared to handle these error cases:

- Protocol version mismatch
- Failure to negotiate required capabilities
- Request [timeouts](#timeouts)

Example initialization error:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Unsupported protocol version",
    "data": {
      "supported": ["2024-11-05"],
      "requested": "1.0.0"
    }
  }
}
```

--- END OF FILE basic/lifecycle.mdx ---


--- START OF FILE basic/security_best_practices.mdx ---
---
title: Security Best Practices
---

<div id="enable-section-numbers" />

## Introduction

### Purpose and Scope

This document provides security considerations for the Model Context Protocol (MCP), complementing the MCP Authorization specification. This document identifies security risks, attack vectors, and best practices specific to MCP implementations.

The primary audience for this document includes developers implementing MCP authorization flows, MCP server operators, and security professionals evaluating MCP-based systems. This document should be read alongside the MCP Authorization specification and [OAuth 2.0 security best practices](https://datatracker.ietf.org/doc/html/rfc9700).

## Attacks and Mitigations

This section gives a detailed description of attacks on MCP implementations, along with potential countermeasures.

### Confused Deputy Problem

Attackers can exploit MCP servers proxying other resource servers, creating "[confused deputy](https://en.wikipedia.org/wiki/Confused_deputy_problem)" vulnerabilities.

#### Terminology

**MCP Proxy Server**
: An MCP server that connects MCP clients to third-party APIs, offering MCP features while delegating operations and acting as a single OAuth client to the third-party API server.

**Third-Party Authorization Server**
: Authorization server that protects the third-party API. It may lack dynamic client registration support, requiring MCP proxy to use a static client ID for all requests.

**Third-Party API**
: The protected resource server that provides the actual API functionality. Access to this
API requires tokens issued by the third-party authorization server.

**Static Client ID**
: A fixed OAuth 2.0 client identifier used by the MCP proxy server when communicating with
the third-party authorization server. This Client ID refers to the MCP server acting as a client
to the Third-Party API. It is the same value for all MCP server to Third-Party API interactions regardless of
which MCP client initiated the request.

#### Architecture and Attack Flows

##### Normal OAuth proxy usage (preserves user consent)

```mermaid
sequenceDiagram
    participant UA as User-Agent (Browser)
    participant MC as MCP Client
    participant M as MCP Proxy Server
    participant TAS as Third-Party Authorization Server

    Note over UA,M: Initial Auth flow completed

    Note over UA,TAS: Step 1: Legitimate user consent for Third Party Server

    M->>UA: Redirect to third party authorization server
    UA->>TAS: Authorization request (client_id: mcp-proxy)
    TAS->>UA: Authorization consent screen
    Note over UA: Review consent screen
    UA->>TAS: Approve
    TAS->>UA: Set consent cookie for client ID: mcp-proxy
    TAS->>UA: 3P Authorization code + redirect to mcp-proxy-server.com
    UA->>M: 3P Authorization code
    Note over M,TAS: Exchange 3P code for 3P token
    Note over M: Generate MCP authorization code
    M->>UA: Redirect to MCP Client with MCP authorization code

    Note over M,UA: Exchange code for token, etc.
```

##### Malicious OAuth proxy usage (skips user consent)

```mermaid
sequenceDiagram
    participant UA as User-Agent (Browser)
    participant M as MCP Proxy Server
    participant TAS as Third-Party Authorization Server
    participant A as Attacker


    Note over UA,A: Step 2: Attack (leveraging existing cookie, skipping consent)
    A->>M: Dynamically register malicious client, redirect_uri: attacker.com
    A->>UA: Sends malicious link
    UA->>TAS: Authorization request (client_id: mcp-proxy) + consent cookie
    rect rgba(255, 17, 0, 0.67)
    TAS->>TAS: Cookie present, consent skipped
    end

   TAS->>UA: 3P Authorization code + redirect to mcp-proxy-server.com
   UA->>M: 3P Authorization code
   Note over M,TAS: Exchange 3P code for 3P token
   Note over M: Generate MCP authorization code
   M->>UA: Redirect to attacker.com with MCP Authorization code
   UA->>A: MCP Authorization code delivered to attacker.com
   Note over M,A: Attacker exchanges MCP code for MCP token
   A->>M: Attacker impersonates user to MCP server
```

#### Attack Description

When an MCP proxy server uses a static client ID to authenticate with a third-party
authorization server that does not support dynamic client registration, the following
attack becomes possible:

1. A user authenticates normally through the MCP proxy server to access the third-party API
2. During this flow, the third-party authorization server sets a cookie on the user agent
   indicating consent for the static client ID
3. An attacker later sends the user a malicious link containing a crafted authorization request which contains a malicious redirect URI along with a new dynamically registered client ID
4. When the user clicks the link, their browser still has the consent cookie from the previous legitimate request
5. The third-party authorization server detects the cookie and skips the consent screen
6. The MCP authorization code is redirected to the attacker's server (specified in the crafted redirect_uri during dynamic client registration)
7. The attacker exchanges the stolen authorization code for access tokens for the MCP server without the user's explicit approval
8. Attacker now has access to the third-party API as the compromised user

#### Mitigation

MCP proxy servers using static client IDs **MUST** obtain user consent for each dynamically
registered client before forwarding to third-party authorization servers (which may require additional consent).

### Token Passthrough

"Token passthrough" is an anti-pattern where an MCP server accepts tokens from an MCP client without validating that the tokens were properly issued _to the MCP server_ and "passing them through" to the downstream API.

#### Risks

Token passthrough is explicitly forbidden in the [authorization specification](/specification/draft/basic/authorization) as it introduces a number of security risks, that include:

- **Security Control Circumvention**
  - The MCP Server or downstream APIs might implement important security controls like rate limiting, request validation, or traffic monitoring, that depend on the token audience or other credential constraints. If clients can obtain and use tokens directly with the downstream APIs without the MCP server validating them properly or ensuring that the tokens are issued for the right service, they bypass these controls.
- **Accountability and Audit Trail Issues**
  - The MCP Server will be unable to identify or distinguish between MCP Clients when clients are calling with an upstream-issued access token which may be opaque to the MCP Server.
  - The downstream Resource Server’s logs may show requests that appear to come from a different source with a different identity, rather than the MCP server that is actually forwarding the tokens.
  - Both factors make incident investigation, controls, and auditing more difficult.
  - If the MCP Server passes tokens without validating their claims (e.g., roles, privileges, or audience) or other metadata, a malicious actor in possession of a stolen token can use the server as a proxy for data exfiltration.
- **Trust Boundary Issues**
  - The downstream Resource Server grants trust to specific entities. This trust might include assumptions about origin or client behavior patterns. Breaking this trust boundary could lead to unexpected issues.
  - If the token is accepted by multiple services without proper validation, an attacker compromising one service can use the token to access other connected services.
- **Future Compatibility Risk**
  - Even if an MCP Server starts as a "pure proxy" today, it might need to add security controls later. Starting with proper token audience separation makes it easier to evolve the security model.

#### Mitigation

MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server.

### Session Hijacking

Session hijacking is an attack vector where a client is provided a session ID by the server, and an unauthorized party is able to obtain and use that same session ID to impersonate the original client and perform unauthorized actions on their behalf.

#### Session Hijack Prompt Injection

```mermaid
sequenceDiagram
    participant Client
    participant ServerA
    participant Queue
    participant ServerB
    participant Attacker

    Client->>ServerA: Initialize (connect to streamable HTTP server)
    ServerA-->>Client: Respond with session ID

    Attacker->>ServerB: Access/guess session ID
    Note right of Attacker: Attacker knows/guesses session ID

    Attacker->>ServerB: Trigger event (malicious payload, using session ID)
    ServerB->>Queue: Enqueue event (keyed by session ID)

    ServerA->>Queue: Poll for events (using session ID)
    Queue-->>ServerA: Event data (malicious payload)

    ServerA-->>Client: Async response (malicious payload)
    Client->>Client: Acts based on malicious payload
```

#### Session Hijack Impersonation

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Attacker

    Client->>Server: Initialize (login/authenticate)
    Server-->>Client: Respond with session ID (persistent session created)

    Attacker->>Server: Access/guess session ID
    Note right of Attacker: Attacker knows/guesses session ID

    Attacker->>Server: Make API call (using session ID, no re-auth)
    Server-->>Attacker: Respond as if Attacker is Client (session hijack)
```

#### Attack Description

When you have multiple stateful HTTP servers that handle MCP requests, the following attack vectors are possible:

**Session Hijack Prompt Injection**

1. The client connects to **Server A** and receives a session ID.
1. The attacker obtains an existing session ID and sends a malicious event to **Server B** with said session ID.

   - When a server supports [redelivery/resumable streams](/specification/draft/basic/transports#resumability-and-redelivery), deliberately terminating the request before receiving the response could lead to it being resumed by the original client via the GET request for server sent events.
   - If a particular server initiates server sent events as a consequence of a tool call such as a `notifications/tools/list_changed`, where it is possible to affect the tools that are offered by the server, a client could end up with tools that they were not aware were enabled.

1. **Server B** enqueues the event (associated with session ID) into a shared queue.
1. **Server A** polls the queue for events using the session ID and retrieves the malicious payload.
1. **Server A** sends the malicious payload to the client as an asynchronous or resumed response.
1. The client receives and acts on the malicious payload, leading to potential compromise.

**Session Hijack Impersonation**

1. The MCP client authenticates with the MCP server, creating a persistent session ID.
2. The attacker obtains the session ID.
3. The attacker makes calls to the MCP server using the session ID.
4. MCP server does not check for additional authorization and treats the attacker as a legitimate user, allowing unauthorized access or actions.

#### Mitigation

To prevent session hijacking and event injection attacks, the following mitigations should be implemented:

MCP servers that implement authorization **MUST** verify all inbound requests.
MCP Servers **MUST NOT** use sessions for authentication.

MCP servers **MUST** use secure, non-deterministic session IDs.
Generated session IDs (e.g., UUIDs) **SHOULD** use secure random number generators. Avoid predictable or sequential session identifiers that could be guessed by an attacker. Rotating or expiring session IDs can also reduce the risk.

MCP servers **SHOULD** bind session IDs to user-specific information.
When storing or transmitting session-related data (e.g., in a queue), combine the session ID with information unique to the authorized user, such as their internal user ID. Use a key format like `<user_id>:<session_id>`. This ensures that even if an attacker guesses a session ID, they cannot impersonate another user as the user ID is derived from the user token and not provided by the client.

MCP servers can optionally leverage additional unique identifiers.

--- END OF FILE basic/security_best_practices.mdx ---


--- START OF FILE basic/transports.mdx ---
---
title: Transports
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

MCP uses JSON-RPC to encode messages. JSON-RPC messages **MUST** be UTF-8 encoded.

The protocol currently defines two standard transport mechanisms for client-server
communication:

1. [stdio](#stdio), communication over standard in and standard out
2. [Streamable HTTP](#streamable-http)

Clients **SHOULD** support stdio whenever possible.

It is also possible for clients and servers to implement
[custom transports](#custom-transports) in a pluggable fashion.

## stdio

In the **stdio** transport:

- The client launches the MCP server as a subprocess.
- The server reads JSON-RPC messages from its standard input (`stdin`) and sends messages
  to its standard output (`stdout`).
- Messages are individual JSON-RPC requests, notifications, or responses.
- Messages are delimited by newlines, and **MUST NOT** contain embedded newlines.
- The server **MAY** write UTF-8 strings to its standard error (`stderr`) for logging
  purposes. Clients **MAY** capture, forward, or ignore this logging.
- The server **MUST NOT** write anything to its `stdout` that is not a valid MCP message.
- The client **MUST NOT** write anything to the server's `stdin` that is not a valid MCP
  message.

```mermaid
sequenceDiagram
    participant Client
    participant Server Process

    Client->>+Server Process: Launch subprocess
    loop Message Exchange
        Client->>Server Process: Write to stdin
        Server Process->>Client: Write to stdout
        Server Process--)Client: Optional logs on stderr
    end
    Client->>Server Process: Close stdin, terminate subprocess
    deactivate Server Process
```

## Streamable HTTP

<Info>

This replaces the [HTTP+SSE
transport](/specification/2024-11-05/basic/transports#http-with-sse) from
protocol version 2024-11-05. See the [backwards compatibility](#backwards-compatibility)
guide below.

</Info>

In the **Streamable HTTP** transport, the server operates as an independent process that
can handle multiple client connections. This transport uses HTTP POST and GET requests.
Server can optionally make use of
[Server-Sent Events](https://en.wikipedia.org/wiki/Server-sent_events) (SSE) to stream
multiple server messages. This permits basic MCP servers, as well as more feature-rich
servers supporting streaming and server-to-client notifications and requests.

The server **MUST** provide a single HTTP endpoint path (hereafter referred to as the
**MCP endpoint**) that supports both POST and GET methods. For example, this could be a
URL like `https://example.com/mcp`.

#### Security Warning

When implementing Streamable HTTP transport:

1. Servers **MUST** validate the `Origin` header on all incoming connections to prevent DNS rebinding attacks
2. When running locally, servers **SHOULD** bind only to localhost (127.0.0.1) rather than all network interfaces (0.0.0.0)
3. Servers **SHOULD** implement proper authentication for all connections

Without these protections, attackers could use DNS rebinding to interact with local MCP servers from remote websites.

### Sending Messages to the Server

Every JSON-RPC message sent from the client **MUST** be a new HTTP POST request to the
MCP endpoint.

1. The client **MUST** use HTTP POST to send JSON-RPC messages to the MCP endpoint.
2. The client **MUST** include an `Accept` header, listing both `application/json` and
   `text/event-stream` as supported content types.
3. The body of the POST request **MUST** be a single JSON-RPC _request_, _notification_, or _response_.
4. If the input is a JSON-RPC _response_ or _notification_:
   - If the server accepts the input, the server **MUST** return HTTP status code 202
     Accepted with no body.
   - If the server cannot accept the input, it **MUST** return an HTTP error status code
     (e.g., 400 Bad Request). The HTTP response body **MAY** comprise a JSON-RPC _error
     response_ that has no `id`.
5. If the input is a JSON-RPC _request_, the server **MUST** either
   return `Content-Type: text/event-stream`, to initiate an SSE stream, or
   `Content-Type: application/json`, to return one JSON object. The client **MUST**
   support both these cases.
6. If the server initiates an SSE stream:
   - The SSE stream **SHOULD** eventually include JSON-RPC _response_ for the
     JSON-RPC _request_ sent in the POST body.
   - The server **MAY** send JSON-RPC _requests_ and _notifications_ before sending the
     JSON-RPC _response_. These messages **SHOULD** relate to the originating client
     _request_.
   - The server **SHOULD NOT** close the SSE stream before sending the JSON-RPC _response_
     for the received JSON-RPC _request_, unless the [session](#session-management)
     expires.
   - After the JSON-RPC _response_ has been sent, the server **SHOULD** close the SSE
     stream.
   - Disconnection **MAY** occur at any time (e.g., due to network conditions).
     Therefore:
     - Disconnection **SHOULD NOT** be interpreted as the client cancelling its request.
     - To cancel, the client **SHOULD** explicitly send an MCP `CancelledNotification`.
     - To avoid message loss due to disconnection, the server **MAY** make the stream
       [resumable](#resumability-and-redelivery).

### Listening for Messages from the Server

1. The client **MAY** issue an HTTP GET to the MCP endpoint. This can be used to open an
   SSE stream, allowing the server to communicate to the client, without the client first
   sending data via HTTP POST.
2. The client **MUST** include an `Accept` header, listing `text/event-stream` as a
   supported content type.
3. The server **MUST** either return `Content-Type: text/event-stream` in response to
   this HTTP GET, or else return HTTP 405 Method Not Allowed, indicating that the server
   does not offer an SSE stream at this endpoint.
4. If the server initiates an SSE stream:
   - The server **MAY** send JSON-RPC _requests_ and _notifications_ on the stream.
   - These messages **SHOULD** be unrelated to any concurrently-running JSON-RPC
     _request_ from the client.
   - The server **MUST NOT** send a JSON-RPC _response_ on the stream **unless**
     [resuming](#resumability-and-redelivery) a stream associated with a previous client
     request.
   - The server **MAY** close the SSE stream at any time.
   - The client **MAY** close the SSE stream at any time.

### Multiple Connections

1. The client **MAY** remain connected to multiple SSE streams simultaneously.
2. The server **MUST** send each of its JSON-RPC messages on only one of the connected
   streams; that is, it **MUST NOT** broadcast the same message across multiple streams.
   - The risk of message loss **MAY** be mitigated by making the stream
     [resumable](#resumability-and-redelivery).

### Resumability and Redelivery

To support resuming broken connections, and redelivering messages that might otherwise be
lost:

1. Servers **MAY** attach an `id` field to their SSE events, as described in the
   [SSE standard](https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation).
   - If present, the ID **MUST** be globally unique across all streams within that
     [session](#session-management)—or all streams with that specific client, if session
     management is not in use.
2. If the client wishes to resume after a broken connection, it **SHOULD** issue an HTTP
   GET to the MCP endpoint, and include the
   [`Last-Event-ID`](https://html.spec.whatwg.org/multipage/server-sent-events.html#the-last-event-id-header)
   header to indicate the last event ID it received.
   - The server **MAY** use this header to replay messages that would have been sent
     after the last event ID, _on the stream that was disconnected_, and to resume the
     stream from that point.
   - The server **MUST NOT** replay messages that would have been delivered on a
     different stream.

In other words, these event IDs should be assigned by servers on a _per-stream_ basis, to
act as a cursor within that particular stream.

### Session Management

An MCP "session" consists of logically related interactions between a client and a
server, beginning with the [initialization phase](/specification/draft/basic/lifecycle). To support
servers which want to establish stateful sessions:

1. A server using the Streamable HTTP transport **MAY** assign a session ID at
   initialization time, by including it in an `Mcp-Session-Id` header on the HTTP
   response containing the `InitializeResult`.
   - The session ID **SHOULD** be globally unique and cryptographically secure (e.g., a
     securely generated UUID, a JWT, or a cryptographic hash).
   - The session ID **MUST** only contain visible ASCII characters (ranging from 0x21 to
     0x7E).
2. If an `Mcp-Session-Id` is returned by the server during initialization, clients using
   the Streamable HTTP transport **MUST** include it in the `Mcp-Session-Id` header on
   all of their subsequent HTTP requests.
   - Servers that require a session ID **SHOULD** respond to requests without an
     `Mcp-Session-Id` header (other than initialization) with HTTP 400 Bad Request.
3. The server **MAY** terminate the session at any time, after which it **MUST** respond
   to requests containing that session ID with HTTP 404 Not Found.
4. When a client receives HTTP 404 in response to a request containing an
   `Mcp-Session-Id`, it **MUST** start a new session by sending a new `InitializeRequest`
   without a session ID attached.
5. Clients that no longer need a particular session (e.g., because the user is leaving
   the client application) **SHOULD** send an HTTP DELETE to the MCP endpoint with the
   `Mcp-Session-Id` header, to explicitly terminate the session.
   - The server **MAY** respond to this request with HTTP 405 Method Not Allowed,
     indicating that the server does not allow clients to terminate sessions.

### Sequence Diagram

```mermaid
sequenceDiagram
    participant Client
    participant Server

    note over Client, Server: initialization

    Client->>+Server: POST InitializeRequest
    Server->>-Client: InitializeResponse<br>Mcp-Session-Id: 1868a90c...

    Client->>+Server: POST InitializedNotification<br>Mcp-Session-Id: 1868a90c...
    Server->>-Client: 202 Accepted

    note over Client, Server: client requests
    Client->>+Server: POST ... request ...<br>Mcp-Session-Id: 1868a90c...

    alt single HTTP response
      Server->>Client: ... response ...
    else server opens SSE stream
      loop while connection remains open
          Server-)Client: ... SSE messages from server ...
      end
      Server-)Client: SSE event: ... response ...
    end
    deactivate Server

    note over Client, Server: client notifications/responses
    Client->>+Server: POST ... notification/response ...<br>Mcp-Session-Id: 1868a90c...
    Server->>-Client: 202 Accepted

    note over Client, Server: server requests
    Client->>+Server: GET<br>Mcp-Session-Id: 1868a90c...
    loop while connection remains open
        Server-)Client: ... SSE messages from server ...
    end
    deactivate Server

```

### Protocol Version Header

If using HTTP, the client **MUST** include the `MCP-Protocol-Version:
<protocol-version>` HTTP header on all subsequent requests to the MCP
server, allowing the MCP server to respond based on the MCP protocol version.

For example: `MCP-Protocol-Version: 2025-06-18`

The protocol version sent by the client **SHOULD** be the one [negotiated during
initialization](/specification/draft/basic/lifecycle#version-negotiation).

For backwards compatibility, if the server does _not_ receive an `MCP-Protocol-Version`
header, and has no other way to identify the version - for example, by relying on the
protocol version negotiated during initialization - the server **SHOULD** assume protocol
version `2025-03-26`.

If the server receives a request with an invalid or unsupported
`MCP-Protocol-Version`, it **MUST** respond with `400 Bad Request`.

### Backwards Compatibility

Clients and servers can maintain backwards compatibility with the deprecated [HTTP+SSE
transport](/specification/2024-11-05/basic/transports#http-with-sse) (from
protocol version 2024-11-05) as follows:

**Servers** wanting to support older clients should:

- Continue to host both the SSE and POST endpoints of the old transport, alongside the
  new "MCP endpoint" defined for the Streamable HTTP transport.
  - It is also possible to combine the old POST endpoint and the new MCP endpoint, but
    this may introduce unneeded complexity.

**Clients** wanting to support older servers should:

1. Accept an MCP server URL from the user, which may point to either a server using the
   old transport or the new transport.
2. Attempt to POST an `InitializeRequest` to the server URL, with an `Accept` header as
   defined above:
   - If it succeeds, the client can assume this is a server supporting the new Streamable
     HTTP transport.
   - If it fails with an HTTP 4xx status code (e.g., 405 Method Not Allowed or 404 Not
     Found):
     - Issue a GET request to the server URL, expecting that this will open an SSE stream
       and return an `endpoint` event as the first event.
     - When the `endpoint` event arrives, the client can assume this is a server running
       the old HTTP+SSE transport, and should use that transport for all subsequent
       communication.

## Custom Transports

Clients and servers **MAY** implement additional custom transport mechanisms to suit
their specific needs. The protocol is transport-agnostic and can be implemented over any
communication channel that supports bidirectional message exchange.

Implementers who choose to support custom transports **MUST** ensure they preserve the
JSON-RPC message format and lifecycle requirements defined by MCP. Custom transports
**SHOULD** document their specific connection establishment and message exchange patterns
to aid interoperability.

--- END OF FILE basic/transports.mdx ---


--- START OF FILE client/elicitation.mdx ---
---
title: Elicitation
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

<Note>

Elicitation is newly introduced in this version of the MCP specification and its design may evolve in future protocol versions.

</Note>

The Model Context Protocol (MCP) provides a standardized way for servers to request additional
information from users through the client during interactions. This flow allows clients to
maintain control over user interactions and data sharing while enabling servers to gather
necessary information dynamically.
Servers request structured data from users with JSON schemas to validate responses.

## User Interaction Model

Elicitation in MCP allows servers to implement interactive workflows by enabling user input
requests to occur _nested_ inside other MCP server features.

Implementations are free to expose elicitation through any interface pattern that suits
their needs&mdash;the protocol itself does not mandate any specific user interaction
model.

<Warning>

For trust & safety and security:

- Servers **MUST NOT** use elicitation to request sensitive information.

Applications **SHOULD**:

- Provide UI that makes it clear which server is requesting information
- Allow users to review and modify their responses before sending
- Respect user privacy and provide clear decline and cancel options

</Warning>

## Capabilities

Clients that support elicitation **MUST** declare the `elicitation` capability during
[initialization](/specification/draft/basic/lifecycle#initialization):

```json
{
  "capabilities": {
    "elicitation": {}
  }
}
```

## Protocol Messages

### Creating Elicitation Requests

To request information from a user, servers send an `elicitation/create` request:

#### Simple Text Request

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "elicitation/create",
  "params": {
    "message": "Please provide your GitHub username",
    "requestedSchema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        }
      },
      "required": ["name"]
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "action": "accept",
    "content": {
      "name": "octocat"
    }
  }
}
```

#### Structured Data Request

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "elicitation/create",
  "params": {
    "message": "Please provide your contact information",
    "requestedSchema": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Your full name"
        },
        "email": {
          "type": "string",
          "format": "email",
          "description": "Your email address"
        },
        "age": {
          "type": "number",
          "minimum": 18,
          "description": "Your age"
        }
      },
      "required": ["name", "email"]
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "action": "accept",
    "content": {
      "name": "Monalisa Octocat",
      "email": "octocat@github.com",
      "age": 30
    }
  }
}
```

**Reject Response Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "action": "decline"
  }
}
```

**Cancel Response Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "action": "cancel"
  }
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Server

    Note over Server,Client: Server initiates elicitation
    Server->>Client: elicitation/create

    Note over Client,User: Human interaction
    Client->>User: Present elicitation UI
    User-->>Client: Provide requested information

    Note over Server,Client: Complete request
    Client-->>Server: Return user response

    Note over Server: Continue processing with new information
```

## Request Schema

The `requestedSchema` field allows servers to define the structure of the expected response using a restricted subset of JSON Schema. To simplify implementation for clients, elicitation schemas are limited to flat objects with primitive properties only:

```json
"requestedSchema": {
  "type": "object",
  "properties": {
    "propertyName": {
      "type": "string",
      "title": "Display Name",
      "description": "Description of the property"
    },
    "anotherProperty": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    }
  },
  "required": ["propertyName"]
}
```

### Supported Schema Types

The schema is restricted to these primitive types:

1. **String Schema**

   ```json
   {
     "type": "string",
     "title": "Display Name",
     "description": "Description text",
     "minLength": 3,
     "maxLength": 50,
     "pattern": "^[A-Za-z]+$",
     "format": "email"
   }
   ```

   Supported formats: `email`, `uri`, `date`, `date-time`

2. **Number Schema**

   ```json
   {
     "type": "number", // or "integer"
     "title": "Display Name",
     "description": "Description text",
     "minimum": 0,
     "maximum": 100
   }
   ```

3. **Boolean Schema**

   ```json
   {
     "type": "boolean",
     "title": "Display Name",
     "description": "Description text",
     "default": false
   }
   ```

4. **Enum Schema**
   ```json
   {
     "type": "string",
     "title": "Display Name",
     "description": "Description text",
     "enum": ["option1", "option2", "option3"],
     "enumNames": ["Option 1", "Option 2", "Option 3"]
   }
   ```

Clients can use this schema to:

1. Generate appropriate input forms
2. Validate user input before sending
3. Provide better guidance to users

Note that complex nested structures, arrays of objects, and other advanced JSON Schema features are intentionally not supported to simplify client implementation.

## Response Actions

Elicitation responses use a three-action model to clearly distinguish between different user actions:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "action": "accept", // or "decline" or "cancel"
    "content": {
      "propertyName": "value",
      "anotherProperty": 42
    }
  }
}
```

The three response actions are:

1. **Accept** (`action: "accept"`): User explicitly approved and submitted with data

   - The `content` field contains the submitted data matching the requested schema
   - Example: User clicked "Submit", "OK", "Confirm", etc.

2. **Decline** (`action: "decline"`): User explicitly declined the request

   - The `content` field is typically omitted
   - Example: User clicked "Reject", "Decline", "No", etc.

3. **Cancel** (`action: "cancel"`): User dismissed without making an explicit choice
   - The `content` field is typically omitted
   - Example: User closed the dialog, clicked outside, pressed Escape, etc.

Servers should handle each state appropriately:

- **Accept**: Process the submitted data
- **Decline**: Handle explicit decline (e.g., offer alternatives)
- **Cancel**: Handle dismissal (e.g., prompt again later)

## Security Considerations

1. Servers **MUST NOT** request sensitive information through elicitation
2. Clients **SHOULD** implement user approval controls
3. Both parties **SHOULD** validate elicitation content against the provided schema
4. Clients **SHOULD** provide clear indication of which server is requesting information
5. Clients **SHOULD** allow users to decline elicitation requests at any time
6. Clients **SHOULD** implement rate limiting
7. Clients **SHOULD** present elicitation requests in a way that makes it clear what information is being requested and why

--- END OF FILE client/elicitation.mdx ---


--- START OF FILE client/roots.mdx ---
---
title: Roots
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) provides a standardized way for clients to expose
filesystem "roots" to servers. Roots define the boundaries of where servers can operate
within the filesystem, allowing them to understand which directories and files they have
access to. Servers can request the list of roots from supporting clients and receive
notifications when that list changes.

## User Interaction Model

Roots in MCP are typically exposed through workspace or project configuration interfaces.

For example, implementations could offer a workspace/project picker that allows users to
select directories and files the server should have access to. This can be combined with
automatic workspace detection from version control systems or project files.

However, implementations are free to expose roots through any interface pattern that
suits their needs&mdash;the protocol itself does not mandate any specific user
interaction model.

## Capabilities

Clients that support roots **MUST** declare the `roots` capability during
[initialization](/specification/draft/basic/lifecycle#initialization):

```json
{
  "capabilities": {
    "roots": {
      "listChanged": true
    }
  }
}
```

`listChanged` indicates whether the client will emit notifications when the list of roots
changes.

## Protocol Messages

### Listing Roots

To retrieve roots, servers send a `roots/list` request:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "roots/list"
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "roots": [
      {
        "uri": "file:///home/user/projects/myproject",
        "name": "My Project"
      }
    ]
  }
}
```

### Root List Changes

When roots change, clients that support `listChanged` **MUST** send a notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/roots/list_changed"
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant Server
    participant Client

    Note over Server,Client: Discovery
    Server->>Client: roots/list
    Client-->>Server: Available roots

    Note over Server,Client: Changes
    Client--)Server: notifications/roots/list_changed
    Server->>Client: roots/list
    Client-->>Server: Updated roots
```

## Data Types

### Root

A root definition includes:

- `uri`: Unique identifier for the root. This **MUST** be a `file://` URI in the current
  specification.
- `name`: Optional human-readable name for display purposes.

Example roots for different use cases:

#### Project Directory

```json
{
  "uri": "file:///home/user/projects/myproject",
  "name": "My Project"
}
```

#### Multiple Repositories

```json
[
  {
    "uri": "file:///home/user/repos/frontend",
    "name": "Frontend Repository"
  },
  {
    "uri": "file:///home/user/repos/backend",
    "name": "Backend Repository"
  }
]
```

## Error Handling

Clients **SHOULD** return standard JSON-RPC errors for common failure cases:

- Client does not support roots: `-32601` (Method not found)
- Internal errors: `-32603`

Example error:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Roots not supported",
    "data": {
      "reason": "Client does not have roots capability"
    }
  }
}
```

## Security Considerations

1. Clients **MUST**:

   - Only expose roots with appropriate permissions
   - Validate all root URIs to prevent path traversal
   - Implement proper access controls
   - Monitor root accessibility

2. Servers **SHOULD**:
   - Handle cases where roots become unavailable
   - Respect root boundaries during operations
   - Validate all paths against provided roots

## Implementation Guidelines

1. Clients **SHOULD**:

   - Prompt users for consent before exposing roots to servers
   - Provide clear user interfaces for root management
   - Validate root accessibility before exposing
   - Monitor for root changes

2. Servers **SHOULD**:
   - Check for roots capability before usage
   - Handle root list changes gracefully
   - Respect root boundaries in operations
   - Cache root information appropriately

--- END OF FILE client/roots.mdx ---


--- START OF FILE client/sampling.mdx ---
---
title: Sampling
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) provides a standardized way for servers to request LLM
sampling ("completions" or "generations") from language models via clients. This flow
allows clients to maintain control over model access, selection, and permissions while
enabling servers to leverage AI capabilities&mdash;with no server API keys necessary.
Servers can request text, audio, or image-based interactions and optionally include
context from MCP servers in their prompts.

## User Interaction Model

Sampling in MCP allows servers to implement agentic behaviors, by enabling LLM calls to
occur _nested_ inside other MCP server features.

Implementations are free to expose sampling through any interface pattern that suits
their needs&mdash;the protocol itself does not mandate any specific user interaction
model.

<Warning>

For trust & safety and security, there **SHOULD** always
be a human in the loop with the ability to deny sampling requests.

Applications **SHOULD**:

- Provide UI that makes it easy and intuitive to review sampling requests
- Allow users to view and edit prompts before sending
- Present generated responses for review before delivery

</Warning>

## Capabilities

Clients that support sampling **MUST** declare the `sampling` capability during
[initialization](/specification/draft/basic/lifecycle#initialization):

```json
{
  "capabilities": {
    "sampling": {}
  }
}
```

## Protocol Messages

### Creating Messages

To request a language model generation, servers send a `sampling/createMessage` request:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "What is the capital of France?"
        }
      }
    ],
    "modelPreferences": {
      "hints": [
        {
          "name": "claude-3-sonnet"
        }
      ],
      "intelligencePriority": 0.8,
      "speedPriority": 0.5
    },
    "systemPrompt": "You are a helpful assistant.",
    "maxTokens": 100
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "role": "assistant",
    "content": {
      "type": "text",
      "text": "The capital of France is Paris."
    },
    "model": "claude-3-sonnet-20240307",
    "stopReason": "endTurn"
  }
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant Server
    participant Client
    participant User
    participant LLM

    Note over Server,Client: Server initiates sampling
    Server->>Client: sampling/createMessage

    Note over Client,User: Human-in-the-loop review
    Client->>User: Present request for approval
    User-->>Client: Review and approve/modify

    Note over Client,LLM: Model interaction
    Client->>LLM: Forward approved request
    LLM-->>Client: Return generation

    Note over Client,User: Response review
    Client->>User: Present response for approval
    User-->>Client: Review and approve/modify

    Note over Server,Client: Complete request
    Client-->>Server: Return approved response
```

## Data Types

### Messages

Sampling messages can contain:

#### Text Content

```json
{
  "type": "text",
  "text": "The message content"
}
```

#### Image Content

```json
{
  "type": "image",
  "data": "base64-encoded-image-data",
  "mimeType": "image/jpeg"
}
```

#### Audio Content

```json
{
  "type": "audio",
  "data": "base64-encoded-audio-data",
  "mimeType": "audio/wav"
}
```

### Model Preferences

Model selection in MCP requires careful abstraction since servers and clients may use
different AI providers with distinct model offerings. A server cannot simply request a
specific model by name since the client may not have access to that exact model or may
prefer to use a different provider's equivalent model.

To solve this, MCP implements a preference system that combines abstract capability
priorities with optional model hints:

#### Capability Priorities

Servers express their needs through three normalized priority values (0-1):

- `costPriority`: How important is minimizing costs? Higher values prefer cheaper models.
- `speedPriority`: How important is low latency? Higher values prefer faster models.
- `intelligencePriority`: How important are advanced capabilities? Higher values prefer
  more capable models.

#### Model Hints

While priorities help select models based on characteristics, `hints` allow servers to
suggest specific models or model families:

- Hints are treated as substrings that can match model names flexibly
- Multiple hints are evaluated in order of preference
- Clients **MAY** map hints to equivalent models from different providers
- Hints are advisory&mdash;clients make final model selection

For example:

```json
{
  "hints": [
    { "name": "claude-3-sonnet" }, // Prefer Sonnet-class models
    { "name": "claude" } // Fall back to any Claude model
  ],
  "costPriority": 0.3, // Cost is less important
  "speedPriority": 0.8, // Speed is very important
  "intelligencePriority": 0.5 // Moderate capability needs
}
```

The client processes these preferences to select an appropriate model from its available
options. For instance, if the client doesn't have access to Claude models but has Gemini,
it might map the sonnet hint to `gemini-1.5-pro` based on similar capabilities.

## Error Handling

Clients **SHOULD** return errors for common failure cases:

Example error:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -1,
    "message": "User rejected sampling request"
  }
}
```

## Security Considerations

1. Clients **SHOULD** implement user approval controls
2. Both parties **SHOULD** validate message content
3. Clients **SHOULD** respect model preference hints
4. Clients **SHOULD** implement rate limiting
5. Both parties **MUST** handle sensitive data appropriately

--- END OF FILE client/sampling.mdx ---


--- START OF FILE server/utilities/completion.mdx ---
---
title: Completion
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) provides a standardized way for servers to offer
argument autocompletion suggestions for prompts and resource URIs. This enables rich,
IDE-like experiences where users receive contextual suggestions while entering argument
values.

## User Interaction Model

Completion in MCP is designed to support interactive user experiences similar to IDE code
completion.

For example, applications may show completion suggestions in a dropdown or popup menu as
users type, with the ability to filter and select from available options.

However, implementations are free to expose completion through any interface pattern that
suits their needs&mdash;the protocol itself does not mandate any specific user
interaction model.

## Capabilities

Servers that support completions **MUST** declare the `completions` capability:

```json
{
  "capabilities": {
    "completions": {}
  }
}
```

## Protocol Messages

### Requesting Completions

To get completion suggestions, clients send a `completion/complete` request specifying
what is being completed through a reference type:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "code_review"
    },
    "argument": {
      "name": "language",
      "value": "py"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "completion": {
      "values": ["python", "pytorch", "pyside"],
      "total": 10,
      "hasMore": true
    }
  }
}
```

For prompts or URI templates with multiple arguments, clients should include previous completions in the `context.arguments` object to provide context for subsequent requests.

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "completion/complete",
  "params": {
    "ref": {
      "type": "ref/prompt",
      "name": "code_review"
    },
    "argument": {
      "name": "framework",
      "value": "fla"
    },
    "context": {
      "arguments": {
        "language": "python"
      }
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "completion": {
      "values": ["flask"],
      "total": 1,
      "hasMore": false
    }
  }
}
```

### Reference Types

The protocol supports two types of completion references:

| Type           | Description                 | Example                                             |
| -------------- | --------------------------- | --------------------------------------------------- |
| `ref/prompt`   | References a prompt by name | `{"type": "ref/prompt", "name": "code_review"}`     |
| `ref/resource` | References a resource URI   | `{"type": "ref/resource", "uri": "file:///{path}"}` |

### Completion Results

Servers return an array of completion values ranked by relevance, with:

- Maximum 100 items per response
- Optional total number of available matches
- Boolean indicating if additional results exist

## Message Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Note over Client: User types argument
    Client->>Server: completion/complete
    Server-->>Client: Completion suggestions

    Note over Client: User continues typing
    Client->>Server: completion/complete
    Server-->>Client: Refined suggestions
```

## Data Types

### CompleteRequest

- `ref`: A `PromptReference` or `ResourceReference`
- `argument`: Object containing:
  - `name`: Argument name
  - `value`: Current value
- `context`: Object containing:
  - `arguments`: A mapping of already-resolved argument names to their values.

### CompleteResult

- `completion`: Object containing:
  - `values`: Array of suggestions (max 100)
  - `total`: Optional total matches
  - `hasMore`: Additional results flag

## Error Handling

Servers **SHOULD** return standard JSON-RPC errors for common failure cases:

- Method not found: `-32601` (Capability not supported)
- Invalid prompt name: `-32602` (Invalid params)
- Missing required arguments: `-32602` (Invalid params)
- Internal errors: `-32603` (Internal error)

## Implementation Considerations

1. Servers **SHOULD**:

   - Return suggestions sorted by relevance
   - Implement fuzzy matching where appropriate
   - Rate limit completion requests
   - Validate all inputs

2. Clients **SHOULD**:
   - Debounce rapid completion requests
   - Cache completion results where appropriate
   - Handle missing or partial results gracefully

## Security

Implementations **MUST**:

- Validate all completion inputs
- Implement appropriate rate limiting
- Control access to sensitive suggestions
- Prevent completion-based information disclosure

--- END OF FILE server/utilities/completion.mdx ---


--- START OF FILE server/utilities/logging.mdx ---
---
title: Logging
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) provides a standardized way for servers to send
structured log messages to clients. Clients can control logging verbosity by setting
minimum log levels, with servers sending notifications containing severity levels,
optional logger names, and arbitrary JSON-serializable data.

## User Interaction Model

Implementations are free to expose logging through any interface pattern that suits their
needs&mdash;the protocol itself does not mandate any specific user interaction model.

## Capabilities

Servers that emit log message notifications **MUST** declare the `logging` capability:

```json
{
  "capabilities": {
    "logging": {}
  }
}
```

## Log Levels

The protocol follows the standard syslog severity levels specified in
[RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424#section-6.2.1):

| Level     | Description                      | Example Use Case           |
| --------- | -------------------------------- | -------------------------- |
| debug     | Detailed debugging information   | Function entry/exit points |
| info      | General informational messages   | Operation progress updates |
| notice    | Normal but significant events    | Configuration changes      |
| warning   | Warning conditions               | Deprecated feature usage   |
| error     | Error conditions                 | Operation failures         |
| critical  | Critical conditions              | System component failures  |
| alert     | Action must be taken immediately | Data corruption detected   |
| emergency | System is unusable               | Complete system failure    |

## Protocol Messages

### Setting Log Level

To configure the minimum log level, clients **MAY** send a `logging/setLevel` request:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "logging/setLevel",
  "params": {
    "level": "info"
  }
}
```

### Log Message Notifications

Servers send log messages using `notifications/message` notifications:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/message",
  "params": {
    "level": "error",
    "logger": "database",
    "data": {
      "error": "Connection failed",
      "details": {
        "host": "localhost",
        "port": 5432
      }
    }
  }
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Note over Client,Server: Configure Logging
    Client->>Server: logging/setLevel (info)
    Server-->>Client: Empty Result

    Note over Client,Server: Server Activity
    Server--)Client: notifications/message (info)
    Server--)Client: notifications/message (warning)
    Server--)Client: notifications/message (error)

    Note over Client,Server: Level Change
    Client->>Server: logging/setLevel (error)
    Server-->>Client: Empty Result
    Note over Server: Only sends error level<br/>and above
```

## Error Handling

Servers **SHOULD** return standard JSON-RPC errors for common failure cases:

- Invalid log level: `-32602` (Invalid params)
- Configuration errors: `-32603` (Internal error)

## Implementation Considerations

1. Servers **SHOULD**:

   - Rate limit log messages
   - Include relevant context in data field
   - Use consistent logger names
   - Remove sensitive information

2. Clients **MAY**:
   - Present log messages in the UI
   - Implement log filtering/search
   - Display severity visually
   - Persist log messages

## Security

1. Log messages **MUST NOT** contain:

   - Credentials or secrets
   - Personal identifying information
   - Internal system details that could aid attacks

2. Implementations **SHOULD**:
   - Rate limit messages
   - Validate all data fields
   - Control log access
   - Monitor for sensitive content

--- END OF FILE server/utilities/logging.mdx ---


--- START OF FILE server/utilities/pagination.mdx ---
---
title: Pagination
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) supports paginating list operations that may return
large result sets. Pagination allows servers to yield results in smaller chunks rather
than all at once.

Pagination is especially important when connecting to external services over the
internet, but also useful for local integrations to avoid performance issues with large
data sets.

## Pagination Model

Pagination in MCP uses an opaque cursor-based approach, instead of numbered pages.

- The **cursor** is an opaque string token, representing a position in the result set
- **Page size** is determined by the server, and clients **MUST NOT** assume a fixed page
  size

## Response Format

Pagination starts when the server sends a **response** that includes:

- The current page of results
- An optional `nextCursor` field if more results exist

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "result": {
    "resources": [...],
    "nextCursor": "eyJwYWdlIjogM30="
  }
}
```

## Request Format

After receiving a cursor, the client can _continue_ paginating by issuing a request
including that cursor:

```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "params": {
    "cursor": "eyJwYWdlIjogMn0="
  }
}
```

## Pagination Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Client->>Server: List Request (no cursor)
    loop Pagination Loop
      Server-->>Client: Page of results + nextCursor
      Client->>Server: List Request (with cursor)
    end
```

## Operations Supporting Pagination

The following MCP operations support pagination:

- `resources/list` - List available resources
- `resources/templates/list` - List resource templates
- `prompts/list` - List available prompts
- `tools/list` - List available tools

## Implementation Guidelines

1. Servers **SHOULD**:

   - Provide stable cursors
   - Handle invalid cursors gracefully

2. Clients **SHOULD**:

   - Treat a missing `nextCursor` as the end of results
   - Support both paginated and non-paginated flows

3. Clients **MUST** treat cursors as opaque tokens:
   - Don't make assumptions about cursor format
   - Don't attempt to parse or modify cursors
   - Don't persist cursors across sessions

## Error Handling

Invalid cursors **SHOULD** result in an error with code -32602 (Invalid params).

--- END OF FILE server/utilities/pagination.mdx ---


--- START OF FILE server/index.mdx ---
---
title: Overview
---

<Info>**Protocol Revision**: draft</Info>

Servers provide the fundamental building blocks for adding context to language models via
MCP. These primitives enable rich interactions between clients, servers, and language
models:

- **Prompts**: Pre-defined templates or instructions that guide language model
  interactions
- **Resources**: Structured data or content that provides additional context to the model
- **Tools**: Executable functions that allow models to perform actions or retrieve
  information

Each primitive can be summarized in the following control hierarchy:

| Primitive | Control                | Description                                        | Example                         |
| --------- | ---------------------- | -------------------------------------------------- | ------------------------------- |
| Prompts   | User-controlled        | Interactive templates invoked by user choice       | Slash commands, menu options    |
| Resources | Application-controlled | Contextual data attached and managed by the client | File contents, git history      |
| Tools     | Model-controlled       | Functions exposed to the LLM to take actions       | API POST requests, file writing |

Explore these key primitives in more detail below:

<CardGroup cols={3}>
  <Card
    title="Prompts"
    icon="message"
    href="/specification/draft/server/prompts"
  />
  <Card
    title="Resources"
    icon="file-lines"
    href="/specification/draft/server/resources"
  />
  <Card title="Tools" icon="wrench" href="/specification/draft/server/tools" />
</CardGroup>

--- END OF FILE server/index.mdx ---


--- START OF FILE server/prompts.mdx ---
---
title: Prompts
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) provides a standardized way for servers to expose prompt
templates to clients. Prompts allow servers to provide structured messages and
instructions for interacting with language models. Clients can discover available
prompts, retrieve their contents, and provide arguments to customize them.

## User Interaction Model

Prompts are designed to be **user-controlled**, meaning they are exposed from servers to
clients with the intention of the user being able to explicitly select them for use.

Typically, prompts would be triggered through user-initiated commands in the user
interface, which allows users to naturally discover and invoke available prompts.

For example, as slash commands:

![Example of prompt exposed as slash command](/specification/draft/server/slash-command.png)

However, implementors are free to expose prompts through any interface pattern that suits
their needs&mdash;the protocol itself does not mandate any specific user interaction
model.

## Capabilities

Servers that support prompts **MUST** declare the `prompts` capability during
[initialization](/specification/draft/basic/lifecycle#initialization):

```json
{
  "capabilities": {
    "prompts": {
      "listChanged": true
    }
  }
}
```

`listChanged` indicates whether the server will emit notifications when the list of
available prompts changes.

## Protocol Messages

### Listing Prompts

To retrieve available prompts, clients send a `prompts/list` request. This operation
supports [pagination](/specification/draft/server/utilities/pagination).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "prompts/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "prompts": [
      {
        "name": "code_review",
        "title": "Request Code Review",
        "description": "Asks the LLM to analyze code quality and suggest improvements",
        "arguments": [
          {
            "name": "code",
            "description": "The code to review",
            "required": true
          }
        ]
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

### Getting a Prompt

To retrieve a specific prompt, clients send a `prompts/get` request. Arguments may be
auto-completed through [the completion API](/specification/draft/server/utilities/completion).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code": "def hello():\n    print('world')"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "description": "Code review prompt",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "Please review this Python code:\ndef hello():\n    print('world')"
        }
      }
    ]
  }
}
```

### List Changed Notification

When the list of available prompts changes, servers that declared the `listChanged`
capability **SHOULD** send a notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/prompts/list_changed"
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Note over Client,Server: Discovery
    Client->>Server: prompts/list
    Server-->>Client: List of prompts

    Note over Client,Server: Usage
    Client->>Server: prompts/get
    Server-->>Client: Prompt content

    opt listChanged
      Note over Client,Server: Changes
      Server--)Client: prompts/list_changed
      Client->>Server: prompts/list
      Server-->>Client: Updated prompts
    end
```

## Data Types

### Prompt

A prompt definition includes:

- `name`: Unique identifier for the prompt
- `title`: Optional human-readable name of the prompt for display purposes.
- `description`: Optional human-readable description
- `arguments`: Optional list of arguments for customization

### PromptMessage

Messages in a prompt can contain:

- `role`: Either "user" or "assistant" to indicate the speaker
- `content`: One of the following content types:

#### Text Content

Text content represents plain text messages:

```json
{
  "type": "text",
  "text": "The text content of the message"
}
```

This is the most common content type used for natural language interactions.

#### Image Content

Image content allows including visual information in messages:

```json
{
  "type": "image",
  "data": "base64-encoded-image-data",
  "mimeType": "image/png"
}
```

The image data **MUST** be base64-encoded and include a valid MIME type. This enables
multi-modal interactions where visual context is important.

#### Audio Content

Audio content allows including audio information in messages:

```json
{
  "type": "audio",
  "data": "base64-encoded-audio-data",
  "mimeType": "audio/wav"
}
```

The audio data MUST be base64-encoded and include a valid MIME type. This enables
multi-modal interactions where audio context is important.

#### Embedded Resources

Embedded resources allow referencing server-side resources directly in messages:

```json
{
  "type": "resource",
  "resource": {
    "uri": "resource://example",
    "name": "example",
    "title": "My Example Resource",
    "mimeType": "text/plain",
    "text": "Resource content"
  }
}
```

Resources can contain either text or binary (blob) data and **MUST** include:

- A valid resource URI
- The appropriate MIME type
- Either text content or base64-encoded blob data

Embedded resources enable prompts to seamlessly incorporate server-managed content like
documentation, code samples, or other reference materials directly into the conversation
flow.

## Error Handling

Servers **SHOULD** return standard JSON-RPC errors for common failure cases:

- Invalid prompt name: `-32602` (Invalid params)
- Missing required arguments: `-32602` (Invalid params)
- Internal errors: `-32603` (Internal error)

## Implementation Considerations

1. Servers **SHOULD** validate prompt arguments before processing
2. Clients **SHOULD** handle pagination for large prompt lists
3. Both parties **SHOULD** respect capability negotiation

## Security

Implementations **MUST** carefully validate all prompt inputs and outputs to prevent
injection attacks or unauthorized access to resources.

--- END OF FILE server/prompts.mdx ---


--- START OF FILE server/resource-picker.png ---
�PNG

   
IHDR   �   �   �Ķ  `iCCPICC Profile  (�u�;HA��h$D��H!Q�*���rF,� XQ��K��d�w������6bci��B҉��"��B4���z�������0��3� �%�g�	ium]�!
?n���.P	�����z7&fͤcR�rp68$o��?����x�����~P�t�m���;6|H��`����-�5k�2I�{�^�r��đl�o�q��ֿv���E�0�0R�ä��
�P ӟ"�?}J�/�2�����	�¤��Q��qD�eLR*�޿��zG������%P��׮7z\7L���u=u���[�@ϛ㼎 �K�����q�@�#P�|.La�vY'   beXIfMM *           �i       &     ��       P�       ��       �    ASCII   Screenshot9UD  =iTXtXML:com.adobe.xmp     <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 6.0.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/">
         <exif:PixelYDimension>181</exif:PixelYDimension>
         <exif:UserComment>Screenshot</exif:UserComment>
         <exif:PixelXDimension>174</exif:PixelXDimension>
         <tiff:Orientation>1</tiff:Orientation>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
oP�=  3HIDATx�}�ՑnMM�fA(�0BFH"�dl����omd���9�. �k�g>{�k�
�Ȁ�������m�EAH��r�H3�h�h�����ܾ}c���#���Vש:u�ԩS]}�oߢ��S�Q�r�X�e��1��ޑ�ED�,�_�RQ� ���W�Hzd�L,P,N+�?2����x"���i%�f
��P�^]]M���
�������B�w�*%+��f�L�� w��i:]}�Uq�oXO�>�;���[iz�4���w��C@��;��.�[�>k�����O���h��IT\TL}�i�կ~� ����������6嗿�5=��v9眳隫��;v��I��7��-����6۠cA���
Z�N���k���E���
�暫h������~''��UW�O�s�R�-i�%���!���XW\~-�Ń��~��w�����|9mݶ=��1c�ҋ/�H+V����ڽ�=��ȑ#�c[L_������>!���]K睷� w̘1��֛�/~��=��@!�n��Ϊ�*8�)=D��pЛn��+�N#z�
"<�z.�.��Wn�5k�ҵ<�C��uz0n�XZ��
zs��J��G��]D]]�B�|,�����r
}��R�?����N+J�+.���K�������4o�\ڶm��� ;w���=W��w�Fw��}���o�)�N��o�I<���%�L�:E���H;/�����������/|������8p��m JF�l�9.�ٹnΚ(^SSM�����d�-r�WG������b֑�D�_��ujDeԟw޹�U��A�m`���ӧ�/���x�v[���aÆ���_K����y��s�Cs�̦q��q���z0�����.����|{��}������	/�8Ϗ|/=������>��O�m�1�A��4o�<q�W^y��{�o4��VUEXTp�9s���ɓ%y���i5/�k�����hϞ�4f�h�����{~(i����yA\�����`>n��K��3�R'�;ХX�)��c��xH"ڦ+�~|pz8
"3rT�!��O��)?����Z���A�~�C���|�
G���4����O[�DWg-�?�>��%t���"Q�bagjg��G�*��K_���8���}ｒ�x�
ڷo��!Ү]�V�#��������}��~{mٲ�^}M�6U�Q�Z�����#nٺ��0�y�fB�EyGd8<���_�	N�h-|̜ٔ���&�eBH���M%W`ĆJ��d#
�~��BM/� t�u�c��h���N�o_��:�`���Q>]#����K�����-{���ɷ���/���.ਸ��.�����f��ߡ/�k4��s��.��|����>"�|��I�"���ΦM�h�"�*��JKJ��HwO�fc�ĉt�I'�%l��Ŵu�6�%�}���qMP��9Xja师�,�7ǵ��T�������:/�׭[*��Q4Sm��p|��9��D?ɑc��䰛�wtt�i��~���i,粋���� ���bp¦3�Z��#䊽���^|�%z�����q�x�ɿP
絼-�Q��?��ښZz�h�����>v���ڵ�Q�v^uZЂwWsXd��s� �%��%+��~FBJ�
N�M�#k�v���3�ſ��/��n��tE�)w��E��+n\��?��*++]�]�v'��r�g�R���ߖS	_��WH�0~�I�446����� 4�i��/��ظ�˦�A]�a9-����l ��,�=F��g�u
^8N�p�d�#"2����ԡ�tੜ�6]��.*���I�N�Yg��N*Ҁ3N�h��;��u�2�Tj�s\�O�۽8mF�ZerRGOw7����d�@�fϞ�g�9�=§��謳Β(б�>�,�ӓO
;��Q���b�t�x�'j�����q:����i��y�mh�oWK���2�~�@�7UQ�i�wW�DZ�����]����	mW�pP@���-�ַ�{�q�%�б"Z������<���s�%�!���U�ptе�қ�7��Q�r
>w��W�����|��v~9..~&L�@��=���k���/�V��|>u�:�����g-_P������r�f�F�pn����0o�!ո��2i�Dzoo���H
�td7����>��X�҅.�?>�ȯ���?B�G�f�C6l���z/�u�8y����@�nlh���p.��R:�ǈvm�?Ҙ��r��wH�{�<�S��g��}�f�~8+\v��4m�T�����ڪ�����PGGx�EMM�tl'MM�%���apX��ξ!�Ӣw����|	�t�S��#���M�L��c����U��m���(�U:���QT"[]�<I��>���$nAba�p ik��,�ZQQɻ�O��#G����N����o]m$]`�����F�*�� Y�}V���q�����W�FL�?��}6��%�P�L���#Y��luN���o#�)��r�`���?~��Q>R�ĵ@B����r\l�`��?
�'����=9���FV�\�;k�@�Mf�4r����W��� N���틻s�.�`Z 7�8��33�gqq0*���r�Qn.������w0g,�[,P�h+NčǙǢ��?�x�8��i�A�i�49.TK�};�A��r\�YWo�9����츩s[?zo�Q�h��/�O8�E.��<��O'��DZ���c��?ŏ��ѷ�Dh�W#k6�0?N��+g�T�@2�����q�r�d��&�=F���hKK�\���D(d��������8��}��^?��*++�������b�]�@D^��o^��&m���NpG�σܧ�D��$��ǋ�䆅�_�(����T�[S�~���e�xy���<�$yBY��y\�7��f!9D�p�
�e���Z�;W���>ŮC��V0�
��D���Y���]�����N��B CP�a됻l����d#e";��S(9��>�a��d����`d��� i�'t��i�TtD\�����&�D8��g����Oz;X���,�N�Qm7!#�����qZs!fG\G�����ZtE��F0SX��܄C"���A��-���;��,_��k~̫�4
��Q�-Ǖ�Df$��]L�E���� �Ԩ7%�7�Q��⢠S�uʥx&<ٴ�����������LxT����]n�W̥zf�sjct��X�$�������ǤaA�X�x|�Kn
6�9r�d/7�>.{B'�r�?��t	�֐|�
0��.�C Hqګ��99'-^�^e6ӂ�xTF&<f����r���MR�,Ƥ2��7�>��x���&�ѹ89>DyŅb>�
9�IWk�?����JJ�0�G�L:�f�/ Q	b�R���M�Dlؠ0���R�&�h����
���ܛ���?�h��+'������[�����渐e���KPbA�JCnB����$��J�x,��a�09.7:���L@�����E����������<!+T�!'�����ar\g|�8�@6x�sS��9�~�|o��GWKh�T�ɵ�!#׾O�vy�qu�`�xW�H�.�B��,Y,:�0d�Ԩ� 0}<2��/�H�%���+2�4a���������,z��JMCF�Nh����L��q3���"���3Xx�	=����ͳ
���Gs7Vр�������!˲3-?E��(=���uţ�d�o�9���B� �8~�e�
��Hן΍/�ƺڼLJG}:�dt��������D�\��g�Q�-�o���g�,Nׯ�{n�B8�Q$O::�O�8_�}W�N���Ul���&��Qv��g��__B�^r)-�����/�I�C�2��3�I�GT���'��B�y��;�ivXr���[L���gM�E?˖-������aGC��?��A:�p��Œ�z��ҥK%£%.�uN^}��E���}\���8t1���|�!���y�v�9s���e���l�Q7����
�����]��2����z�QC��>��
��������{6\�i"L9����t4�����#��촜�"� �"ǽ�����9?)$C�Cy��5�����y5���i莣�QOZp����EZ8�uѝ8-緈���D�0�}X�A�	���;�b $H���z��<�}9�;���NΘ����W�5g�ۑv�㴈�ϝiﻟ�s�k�t��'����Y��>S\��q�mm>�}9�V{['G�4߀0}�-�f�1�r ��JN�M8��ϑv�w�ҪU��8#��s�tcJ��(�����{qm��K����Ǚ����j�#�#.Jl�6(.aP�50 ���V� �E���i���-���q����^c����:"��@�}\]&�dM��Vh�����\N0QW�Z��n�]�:i���KgȱKظ-�=����z��m�s`��6v�W���_���Xe��Oև���J&C�Q�9n�X�� �w� !;>�rziy���������@�ȑ�������P�&G<Ž�K�+����S����:��s�﷿�mN~�]������6a����+^N	��AE�k/�+����EMM�8F!L���aMu5�w�Y�& ҢHf<�=�%�z\B��*�n`r56���)Kw<ru\َ)��>r�f����À5�U�;.ƅ"�.CI�&��"��q�YC����F���1TQ5���o�:���<.��.�|a�an8쓯�æTN-�L�{a0��V���ε�p�$�8�HQ����A�ʲ�Ök��~���o���Ǖ�گ��`S�T|X�0��d�ʬ+&>�*�B�[u4��gz��ϱ��z�y��Q���&N_[�}̼��kZɳ�cP(�X�L�5���s��<��� 
��u��W�C���ぐk���8��NNd
B_w�8+� q��z+���$�"*A,`�,���<�͌.���'Ӭ@��N���@�8����]��j:]D��<�+�mV�(��6�(�x���f*W�i_^\�>��Q�d}{r\g@�Z�s�4Pq/L�K���U�A�W"��ޚ0q�65��O�]ω3B|�b1��H)1'1r
�P�x��*��Im��%�X�����jx�i�*��mk��sf�*U%w��AP�����Ag-�$�鎡��;V>?�J�� �Wl~�m\����ܯ���۸걗8J&<�3������Ǔ�7��
c�a��.͘	ax6�R�����K��<������*�p�>���8���yp��t2��3�#S�X&��v2i�� �
C�ĲL��1�x)�x&|���K���,��
ۙV�q���v�n.��v C!X ��qӍ*vN��l��VQm�Y@��E|5��� ��z�����G��~��������Ǖ�V�+ɽ�h���K{���;U%b��#�7����j�j��j�WTp��G�R?.���Im�������3^nW��n,��а�g�D\�}C9#qx
��m�
�13���@#F�Soo��wRwO���rc"<�[^VFUê��!���Ct����Xf�ŗe ��Сk�Пǭ�����r;v4�tj�8�:+�5i��%�Ŵg�>v|���@��9�ϒ5[N+�+h��qt�����a7¦3���i���,#�~#~�z��K���|�ϡ�� ���q��8l�KW\����c8�vw�1ۂ6h;v�(G#[��Pk���<����=L��S�Ú���Y�u�A�@�]�8����ќ�V��yG����Wr^!���m�hcX�={��<.b��=�5���-��ؾ}|���B�ZZZ�݆�B��myVA#n���g>s��"n�
��j���+��5�^�ڵ{/�x��8��sΤ�ƍ�G{"�s؉��V�m���o�Yq�d��bv�L�*������7�C�5"r��
���pڹg��:/�u+^]�ӂd7bѢ��m7��G��Y@����S��~p7�ͣΟw^(z��QC��e���2������V(����(��6�2�Y�uZ���[��o�������,, ������gS1��=?�ۑ`��g�?z�9n���,�#�j�Vԍ�i��o ��%x��'�D����___o3�ӿ�|3N�t�=�g3p�X�/��"���@��s\^���d1��H������8�y�9n
��-7�_ޣ΋��n~�Lw#��y.�ZQ��h�����[�������Mu�9�y=l��5bD��`8.�G�8/G^L(�����T�n���%����,� 8h�+��G�9���t'�Mk;���r^<�0e��us� �֯x#�'<x��o~M���Bw#.�Չ�� ����g"�F���k��:߈�-/��N�Ǡ%+g�uN2RT���T�n���8罛�#/����?6�3x��J��q�0�jV�F^ŽЗ�M5�*lE���ڎ��Q
��w�V��Ϋ�
k���/����<X�D�[0ɒ6�G^3ϩ�ߨ��^?I�^���q��B\N��+�
�g��#�j9x���y?7`��b��
T[[PR�<h�����Y���u�Mk����9P��	����q|��}g�6zyyi�����sR!]@X�R:;;�nWYi)����n
%�O8-��x�m_μQę�H����apR������wŊ���Ͽi��9��|A�Fq\,���ERWW������Ћ���
�TR\����i'L<���۩�~8K�JPd��G�w��?�O/����3�Rͷw�s�%�"���b`��y#9�9�Ñ2t�����i���W�Ϛ5K�v����3��q\3����G�+^��Ἑο���?��Ï��Tq�p<�x��a�ӏ9B����(�f�x����#�D�V��G�����"/;�D\xn��_���2ǎN�u¹8�|�F}����������DN�iV�\�>-���{]�ʧ��p�=�3je9��O�Q����>�Y���q��q�1���8���7�G���n�y�]wG͈A�Ü�q�W�˼o�m����C~��w�SϿ8�o;�Jw�qU9KYq<OEW��PՊ��Z@�;��O��g�g��?�#�\���O{�Ι�n���(Wz��OJ7�F�C�p�Rޢ�ve/oSb{��{#2pD\\�`g���W�C�q;4�21��L�-�G�JkuFu�
~!�j;�� �-������'�7��6YN��
M����v�ce��4+(^hKHE���ǀZ N����f�h�?D^L�w��t����<�`�d���$#3�iiV�i[������� �N
�Q=�s\�=ֈ��;8(�F\㜈���P#��^�HW�ԕ�����.�gu:�G�:��=V�l�;S�<���mV� W�k�8`�r�S-������q�Gܓ�"��+IO9��j�Md;ߙ�;����QqR�r��ڊ�"-w\�EC��6�x��r\�l��IqI�%(>dg,R\,t���yTFw��� <��!m�8��\�?��8������T�69ᬤ�ur['��H�,��7�����x�q���?I��s\�,.r5���k0:�Ee�Z �?������縺��F\'v����z���=��;o'����7��&��g���}s\^'�Z�yaJ�Qu栴�<�e���-�g;ߙ�{r\d��Eq/T.o=:EQ��9����$��:2MQ�jF3ah̛��1��;�*8ΠNaC5�c�+�GG�҃B�B�v�p��m���}b����
����cSu�@ץ* ru:o���;g~L�S����Z7���q��C��?� �
�Ÿ���8� ����ן��>�z��MCB_qԐ�+��$��4�5��x����Q��H<��K�T&i���:�B
��;CV3����F���������Z���w>\�<==ր;u�x�\������;�QGW�w�Zںiˮ6���~�jHv�k��f��w�^��7-x�Qgwu���|<��/��<��Gڐ���N�����H�st�S�O�q��x4�����ϡ1�ɐ.��Th����Ap凾�����VӺ��,�e~�E��-9�ڏ��?{��_���'�V&�W.�(8>^Y�L?|x
:�C#�W��[ϣ)'�S[g}�g�ѳ��ފ����x}𲩴|����^��t���|���#W6��t�����^�0��e!�zR��v�n��
ں�|�����_�D�f�+�1��/_�6Hޒ��{�
�w"���&ƚO�
q3��vfW�
&	]ze
���ы��x�{���}p����.�?�>{��3}$;q�^����ⴥ%��`�C����k�y�aw4~i;ճ��[���?�#z����g�E�`��d��?�@^{�Y��H����������>���+�k1E��`'=��&^�E���,N;w�h�����Vӽ�YK+�5}0짱�5�d1��$:��W�^������-�+WQ�O�Ŋ�`��}�)|ͦ�8����h2�=sUU�ѿ�������\�����5��0Gֲ2^Q�j�\0�>�x=��V���_�g^�E���l��Kۤ���
ǟ�Qs��fzb�6��qB��?x��T_SF�-��8�'�W��l��߶q�~��zu�������zs�A��o�<��ӗôz��=�qP쇈�y	2�0c���r��p�k(�JW�e�G�։�����DUfvS�dߠ~/�:�z�˞��f�w�_I;�!D0��������4v>D����NK���]�̜2\�o�d^ȇ�v��.7�}������Ά��4�F����`�O���u�4}B�țz�y�*ro��?�[IX�U��|�i�1亃e?�C�����U�;^j�偮B��K8+Ѷ��zM�s�6���_&9�m���'6�)y������b��Z�a?]:b<=��nj=�-N=�x�o_H5��W�9���������|ч2�|��&
�oAt������N|�D�︄&���/��胋�����3��_���0�[��L���\pcit��� ��F>1������g>�r�3g�t�,�r��賛�?y�~��z�Ļ�=��ފn6��l ����ΟD�<�����iG����/��ǯ>�f8�"��L&�8�]{�����y�w$~a�^��=�(����b/U"6?�Q��!�źP�7+.W��ر�"
'��p0 �Wo:��}�kre��{�sg��]�@�:�{�//����)�����W3��"3��4Sw�>��������/+v����M���4ze�q:��h)�M.�����m���8��B�F���?�d����`��������l?�i��
���F��+n�.?uz�P��Zɹ�_��a:c���T����G:�ҁC�PWE�U��K�N�����}4zD�DHIJ-z*�~����Ө�՜&�B���r��F���Y9��\��
\�����>�A�$��J��}�;[����CMm�c�qD��ي�b�-�ǫ*�y'�F���{��F��Mt�F?��eLC��0���%����J���H��~�Y&�������r\6]v�]�Z��XIJ��$0爣w�VsQ1�cs ��=�V��X���r\�$r(��[i�t6Xc�B���W�
��WKX��8���'��lL��
��'�����y��
����x"'Kx��PMRH���M��=��GO5#I�o .���/l{��
1y	9�BY�ŵ]}K���±q0��Q
�>q'Jg����qC�P�0�؈��2�~��Z�ܨ��F6�x�⹩����Y�p����j�^�ZŜ�lhn+y/�'(����,q�1�۟�n,Y��p�|��iO:���מ���B��H?��".`�S��C�+	�,��+��>�d��H�k
9fxB��O�7�>.k):�ޟ��f*.(��Y-���;��C��{���VB"Nb�u��!]��`�Å.,
�j�Gp(ف�
3h�Q�3<�q���Y*��a�I��-s��q�3��a���U����C�EW�}�����/v����N`QrP�����820������l{
�}x�d�B��e|@�yr\�spF�r��toč�<��
��ja�/�Зnx`Dw&�cr����E�U6�����r\�4g� �E��Ņb>�Nq�ˊ�c�"��R�q��u���3��\�_���>���N�9�nąs�%Mua��rL���"݇7�a�m��*B���$벢�
Y
�4�W�v��A�<�2O��eb»��9�ܐ[�{P��dW�� U���M�I�/��>T�gf$6>�]��O�ޓ�c����s�p��s�h�n������6�Ѿ�����y5R�d������P�o�)��r*-����R���1^q2�'���[h~`�f�Q�9.\�%��0��2ǡ��ء 1�^v��#���F��TRZB��m`*�W*�,Ǩ�������N\F�U5�W��[�Ca���g�~����s�|�45���BÏ�纺:�P�~~c���Ruu
���qDMW����]���!�_:��J=�T];�e��S����ޙ�XN�
��q��].�9[����θ��h���p��QL���A������i[쥺�j1�����V��&��r����n��ʨ�� �۳�F�Oe⼅1�ب��yC�
0��#Y���9��0	f�Ŏ���8�Mc�Zh8Vfoo'�4�����ШQch��1���C�[[WǲFӰ�rڷ{;Ga�F�B��>p:Pr��T�݈�����D�\q�(;Ī���2���&�PH�Qv��{wSͰa4r�(����yn<�4���F��]�wQgG�
�n�I�'4?H�_\�+�l�E�3����JI�,��ݬh��&����*x�A���C�|�-�ӻ;��loo/߲�WH��x**L�
zG{;�3�u.'���DcC#m߹�y�=c�?�9��'�3O�̹�	����bH�H�+��Υ���ZK�����>�KK=5���8PQ�} ��|A�s�Vj^G���dЎz�����c;^�+xf��1��/���~�6l�@---TSSM3f�Fg�9�,N�	���j�d���n��a^�WE�=� �0��1~�u���3��=��<B7�� ��+��kĕ��s��eRz��}r����D�E�A�5�
�KG�����B������[i�[o����fjhl������A�g͢�~��ny�N7�֬y�֯[O�9�=��mQ�K��s���N���g�lg~Ǘ����n��s�8�p�M�������iB�<(���Ӥ���)x]o�_�v
͚}6�>9��\�:�9w�\�� �<�_����k��͸YS-���]@3gΤu��ѓO>Is�Υ3�<�w�����6mz��O�Ns�=��vp�-� �p�۾c�7��Ga�P�,ؘ����x����:��?�帆�p_�x1<#:4���8 W|�����W��G�����pG9�C:S0�t��8���\�J<�����)S��)���3~ؤ�&N� ��Iݽ{7Mc�mim��W�����=����"����!�~����+uȃ0~���?��r� a�b��0)o���W��(�8f8|�����?���kjiܸSX��^�S�[�|��ù0Q�Z��xX��͟T�W]w�u�6�{؉�*���kr�b޼y>��}���[��߉s�!�-q� �w���s�8mܸA�2��a��A����>.[�W�>��_��z�٧8:��L��[��x0;��� NGN��?����.�6o�$<��>�����G۷mK����n�{9o�����gϮ��sOѲ�~�h|����quq�E�p�	���6N�i6�,�&r�w~�[��_vŕ|:E5�u���bWEUu !�uh㼴���/�pєX�#;�&�c���҆�%ڎ;��S襉�&�ԩSyPbIW�Ѿ>v�4~©�9�a�(�@C<H��#m������$��P(�|gҾh��
��q��
/�ޱ�Ƈ>��2�o@�8ܯ��755�E]D��~:���$<M5�[?��L�y�`�xNg|JGם;wҪ�+Y�Yt꩓��z+v֮������qq1����ሎ�oQ1~��X�|��*ly�ݻ��|�Mz���4��A���EM��%!
�
��Ώ���R^�`�L�r*}��_�S}հ���CD��ZRR*�^HZ[[y[m
}�/�����D���be���ꮝ�h��-t�y?�:���v�9��	�Y��xZl׮�����ü�r��5����a:���:����~z/縷H�ll)[_�a>�]]������uo��իN(��t��dԨ��Ż��>^�?��=K�y����`|'l떭t������JX�]���D��
�={v��U��'��_ ��v��OJo�ڪ)���&�|���<�
�����l�L�|�#����K��{qA���f��"8p���ٴ�}����#���_�L'�D���U`��*�������Sg쉨d�������Orag��/�'�e;��뼯�W.���o�m۶�3|������Ԟ8ǩ�\K3>wW!,�)�G�I�ÿs���JH�1���!���'�r���������s�=������
���;sHR�D+���c:��&�ʠ�u��������b���Ώ�EŘԜ�2��y�+S����Up���*�9�ǽ�rN̣�ncz�A\�Z�����>.ŝ��
�[�f�bs�f.���#'{����0�Gd'�����AbDq�t�=��qq� �  A���h6�0��:�u�8e�����$�Fv`��ną�aH��8\곣��'l

�����E\�Fxd��y������A3h0    IEND�B`�
--- END OF FILE server/resource-picker.png ---


--- START OF FILE server/resources.mdx ---
---
title: Resources
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) provides a standardized way for servers to expose
resources to clients. Resources allow servers to share data that provides context to
language models, such as files, database schemas, or application-specific information.
Each resource is uniquely identified by a
[URI](https://datatracker.ietf.org/doc/html/rfc3986).

## User Interaction Model

Resources in MCP are designed to be **application-driven**, with host applications
determining how to incorporate context based on their needs.

For example, applications could:

- Expose resources through UI elements for explicit selection, in a tree or list view
- Allow the user to search through and filter available resources
- Implement automatic context inclusion, based on heuristics or the AI model's selection

![Example of resource context picker](/specification/draft/server/resource-picker.png)

However, implementations are free to expose resources through any interface pattern that
suits their needs&mdash;the protocol itself does not mandate any specific user
interaction model.

## Capabilities

Servers that support resources **MUST** declare the `resources` capability:

```json
{
  "capabilities": {
    "resources": {
      "subscribe": true,
      "listChanged": true
    }
  }
}
```

The capability supports two optional features:

- `subscribe`: whether the client can subscribe to be notified of changes to individual
  resources.
- `listChanged`: whether the server will emit notifications when the list of available
  resources changes.

Both `subscribe` and `listChanged` are optional&mdash;servers can support neither,
either, or both:

```json
{
  "capabilities": {
    "resources": {} // Neither feature supported
  }
}
```

```json
{
  "capabilities": {
    "resources": {
      "subscribe": true // Only subscriptions supported
    }
  }
}
```

```json
{
  "capabilities": {
    "resources": {
      "listChanged": true // Only list change notifications supported
    }
  }
}
```

## Protocol Messages

### Listing Resources

To discover available resources, clients send a `resources/list` request. This operation
supports [pagination](/specification/draft/server/utilities/pagination).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resources": [
      {
        "uri": "file:///project/src/main.rs",
        "name": "main.rs",
        "title": "Rust Software Application Main File",
        "description": "Primary application entry point",
        "mimeType": "text/x-rust"
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

### Reading Resources

To retrieve resource contents, clients send a `resources/read` request:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "resources/read",
  "params": {
    "uri": "file:///project/src/main.rs"
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "contents": [
      {
        "uri": "file:///project/src/main.rs",
        "name": "main.rs",
        "title": "Rust Software Application Main File",
        "mimeType": "text/x-rust",
        "text": "fn main() {\n    println!(\"Hello world!\");\n}"
      }
    ]
  }
}
```

### Resource Templates

Resource templates allow servers to expose parameterized resources using
[URI templates](https://datatracker.ietf.org/doc/html/rfc6570). Arguments may be
auto-completed through [the completion API](/specification/draft/server/utilities/completion).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/templates/list"
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "resourceTemplates": [
      {
        "uriTemplate": "file:///{path}",
        "name": "Project Files",
        "title": "📁 Project Files",
        "description": "Access files in the project directory",
        "mimeType": "application/octet-stream"
      }
    ]
  }
}
```

### List Changed Notification

When the list of available resources changes, servers that declared the `listChanged`
capability **SHOULD** send a notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/list_changed"
}
```

### Subscriptions

The protocol supports optional subscriptions to resource changes. Clients can subscribe
to specific resources and receive notifications when they change:

**Subscribe Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/subscribe",
  "params": {
    "uri": "file:///project/src/main.rs"
  }
}
```

**Update Notification:**

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "file:///project/src/main.rs",
    "title": "Rust Software Application Main File"
  }
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server

    Note over Client,Server: Resource Discovery
    Client->>Server: resources/list
    Server-->>Client: List of resources

    Note over Client,Server: Resource Access
    Client->>Server: resources/read
    Server-->>Client: Resource contents

    Note over Client,Server: Subscriptions
    Client->>Server: resources/subscribe
    Server-->>Client: Subscription confirmed

    Note over Client,Server: Updates
    Server--)Client: notifications/resources/updated
    Client->>Server: resources/read
    Server-->>Client: Updated contents
```

## Data Types

### Resource

A resource definition includes:

- `uri`: Unique identifier for the resource
- `name`: The name of the resource.
- `title`: Optional human-readable name of the resource for display purposes.
- `description`: Optional description
- `mimeType`: Optional MIME type
- `size`: Optional size in bytes

### Resource Contents

Resources can contain either text or binary data:

#### Text Content

```json
{
  "uri": "file:///example.txt",
  "name": "example.txt",
  "title": "Example Text File",
  "mimeType": "text/plain",
  "text": "Resource content"
}
```

#### Binary Content

```json
{
  "uri": "file:///example.png",
  "name": "example.png",
  "title": "Example Image",
  "mimeType": "image/png",
  "blob": "base64-encoded-data"
}
```

## Common URI Schemes

The protocol defines several standard URI schemes. This list not
exhaustive&mdash;implementations are always free to use additional, custom URI schemes.

### https://

Used to represent a resource available on the web.

Servers **SHOULD** use this scheme only when the client is able to fetch and load the
resource directly from the web on its own—that is, it doesn’t need to read the resource
via the MCP server.

For other use cases, servers **SHOULD** prefer to use another URI scheme, or define a
custom one, even if the server will itself be downloading resource contents over the
internet.

### file://

Used to identify resources that behave like a filesystem. However, the resources do not
need to map to an actual physical filesystem.

MCP servers **MAY** identify file:// resources with an
[XDG MIME type](https://specifications.freedesktop.org/shared-mime-info-spec/0.14/ar01s02.html#id-1.3.14),
like `inode/directory`, to represent non-regular files (such as directories) that don’t
otherwise have a standard MIME type.

### git://

Git version control integration.

### Custom URI Schemes

Custom URI schemes **MUST** be in accordance with [RFC3986](https://datatracker.ietf.org/doc/html/rfc3986),
taking the above guidance in to account.

## Error Handling

Servers **SHOULD** return standard JSON-RPC errors for common failure cases:

- Resource not found: `-32002`
- Internal errors: `-32603`

Example error:

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "error": {
    "code": -32002,
    "message": "Resource not found",
    "data": {
      "uri": "file:///nonexistent.txt"
    }
  }
}
```

## Security Considerations

1. Servers **MUST** validate all resource URIs
2. Access controls **SHOULD** be implemented for sensitive resources
3. Binary data **MUST** be properly encoded
4. Resource permissions **SHOULD** be checked before operations

--- END OF FILE server/resources.mdx ---


--- START OF FILE server/slash-command.png ---
�PNG

   
IHDR  %   j   �Gz  ^iCCPICC Profile  (�u�;HA���h0�"����b$�6"�"XQ��es^�K\7'b���66������+E�O��
��EM������33��u�-�B��٤�������!��Og%�дy*�����#<R�G����i��W^��;#���-/�3J��r�qa�X۵��∠���%�u����s٭Y̤���,��+��l�o6q��a_;��Fqi����i�($��8T��O�>��Ka{؄�<lw��h��9�0�(q㔪���;6��;`f�`��%9p�t�4��# t
܎q]�?��T}��x��A��9�k/�j�q�O�vx����'�9aj�J�   DeXIfMM *           �i       &     �      %�       j    oI��  iTXtXML:com.adobe.xmp     <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 6.0.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/"
            xmlns:exif="http://ns.adobe.com/exif/1.0/">
         <tiff:Orientation>1</tiff:Orientation>
         <exif:PixelXDimension>293</exif:PixelXDimension>
         <exif:PixelYDimension>106</exif:PixelYDimension>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
l0�5  lIDATx�]	xUE�>Y YH����HXH�DDdw�Glhm�lu�F���vz>��v�[g[wT�%HXd�%a'+	[ !�Ad�_�.���Gܼ֗w���Wu�֭[�׽�=uN�[^W�^�N"��  Xo��C�!��B@HI.A@�BJ����  )�5 �B@H�R�!�!%�A�R)Y�;�2��  �$׀  X
!%Ku�TF���K! �d�������\�� `)��,�RA@���+��]��������^i� �PM�����[pS��ܴc�Y�@CE@H�����[pS��ܴc�Y�@CE@H�����[pS��ܴc�Y�@CE�头n�zJKK�1>�Ν�����#���p))���ӛo�C.�����YN��C�,���r���(.n��\p�Gv���p))�Z��Z�jE�^#$��5%/oo
n��i9�h��7����N��A@�>���bAA>�ر��1���n�}EE���l�¢+4tH�nm;�zܸ�4f�h���qZ��$��9Gv
��҆������Ə���G�PjJ7������5k��ˋ�B[)R�p�ĉ�c;v�@���F�իW())Emo���
��3(((��ޑ���m����p)�]������÷PJ��濼���m���Kt�:���G��Ggy���wc�y��*�K'�g��y�E���%��f����ѐ!�m�dC���KH)99�RSSi��+���VҼy��iS'Sn�eE>�>��&M�H�o؍���>�@�ɞ���_-WV���F���[o�KO>��h�
3��#�RZ�z�f�9|X9�O�F���)���ǗBBB�^t/���q�3H��w�k׮���_�FF�3gΪ]�Ut���������u-))���[i�ȑ��[���3� Oz�M{Qrr�:S�V-�qF9D�	��Q���m�F��y�8a�Ò��Z�f����iP�@5�i߾x�۷/a8&"��@�kJk؋֣{
w�l�vm��;�)���G����f>� -^�z�S(��� �VԪ����I�g�~�)H0t���H�/��]��N�Uu��O��kU� �A��URZ�j
������w;�����W��O��<5Iٞ:w�)S&Q�.]Ա��}�|��C����n�ԴT���ݻ���WϞl@oD˿����T6g	�3�O3�Ķ�  X�Z#����X�09|�PjҤ��V7o��G����5f$��iӦʹk��l�ER�y�t�G
yz�*# �����dC�6mJ�-xEM�<s���~�
σ��@���n&��2���9m|^�ez��͙�=��t�|q[�ҢE�WSv��i8EFFһ�i���
L'�S
*�+�A��Ԛ!f��uԖ��QQ�N[��_@׮]�ݻ��'O�|а2xz �f���`ʟ  x&��)�������9�M�6t��hժ����O�mM�е�kj�^9y�g+
�3�BZ-@�+;;��_��t����F}x�eHp0EDt�ƍ�\�+��AC�!Pk�RU���ۢ�k�����Ϝמ�����"�� `ꅔ��L>7�G��>rVA@p��ۓ��)N�������R�P:8�#�$M\����������4ɘC��|9O��o�/��}���F�'8C�4�2��


)??_y
�����'q:I�A��p[R���Ԅ�yR�/_��M�+)u��I*��[��&$���5�!5k֌?.�|��'�A�5�z��k�Y'�j2���lHxaW�N����F��HIkI@q=t��Ըq�j%
�@� ���7@��I�ڎڗ.]T3�KJJ�q9�  ��$%3!iRr�^^vv6]�X�%�o����*#�v�7��&#����>
!i$$���[��#�)Y��&�� �p+Rҍҡ&)�t	A���%)		Y����	!���dn4���@�A�mIɬ-���5�ya�%Z��Z������{����	��SU*������Z����o��ʡ5Λ�{��|���������'q�ܖ�ꪯN�<��>������y���PRR/
q���]'��8EV�<n۾����~��}�EE4�/������X.L��U����n9O�f�j7v��1:p���%�Ѓ�啕څ�%����"|���+ԡ}{�h]rb.�k��4o�
��	� ��R%���sK�|��`����1}��R%���l�"������|jZ����!YeoDE��lv�w!%'�BVV6�Z��RRR)_��.AH�������`���n�A6�R.�֡4u�$�ѽ��ҝ'c�����4���)==������x���G{��5
�ׯ/��I��K�\� ^��_?n�L���_A���
/�މW;�����4Z�r-��?}���;�4ns˖-l�>|�֭����s�a^�а0�ݫ�7nL9R�۲]��w�|6�����={�6뗨�x����凄���͠��vӱ��TXTHO?�k���Ͼ�ӧNy�ر�|���ϖ}�>�ݟ빉2�f�6�s
`�!��x�Fշ��A��3C9-O>1���y��bz����dFD��)�'ڤa$��[�"���g��{G��I'�f���������s�ԇ��6�1�`�F|,X�Тu�v�����
�R^�	￙%��t$EEE��;��	��9�b�<����bz��������ݯn�l&�!�Q@@ �8��Ã
��Um��C��P<���R�{��ԡC;^)8��;N%�%��KU�B�X��-Z��C|�C#X�7z�I�:LP�@&�(���_}���n�I-}3�?�Ҕ�oؤ�>8o�.᪨�Ǔ��y�����JH8D[�m�Aw�l3Fr�`Æ
��o�O^�����wR��Կ_�j+V�᥷�(�:t0�����{��!%%���A�O�:C���t<1���C��
���U�����ڂ���A���o#�G�I9��[������	�r@8��(�SGjժ�"�]�~V����v�Ԧ��ÇVi�d_�QuD=S�R������a�]��`^�gȐ;�����E�|��}r<1�j�3
�h��.�h%�ZIɩt�b�awƌit��!��M����P�|�@+����M�?��qQB��ᇕt��Q:$Fg�R8m�d���S3y�DZ��bڶm'�;F�����08���d^6}p9�̉�fߵkk	-��W^242ܘ��ֻ���Ԋo�}᷆�ً�x�M^6}����0���֭[U�!|����۵�06oުHj����N��i-A��N�_�>Ť���L��~��֎���T��2����O�����?<�~��o��;Ǆ��O�Ic7�r���E��?J��N-�XڶmC���k����t��o�c��&.�sDD=���F9+��7�� ���_�>F�+�1�p�E��tH1kGZ�-Z��$�m&c�#xJ�$ң�)a];����Y�I4'����1�&
�x��/��߇��.�6m��.#���k��m����+�Ϝ�ҋ�e��<��d	k3�BB^y�r�
�gϞ%h�gyHf� �132NImZ���7|`�u��ʚG;��͂cԹ��3'ӨQw�l�o��&NW����3'��������}�ḹ����j�h'�D�@^Z��lHC�W6<q"]vt�m�DG+RJMM�)���Xe�o�|BJz�\��y؇!�a~Re����G
�f$駶�"�ή]�����ȇn G��YBC�n�K�����w��ټY.޷o��؝y��.�\.D�9�9��]6�Ő	?{)5}ZƄ��(n�6C��a��֭+=0c��x=ݠ)�"-YW��y��Vy`�:}��;�Â��x!���;��9
�rrlh6�x��5f��!n)9�5���,��_�g;�!͚6S�M_�Ց�����a��u�
St�����!|d���rq�r�R9��p#�5�ر����F��`���aaG�� ;�GK��K/>��
*�\e{]U��6W�,�����
B¹0M ��L
jA?���Wu�'�BJz7З_~K��4{��l轪.�6<�0{EZkIYY���u�	���f����k��|X�ah5�'��f�!��4Mp&�[8���0CΞ=Ǟ�<��C�޽z���X��]۶��0��1��1�����G���T^br�'�Lʆ]pZ�����ϯ�	�����H��ç��N���<�3�ڨQc6�S	���B�KULkH�������W�/�s����q!%=�':l ��K?7<m� �~�]#x(v�ᒃb��W��{�V�={����,8p�Z
��>��k�)��v��
�q=y{Tf'��5�ɳ�)�� v���6�=�^ƏK˸~��և��+�܉<�C�v)}��rJIKe�R��!1mHeO�Q&�^=#�bqCÖ���d1��b��ƍ���`��0���Af��bڂn3
�ۧ�a�&v���,�-Z�g�4{�L�3ZŋYC���?dB�Q��Ν?���pvp�����+��e!ςW��	���}�a 0<�t=[3��[	�(J�}�>�kd�7v�ޫ<w�~z�)9������ֵ+��Sx���p�m:�޶g�\�$�ڂ.�~[�W%7v�zWKϋ��f���F{��c��Vc;%5����VUR�q3�AE�E��Z������Yf���CM�X�r5a#���Ӧ؜������WP�{���	�h��9Mfy��5b�nӦ͊�:u�D�f=dxO�e˾0f��"�I��WQ���bR������~�� �7j�H�ac��L`B��k�f�cJ�o�2�^'��#�1�4L�x�I	�������=t�es��!�%<���6x#�������.�V+�j�2�V�a6.���R�T�fIJ*3^���+xŊUԞ��#G�y���;8))٘�.l%�-p��[��/Z�4��a�����h�LN������Ub0�����ً�(?�e�#��������<z������ɬ�a:ڇ�3++[���uu��X�hJz%!�J-�����{��������P�.ęwΕ�	j�wE穬�����6�n8���\���FMa�)C@H������x�v���Ȏ�ݠ;88R�A��)9@���׍�;�H�j�O
��:w/7�wPL���"�ȿ����V!rP�5jD�I��>X2��)�V)T���M#IuK��qfo�9n��J�A�nKJ��o5�-8���l:���� P���M	������{��"1�_>Wj��l���[���R�b.�J��<͛~"�� `
�j�fO8�i�a2��w����B�#�V�dn��$MJp�c���"�� `]ܒ�@DMH '���;Kx�L�Gֽ �f���ڔ@HچR��h����Ƅ���i��A��#%MF�q��	�B��7��� 4&����3W�]#5<�#%ݍZ�)i1iA:�D�D�:���� P��%)imIBMH��g&$31�}�A���[��њ�֊�Ą}���<:4�#qA@�{ܖ�4����mIoCS�i�+���P�_ܚ�4!4��>�.�n����@�"�֤h5!A2��=)Ak��Ƥ`�?A��p{R�ȚIH�9͜O�%��G�cH	�j2B\kD�4���@�"�Q�d�Z�Ȍ��� psf�u�$5F@HɃ;_�.X!%+���I�`��<��邀R�b�H�F@HɃ;_�.X!%+���I�`��<��邀R�b�H�F@HɃ;_�.X!%+���I�`��<��邀R�b�H�F@HɃ;_�.X!%+���I�`�3DE�A�Xs    IEND�B`�
--- END OF FILE server/slash-command.png ---


--- START OF FILE server/tools.mdx ---
---
title: Tools
---

<div id="enable-section-numbers" />

<Info>**Protocol Revision**: draft</Info>

The Model Context Protocol (MCP) allows servers to expose tools that can be invoked by
language models. Tools enable models to interact with external systems, such as querying
databases, calling APIs, or performing computations. Each tool is uniquely identified by
a name and includes metadata describing its schema.

## User Interaction Model

Tools in MCP are designed to be **model-controlled**, meaning that the language model can
discover and invoke tools automatically based on its contextual understanding and the
user's prompts.

However, implementations are free to expose tools through any interface pattern that
suits their needs&mdash;the protocol itself does not mandate any specific user
interaction model.

<Warning>

For trust & safety and security, there **SHOULD** always
be a human in the loop with the ability to deny tool invocations.

Applications **SHOULD**:

- Provide UI that makes clear which tools are being exposed to the AI model
- Insert clear visual indicators when tools are invoked
- Present confirmation prompts to the user for operations, to ensure a human is in the
  loop

</Warning>

## Capabilities

Servers that support tools **MUST** declare the `tools` capability:

```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    }
  }
}
```

`listChanged` indicates whether the server will emit notifications when the list of
available tools changes.

## Protocol Messages

### Listing Tools

To discover available tools, clients send a `tools/list` request. This operation supports
[pagination](/specification/draft/server/utilities/pagination).

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "cursor": "optional-cursor-value"
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "title": "Weather Information Provider",
        "description": "Get current weather information for a location",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "City name or zip code"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "nextCursor": "next-page-cursor"
  }
}
```

### Calling Tools

To invoke a tool, clients send a `tools/call` request:

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "location": "New York"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current weather in New York:\nTemperature: 72°F\nConditions: Partly cloudy"
      }
    ],
    "isError": false
  }
}
```

### List Changed Notification

When the list of available tools changes, servers that declared the `listChanged`
capability **SHOULD** send a notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

## Message Flow

```mermaid
sequenceDiagram
    participant LLM
    participant Client
    participant Server

    Note over Client,Server: Discovery
    Client->>Server: tools/list
    Server-->>Client: List of tools

    Note over Client,LLM: Tool Selection
    LLM->>Client: Select tool to use

    Note over Client,Server: Invocation
    Client->>Server: tools/call
    Server-->>Client: Tool result
    Client->>LLM: Process result

    Note over Client,Server: Updates
    Server--)Client: tools/list_changed
    Client->>Server: tools/list
    Server-->>Client: Updated tools
```

## Data Types

### Tool

A tool definition includes:

- `name`: Unique identifier for the tool
- `title`: Optional human-readable name of the tool for display purposes.
- `description`: Human-readable description of functionality
- `inputSchema`: JSON Schema defining expected parameters
- `outputSchema`: Optional JSON Schema defining expected output structure
- `annotations`: optional properties describing tool behavior

<Warning>

For trust & safety and security, clients **MUST** consider
tool annotations to be untrusted unless they come from trusted servers.

</Warning>

### Tool Result

Tool results may contain [**structured**](#structured-content) or **unstructured** content.

**Unstructured** content is returned in the `content` field of a result, and can contain multiple content items of different types:

#### Text Content

```json
{
  "type": "text",
  "text": "Tool result text"
}
```

#### Image Content

```json
{
  "type": "image",
  "data": "base64-encoded-data",
  "mimeType": "image/png"
}
```

#### Audio Content

```json
{
  "type": "audio",
  "data": "base64-encoded-audio-data",
  "mimeType": "audio/wav"
}
```

#### Resource Links

A tool **MAY** return links to [Resources](/specification/draft/server/resources), to provide additional context
or data. In this case, the tool will return a URI that can be subscribed to or fetched by the client:

```json
{
  "type": "resource_link",
  "uri": "file:///project/src/main.rs",
  "name": "main.rs",
  "description": "Primary application entry point",
  "mimeType": "text/x-rust"
}
```

<Info>
  Resource links returned by tools are not guaranteed to appear in the results
  of a `resources/list` request.
</Info>

#### Embedded Resources

[Resources](/specification/draft/server/resources) **MAY** be embedded to provide additional context
or data using a suitable [URI scheme](./resources#common-uri-schemes). Servers that use embedded resources **SHOULD** implement the `resources` capability:

```json
{
  "type": "resource",
  "resource": {
    "uri": "file:///project/src/main.rs",
    "title": "Project Rust Main File",
    "mimeType": "text/x-rust",
    "text": "fn main() {\n    println!(\"Hello world!\");\n}"
  }
}
```

#### Structured Content

**Structured** content is returned as a JSON object in the `structuredContent` field of a result.

For backwards compatibility, a tool that returns structured content SHOULD also return functionally equivalent unstructured content.
(For example, serialized JSON can be returned in a `TextContent` block.)

#### Output Schema

Tools may also provide an output schema for validation of structured results.
If an output schema is provided:

- Servers **MUST** provide structured results that conform to this schema.
- Clients **SHOULD** validate structured results against this schema.

Example tool with output schema:

```json
{
  "name": "get_weather_data",
  "title": "Weather Data Retriever",
  "description": "Get current weather data for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "City name or zip code"
      }
    },
    "required": ["location"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": {
        "type": "number",
        "description": "Temperature in celsius"
      },
      "conditions": {
        "type": "string",
        "description": "Weather conditions description"
      },
      "humidity": {
        "type": "number",
        "description": "Humidity percentage"
      }
    },
    "required": ["temperature", "conditions", "humidity"]
  }
}
```

Example valid response for this tool:

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"temperature\": 22.5, \"conditions\": \"Partly cloudy\", \"humidity\": 65}"
      }
    ],
    "structuredContent": {
      "temperature": 22.5,
      "conditions": "Partly cloudy",
      "humidity": 65
    }
  }
}
```

Providing an output schema helps clients and LLMs understand and properly handle structured tool outputs by:

- Enabling strict schema validation of responses
- Providing type information for better integration with programming languages
- Guiding clients and LLMs to properly parse and utilize the returned data
- Supporting better documentation and developer experience

## Error Handling

Tools use two error reporting mechanisms:

1. **Protocol Errors**: Standard JSON-RPC errors for issues like:

   - Unknown tools
   - Invalid arguments
   - Server errors

2. **Tool Execution Errors**: Reported in tool results with `isError: true`:
   - API failures
   - Invalid input data
   - Business logic errors

Example protocol error:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "error": {
    "code": -32602,
    "message": "Unknown tool: invalid_tool_name"
  }
}
```

Example tool execution error:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Failed to fetch weather data: API rate limit exceeded"
      }
    ],
    "isError": true
  }
}
```

## Security Considerations

1. Servers **MUST**:

   - Validate all tool inputs
   - Implement proper access controls
   - Rate limit tool invocations
   - Sanitize tool outputs

2. Clients **SHOULD**:
   - Prompt for user confirmation on sensitive operations
   - Show tool inputs to the user before calling the server, to avoid malicious or
     accidental data exfiltration
   - Validate tool results before passing to LLM
   - Implement timeouts for tool calls
   - Log tool usage for audit purposes

--- END OF FILE server/tools.mdx ---


--- START OF FILE changelog.mdx ---
---
title: Key Changes
---

<div id="enable-section-numbers" />

This document lists changes made to the Model Context Protocol (MCP) specification since
the previous revision, [2025-06-18](/specification/2025-06-18).

## Major changes

## Other schema changes

## Full changelog

For a complete list of all changes that have been made since the last protocol revision,
[see GitHub](https://github.com/modelcontextprotocol/specification/compare/2025-06-18...draft).

--- END OF FILE changelog.mdx ---


--- START OF FILE index.mdx ---
---
title: Specification
---

<div id="enable-section-numbers" />

[Model Context Protocol](https://modelcontextprotocol.io) (MCP) is an open protocol that
enables seamless integration between LLM applications and external data sources and
tools. Whether you're building an AI-powered IDE, enhancing a chat interface, or creating
custom AI workflows, MCP provides a standardized way to connect LLMs with the context
they need.

This specification defines the authoritative protocol requirements, based on the
TypeScript schema in
[schema.ts](https://github.com/modelcontextprotocol/specification/blob/main/schema/draft/schema.ts).

For implementation guides and examples, visit
[modelcontextprotocol.io](https://modelcontextprotocol.io).

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD
NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [BCP 14](https://datatracker.ietf.org/doc/html/bcp14)
[[RFC2119](https://datatracker.ietf.org/doc/html/rfc2119)]
[[RFC8174](https://datatracker.ietf.org/doc/html/rfc8174)] when, and only when, they
appear in all capitals, as shown here.

## Overview

MCP provides a standardized way for applications to:

- Share contextual information with language models
- Expose tools and capabilities to AI systems
- Build composable integrations and workflows

The protocol uses [JSON-RPC](https://www.jsonrpc.org/) 2.0 messages to establish
communication between:

- **Hosts**: LLM applications that initiate connections
- **Clients**: Connectors within the host application
- **Servers**: Services that provide context and capabilities

MCP takes some inspiration from the
[Language Server Protocol](https://microsoft.github.io/language-server-protocol/), which
standardizes how to add support for programming languages across a whole ecosystem of
development tools. In a similar way, MCP standardizes how to integrate additional context
and tools into the ecosystem of AI applications.

## Key Details

### Base Protocol

- [JSON-RPC](https://www.jsonrpc.org/) message format
- Stateful connections
- Server and client capability negotiation

### Features

Servers offer any of the following features to clients:

- **Resources**: Context and data, for the user or the AI model to use
- **Prompts**: Templated messages and workflows for users
- **Tools**: Functions for the AI model to execute

Clients may offer the following features to servers:

- **Sampling**: Server-initiated agentic behaviors and recursive LLM interactions
- **Roots**: Server-initiated inquiries into uri or filesystem boundaries to operate in
- **Elicitation**: Server-initiated requests for additional information from users

### Additional Utilities

- Configuration
- Progress tracking
- Cancellation
- Error reporting
- Logging

## Security and Trust & Safety

The Model Context Protocol enables powerful capabilities through arbitrary data access
and code execution paths. With this power comes important security and trust
considerations that all implementors must carefully address.

### Key Principles

1. **User Consent and Control**

   - Users must explicitly consent to and understand all data access and operations
   - Users must retain control over what data is shared and what actions are taken
   - Implementors should provide clear UIs for reviewing and authorizing activities

2. **Data Privacy**

   - Hosts must obtain explicit user consent before exposing user data to servers
   - Hosts must not transmit resource data elsewhere without user consent
   - User data should be protected with appropriate access controls

3. **Tool Safety**

   - Tools represent arbitrary code execution and must be treated with appropriate
     caution.
     - In particular, descriptions of tool behavior such as annotations should be
       considered untrusted, unless obtained from a trusted server.
   - Hosts must obtain explicit user consent before invoking any tool
   - Users should understand what each tool does before authorizing its use

4. **LLM Sampling Controls**
   - Users must explicitly approve any LLM sampling requests
   - Users should control:
     - Whether sampling occurs at all
     - The actual prompt that will be sent
     - What results the server can see
   - The protocol intentionally limits server visibility into prompts

### Implementation Guidelines

While MCP itself cannot enforce these security principles at the protocol level,
implementors **SHOULD**:

1. Build robust consent and authorization flows into their applications
2. Provide clear documentation of security implications
3. Implement appropriate access controls and data protections
4. Follow security best practices in their integrations
5. Consider privacy implications in their feature designs

## Learn More

Explore the detailed specification for each protocol component:

<CardGroup cols={5}>
  <Card
    title="Architecture"
    icon="sitemap"
    href="/specification/draft/architecture"
  />
  <Card title="Base Protocol" icon="code" href="/specification/draft/basic" />
  <Card
    title="Server Features"
    icon="server"
    href="/specification/draft/server"
  />
  <Card
    title="Client Features"
    icon="user"
    href="/specification/draft/client"
  />
  <Card title="Contributing" icon="pencil" href="/development/contributing" />
</CardGroup>

--- END OF FILE index.mdx ---



--- PROJECT PACKAGING COMPLETE ---