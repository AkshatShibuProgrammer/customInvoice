# Portable Invoice Workspace

## The Single HTML File

The production artifact is **`dist/index.html`**. It contains the application JavaScript, React runtime, styles, invoice images, and all three supplied Canvas integration functions. There are no external script, stylesheet, or image dependencies. Only this HTML file needs to be distributed.

The **Download HTML** button creates `eternal-invoice-generator.html`. It can include current orders and restaurant/address profiles, or open with empty lists. Shared company settings are included in either case. Conversations and unapproved AI drafts are excluded. Each export has its own browser-storage namespace, so another workspace's saved data does not replace its embedded snapshot.

In the development preview, the download action reads the already-generated production HTML through Vite's raw-module endpoint. The production build must exist. In the built or downloaded application, export uses its embedded scripts and CSS and makes no network request.

## Manual And AI Modes

- Manual mode retains the order editor, reusable profiles, shared settings, automatic totals, and restaurant/platform invoice templates.
- The AI assistant uses `geminiGenerateText` to extract a structured multi-order draft from a conversation. It can reuse explicitly requested saved profiles or collect new ones, including different dates and optional local times.
- The assistant asks for missing or ambiguous details. Schema and business validation run locally; model-provided totals are not trusted.
- Defaults and locally generated reference numbers are disclosed in the review. They can be disabled. Registration numbers, prices, and customer details are not filled from invented values.
- Approval adds new orders and any new profiles without rewriting existing invoices. The manual editor opens afterward. Printing requires a separate action.
- A draft is not printable or addable while a request is pending, after a failed refinement, or while required fields/questions remain unresolved.

## Supplied Integrations

The three user-supplied functions are copied unchanged into the `gemini-canvas-integration` script in `index.html`. All API keys remain blank. Search and image generation are retained, but are not used for invoice detail collection. There are no replacement provider API calls and no API-key entry UI.

Google's public Gemini API requires authentication. Blank keys only work if the host runtime actually supplies the interception/authentication behavior described by the user. This behavior cannot be verified or provided by a downloaded HTML file. The application explains authentication/network failures and leaves the manual editor available. AI requires internet; manual editing and printing do not.

Sending a message transmits the current conversation and working draft, plus saved profiles and up to 30 recent orders if saved-context sharing is enabled. Turning off sharing stops attaching the saved context; information already in the conversation remains part of it until a new conversation is started.

## Print And Data Notes

The restaurant invoice retains its banner, signature, FSSAI hyperlinks, and Section 9(5) note. Optional order time is shown only when supplied. Printing uses the preview's CSS and directly extracts invoice roots, avoiding wrapper-related page breaks. Long invoices are allowed to continue instead of being clipped to a fixed-height box. Recommended browser settings: A4, 100% scale, no browser headers/footers, no additional margins.

Browser storage is best-effort, especially for local files and private browsing. If storage is unavailable, the UI reports session-only mode. Download a new HTML copy with current data to make a portable snapshot. An exported file contains customer and business data when that option is enabled; share it carefully.

## Verification

The production build and single-file output structure were checked. Live Canvas authentication and browser interactions, including print/PDF and download round-tripping, require testing in the target browser and were not exercised in this environment.

Suggested browser acceptance checks:

1. Open `dist/index.html` offline; manually edit a price, duplicate an order, switch its profile/date/time, and print.
2. Download with current data, reopen the file, and verify the snapshot restores; download without data and verify order/profile lists start empty.
3. In a supported Canvas runtime, use the two-order example and verify the restaurant food total is INR 407.40 per order, with a separate INR 17.582 platform invoice.
4. Omit an address or food price, answer the assistant's follow-up, and confirm that approval stays disabled until the draft is complete and reviewed.
5. Test malformed AI output, invalid dates, negative amounts, excessive discounts, duplicate invoice references, expired saved-profile IDs, and an unauthorized API response. None should silently change saved orders.
6. Verify late responses after Stop waiting or Start new conversation are ignored, and a draft cannot be added twice by double-clicking.
7. Confirm multiple invoice page breaks, banner/signature loading, and both FSSAI PDF links in the intended browser/printer.