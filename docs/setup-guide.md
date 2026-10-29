# Set up Resource Hero for Claude (admin guide)

This guide is for the Salesforce admin. It connects Claude to Resource Hero in your org so
your users can log time, run timers, request time off and see their own time, forecast and
capacity by asking Claude, in Claude Code or in Claude on the web and desktop. Plan on about
30 minutes. You do it once per org; each user then signs in for themselves
([user guide](user-guide.md)).

> **Early release.** The Resource Hero MCP extension is in limited release (version 0.1).
> Salesforce's MCP features are changing quickly, so a later version may need you to uninstall
> the extension and install the new one instead of upgrading. See
> [Moving to a new version](#moving-to-a-new-version).

## How it fits together

- **The Resource Hero MCP extension** is a free managed package that adds 16 Resource Hero
  tools to your org: list my assignments, log, change and delete my time, run timers,
  summarize my time, forecast and capacity, and request time off.
- **A Resource Hero User MCP server** is a Salesforce-hosted MCP server that you create in
  Setup and that offers exactly those 16 tools, nothing else. Claude connects to it.
- **An External Client App** lets Claude sign in to that server as each user, through the
  normal Salesforce login.

Everything runs as the signed-in user. A user can only see and change their own time, and
your sharing rules, field security, validation rules and flows apply as they do in Resource
Hero's Time Tracking component.

## Before you start

- Resource Hero 16.2 or later is installed.
- You can create External Client Apps and MCP servers in Setup (System Administrator).
- Try it in a sandbox first if you like. The steps are the same; the server URL differs.
- **Salesforce may bill MCP usage.** Setup shows "You might be billed for Salesforce MCP
  server usage" on the MCP Servers page. Salesforce plans to charge Flex Credits for calls
  that agents make to production orgs; it hasn't published the rate, isn't metering yet, and
  has said it will give 30 days' notice. Sandboxes, scratch orgs and Developer Edition orgs
  are exempt. Ask your Salesforce account executive how this applies to your contract.
  Resource Hero doesn't charge for the extension.

## Step 1: Install the Resource Hero MCP extension

1. Open the install link for your org type, signed in as an admin (version 0.1):
   - Production or Developer Edition:
     `https://login.salesforce.com/packaging/installPackage.apexp?p0=04tPf000001ipflIAA`
   - Sandbox: `https://test.salesforce.com/packaging/installPackage.apexp?p0=04tPf000001ipflIAA`
2. On **Install Resource Hero MCP**, select **Install for Admins Only** (the page selects
   Install for All Users by default). Users still get access: the permission set in step 2
   grants exactly what the tools need, to exactly the users you choose. (Install for All
   Users reaches only custom profiles, so users on standard profiles would need the
   permission set anyway.)
3. Click **Install**.

## Step 2: Give users access

Each user who will use Claude needs:

1. The **Resource Hero MCP User** permission set (from the extension). It carries everything
   the tools need; no other Resource Hero permission set is required. It includes create and
   edit access to Time Off Request (Status, Type and Description), so users can request and
   cancel their own time off. New requests get your org's default Time Off Request status, so
   your own approval process applies; if you approve time off on entry, so does Claude.
2. A Resource Hero license.
3. Exactly one active Resource record linked to their user.

Assign the set from Setup > Permission Sets > Resource Hero MCP User > Manage Assignments >
Add Assignment.

## Step 3: Create the Resource Hero User MCP server

Choose one way to build the server:

| | Option A: in Setup | Option B: deploy with the Salesforce CLI |
|---|---|---|
| Needs | Setup access only | The Salesforce CLI, signed in to the org |
| Read-only and Destructive hints for Claude | Yes, set per tool | Yes, already set in the definition |
| Tool descriptions | Saved when you add each tool; re-add the tools after you upgrade the extension | Always the extension's current descriptions |

Either way, Claude confirms before it logs, changes or deletes time, because the tool
descriptions tell it to.

### Option A: in Setup

1. In Setup, enter **MCP** in Quick Find and open **Integrations > API Catalog > MCP
   Servers**. (Registered MCP Servers, under Einstein, is a different page.)
2. Click **Add MCP Server > Create Salesforce MCP Server**:
   - Name: `Resource Hero User`
   - API name: `ResourceHeroUser`
   - Description: `Resource Hero time tracking for the signed-in user`
3. On the server's **Tools** tab, use **Add Server Assets** to add the 16 Apex actions in
   the `rhamcp` namespace: `rhamcp__GetMyAssignments`, `rhamcp__GetMyTrackedTime`,
   `rhamcp__InsertActuals`, `rhamcp__UpdateActuals`, `rhamcp__DeleteActuals`,
   `rhamcp__GetMyTimers`, `rhamcp__StartTimer`, `rhamcp__PauseTimer`, `rhamcp__StopTimer`,
   `rhamcp__CancelTimer`, `rhamcp__GetMyTimeSummary`, `rhamcp__GetMyTimeOff`,
   `rhamcp__GetMyForecast`, `rhamcp__GetMyCapacity`, `rhamcp__RequestTimeOff`,
   `rhamcp__CancelTimeOff`. Check that the header shows **Tools 16**.
4. Click **Edit** on each tool and set its Tool Label, Tool Name and annotations as below.
   Salesforce generates long tool names (`rhamcp_GetMyTimersapex_rhamcp_GetMyTimers`); short
   names keep Claude's tool list readable. Annotations tell Claude which tools only read and
   which ones to confirm before running.

   | Tool | Tool Label | Tool Name | Annotations |
   |---|---|---|---|
   | rhamcp__GetMyAssignments | Get My Assignments | `getMyAssignments` | Read-only, Idempotent |
   | rhamcp__GetMyTrackedTime | Get My Tracked Time | `getMyTrackedTime` | Read-only, Idempotent |
   | rhamcp__GetMyTimers | Get My Timers | `getMyTimers` | Read-only, Idempotent |
   | rhamcp__GetMyTimeSummary | Get My Time Summary | `getMyTimeSummary` | Read-only, Idempotent |
   | rhamcp__GetMyTimeOff | Get My Time Off | `getMyTimeOff` | Read-only, Idempotent |
   | rhamcp__GetMyForecast | Get My Forecast | `getMyForecast` | Read-only, Idempotent |
   | rhamcp__GetMyCapacity | Get My Capacity | `getMyCapacity` | Read-only, Idempotent |
   | rhamcp__InsertActuals | Insert Actuals | `insertActuals` | none |
   | rhamcp__UpdateActuals | Update Actuals | `updateActuals` | Idempotent, Destructive |
   | rhamcp__DeleteActuals | Delete Actuals | `deleteActuals` | Destructive |
   | rhamcp__StartTimer | Start Timer | `startTimer` | none |
   | rhamcp__PauseTimer | Pause Timer | `pauseTimer` | none |
   | rhamcp__StopTimer | Stop Timer | `stopTimer` | none |
   | rhamcp__CancelTimer | Cancel Timer | `cancelTimer` | Destructive |
   | rhamcp__RequestTimeOff | Request Time Off | `requestTimeOff` | none |
   | rhamcp__CancelTimeOff | Cancel Time Off | `cancelTimeOff` | Destructive |

   Leave **Open world** unchecked on every tool: nothing leaves Salesforce.
5. Click **Activate**. The server doesn't answer until it's active.
6. From the server's menu choose **Copy Server URL** and keep it for step 5. It starts with
   `https://api.salesforce.com/platform/mcp/v1/` and ends with `/custom/ResourceHeroUser`;
   use it exactly as copied.

### Option B: deploy with the Salesforce CLI

The server definition is in this repo at
`plugins/rh-connect/skills/rh-connect-setup/assets/`, with the 16 tools, their names and the
annotations from the Option A table set.

1. Copy the `assets` folder, then from that copy run:

   ```
   sf project deploy start --source-dir force-app/main/default/mcpServerDefinitions --target-org <your org>
   ```

2. In Setup > MCP Servers, open **Resource Hero User** and click **Activate** (deploying
   doesn't activate it). The Setup page shows no tool descriptions; that's expected, as the
   server passes the extension's own descriptions to Claude.
3. Copy the server URL as in Option A, step 6.

## Step 4: Create the External Client App

1. In Setup, open **External Client App Manager** and click **New External Client App**.
   - Name: `Resource Hero MCP`; Contact Email: yours; Distribution State: **Local**.
2. Under **API (Enable OAuth Settings)**, check **Enable OAuth** and set:
   - Callback URLs, one per line:
     `http://localhost:8765/callback` (Claude Code) and
     `https://claude.ai/api/mcp/auth_callback` (Claude on the web and desktop).
     After a user signs in, Salesforce sends their browser back to one of these with a
     one-time code. Claude Code catches it with a short-lived listener on the user's own
     computer (localhost, port 8765), so nothing is exposed to the internet. Keep only the
     one for the Claude apps your users have.
   - OAuth scopes: **Access Salesforce hosted MCP servers (mcp_api)** and
     **Perform requests at any time (refresh_token, offline_access)**
   - Flow enablement: leave everything unchecked.
   - Security: check **Require Proof Key for Code Exchange (PKCE)** and
     **Issue JSON Web Token (JWT)-based access tokens for named users**; uncheck
     **Require secret for Web Server Flow**.
3. Create the app. Salesforce can take a few minutes to make a new app available.
4. On the app's **Settings** tab, open **OAuth Settings > Consumer Key and Secret** and copy
   the **Consumer Key**.

## Step 5: Send your users two values

- The **server URL** from step 3.
- The **consumer key** from step 4. It isn't a secret: on its own it grants nothing, since
  each user still signs in with their own Salesforce login.

Claude Code users add the server with one command, which you can fill in for them:

```
claude mcp add --transport http --scope user --client-id <consumer key> --callback-port 8765 resource-hero <server URL>
```

Point them to the [user guide](user-guide.md).

## Claude on the web and desktop (Team and Enterprise)

An Owner of your Claude organization can set this up once for everyone, so users don't paste
any values:

1. **Add the connector for the organization.** In Claude, open **Organization settings >
   Connectors** and add a custom connector named `Resource Hero` with the server URL from
   step 3 and, under Advanced settings, the consumer key from step 4 as the OAuth Client ID.
   Each user then connects it with their own Salesforce login.
2. **Add the Resource Hero plugin.** The `rh-user` plugin teaches Claude how to log time,
   request time off and build a personal time dashboard. Plugins added here also reach your
   users' Claude Code. Choose one way:

   - **Upload the zip (simplest).** Download `rh-user.zip` from the toolkit's
     [Releases page](https://github.com/Resource-Hero/rh-agent-toolkit/releases). In **Organization settings > Plugins & skills**, choose **Add >
     Upload a plugin** and upload it. To update it later, open the plugin's menu and choose
     **Upload new version** with the newer zip.
   - **Sync from your own copy of the repository.** Claude syncs organization plugins only from
     a **private** repository that has the Claude GitHub App installed, so copy the toolkit
     into a private repository in your GitHub organization. Use GitHub's **Import repository**
     (a fork of a public repository can't be made private). Then choose **Add > Sync from
     GitHub**, pick your copy, and install the Claude GitHub App when asked. To update, pull
     the toolkit's new release into your copy; Claude syncs on push.

   Then open the plugin's menu, choose **Default access**, and set it to **Installed by
   default** (or **Available to install** to let users choose).

After a plugin update, users rebuild their dashboard from a new chat to get the new page.

Without an Owner, each user adds the connector (and, if they like, the plugin) themselves
([user guide](user-guide.md)).

## Upgrading the extension

New versions of the extension can improve what each tool tells Claude. A server built in
Setup keeps each tool's description from when you added the tool, so after an upgrade:

1. Open the Resource Hero User server and click **Deactivate** (tools can't be changed while
   the server is active).
2. Option A servers: **Remove** each tool and add it again with **Add Server Assets**, then
   set its label, name and annotations as in step 3. Option B servers need nothing here; they
   already use the new descriptions.
3. Click **Activate**. Users reconnect with `/mcp` to pick up the changes.

## Moving to a new version

When a new version can't upgrade the one you have, Resource Hero's release notes say so.
Salesforce won't uninstall the extension while anything still uses it, so:

1. In Setup > MCP Servers, open **Resource Hero User**, click **Deactivate**, then delete the
   server.
2. Remove the **Resource Hero MCP User** permission set from every user (Manage Assignments).
   Write down who had it.
3. In Setup > Installed Packages, uninstall **Resource Hero MCP**. Users' time, timers and time
   off are Resource Hero records and stay as they are.
4. Install the new version (step 1), create the server again with the **same API name**
   `ResourceHeroUser` (step 3) and activate it, and give the permission set back to the same
   users.

The External Client App stays. With the same server API name the server URL doesn't change,
so users' Claude connectors keep working; they reconnect once to pick up the tools.

## Troubleshooting

| What the user sees | Fix |
|---|---|
| `invalid_client_id` when signing in | The External Client App isn't available yet (wait a few minutes) or the consumer key was mistyped. |
| `OAUTH_AUTHORIZATION_BLOCKED` or a cross-org error | The browser is signed in to a different org. Sign out of it, or use a private window. |
| "MCP endpoint not found" | The server isn't activated, or the URL wasn't copied from Setup. |
| A tool is missing | Add it to the server, then the user reconnects. |
| NO_RESOURCE / MULTIPLE_RESOURCES | Link exactly one active Resource to the user. |
| NOT_LICENSED | Assign the user a Resource Hero license. |
| NO_ACCESS | Assign the Resource Hero MCP User permission set. |
