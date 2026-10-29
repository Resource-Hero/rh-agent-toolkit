---
name: rh-user-time-dashboard
description: "Build a personal Resource Hero time dashboard: a live Claude page of the user's own week (planned, logged and left-to-log hours, a week grid, an entries list they can add to and edit), a timer, and upcoming holidays and time off. Ships a ready-made page in Resource Hero's colors to publish as is. Use when someone asks for a dashboard, timesheet page, chart, scorecard or saved view of their own time, utilization, capacity or time off, or asks to change their dashboard (remove the help text from my time dashboard, remove the timer). Needs the Resource Hero MCP extension's tools. Not for logging time in chat (use rh-user-log-time) or for team and company reporting (use Salesforce reports)."
metadata:
  version: "0.15"
  product: "Resource Hero"
  productVersion: "16.2"
  domains: ["User"]
  relatedSkills:
    - "rh-user-log-time"
---

# Build a personal time dashboard

## Overview

The Resource Hero MCP extension gives each user tools that work on their own time. A dashboard
built on them runs those tools live, as whoever opens it, so it always shows the viewer's own
data and stays current.

This skill ships that dashboard ready-made: [assets/time-dashboard.html](assets/time-dashboard.html),
a page in Resource Hero's colors. **Publish it as is** unless the user asks for something
different; fill in two settings and declare its connector, and it works for any user. The rest of
this skill explains the tools behind it and the definitions that keep its numbers matching
Resource Hero's own reports and matrix, for when the user wants a change or a page of their own.

## Before you start

- The org has the Resource Hero MCP extension installed and an active Resource Hero User MCP
  server with the tools below. The page runs inside Claude, so the user needs the server added
  as a **connector in Claude** (Settings > Connectors; the setup guide names it `Resource
  Hero`). A server added only to Claude Code (`claude mcp add`) is not enough for the page. If the
  tools are missing, the admin adds them to the server.
- The user has a Resource Hero license, the Resource Hero MCP User permission set, a Resource
  linked to their user, and RH Capacity records. Without capacity, utilization shows as
  NoCapacity.
- Call `getMyAssignments`, `getMyTimeSummary`, `getMyTimeOff` and `getMyTrackedTime` once
  yourself before publishing, and look at the replies. A failure here (NO_RESOURCE, NO_ACCESS)
  would fail on the page too; fix it first.

## Publish the ready-made page

1. **Find the connector's name** as Claude shows it to the user (usually `Resource Hero`). If
   you can't see it, ask the user what their Resource Hero connector is called.
2. **Find each tool's name** on that server (see "The tools" below; names vary with how the admin
   built the server).
3. **Copy the page and fill in its settings.** In the copy of
   [assets/time-dashboard.html](assets/time-dashboard.html), set `SERVER` to the connector name
   and each value in `TOOLS` to that tool's name on the server. There are 16: `getMyAssignments`,
   `getMyTrackedTime`, `getMyTimeSummary`, `getMyTimeOff`, `getMyForecast`, `getMyCapacity`,
   `insertActuals`, `updateActuals`, `deleteActuals`, `requestTimeOff`, `cancelTimeOff`,
   `getMyTimers`, `startTimer`, `pauseTimer`, `stopTimer` and `cancelTimer`. Change nothing else
   unless the user asks.
4. **Publish it as a page** with the Artifact tool, declaring the connector so the page may call
   it: `capabilities: {"mcp": {"servers": [{"server": "<connector name>", "tools": [<every name
   in TOOLS>]}]}}`. List all 16; a tool left out fails on the page. Give it the title "My time and timers" and an icon such as `clock`.
5. **Tell the user** it reads and writes live as them, that Claude asks once for permission to
   use the connector, and that it's private until they share it. Anyone they share it with sees
   their own time, not the user's.

If the server lacks the write, time off or timer tools, the page's add, edit, request, cancel and
timer controls fail with a clear message. Offer to remove those parts, or build a read-only page from the sections
below.

### What the page shows

