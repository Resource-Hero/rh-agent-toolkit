# Use Resource Hero with Claude (user guide)

Log time, run timers, request time off and check your week in Resource Hero by asking Claude,
in Claude on the web or desktop or in Claude Code. Claude works as you: it sees only your own
assignments and time, and your org's Resource Hero rules apply.

Your Salesforce admin sets this up once ([admin guide](setup-guide.md)). If your organization
didn't add the Resource Hero connector for you, the admin sends you two values: a **server
URL** and a **consumer key**.

## Claude on the web or desktop

### Connect

If your organization already added the Resource Hero connector, open **Settings >
Connectors**, find **Resource Hero** and click **Connect**. Otherwise:

1. In Claude, open **Settings > Connectors** and add a custom connector.
2. Name it `Resource Hero`, paste the server URL, and under **Advanced settings** paste the
   consumer key as the OAuth Client ID.
3. Click **Connect** and sign in with your Salesforce login. If the browser is already signed
   in to a different Salesforce org, sign out of it first or use a private window.

In a chat, make sure the Resource Hero connector is turned on (the connectors menu under the
message box), then ask: **"What am I assigned to?"**

### Add the Resource Hero plugin (optional, recommended)

The plugin teaches Claude how to work with Resource Hero well: confirming before it saves,
handling dates and read-only assignments, and building your time dashboard. It works the same
on personal plans (Pro, Max) and in Team and Enterprise organizations. If your organization
installed it for everyone, you already have it. Otherwise, open **Customize > Plugins**, click
**Add**, and choose one:

- **Add marketplace:** enter `https://github.com/Resource-Hero/rh-agent-toolkit`, then install
  **rh-user** from it.
- **Upload plugin:** upload `rh-user.zip` from the toolkit's
  [Releases page](https://github.com/Resource-Hero/rh-agent-toolkit/releases). To update it,
  remove it and upload the newer zip.

In a Team or Enterprise organization, if **Add** doesn't offer these, your organization has
turned them off; ask your Claude admin.

## Claude Code

1. Add the Resource Hero marketplace and install the plugin:

   ```
   /plugin marketplace add Resource-Hero/rh-agent-toolkit
   /plugin install rh-user@resource-hero
   ```

2. Add your org's Resource Hero server, filling in the consumer key and server URL from your
   admin. Type it in Claude Code with a leading `!`, or run it in a terminal without the `!`:

   ```
   ! claude mcp add --transport http --scope user --client-id <consumer key> --callback-port 8765 resource-hero <server URL>
   ```

3. Run `/mcp`, select **resource-hero**, and sign in with your Salesforce login in the
   browser window that opens. If the browser is already signed in to a different Salesforce
   org, use a private window.
4. Ask: **"What am I assigned to?"** Claude lists your open assignments.

## Things to ask

- "What am I assigned to?"
- "Log 2 hours to Acme Implementation today, notes: design review."
- "I worked 6 hours on the Smith project yesterday, 4 of them billable."
- "What did I log this week?"
- "Change row 2 to 1.5 hours." / "Delete the entry on Tuesday."
- "Start a timer on Acme." / "Pause my timer." / "Stop my timer and log it."
- "How does my week look?" / "When is my next time off?"
- "What am I scheduled for next week?" / "When do I have time free this month?"
- "Request next Friday off, 8 hours, vacation." / "Cancel my time off request for the 14th."
- "Build me a dashboard of my time."

Claude shows what it is about to save and waits for your yes before it logs, changes or
deletes anything, or requests time off.

## Your time dashboard

In Claude on the web or desktop, ask **"Build me my Resource Hero time dashboard"** (with the
plugin installed). Claude publishes a private page, **My time and timers**, that reads and saves
your Resource Hero time live, as you:

- **Coming up:** your next holidays and time off. **+ Request time off** asks for days off;
  hours per day start from your capacity. **Cancel** appears on requests that aren't approved
  yet.
- **Timer:** start a timer by picking an assignment; pause it, stop it to log the time, or
  throw it away. Starting a new timer pauses the running one.
- **Quick log:** tap buttons (your own increments from Resource Hero, such as 15min, 1hr, 4hr)
  to log time on an assignment. Taps add up and save as one entry a moment after the last one,
  with an Undo. Each row shows what's logged that day against what's planned, and you can
  change the day.
- **The week:** planned, logged and left-to-log hours, a grid of your hours by assignment and
  day, and every entry, which you can add to, edit or delete. Holidays, time off, and locked or
  archived assignments show their hours but can't take new time. Names link to the records in
  Salesforce.

The first time, Claude asks for permission to use the Resource Hero connector from the page;
choose Allow. The page refreshes when you open it, when you click ↻, after any change, and every
minute while a timer runs.

**Make it yours.** Ask Claude to change the page: "remove the timer", "add my utilization by
week", "use larger text". Short notes on the page explain each part; when you no longer need
them, ask Claude to **"remove the help text from my time dashboard"**. To start over, delete the
page and ask for the dashboard again in a new chat.

If you share the page, everyone who opens it sees their own time, not yours.

## Good to know

- Claude works as you. It sees only your own assignments and time, and your org's rules
  (locked periods, required notes, daily limits) apply as in Resource Hero.
- Time Claude logs is the same time you see in Resource Hero's Time Tracking and the matrix.
- Holidays and approved time off appear in your time, but you can't change them here.
- Time off you request through Claude follows your org's process: it may be approved right
  away or wait for approval. Claude tells you which. You can cancel a request until it is
  approved; after that, ask your approver.
- If Claude says it can't reach Resource Hero, reconnect: in Claude Code run `/mcp` and sign in
  again; in Claude on the web or desktop, open Settings > Connectors and connect Resource Hero
  again.
