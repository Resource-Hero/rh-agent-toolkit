---
name: rh-connect-setup
description: "Set up Resource Hero for Claude in a Salesforce org, as the admin: install the Resource Hero MCP extension, give users access, create and activate the Resource Hero User MCP server, create the External Client App, and hand users the server URL and consumer key. Also connects Claude Code to that server and fixes sign-in errors (invalid_client_id, MCP endpoint not found, missing tools, NO_RESOURCE, NO_ACCESS). Use when someone says set up Resource Hero for Claude, connect Claude to Resource Hero, configure rh-connect, or the Resource Hero tools are missing or won't sign in."
metadata:
  version: "1.1"
  product: "Resource Hero"
  productVersion: "16.2"
  domains: ["Admin", "User"]
  relatedSkills:
    - "rh-user-log-time"
---

# Set up Resource Hero for Claude

## Overview

Claude reaches Resource Hero through a Salesforce-hosted MCP server that the org's admin
creates. That server offers only the 16 tools of the Resource Hero MCP extension (a free
managed package, namespace `rhamcp`), and every call runs as the signed-in user, who can see
and change only their own time. Setup has five admin steps, done once per org, and one
sign-in per user. Sandbox first is fine; the steps are the same.

## Before you start

- The org runs Resource Hero 16.2 or later, and the person doing setup is a System
  Administrator.
- If the Salesforce CLI (`sf`) is signed in to the org, use it to check each step. Ask which
  org alias to use; never assume the default org.

## Admin steps

1. **Install the extension.** The admin opens the install link (Production or Developer
   Edition: `https://login.salesforce.com/packaging/installPackage.apexp?p0=04tPf000001ipflIAA`, version 0.1;
   sandbox: `test.salesforce.com`) and installs for **Admins Only**.
   Check: `sf package installed list -o <org>` lists `rhamcp`.
2. **Give users access.** Each user needs the **Resource Hero MCP User** permission set
   (`rhamcp__Resource_Hero_MCP_User`, which carries everything the tools need), a Resource
   Hero license, and exactly one active Resource linked to their user
   (`ResourceHeroApp__Resource__c.ResourceHeroApp__User__c`).
3. **Create the Resource Hero User MCP server.** In Setup > MCP Servers, create a custom
   server named `Resource Hero User` (API name `ResourceHeroUser`) with the 16 `rhamcp` tools
   from the API Catalog: Get My Assignments, Get My Tracked Time, Insert Actuals, Update
   Actuals, Delete Actuals, Get My Timers, Start Timer, Pause Timer, Stop Timer, Cancel Timer,
   Get My Time Summary, Get My Time Off, Get My Forecast, Get My Capacity, Request Time Off,
   Cancel Time Off. Save and **activate** it, then copy its server URL from the server's menu.
   With the CLI instead: deploy
   `assets/force-app/main/default/mcpServerDefinitions` (`sf project deploy start --source-dir
   <path> -o <org>` from a copy of `assets/`), then activate the server in Setup; deploying
   doesn't activate it.
4. **Create the External Client App.** Setup > External Client App Manager > New: name
   `Resource Hero MCP`, distribution **Local**, OAuth enabled with callback URLs
   `http://localhost:8765/callback` and `https://claude.ai/api/mcp/auth_callback`, scopes
   `mcp_api` and `refresh_token`, PKCE required, JWT-based access tokens for named users on,
   secret not required for the web server flow. Copy the **Consumer Key** from its OAuth
   settings. With the CLI: the templates are in `assets/force-app/main/default/` (set your
   contact email in `externalClientApps/Resource_Hero_MCP.eca-meta.xml` first).
5. **Send users** the server URL and the consumer key. The key isn't a secret: each user still
   signs in with their own Salesforce login.

## Connect Claude Code (each user)

1. Install `rh-user` (it brings `rh-connect`).
2. Add the server with the admin's two values (in Claude Code, prefix it with `!`):
   `claude mcp add --transport http --scope user --client-id <consumer key> --callback-port 8765 resource-hero <server URL>`
3. Run `/mcp`, select **resource-hero**, and sign in in the browser (a private window if it
   is signed in to another org).
4. Check with `getMyAssignments`: it returns the user's Resource name and open assignments.

In Claude on the web or desktop, add a custom connector with the server URL and, under
Advanced settings, the consumer key as the OAuth Client ID.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `invalid_client_id` at sign-in | The External Client App isn't available yet (wait a few minutes) or the key is wrong. |
| `OAUTH_AUTHORIZATION_BLOCKED` | The browser is signed in to another org. Sign out or use a private window. |
| "MCP endpoint not found" | The server isn't activated, or the URL wasn't copied from Setup. |
| A tool is missing | Add it to the server, then reconnect (`/mcp`). |
| NO_RESOURCE / MULTIPLE_RESOURCES | Link exactly one active Resource to the user. |
| NOT_LICENSED | Assign a Resource Hero license. |
| NO_ACCESS | Assign the Resource Hero MCP User permission set. |
| Uninstall is blocked | Deactivate and delete the MCP server and remove the permission set from every user first (see "Moving to a new version" in the admin guide). |

## Sources

- https://www.resourceheroapp.com/support/enhanced-time-tracking-component/ (modified 2026-02-18)