- **Header band:** a greeting, the time of the last refresh with a refresh button, **Coming up**
  (the next holidays and time off, one line each, with **Request time off** and a **Cancel** on
  requests still Open or Submitted), and the **timer** (the active timer with
  pause, stop-and-log and discard; picking an assignment starts or resumes a timer on it).
- **The week**, with previous / this / next week: tiles for **Planned**, **Logged** (with
  billable hours and a progress bar) and **Left to log**; a **grid** of assignments by day,
  shaded by hours; and an **Entries** list (date, assignment, hours, billable, category, notes)
  whose first row adds an entry. Clicking a grid cell narrows the list to that day and fills the
  add row with the cell's assignment and date. Each entry has an Edit link that turns the row into
  fields, with Save and Delete; a delete of an entry that also holds forecast hours offers to
  clear only the logged hours.
- **Request time off:** a small form under Coming up: start date (the next working day), an
  optional end date, hours per day (the user's capacity that day, else 8), type (Vacation, Sick,
  Personal Day or none) and a description up to 80 characters. A one-line summary with weekdays
  shows above the Request button, and pressing Request is the confirmation. The reply's status
  shows in plain words. Cancel asks for confirmation inline; approved time off has no Cancel (the
  user asks their approver).
- **Quick log:** its own card under the header, for tap tracking as in Resource Hero. Each open
  assignment has a row of the user's own tap buttons (such as 15min, 1hr, 4hr, from their
  Resource Hero settings). Each tap adds to a pending total with a countdown and a × to cancel;
  1.5 seconds after the last tap, the total saves as one entry. After a save, Undo deletes the
  entry for about 10 seconds.
  - **The day:** a date control by the title (‹ previous day, the date, › next day, and Today
    when it's another day) sets the day taps log to. Picking a cell in the grid sets it too.
    Changing the day first saves any pending taps to the day they were tapped on. Future days
    are allowed; Resource Hero's rules decide.
  - **Totals:** each row ends with that assignment's hours logged on the day, in a right-hand
    column, with the planned hours under it ("of 4 h"). The card ends with the day total for all
    project time ("Day total 5.5 h of 8 h planned"). Pending taps aren't counted until they save;
    saves count as soon as they land.
  - **Order:** rows planned for the day come first; past five rows, the rest sit behind "Show
    all".
  - The card is hidden when the user has tap tracking off or no tap buttons. The timer is hidden
    when the user's timer is off.
- **Record links:** each assignment's project or opportunity name (grid, entries, timer, Quick
  log) opens that record in Salesforce in a new tab, and the user's name in the greeting opens
  their Resource record. Names stay plain text when the reply has no org URL or Id.
- **Help text:** an "About this page" summary at the top says what the page does, that the user
  can ask Claude to add, remove or change any part, and how to remove the help text. A short
  plain-language note in each section says what it does. Every note has the class `rh-help`
  (see "Remove the help text").
- Holidays and time off show in their own rows and can't be edited; entries on a read-only
  assignment show a Locked tag.
- **Read-only rows:** in the grid, the Holidays and Time off rows and any locked (read-only) or
  archived assignment show their hours as plain text: their cells can't be clicked or tabbed to,
  and a tooltip says why. Entries on archived assignments can still be edited or deleted, but no
  picker, prefill, Quick log row or timer resume offers a locked or archived assignment.
- It follows the viewer's light or dark theme and works at phone width.

## Remove the help text

When the user asks to remove the help text from a dashboard that's already published:

