# Claude for Small Business: the 20-minute setup

Set up the new Claude (Cowork is now built in) with Anthropic's free Small Business plugin, without connecting your bank or email. One file tells Claude about your business, four spreadsheet exports replace the connectors, and each day of the week gets one command.

📺 Video walkthrough on [YouTube @workflowkitchen](https://www.youtube.com/@workflowkitchen) (premieres Nov 3, 2026)

## What's inside

| File | Job |
|---|---|
| `about-my-business.md` | Half a page about your business: what you sell, customers, prices, tone, who approves money, weekly jobs. Paste it into your Claude project's instructions |
| `demo-data/square_sales_oct2026.csv` | Daily sales by category, as exported from Square |
| `demo-data/quickbooks_invoices.csv` | Invoice list, as exported from QuickBooks |
| `demo-data/bank_statement_oct2026.csv` | One month of bank transactions |
| `demo-data/customers.csv` | Customer list with payment habits |
| `demo-data/catering_inquiry.txt` | A sample quote request for `/proposal-builder` |

All demo data belongs to **Maple Street Bakery**, a made-up bakery in Austin, TX. It's there so you can try every command before you upload your own files. The planted problems: $7,060 in overdue invoices, a missing Square payout, a double charge and three expenses with no receipts. See if Claude finds them.

## Setup (about 20 minutes)

**You need:** a paid Claude plan (Pro is $20/month). The free plan doesn't include the plugin.

1. **Safety first.** Settings → Privacy → decide on "Help improve our AI models". Under the message box, set the permission mode to **Manual** while you're learning.
2. **Create a project** (Projects → New project). Paste `about-my-business.md`, with your own details, into the project instructions.
3. **Add your files** to the project: exports from Square, QuickBooks, your bank and your customer list. Or use the demo files first.
4. **Install the plugin:** Customize → Plugins → search "small business" → Add. (The "Install in Cowork" button on claude.com opens the desktop app; in a browser, use Customize.)
5. In the project, type `/smb-onboard` and add: *"Don't connect any apps yet. Use the files in this project."*

## Your week

| Day | Command | What you get |
|---|---|---|
| Mon | `/monday-brief` | Cash, last week's sales and who owes you, on one page |
| Tue | `/invoice-chase` | Reminder drafts with a tone for each customer. Nothing is sent |
| Wed | `/proposal-builder` + paste the inquiry | A priced quote from your price list (DOCX + PDF) |
| Thu | `/social-content-engine` | Next week's posts, based on what actually sold |
| Fri | `/close-month` | Bank vs. sales check and a list of what to fix before you call your accountant |

Plain words work too: "who owes me money" starts the same skill as `/invoice-chase`.

## What it cost in our test (October 2026)

Setup plus all five commands took **7% of one 5-hour session** on the Max 5x plan. On Pro that's roughly **35% of one session** (an estimate; we didn't measure on Pro).

To make your limit last: ask quick questions in plain chat, group related jobs into one task, start a new chat for unrelated work.

## Not working? Quick fixes

| Problem | Fix |
|---|---|
| No "Cowork" tab | Normal. Cowork was merged into Claude in September 2026. If your message box still shows Chat and Cowork, you're on the old version; everything here works on both |
| Typing `/` on the project page opens search | Click inside the message box first |
| Pages or Numbers files | Export to Excel, CSV or PDF first |
| `/close-month` won't close the month | That's on purpose: it needs real books. Export **P&L** and **Transaction Detail** from QuickBooks |

## Scheduling

Scheduled → New task → weekly, Monday → `/monday-brief`. Scheduled tasks run **without pausing for approval**, so schedule the reading and the drafting only. Keep anything that sends, pays or deletes manual.
