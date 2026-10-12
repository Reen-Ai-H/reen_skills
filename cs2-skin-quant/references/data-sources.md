# Compliant data sources

Revalidate these sources at runtime. Fees, endpoints, restrictions, and platform access can change without notice.

## Required source hierarchy

1. Official Valve/Steam rules and announcements.
2. Official platform API or help center.
3. Public price aggregators for discovery only.
4. User-provided screenshots or exports, clearly labeled as such.

Never substitute an unofficial scraper when a source blocks automated access.

## Valve and Steam

- Subscriber Agreement: <https://store.steampowered.com/agreement/?l=english>
- Trading and Market Restrictions: <https://help.steampowered.com/en/faqs/view/451E-96B3-D194-50FC>
- Community Market FAQ: <https://help.steampowered.com/en/faqs/view/61F0-72B7-9A18-C70B>
- Trade Protection FAQ: <https://help.steampowered.com/en/faqs/view/365F-4BEE-2AE2-7BDD>
- CS2 announcements: <https://store.steampowered.com/news/app/730>

Check these before relying on cooldown, fee, reversibility, or automation assumptions. Do not automate Steam interaction.

## Discovery and verification

### CSQAQ

- Documentation: <https://docs.csqaq.com/>
- API base URL: `https://api.csqaq.com/api/v1`.
- Send the user token only in the documented `ApiToken` request header.
- Read the token from `CS2_CSQAQ_API_TOKEN` when set; otherwise use the first
  `CS2_CSQAQ_API_TOKEN=...` entry in
  `~/.config/cs2-skin-quant/secrets.env`. Keep that directory at mode `0700`
  and the file at mode `0600`.
- Never print, log, summarize, or copy the token into a project file. Use
  `scripts/csqaq_api.py --health` to test authentication without exposing it.
- The official whitelist binding endpoint is
  `POST /sys/bind_local_ip`. Rebinding changes account state, so do it only
  when the user explicitly asks to configure or repair API access.
- Respect the documented limit of one request per second per IP.
- Steam buy-order 挂刀 definition: `third-party lowest price / (Steam buy order × 0.869)`.
- Treat aggregator refresh intervals as discovery latency. Reconfirm executable bids before recommending an order.

### C5GAME OpenAPI

- Documentation: <https://opendoc.c5game.com/> (machine-readable index: <https://opendoc.c5game.com/llms.txt>)
- Production base URL: `https://openapi.c5game.com`.
- Authentication is the query parameter `app-key`; current official docs state there is no signature mechanism. Never put it in a URL shown to the user, logs, or chat.
- Read the key from `CS2_C5_API_KEY` when set; otherwise use the first `CS2_C5_API_KEY=...` entry in `~/.config/cs2-skin-quant/secrets.env` (directory `0700`, file `0600`).
- Current official notice requires an `Accept-Encoding: gzip, br, zstd, deflate` header. Use [scripts/c5_api.py](../scripts/c5_api.py) so response compression and key handling are centralized.
- For screening prefer the released read-only endpoint `POST /merchant/market/v2/item/stat/hash/name` (up to 100 names; returns lowest sell price/count and highest buy price/count) and `GET /merchant/purchase/v1/max-price`. The batch minimum-price endpoint is currently marked developing; the old condition-list endpoint is obsolete and has stricter throttling.
- Default platform limit is documented as 50 QPS, but obey any endpoint-specific limit and back off on errors. Never call purchase, listing, repricing, delivery, or withdrawal endpoints from the Skill.
- Query current per-order fees rather than relying on old public fee tables.

### YouPin

- Fee standard: <https://h5.youpin898.com/pc/chargeStandard.html>
- User agreement: <https://protocol.youpin898.com/youpin/youpin-sysconfig/uu898_20240724153416_64.html?id=1&position=8>
- Use for the user's manual visible checks and transactions during validation.
- Do not bypass robots, anti-crawl controls, or undocumented access restrictions.

### Web-only platforms (YouPin / BUFF)

- Read [references/web-market-visibility.md](web-market-visibility.md) before using a web-only source.
- A browser-visible page is a timestamped observation, not an API feed. Preserve URL, visible fields, screenshot/OCR provenance, and data age.
- If no compliant page is accessible, do not substitute scraping or an unofficial API; return `INSUFFICIENT COMPLIANT DATA`.

## Optional comparison sources

- BUFF fee help: <https://buff.163.com/help/page?slug=N_fees_new&platform=0>
- BUFF withdrawal help: <https://buff.163.com/help/page?slug=N_charge_withdraw_new&platform=0>
- IGXE fee help: <https://www.igxe.cn/help/235>
- cs2.sh API reference: <https://cs2.sh/zh-cn/docs/api-reference/prices-latest-post>

Use these only after confirming current accessibility and terms. Do not treat a lack of public API as permission to scrape.

## Snapshot requirements

For every candidate preserve:

- item market name and exact variant;
- source URL or documented endpoint;
- timezone-aware timestamp in Asia/Shanghai unless the API provides UTC;
- executable bid and quantity;
- lowest listing for spread context only;
- top-three bid depth;
- 30-day average daily volume and its definition;
- all fee and withdrawal assumptions;
- data age in minutes;
- whether the observation was API-derived, browser-visible, or user-provided.

If two sources disagree materially, use the more conservative executable value or return `INSUFFICIENT COMPLIANT DATA`.
