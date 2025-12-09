# Copilot Instructions for QQ Chat Bot

## Big Picture

- Built on the `ncatbot` package: `BotClient` (`ncatbot/core/client.py`) wires NapCat websocket events -> `Adapter` -> `EventBus` -> plugins -> `BotAPI` for outbound actions.
- `Adapter` (`ncatbot/core/adapter/adapter.py`) keeps a single websocket to NapCat, turns `post_type` payloads into typed events, and routes them by `OFFICIAL_*` keys; event callbacks are fire-and-forget async tasks.
- Plugin system (`ncatbot/plugin_system`) is first-class: loader pulls built-ins (`SystemManager`, `UnifiedRegistryPlugin`) then external plugins from `plugins/`, resolves dependencies, enforces version constraints, and persists RBAC to `data/rbac.json`.
- Default entrypoint `main.py` shows direct decorators on `BotClient`; for anything nontrivial prefer plugins so hot-reload and dependency handling work.

## Running & Debugging

- Python 3.8+ (Windows prefers 3.12). Run the bot with `python main.py`; `BotClient.run()` blocks the main thread and ensures NapCat is up before connecting.
- Config is loaded from `config.yaml` (see sample in repo). The helper setters in `ncatbot.utils.config` (`set_bot_uin`, `set_root`, `set_ws_uri`, `set_ws_token`, `set_webui_uri`, `set_webui_token`) update `ncatbot_config` and persist on validation.
- NapCat service bootstrap (`ncatbot/core/adapter/nc/launch.py`):
  - Local mode (default) auto-installs/updates NapCat, configures it, starts it, then performs QR/fast login via WebUI when enabled.
  - Remote mode (`napcat.remote_mode: true`) skips local install and only connects; if tokens/QQ mismatch, raises `NcatBotLoginError`.
  - Websocket URL sent as `ws_uri/?access_token=<token>`; failure to connect triggers reconnect with timeout `websocket_timeout` in config.

## Event Handling (BotClient)

- Only one `BotClient` instance is allowed (`_initialized` guard). Use decorators `@bot.private_event()`, `@bot.group_event()`, `@bot.notice_event()`, etc.; filters accept `MessageSegment` subclasses to prefilter.
- Handlers are executed concurrently via `asyncio.create_task`; they must be async-safe and tolerate out-of-order completion. Returning values is ignored at this layer; side effects should go through `bot.api`.
- `Adapter` converts NapCat payloads into event classes (`PrivateMessageEvent`, `GroupMessageEvent`, `NoticeEvent`, `RequestEvent`, `MetaEvent`, `MessageSentEvent`); `meta_event` with `connect` triggers startup handlers.

## Plugin System Patterns

- Create plugins in `plugins/`. Each module must export plugin classes in `__all__`; each class inherits `BasePlugin`, defines `name` and `version`, and optional `dependencies` (uses `packaging` specifiers).
- Plugin lifecycle hooks: `_init_` / `_reinit_` / `_close_` (sync) and `on_load` / `on_reload` / `on_close` (async). Config per plugin is read/written as YAML at `data/<plugin>/<plugin>.yaml` during `__onload__`/`__unload__`.
- Subscribe to events via `self.register_handler(event_type, handler, priority=0, timeout=None)` or the decorators in `plugin_system/decorator.py`:
  - `@register_handler(event_type, priority, get_event=True)` receives `NcatBotEvent` or raw data (when `get_event=False`).
  - `@register_server(addr)` exposes a request-style handler reachable via `await plugin.request(addr, data)`.
- Event types are free-form strings; for NapCat passthrough use constants like `OFFICIAL_PRIVATE_MESSAGE_EVENT`, `OFFICIAL_GROUP_MESSAGE_EVENT`, etc. Regex subscriptions are supported by prefixing `re:`.
- EventBus (`plugin_system/event/event_bus.py`) runs handlers concurrently with per-handler timeouts (default 120s); exceptions and timeouts are collected on the event object.

## Bot API Usage

- `bot.api` is a `BotAPI` composed from `AccountAPI`, `GroupAPI`, `MessageAPI`, `PrivateAPI`, `SupportAPI` (`ncatbot/core/api`). Methods send actions over the websocket via `Adapter.send`, expecting OneBot-style responses (`status`, `retcode`, `data`).
- Calls are async; when invoked from sync code, use `asyncio` helpers (e.g., run inside async handlers or wrap with `asyncio.run` only in top-level scripts).

## Data & Conventions

- Global config and state live in `config.yaml` and `ncatbot.utils.status`; tokens for NapCat WebSocket/WebUI are stored here—keep them secret.
- Plugins store runtime data under `data/` and configs under `config/` by default (`PluginSystemConfig` in `plugin_system/config.py`).
- RBAC state is persisted in `data/rbac.json`; `PluginLoader` injects `RBACManager` into plugins, so role changes should be saved via loader shutdown/unload paths.
- Message filtering: `GroupMessageEvent`/`PrivateMessageEvent` expose `event.message.filter(filter)` used in `BotClient` wrappers—provide a `MessageSegment` subclass to limit handler invocations.

## Gotchas

- Adapter’s websocket loop is long-lived; unhandled exceptions in callbacks can tear down the connection—catch/log inside handlers.
- `skip_plugin_load` (config) disables external plugins but still loads built-ins; useful for debugging `main.py` handlers.
- Because events are fan-out async, avoid shared mutable state without locks; prefer plugin-local data files or per-event context.
