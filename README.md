# Resource Hero Agent Toolkit

Plugins that let people log, review and chart their own time in
[Resource Hero](https://www.resourceheroapp.com), the Salesforce-native resource management
app, by asking Claude, in Claude on the web and desktop or in Claude Code.

- "Log 2 hours to Acme Implementation today, notes: design review."
- "What did I log this week?" / "Change row 2 to 1.5 hours."
- "Start a timer on Acme." / "Stop my timer."
- "How does my week look?" / "Build me a dashboard of my time."
- "Request next Friday off." / "When do I have time free this month?"

Claude connects to a Salesforce-hosted MCP server in your own org that offers only the
Resource Hero MCP extension's tools. Every call runs as the signed-in user, who sees and
changes only their own time, under your org's sharing, field security, validation rules and
flows. Requires Resource Hero 16.2 or later and the Resource Hero MCP extension 0.1, which is
in limited release.

## Get started

1. **Your Salesforce admin** sets up the org once: [admin setup guide](docs/setup-guide.md).
   They send you a server URL and a consumer key.
2. **You** connect Claude and sign in: [user guide](docs/user-guide.md). In Claude Code:

```
/plugin marketplace add Resource-Hero/rh-agent-toolkit
/plugin install rh-user@resource-hero
```

## Plugins

| Plugin | Covers |
|---|---|
| `rh-user` | `rh-user-log-time`: log, change, delete and review your time, run timers, check your forecast and capacity, and request or cancel time off. `rh-user-time-dashboard`: a ready-made live page of your week where you can log and edit time, tap-log time and run timers, plus your upcoming holidays and time off, with links to your records. |
| `rh-connect` | `rh-connect-setup`: the admin setup steps, the command each user runs to add the Resource Hero server to Claude Code, and sign-in troubleshooting. Installed with `rh-user`. |

The skills follow the [Agent Skills](https://agentskills.io/) format, so other agent tools
that support it can use the folders under `plugins/*/skills/` too.

## Layout

```
.claude-plugin/marketplace.json   # the resource-hero marketplace
docs/                             # admin setup guide and user guide
plugins/
  rh-user/skills/                 # rh-user-log-time, rh-user-time-dashboard
  rh-connect/
    skills/rh-connect-setup/      # admin setup; assets/ holds the server definition and
                                  # External Client App templates
tools/check.py                    # repository checks run in CI
tools/run_evals.sh                # routing evals for a plugin
```

## Support

The plugins and the Resource Hero MCP extension are supported by Resource Hero.
[Request assistance](https://www.resourceheroapp.com/contact/).

## License

MIT. See [LICENSE](LICENSE).