1. Read the artifact (Artifact `read` with its URL; find it with `list` if you don't have it).
2. Delete every element with the class `rh-help`, and the CSS rules under the
   `/* help text … */` comment (every selector there names `.rh-help`).
3. Change nothing else. Keep `SERVER`, `TOOLS` and the capabilities as they are.
4. Republish to the same artifact URL, so the user's link keeps working.

Remove a whole section the same way when asked ("remove the timer", "remove Quick log"), and
leave the rest. The script looks up section elements by id, so deleting an element alone can
break the page; hide it instead and keep its code:

- **Timer:** in `loadAssignments`, change `$("#timerBox").hidden = out.showTimer === false;` to
  `$("#timerBox").hidden = true;`.
- **Quick log:** the card starts hidden; delete the `setQuickLog(out);` line in
  `loadAssignments` so it never shows. To remove it outright, also delete its card and its
  `// ---------- quick log ----------` script block.

Then republish to the same URL.

## The tools

Tool names depend on how the admin built the server: `getMyAssignments`, `GetMyAssignments`,
or a generated name such as `rhamcp_GetMyAssignmentsapex_rhamcp_GetMyAssignments`. Find each
tool by the action name in it, ignoring case; this skill uses the camelCase form.

| Part of the dashboard | Tool and arguments |
|---|---|
| Greeting, assignment pickers, Locked tags, record links (`orgUrl`, `resourceId`, each assignment's `assignedToId`), Quick log buttons and whether Quick log and the timer show (`tapIncrements`, `showTapTracking`, `showTimer`) | `getMyAssignments` {} |
| Planned tile (and utilization, weekly charts) | `getMyTimeSummary` {weeksBack: 4, weeksAhead: 4} |
| Hours by project, stacked | `getMyTimeSummary` {weeksBack: 4, weeksAhead: 4, groupBy: "WeekAndAssignment"} |
| Coming up | `getMyTimeOff` {} (this week plus 12 ahead) |
| Request and cancel time off | `requestTimeOff` {startDate, endDate, hoursPerDay, type, description}, `cancelTimeOff` {timeOffRequestId} |
| Hours per day in the request form (only when the form opens) | `getMyCapacity` {weeksBack: 0, weeksAhead: 12} |
| Quick log's planned hours | `getMyForecast` {weeksBack: 0, weeksAhead: 1}; for another day, a window that covers its week (up to 26 weeks either way; beyond that, no plan) |
| Quick log's logged hours for a day outside the week shown | `getMyTrackedTime` {startDate: day, endDate: day}, cached until the next save, undo or refresh |
| Week grid, entries list, Logged tile | `getMyTrackedTime` {startDate, endDate} for the week shown (or {daysBack: 7}) |
| Add, edit, delete entries | `insertActuals`, `updateActuals`, `deleteActuals` |
| Quick log saves and Undo | `insertActuals` {entries: [{assignmentId, entryDate, hours}]}, billable left to the org default; Undo is `deleteActuals` {timeEntryIds: [the reply's `results[0].recordId`]} |
| Timer | `getMyTimers`, `startTimer`, `pauseTimer`, `stopTimer`, `cancelTimer` |

The ready-made page computes the week's dates from today in the viewer's browser, so it stays
current; it never stores dates.

Requested time off takes the org's default status: some orgs approve it at once, others leave it
Submitted or Open for approval. Show the reply's `status`; never assume Submitted. Only Open and
Submitted requests can be cancelled (otherwise `TIME_OFF_STATE`).

In a page you build yourself, **use the relative arguments** (`weeksBack`, `weeksAhead`,
`daysBack`, `daysAhead`) or dates computed from today at view time, never dates typed in. Fixed
dates would freeze the page on the day it was built.

## Reading the replies

Salesforce's MCP server wraps every Resource Hero tool. Calls take the arguments inside an
`inputs` list, and replies come back as a list of results with the tool's fields under
`outputValues`, sometimes inside an MCP text block:

```json
// call
{"inputs": [{"weeksBack": 4, "weeksAhead": 4}]}
// reply
[{"isSuccess": true, "outputValues": {"success": true, "rangeStart": "…", "rows": [ … ]}}]
```

A dashboard therefore needs a small step that unwraps each reply into rows (the ready-made page's
`unwrap` does this). In a page of your own, one function works for the read tools; pass the list
field (`rows` for the summary and time off, `entries` for tracked time):

```js
function unwrap(answer, listField) {
  let a = typeof answer === 'string' ? JSON.parse(answer) : answer;
  if (a && !Array.isArray(a) && Array.isArray(a.content)) {
    const t = a.content.find((c) => c && c.type === 'text');
    a = t ? JSON.parse(t.text) : a.content;
  }
  const r = Array.isArray(a) ? a[0] : a;
  const out = (r && r.outputValues) || {};
  if (!r || r.isSuccess === false || out.success === false) {
    throw new Error(out.errorMessage || 'Resource Hero reported a failure.');
  }
  return out[listField] || [];
}
```

When `success` is false, show `errorMessage`. The `errorCode` says who fixes it: NO_RESOURCE
or MULTIPLE_RESOURCES (the admin links exactly one Resource to the user), NOT_LICENSED (the
admin assigns a license), NO_ACCESS (permission sets).

## Picking weeks

Every summary row has `weekOffset`: 0 is this week, -1 last week, 1 next week. **Select rows
by `weekOffset`, never by position.** Row 4 is this week only while `weeksBack` is 4; a
dashboard that counts rows shows the wrong week as soon as someone widens the window.

Weeks start on Monday, as Resource Hero's Week Beginning field and matrix do. Salesforce
reports filtered on THIS_WEEK follow the user's locale, which starts on Sunday in the US, so
their week totals can differ slightly. Say "Monday weeks" on the chart.

## Which numbers to show

Resource Hero stores holidays and approved time off as both forecast and actual hours, and
submitted time off as forecast only. Its reports count all of that toward utilization. Use
each number for what it means:

| Tile or series | Field | Why |
|---|---|---|
| Logged this week | `projectActualHours` | Time the user entered. `actualHours` also includes holidays and approved time off, which the user didn't log. |
| Planned this week | `projectForecastHours` | `forecastHours` also includes holidays and time off. |
| Left to log | `projectForecastHours − projectActualHours`, not below 0 | Submitted time off is in `forecastHours` but can never be logged. |
| Billable | `billableActualHours` | Project time only. Holiday and time off rows aren't billable. |
| Utilization % and status | `forecastUtilizationPct`, `actualUtilizationPct`, `utilizationStatus` | As the packaged My Resource Hero reports define them: all hours over capacity. Keep these as they are so the dashboard agrees with Resource Hero. |
| Holidays and time off | `holidayHours`, `timeOffApprovedHours`, `timeOffSubmittedHours` | Show them beside the project numbers, for example "+8 h holiday". |

`utilizationStatus` is Under below 80% of capacity, Target from 80% to 120%, Over above 120%
(the matrix's band), and NoCapacity without capacity.

## Building your own page instead

When the user wants something the ready-made page doesn't do (utilization by week, a chart of
hours by project, a read-only view), start from the ready-made page and add to it, or build new.
Keep the look: Resource Hero's palette (Deep Navy `#0E4858`, Teal Blue `#1695AE`, Beige
`#F2EBE6`, Light Blue `#BADCE3`, one Orange `#FD8E25` accent), the Lato font, and the page's
light and dark color tokens. Useful additions:

- **Utilization by week:** stacked bars of project, holiday and time off hours from
  `getMyTimeSummary`, a capacity line, a status chip per week, the current week shaded.
- **Hours by project:** `groupBy: "WeekAndAssignment"`, planned against logged per assignment.

Every number on the page comes from a tool reply or from arithmetic on one; never type values
into the page.

## Troubleshooting

- **A tool isn't listed:** the admin adds it to the Resource Hero User MCP server and activates
  the server; then reconnect so the client refreshes its tool list.
- **Utilization is blank or NoCapacity:** the user has no RH Capacity for those weeks (see
  the Resource Hero admin creates it).
- **A time off request is missing:** cancelled and rejected requests have no hours and aren't
  listed; an Open request shows with 0 hours on the chart until it is submitted.
- **An entry shows 0 hours:** time logged through the time tracker is kept even at 0 hours,
  as in Resource Hero's own time tracking list.

## Sources

- https://www.resourceheroapp.com/support/enhanced-time-tracking-component/ (modified 2026-02-18)
