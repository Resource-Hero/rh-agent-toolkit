---
name: rh-user-log-time
description: "Log, correct, delete and review your own time in Resource Hero, the Salesforce-native resource management app, run timers, check your forecast and capacity, and request or cancel time off. Use when someone says log time, log 3 hours to a project, enter my hours, fix yesterday's time, change or delete an entry, what did I log this week, what am I assigned to, start, pause or stop a timer, what am I scheduled for next week, when do I have time free, request a day off, or cancel my time off request. Uses the Resource Hero MCP extension's tools. Not for dashboards or charts of your time (use rh-user-time-dashboard)."
metadata:
  version: "1.1"
  product: "Resource Hero"
  productVersion: "16.2"
  domains: ["User"]
  relatedSkills:
    - "rh-user-time-dashboard"
  sources:
    - "https://www.resourceheroapp.com/support/enhanced-time-tracking-component/"
---

# Log your time in Resource Hero

## Overview

Resource Hero keeps logged time as time entries on the user's assignments. The Resource Hero
MCP extension gives each user tools that work on their own assignments and time only: list
assignments, list, log, change and delete time, run timers, read their forecast and capacity,
and request or cancel time off. This skill drives those tools. It never changes forecasts,
capacity or holidays, and it never sets a time off request's status itself.

## When to use

- "Log 3 hours to Acme Implementation today."
- "I worked 6 hours on the Smith project yesterday, 4 billable."
- "Change Tuesday's time on Project X to 2.5." / "Delete row 3."
- "What did I log this week?" / "Which projects am I on?"
- "Start a timer on Acme." / "Stop my timer."
- "What am I scheduled for next week?" / "When do I have time free this month?"
- "Request next Friday off." / "Cancel my time off request for the 14th."

## Before you start

- The user's Resource Hero server is added and signed in. Its tools are named
  `mcp__resource-hero__<tool>`. If they are missing, the user adds the server (see the
  `rh-connect-setup` skill); if they report "Needs authentication", the user runs `/mcp` and
  signs in to **resource-hero**.
- Everything runs as the user. Salesforce sharing, field security and the org's validation
  rules and flows apply as they do in Resource Hero's Time Tracking component.

## Calling the tools

Tool names depend on how the admin built the server: `getMyAssignments`, `GetMyAssignments`,
or a generated name such as `rhamcp_GetMyAssignmentsapex_rhamcp_GetMyAssignments`. Find each
tool by the action name in it, ignoring case; this skill uses the camelCase form.

Salesforce wraps every tool. Put the arguments inside an `inputs` list with one object, and
read the reply from `outputValues` of the first result:

```json
// call
{"inputs": [{"search": "Acme"}]}
// reply
[{"isSuccess": true, "outputValues": {"success": true, "assignments": [ … ]}}]
```

When `success` is false, show `errorMessage`. The `errorCode` tells the user who fixes it:

| Code | Meaning |
|---|---|
| NO_RESOURCE, MULTIPLE_RESOURCES | The admin links exactly one active Resource to the user. |
| NOT_LICENSED | The admin assigns a Resource Hero license. |
| NO_ACCESS | The admin assigns the Resource Hero MCP User permission set. |
| INVALID_INPUT | Fix the request (date format, hours, notes over 500 characters). |
| NOT_FOUND, NOT_YOUR_RESOURCE | List again; the Id is stale or not the user's. |
| READ_ONLY | The assignment's project or opportunity is marked read only in Resource Hero, so no time can be logged or changed on it. Say that plainly ("read only", not "locked") and pick another assignment; a project manager or admin can unmark it. |
| ARCHIVED | The assignment is archived and takes no new time; pick another. |
| TIME_OFF_STATE | That time off request is already approved, cancelled or rejected. Approved time off is changed by the approver. |
| CORE_RULE, ORG_RULE | A Resource Hero rule or the org's own rule refused it (a locked period, required notes). Show the message as is; the admin owns those rules. |

Write tools save each entry on its own and return one result per entry (`results`, with
`savedCount` and `failedCount`). Report each failed entry with its message.

## The tools

| Tool | Use |
|---|---|
| `getMyAssignments` {search} | Open assignments with `assignmentId`, `assignedTo`, `role`, `readOnly`. |
| `getMyTrackedTime` {startDate, endDate} or {daysBack, daysAhead} | Time entries with `timeEntryId`, `hours`, `billable`, `category`, `notes`, `kind`, plus `totalHours` and `billableHours`. |
| `insertActuals` {entries: [{assignmentId, entryDate, hours, notes, billable, category}]} | Log new time. |
| `updateActuals` {entries: [{timeEntryId, …only the fields to change}]} | Change logged time. |
| `deleteActuals` {timeEntryIds, clearActualOnly} | Delete logged time. |
| `getMyTimers`, `startTimer` {assignmentId, targetDate, notes}, `pauseTimer`, `stopTimer` {notes, billable}, `cancelTimer` | Timers. Omit `timerId` when the user has one active timer. |
| `getMyForecast` {weeksBack, weeksAhead} | Planned hours, one row per day and assignment, with `kind` (Project, Holiday, TimeOff) and `totalHours`. Default: this week and 4 ahead. |
| `getMyCapacity` {weeksBack, weeksAhead} | Every day's `capacityHours`, `forecastHours`, `actualHours`, `holidayHours`, `timeOffHours` and `availableHours` (capacity minus forecast). |
| `getMyTimeOff` {weeksBack, weeksAhead} | Holidays and time off requests with `timeOffRequestId` and `status`. Default: this week and 12 ahead. |
| `requestTimeOff` {startDate, endDate, hoursPerDay, type, description} | Request time off. It gets the org's default status; the reply's `status` says which. |
| `cancelTimeOff` {timeOffRequestId} | Cancel an Open or Submitted request. |

Lists are numbered (`rowNumber`). Show them as a table with a # column; when the user names a
row, use that row's Id from the most recent list.

## Log time

1. Resolve relative dates ("yesterday", "Tuesday") to YYYY-MM-DD in the user's time zone and
   show the date. Hours are a number with up to two decimals ("1h 30m" is 1.5).
2. Call `getMyAssignments`, with `search` when the user named a project. Match the name
   against `assignedTo`. If more than one matches or none does, show the list and ask. Never
   guess between two matches. A `readOnly` assignment can't take time; say so.
3. Show one line per entry and wait for a yes:

   | Date | Assignment | Hours | Billable | Category | Notes |
   |---|---|---|---|---|---|

4. Call `insertActuals` with all confirmed entries in one call. Each call adds a new entry,
   even when the user already has time on that assignment and date; several entries per day
   are normal. Pass `billable`, `category` and `notes` only when the user gave them (billable
   otherwise follows the org's default).
5. Show the saved entries with `getMyTrackedTime` for the affected dates.

"Log 2 more hours" is a new entry. "Make Tuesday 2 hours" changes the existing entry: use
Change time.

## Change or delete time

1. Call `getMyTrackedTime` for the dates in question and show the numbered list.
2. Find the entry the user means. Entries with `kind` Holiday or TimeOff come from holiday
   schedules and approved time off; they can't be changed here.
3. Show the change (before and after) or the entries to delete, and wait for a yes.
4. Call `updateActuals` with only the changed fields (an empty string clears notes or
   category), or `deleteActuals` with the Ids.
5. If a delete fails with OTHER_MEFS_POPULATED, the entry also holds planning values such as
   forecast hours. Explain that, and with the user's yes retry with `clearActualOnly: true`,
   which removes the logged hours and notes and keeps the plan.

## Review time

Call `getMyTrackedTime` for the range ("this week" is Monday to Sunday) and show a
day-by-assignment table with daily totals, `totalHours` and `billableHours`. Show holiday and
time off hours apart from project hours.

## Timers

- **Start:** find the assignment as in Log time, then `startTimer`. Starting a timer on an
  assignment with a paused timer resumes it.
- **Pause:** `pauseTimer`. **Status:** `getMyTimers` shows elapsed time and the hours stopping
  now would log after the org's rounding.
- **Stop:** `stopTimer` logs the time as a new entry; pass `notes` and `billable` if the user
  gave them.
- **Cancel:** discards the tracked time and logs nothing. Confirm first, then `cancelTimer`.

## Forecast and capacity

- **"What am I scheduled for?"** Call `getMyForecast` for the weeks asked and show a
  day-by-assignment table of planned hours. Show holiday and time off rows apart from project
  work.
- **"When do I have time?" / "How booked am I?"** Call `getMyCapacity` and show the days with
  their capacity, planned hours and `availableHours`. Negative available hours mean the user is
  overbooked that day.
- For planned against logged, put `getMyForecast` beside `getMyTrackedTime` for the same dates.

These are read only: the user can't change their forecast or capacity here.

## Time off

- **Request:** resolve the dates to YYYY-MM-DD in the user's time zone. Ask for the hours per
  day if the user didn't say (usually their working day, such as 8; 4 for a half day) and the
  type if they want one (normally Vacation, Sick or Personal Day). Show the dates with weekdays,
  hours per day and type, and wait for a yes. Then `requestTimeOff`. Tell the user the request's
  `status` from the reply: the org decides whether new requests are approved right away or wait
  for approval.
- **Cancel:** call `getMyTimeOff` (widen `weeksAhead` if needed), find the request, show it and
  wait for a yes, then `cancelTimeOff` with its `timeOffRequestId`. Only Open or Submitted
  requests can be cancelled here.
- Holidays come from the org's holiday schedule; they can't be requested or cancelled.

## Sources

- https://www.resourceheroapp.com/support/enhanced-time-tracking-component/ (modified 2026-02-18)
