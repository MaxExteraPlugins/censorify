# -*- coding: utf-8 -*-
__id__ = "censorify"
__name__ = "Censorify"
__description__ = "Locally replaces profanity with selected characters in all messages."
__version__ = "1.6.4"
__min_version__ = "12.10.6"
__author__ = "@itNotMax - @MaxExteraPlugins"
__icon__ = "MaxExteraPluginsStickers/15"

import re
from typing import List, Any
from base_plugin import BasePlugin, MethodHook
from hook_utils import find_class, set_private_field
from ui.settings import Header, Selector, Input, Divider, EditText

_PATTERNS = [
    r"(?:(?:за|на|вы|по|пере|при|у|под|от|об|с|в|раз|рас|про|из|ис|до|не|бес|без|вз|недо)?[её]б(?:а(?:т(?:ь(?:ся)?)?|н\w*|л\w*|ш\w*|щ\w*)?|у[чтн]\w*|[её][тш]\w*|и\w*|л\w*|н\w*|ут\w*|ок|ка|ке|ки|ку|ств\w*|ущ\w*|ач\w*|ал\w*|ну\w*|[её]ж\w*|ист\w*)?)",
    r"[хx][уy][ёеeийяюалонтсьвщж]\w*",
    r"[хx][уy][йj]\w*",
    r"(?:(?:за|на|вы|по|при|у|под|от|об|с|в|раз|рас|про|из|до|не)?[хx][уy](?:[ёеeийяюалонтсьвщж]\w*|[йj]\w*))",
    r"[пp][иieё][зz3][дd][аaеёоуыюяc]\w*",
    r"(?:(?:за|на|вы|по|при|у|под|от|об|с|в|рас|про|из|до|не|пере)?[пp][иieё][зz3][дd](?:[аеёиоуыюя]\w*|ец\w*|[ёе]ж\w*|юк\w*|юл\w*)?)",
    r"[бb][лl][яыь][дd]\w*",
    r"(?:(?:за|на|по|от|вы|у|при|под|рас|из|об|не|про)?[бb][лl][яыь][дd]\w*)",
    r"(?:(?:за|на|по|вы|от|при|под|об|про|у|из|не|рас)?[мm][уy][дd](?:[аоиеёыюя]\w*|ак\w*|ил\w*|озвон\w*|охат\w*))",
    r"(?:(?:за|вы|от|на|по|при|под|не)?[сs][уy][чc](?:[аиьеёкйю]\w*|онок\w*|ар\w*)?)",
    r"[гg][аa][нn][дd][оo][нn]\w*",
    r"(?:(?:за|на|по|от|вы|про|при|под|об|у)?[дd][рpr][оo][чc](?:[иеёаул]\w*|к\w*|ил\w*)?)",
    r"[мm][аa][нn][дd][аaоуыеёюя]\w*",
    r"(?:(?:за|на|по|от|про)?[шщ][лl][юy][хx]\w*)",
    r"(?:(?:за|от|на|вы|по|пере|у|про|при|под|об)?[тt][рpr][аa][хx](?:[аеёиоуыьюян]\w*)?)",
    r"[зz][аa][лl][уy][пp]\w*",
    r"(?:(?:за|от|на|по|вы|про|при|под|у)?[жj][оo][пp](?:[аеёиоуыьюян]\w*)?)",
    r"[дd][еe][рpr][ьъ][мm]\w*",
    r"(?:(?:на|за|по|от|вы|у|про|об|до|при|под)?[сs][рpr][а][тtнл]\w*)",
    r"[сs][рpr][а][кн]\w*",
    r"(?:(?:за|на|по|у|ис|вы)?[пp][еe][рpr][дd](?:[ёеиуноьэ]\w*)?)",
    r"[пp][аa][дd][лl][аaоеы]\w*",
    r"[дd][аa][лl][бb][аa]?[ёе][бb6]\w*",
    r"долб[оа]?[ёеe][бb6]\w*",
    r"(?:(?:за|на|по|от|вы|у|про|при|не)?[нn][аa][хx][уy][ёеийяю]\w*)",
    r"(?:(?:за|на|по|от|вы|у|про|при)?[оo][хx][уy][ёеийетюялн]\w*)",
    r"[аa][хx][уy][ёеийетюялн]\w*",
    r"[зz][аa][ёеe][бb6]\w*",
    r"[оo][тt][ъь]?[ёеe][бb6]\w*",
    r"[уy][ёеe][бb6]\w*",
    r"[вv][ъь]?[ёеe][бb6]\w*",
    r"[нn][аa][ёеe][бb6]\w*",
    r"[пp][оo][ёеe][бb6]\w*",
    r"[рpr][аa][зz][ъь]?[ёеe][бb6]\w*",
    r"[сs][ъь]?[ёеe][бb6]\w*",
    r"[пp][рpr][оo][ёеe][бb6]\w*",
    r"[пp][рpr][и][ёеe][бb6]\w*",
    r"[вv][ыy][бb][лl][яыь][дd]\w*",
    r"[шщ][аa][лl][аa][вv]\w*",
    r"[кk][уy][рpr][вv][аоыеёиьюя]\w*",
    r"[пp][оo][тt][аa][сs][кk]\w*",
    r"[пp][оo][тt][аa][шщ][кk]\w*",
    r"[пp][рpr][оo][сs][тt][иi][тt][уy][тt]\w*",
    r"[чc][мm][оo](?!к)\w{0,6}",
    r"[чc][мm][ыy][рpr]\w*",
    r"[бb][зz][дd][еёиыуюян]\w*",
    r"[пp][иi][дd][аa][рpr]\w*",
    r"[пp][иi][дd][оo][рpr]\w*",
    r"[пp][еe][дd][еe][рpr][аa][сs][тt]\w*",
    r"[гg][оo][вv][нn][оаеёиуыюя]\w*",
    r"[ёеe][бb6][аa][нn]\w*",
    r"[ёеe][бb6][лl][оаиыу]\w*",
    r"[ёеe][бb6][уy][чc]\w*",
    r"[ёеe][бb6][кk]\w*",
    r"[мm][иi][нn][ёеe][тt]\w*",
    r"(?:(?:за|от|на|по|вы|у|при|про|не|под)?[хx][ёеe][рpr](?:н[яиеёоау]\w*|ов\w*|ач\w*|[её]т\w*|ит\w*|ан\w*|ню\w*|от\w*))",
    r"[зz][аa][сs][рpr][аa][нn]\w*",
    r"[зz][аa][сs][еe][рpr]\w*",
    r"[пp][оo][хx][уy](?:й|ист\w*|изм\w*|ю)",
    r"[хx][уy][еe][сs][оo][сs]\w*",
    r"[хx][уy][еe][пp][лl][ёеe][тt]\w*",
    r"[хx][уy][еe][тt][аеё]\w*",
    r"[хx][уy][ёеe][вv]\w*",
    r"[хx][уy][яыь]\w+",
    r"[хx][уy][ил][иь]?\w{1,5}",
    r"[еe][бb6][аa][тt](?:ь(?:ся)?|ься)?\w*",
    r"[еe][бb6][аa][лl][ьъ]?\w*",
    r"[ёеe][бb6][ёеe]\w*",
    r"[ёеe][бb6][иi]\w*",
    r"[ёеe][бb6][нn]\w*",
    r"[ёеe][бb6][сs]\w*",
    r"[ёеe][бb6][уy]\w*",
    r"сука\w*",
    r"суки\w*",
    r"сукин\w*",
    r"бля(?:дь|ть|ди|дин\w*|дск\w*|дств\w*|дов\w*|дищ\w*|дух\w*|дёж\w*|дун\w*|ха\w*|)",
    r"ебл[аоиыу]\w*",
    r"[ёе]бл[аоиыу]\w*",
    r"[пp][иi][зz][дd](?:ат\w*|ец\w*|ан\w*|ёж\w*|юк\w*|юл\w*|як\w*|ос\w*|ош\w*)",
]

_EXACT = [
    "бля", "блять", "блядь", "блядина", "сука", "нахуй", "нахуя", "похуй", "похую",
    "охуеть", "ахуеть", "хуй", "хуя", "хуё", "хуи", "хую",
    "пизда", "пиздец", "пиздёж",
    "ебать", "ёбаный", "ёбаная", "ёбаное", "ёбаные",
    "мудак", "мудила", "мудень", "мудозвон",
    "залупа", "шлюха", "дрочить", "дрочила",
    "сучка", "сучара", "сучий",
    "гандон", "гондон",
    "пидор", "пидар", "пидорас", "педераст", "педик",
    "говно", "говнюк", "говнище",
    "ёбт", "пздц",
    "херня", "херов", "хуёвый", "хуёво",
    "жопа", "жопу", "жопой", "жопе",
    "дерьмо", "дерьмовый",
    "сраный", "сраная", "сраное", "сраные",
    "срань", "засранец", "засранка",
    "ублюдок", "ублюдки",
    "выблядок", "шалава", "потаскуха", "курва", "минет",
    "долбоёб", "долбаёб", "мандавошка",
    "хуесос", "хуеплёт",
    "ёбарь", "пиздобол", "пиздолиз", "хуйня",
    "ёбнутый", "ёбнутая", "ёбнутое", "ёбнутые",
    "уёбок", "уёбище", "мудоёб", "хуеглот",
    "ёбаловка", "ёбанат", "блядюга", "хуёвина",
    "пиздюк", "пиздюлина", "мандюк", "подзалупный",
    "ёбнуть", "ёбнул", "ёбнула", "наёбка", "проёб",
    "отъебись", "заебал", "заебала", "заебали", "заебись",
    "охуенно", "охуенный", "нихуя", "нихера", "похер",
    "перехуярить", "расхуярить", "разъебать",
    "объебать", "выебать", "выебон",
    "ёбля", "поебень", "мудачьё", "мудачка", "мудачина",
    "пиздатый", "пиздато",
]


def _build_re():
    parts = list(_PATTERNS)
    for w in _EXACT:
        parts.append(re.escape(w) + r"\w*")
    combined = "|".join(parts)
    return re.compile(
        r"(?<![а-яёa-z])(?:" + combined + r")(?![а-яёa-z])",
        re.IGNORECASE | re.UNICODE,
    )


_RE = _build_re()
_LEET_TABLE = str.maketrans('036@$!1', 'обзасии')

_cfg_mode = 0
_cfg_char = "#"
_cfg_phrase = "[censored]"
_custom_re = None
_custom_words_cache = ""
_cache = {}
_CACHE_MAX = 4096


def _clear_cache():
    _cache.clear()


def _rebuild_custom_re(raw):
    global _custom_re, _custom_words_cache
    if raw == _custom_words_cache:
        return
    _custom_words_cache = raw
    _clear_cache()
    words = [w.strip() for w in raw.replace(',', '\n').split('\n') if w.strip()]
    if not words:
        _custom_re = None
        return
    parts = [re.escape(w.lower()) + r"\w*" for w in words]
    combined = "|".join(parts)
    _custom_re = re.compile(
        r"(?<![а-яёa-z])(?:" + combined + r")(?![а-яёa-z])",
        re.IGNORECASE | re.UNICODE,
    )


def _censor(text):
    if not text:
        return text
    s = str(text)

    cached = _cache.get(s)
    if cached is not None:
        return cached

    n = s.lower().translate(_LEET_TABLE)

    all_matches = list(_RE.finditer(n))
    if _custom_re is not None:
        all_matches.extend(_custom_re.finditer(n))

    if not all_matches:
        if len(_cache) >= _CACHE_MAX:
            _cache.clear()
        _cache[s] = s
        return s

    out = list(s)
    all_matches.sort(key=lambda m: m.start())
    used = set()

    for m in all_matches:
        start = m.start()
        end = min(m.end(), len(out))
        if start in used:
            continue
        if _cfg_mode == 0:
            for i in range(start, end):
                if i not in used and out[i] not in (' ', '\n', '\t'):
                    out[i] = _cfg_char
                used.add(i)
        else:
            for i in range(start, end):
                out[i] = None
                used.add(i)
            out[start] = _cfg_phrase

    result = ''.join(ch for ch in out if ch is not None)

    if len(_cache) >= _CACHE_MAX:
        _cache.clear()
    _cache[s] = result
    return result


def _apply(obj, *fields):
    for f in fields:
        try:
            val = getattr(obj, f, None)
            if val is None:
                continue
            s = str(val)
            c = _censor(s)
            if c != s:
                set_private_field(obj, f, c)
        except Exception:
            pass


class _CtorHook(MethodHook):
    def after_hooked_method(self, param):
        try:
            _apply(param.thisObject, 'messageText', 'caption', 'messageTextForReply', 'messageTextShort')
        except Exception:
            pass


class _TextUpdateHook(MethodHook):
    def after_hooked_method(self, param):
        try:
            _apply(param.thisObject, 'messageText', 'caption', 'messageTextForReply', 'messageTextShort')
        except Exception:
            pass


class _NotificationHook(MethodHook):
    def after_hooked_method(self, param):
        try:
            result = param.getResult()
            if result is not None:
                s = str(result)
                c = _censor(s)
                if c != s:
                    param.setResult(c)
        except Exception:
            pass



# ============================================================
# MaxExteraPlugins Shared Author & Channel Subscription Module
# ============================================================

# ============================================================
# MaxExteraPlugins Shared Author & Channel Subscription Module
# ============================================================

# ============================================================
# MaxExteraPlugins Shared Author & Channel Subscription Module
# ============================================================
class AuthorChannelHelper:
    CONFIG_URL = "https://raw.githubusercontent.com/MaxExteraPlugins/config/main/links.json"

    DEFAULT_LINKS = {
        "channel_username": "MaxExteraPlugins",
        "channel_url": "https://t.me/MaxExteraPlugins",
        "header": {"ru": "MaxExteraPlugins", "en": "MaxExteraPlugins"},
        "buttons": [
            {"title": {"ru": "Канал автора", "en": "Author's Channel"}, "icon": "msg_channel", "url": "https://t.me/MaxExteraPlugins"},
            {"title": {"ru": "Поддержать автора", "en": "Support author"}, "icon": "msg_share", "url": "https://t.me/itNotMax"},
            {"title": {"ru": "Сообщить о баге", "en": "Report a bug"}, "icon": "msg_help", "url": "https://t.me/itNotMax"}
        ]
    }

    _TEXTS = {
        "install_card_title": {"ru": "Подпишитесь на канал", "en": "Subscribe to channel"},
        "install_card_msg": {
            "ru": (
                "Мы делаем плагины бесплатными и доступными для всех: пожалуйста, "
                "поддержите нас подпиской на официальный канал @MaxExteraPlugins.\n\n"
                "Там публикуются обновления, важные новости и анонсы новых плагинов."
            ),
            "en": (
                "We keep our plugins free and accessible for everyone: please "
                "support us by subscribing to our official channel @MaxExteraPlugins.\n\n"
                "Updates, news, and new plugin announcements are published there."
            )
        },
        "open_channel_btn": {"ru": "Перейти на канал", "en": "Open channel"},
        "remind_later_btn": {"ru": "Напомнить позже", "en": "Remind later"},
        "never_show_btn": {"ru": "Больше не показывать", "en": "Don't show again"},
        "sub_thank_you": {"ru": "Спасибо за подписку на наш канал!", "en": "Thank you for subscribing to our channel!"},
        "settings_channel": {"ru": "Канал автора", "en": "Author's Channel"},
        "settings_donate": {"ru": "Поддержать автора", "en": "Support author"},
        "settings_bug_report": {"ru": "Сообщить о баге", "en": "Report a bug"}
    }

    @classmethod
    def is_ru(cls) -> bool:
        try:
            from org.telegram.messenger import LocaleController
            lang = str(LocaleController.getInstance().getCurrentLocale().getLanguage() or "").lower()
            return lang in ("ru", "be", "uk", "kk")
        except Exception:
            return True

    @classmethod
    def tr(cls, key: str) -> str:
        entry = cls._TEXTS.get(key, {})
        return entry.get("ru" if cls.is_ru() else "en", entry.get("en", key))

    def __init__(self, plugin, icon_sticker=None):
        self.plugin = plugin
        self.icon_sticker = icon_sticker or getattr(plugin, "__icon__", "MaxExteraPluginsStickers/1")
        self._stopped = False
        self._active_dialog = None

    def on_load(self):
        self._stopped = False
        self._active_dialog = None
        self._load_remote_links_async()
        self._check_initial_subscription_flow()

    def on_event(self, event_type):
        try:
            name = str(event_type).upper()
            if name.endswith("START") or name.endswith("RESUME"):
                if self.is_subscribed() and not self.plugin.get_setting("was_subscribed", False):
                    self.plugin.set_setting("was_subscribed", True)
                    self._dismiss_active_dialog()
                    self._notify_subscribed()
        except Exception:
            pass

    def on_unload(self):
        self._stopped = True
        self._dismiss_active_dialog()

    def is_allowed(self) -> bool:
        return True

    def _get_links(self) -> dict:
        raw = self.plugin.get_setting("remote_links_cache", None)
        if raw:
            try:
                import json
                data = json.loads(raw)
                if isinstance(data, dict): return data
            except Exception:
                pass
        return self.DEFAULT_LINKS

    def _load_remote_links_async(self):
        def worker():
            try:
                import urllib.request, json
                req = urllib.request.Request(self.CONFIG_URL, headers={"User-Agent": "MaxExteraPlugins"})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        if isinstance(data, dict):
                            self.plugin.set_setting("remote_links_cache", json.dumps(data))
                            self._resolve_channel_in_telegram(data.get("channel_username", "MaxExteraPlugins"))
            except Exception:
                pass
        import threading
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def _open_url(self, url: str, view=None):
        try:
            from org.telegram.messenger.browser import Browser
            from org.telegram.messenger import ApplicationLoader
            from client_utils import get_last_fragment
            ctx = None
            if view is not None:
                ctx = view.getContext()
            if ctx is None:
                frag = get_last_fragment()
                if frag is not None:
                    ctx = frag.getParentActivity()
            if ctx is None:
                ctx = ApplicationLoader.applicationContext
            Browser.openUrl(ctx, url)
        except Exception:
            pass

    def _resolve_channel_in_telegram(self, username: str):
        try:
            from org.telegram.messenger import UserConfig, MessagesController
            from org.telegram.tgnet import TLRPC, ConnectionsManager, RequestDelegate
            clean_user = username.lstrip("@")
            acc = int(UserConfig.selectedAccount)
            mc = MessagesController.getInstance(acc)
            if not mc: return
            req = TLRPC.TL_contacts_resolveUsername()
            req.username = clean_user
            helper_ref = self
            class Delegate(RequestDelegate):
                def run(self, response, error):
                    if error is None and response is not None:
                        chats = getattr(response, "chats", None)
                        if chats is not None and chats.size() > 0:
                            for a in range(UserConfig.MAX_ACCOUNT_COUNT):
                                try:
                                    if UserConfig.getInstance(a).isClientActivated():
                                        MessagesController.getInstance(a).putChats(chats, False)
                                except Exception:
                                    pass
                            c = chats.get(0)
                            cid = getattr(c, "id", 0)
                            if cid > 0:
                                helper_ref.plugin.set_setting("resolved_channel_id", int(cid))
            ConnectionsManager.getInstance(acc).sendRequest(req, Delegate())
        except Exception:
            pass

    def is_subscribed(self) -> bool:
        try:
            from org.telegram.messenger import UserConfig, MessagesController, MessagesStorage
            from java.lang import Long as JLong
            links = self._get_links()
            target = str(links.get("channel_username", "MaxExteraPlugins") or "MaxExteraPlugins").lower().lstrip("@")
            saved_cid = int(self.plugin.get_setting("resolved_channel_id", 0) or 0)

            for acc in range(UserConfig.MAX_ACCOUNT_COUNT):
                try:
                    uconf = UserConfig.getInstance(acc)
                    if not uconf.isClientActivated():
                        continue

                    mc = MessagesController.getInstance(acc)
                    storage = MessagesStorage.getInstance(acc)

                    # 1. In-memory check by resolved_channel_id
                    if saved_cid and mc is not None:
                        try:
                            c = mc.getChat(JLong(saved_cid))
                            if c is not None:
                                left = bool(getattr(c, "left", True))
                                kicked = bool(getattr(c, "kicked", False))
                                if not left and not kicked:
                                    return True
                        except Exception:
                            pass

                    # 2. In-memory check by username
                    if mc is not None:
                        try:
                            chat = mc.getUserOrChat(target)
                            if chat is not None:
                                cid = int(getattr(chat, "id", 0) or 0)
                                if cid and not saved_cid:
                                    saved_cid = cid
                                    self.plugin.set_setting("resolved_channel_id", cid)
                                left = bool(getattr(chat, "left", True))
                                kicked = bool(getattr(chat, "kicked", False))
                                if not left and not kicked:
                                    return True
                        except Exception:
                            pass

                    # 3. In-memory dialogs check
                    if mc is not None:
                        try:
                            dialog_lists = []
                            d_chan = getattr(mc, "dialogsChannelsOnly", None)
                            if d_chan is not None and d_chan.size() > 0:
                                dialog_lists.append(d_chan)
                            d_all = getattr(mc, "allDialogs", None)
                            if d_all is not None and d_all.size() > 0:
                                dialog_lists.append(d_all)

                            for d_list in dialog_lists:
                                limit = min(d_list.size(), 300)
                                for i in range(limit):
                                    d = d_list.get(i)
                                    did = getattr(d, "id", 0)
                                    if did < 0:
                                        cid = -did
                                        if saved_cid and cid == saved_cid:
                                            c = mc.getChat(JLong(cid))
                                            if c is not None:
                                                left = bool(getattr(c, "left", True))
                                                kicked = bool(getattr(c, "kicked", False))
                                                if not left and not kicked:
                                                    return True
                                        else:
                                            c = mc.getChat(JLong(cid))
                                            if c is not None:
                                                uname = str(getattr(c, "username", "") or "").lower()
                                                if uname == target:
                                                    if not saved_cid:
                                                        saved_cid = cid
                                                        self.plugin.set_setting("resolved_channel_id", cid)
                                                    left = bool(getattr(c, "left", True))
                                                    kicked = bool(getattr(c, "kicked", False))
                                                    if not left and not kicked:
                                                        return True
                        except Exception:
                            pass

                    # 4. Storage check (SQLite on disk)
                    if storage is not None:
                        if saved_cid:
                            try:
                                if storage.containsLocalDialog(JLong(-saved_cid)):
                                    c_sync = storage.getChatSync(JLong(saved_cid))
                                    if c_sync is not None:
                                        left = bool(getattr(c_sync, "left", True))
                                        kicked = bool(getattr(c_sync, "kicked", False))
                                        if not left and not kicked:
                                            return True
                                    else:
                                        return True
                            except Exception:
                                pass

                        try:
                            db = storage.getDatabase()
                            if db is not None:
                                if saved_cid:
                                    try:
                                        cur = db.queryFinalized("SELECT did FROM dialogs WHERE did = ?", [JLong(-saved_cid)])
                                        if cur is not None:
                                            has_row = bool(cur.next())
                                            cur.dispose()
                                            if has_row:
                                                return True
                                    except Exception:
                                        pass

                                try:
                                    cur = db.queryFinalized("SELECT uid, name FROM chats WHERE LOWER(name) LIKE ?", ["%" + target + "%"])
                                    if cur is not None:
                                        while cur.next():
                                            c_id = cur.longValue(0)
                                            if c_id > 0:
                                                if not saved_cid:
                                                    saved_cid = int(c_id)
                                                    self.plugin.set_setting("resolved_channel_id", saved_cid)
                                                cur_d = db.queryFinalized("SELECT did FROM dialogs WHERE did = ?", [JLong(-c_id)])
                                                if cur_d is not None:
                                                    in_dlg = bool(cur_d.next())
                                                    cur_d.dispose()
                                                    if in_dlg:
                                                        cur.dispose()
                                                        return True
                                        cur.dispose()
                                except Exception:
                                    pass
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass
        return False

    def prepend_settings(self, original_items=None) -> list:
        from ui.settings import Header, Text, Divider

        if original_items and any(getattr(x, "text", "") == "MaxExteraPlugins" for x in original_items if type(x).__name__ == "Header"):
            return original_items

        links = self._get_links()
        buttons_config = links.get("buttons")

        author_items = []
        if isinstance(buttons_config, list):
            for btn in buttons_config:
                if not isinstance(btn, dict): continue
                raw_url = btn.get("url")
                if isinstance(raw_url, dict):
                    keys = [
                        getattr(self.plugin, "id", None),
                        globals().get("__id__", None),
                        globals().get("__name__", None),
                        self.plugin.__class__.__name__
                    ]
                    keys += [k.lower() for k in keys if isinstance(k, str)]
                    resolved_url = ""
                    for k in keys:
                        if k and k in raw_url:
                            resolved_url = str(raw_url[k] or "").strip()
                            if resolved_url:
                                break
                    url = resolved_url
                elif isinstance(raw_url, str):
                    url = raw_url.strip()
                else:
                    url = ""

                if not url: continue

                title_data = btn.get("title")
                if isinstance(title_data, dict):
                    title = title_data.get("ru" if self.is_ru() else "en") or title_data.get("en") or title_data.get("ru") or ""
                elif isinstance(title_data, str) and title_data:
                    title = title_data
                else:
                    title = btn.get("title_ru" if self.is_ru() else "title_en") or btn.get("title_ru") or btn.get("title_en") or ""

                if not title: continue
                icon = str(btn.get("icon") or "msg_channel").strip()

                def make_click(u):
                    return lambda v=None: self._open_url(u, v)

                author_items.append(Text(text=title, icon=icon, on_click=make_click(url)))
        else:
            for k, text_key, icon_name in [
                ("channel_url", "settings_channel", "msg_channel"),
                ("donate_url", "settings_donate", "msg_share"),
                ("bug_report_url", "settings_bug_report", "msg_help")
            ]:
                u = str(links.get(k) or "").strip()
                if u:
                    author_items.append(Text(text=self.tr(text_key), icon=icon_name, on_click=lambda v=None, target_u=u: self._open_url(target_u, v)))

        res = []
        if author_items:
            hdr = links.get("header") or "MaxExteraPlugins"
            if isinstance(hdr, dict):
                hdr_text = hdr.get("ru" if self.is_ru() else "en") or hdr.get("ru") or hdr.get("en") or "MaxExteraPlugins"
            else:
                hdr_text = str(hdr)
            res.append(Header(text=hdr_text))
            res.extend(author_items)
            res.append(Divider())

        cleaned_items = []
        if original_items:
            skipping_info = False
            for item in original_items:
                item_cls = type(item).__name__
                if item_cls == "Header":
                    txt = str(getattr(item, "text", "") or getattr(item, "title", "") or "").lower()
                    if "информ" in txt or "inform" in txt:
                        skipping_info = True
                        continue
                    else:
                        skipping_info = False
                elif skipping_info and item_cls == "Divider":
                    skipping_info = False
                    continue

                if not skipping_info:
                    cleaned_items.append(item)

        res.extend(cleaned_items)
        return res

    def _dismiss_active_dialog(self):
        try:
            if self._active_dialog is not None:
                self._active_dialog.dismiss()
        except Exception:
            pass
        self._active_dialog = None

    def _is_dialog_active(self) -> bool:
        try:
            if self._active_dialog is not None:
                return bool(self._active_dialog.isShowing())
        except Exception:
            pass
        return False

    def _notify_subscribed(self):
        try:
            from ui.bulletin import BulletinHelper
            BulletinHelper.show_success(self.tr("sub_thank_you"))
        except Exception:
            pass

    def _check_initial_subscription_flow(self):
        def flow():
            try:
                if self.plugin.get_setting("never_show_sub_prompt", False):
                    return

                current_ver = str(getattr(self.plugin, "__version__", globals().get("__version__", "1.0.0")) or "1.0.0")
                last_prompted_ver = self.plugin.get_setting("last_prompted_version", None)

                # Only show on install (last_prompted_ver is None) or update (last_prompted_ver != current_ver)
                if last_prompted_ver is not None and str(last_prompted_ver) == current_ver:
                    return

                if self.is_subscribed():
                    self.plugin.set_setting("last_prompted_version", current_ver)
                    self.plugin.set_setting("was_subscribed", True)
                    return

                self._show_subscription_prompt(current_ver)
            except Exception:
                pass
        from android_utils import run_on_ui_thread
        run_on_ui_thread(flow, 1500)

    def _create_card_content(self, act, title_text, message_text):
        try:
            from android.widget import LinearLayout, TextView, ImageView
            from android.view import Gravity
            from org.telegram.messenger import AndroidUtilities
            from org.telegram.ui.ActionBar import Theme
            from client_utils import create_sticker_drawable

            dp = AndroidUtilities.dp

            layout = LinearLayout(act)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.setGravity(Gravity.CENTER_HORIZONTAL)
            layout.setPadding(dp(24), dp(20), dp(24), dp(10))

            sticker_drawable = None
            if self.icon_sticker:
                try:
                    sticker_drawable = create_sticker_drawable(self.icon_sticker, dp(120), dp(120))
                except Exception:
                    pass

            if sticker_drawable is not None:
                iv = ImageView(act)
                iv.setImageDrawable(sticker_drawable)
                lp_iv = LinearLayout.LayoutParams(dp(120), dp(120))
                lp_iv.gravity = Gravity.CENTER_HORIZONTAL
                lp_iv.bottomMargin = dp(14)
                layout.addView(iv, lp_iv)

            if title_text:
                tt = TextView(act)
                tt.setText(title_text)
                tt.setTextSize(19.0)
                tt.setTypeface(AndroidUtilities.bold())
                tt.setTextColor(Theme.getColor(Theme.key_dialogTextBlack))
                tt.setGravity(Gravity.CENTER_HORIZONTAL)
                lp_t = LinearLayout.LayoutParams(-1, -2)
                lp_t.bottomMargin = dp(8)
                layout.addView(tt, lp_t)

            if message_text:
                mt = TextView(act)
                mt.setText(message_text)
                mt.setTextSize(15.0)
                mt.setTextColor(Theme.getColor(Theme.key_dialogTextBlack))
                mt.setLineSpacing(float(dp(3)), 1.0)
                mt.setGravity(Gravity.CENTER_HORIZONTAL)
                lp_m = LinearLayout.LayoutParams(-1, -2)
                mt.setLayoutParams(lp_m)
                layout.addView(mt)

            return layout
        except Exception:
            return None

    def _show_subscription_prompt(self, current_ver: str):
        def show():
            try:
                if self._is_dialog_active(): return
                from client_utils import get_last_fragment
                frag = get_last_fragment()
                if not frag: return
                act = frag.getParentActivity()
                if not act: return

                links = self._get_links()
                url = links.get("channel_url", "https://t.me/MaxExteraPlugins")

                from ui.alert import AlertDialogBuilder
                b = AlertDialogBuilder(act)
                content = self._create_card_content(act, self.tr("install_card_title"), self.tr("install_card_msg"))
                if content is not None:
                    b.set_view(content)
                else:
                    b.set_title(self.tr("install_card_title"))
                    b.set_message(self.tr("install_card_msg"))

                def on_open_channel(dialog, which):
                    self._dismiss_active_dialog()
                    self.plugin.set_setting("last_prompted_version", current_ver)
                    self._open_url(url)

                def on_remind_later(dialog, which):
                    self._dismiss_active_dialog()
                    self.plugin.set_setting("last_prompted_version", current_ver)

                def on_never_show(dialog, which):
                    self._dismiss_active_dialog()
                    self.plugin.set_setting("never_show_sub_prompt", True)
                    self.plugin.set_setting("last_prompted_version", current_ver)

                b.set_positive_button(self.tr("open_channel_btn"), on_open_channel)
                b.set_neutral_button(self.tr("remind_later_btn"), on_remind_later)
                b.set_negative_button(self.tr("never_show_btn"), on_never_show)

                def on_dismiss(builder):
                    self.plugin.set_setting("last_prompted_version", current_ver)
                try:
                    b.set_on_dismiss_listener(on_dismiss)
                except Exception:
                    pass

                self._active_dialog = b.show()
                self.plugin.set_setting("last_prompted_version", current_ver)
            except Exception:
                pass
        from android_utils import run_on_ui_thread
        run_on_ui_thread(show)

class CensorifyPlugin(BasePlugin):

    def on_app_event(self, event_type):
        if hasattr(self, "_author_helper"):
            self._author_helper.on_event(event_type)

    def _load_cfg(self):
        global _cfg_mode, _cfg_char, _cfg_phrase
        _cfg_mode = self.get_setting("censor_mode", 0)
        sym = self.get_setting("censor_symbol", "#")
        _cfg_char = sym[0] if sym else "#"
        ph = self.get_setting("censor_phrase", "[censored]")
        _cfg_phrase = ph if ph else "[censored]"
        _rebuild_custom_re(self.get_setting("custom_words", ""))

    def on_plugin_load(self):
        self._author_helper = AuthorChannelHelper(self, icon_sticker="MaxExteraPluginsStickers/15")
        self._author_helper.on_load()
        self._load_cfg()

        try:
            cls = find_class("org.telegram.messenger.MessageObject")
            if cls is None:
                self.log("Error: MessageObject not found")
                return

            try:
                java_cls = cls.getClass()
            except Exception:
                java_cls = cls

            self.hook_all_constructors(java_cls, _CtorHook())

            tu = _TextUpdateHook()
            for method in ("applyNewText", "updateMessageText", "updateTranslation", "generateCaption"):
                try:
                    self.hook_all_methods(java_cls, method, tu)
                except Exception:
                    pass

        except Exception as e:
            self.log(f"Error: {e}")

        try:
            notif_cls = find_class("org.telegram.messenger.NotificationsController")
            if notif_cls is None:
                return

            try:
                notif_java = notif_cls.getClass()
            except Exception:
                notif_java = notif_cls

            nh = _NotificationHook()
            for method in ("getStringForMessage", "getShortStringForMessage"):
                try:
                    self.hook_all_methods(notif_java, method, nh)
                except Exception:
                    pass

        except Exception:
            pass

    def on_plugin_unload(self):
        if hasattr(self, "_author_helper"):
            self._author_helper.on_unload()
        _clear_cache()

    def _on_mode_change(self, new_index: int):
        global _cfg_mode
        _cfg_mode = new_index
        _clear_cache()
        self.set_setting("censor_mode", new_index, reload_settings=True)

    def _on_symbol_change(self, new_value: str):
        global _cfg_char
        _cfg_char = new_value[0] if new_value else "#"
        _clear_cache()
        self.set_setting("censor_symbol", _cfg_char)

    def _on_phrase_change(self, new_value: str):
        global _cfg_phrase
        _cfg_phrase = new_value if new_value else "[censored]"
        _clear_cache()
        self.set_setting("censor_phrase", _cfg_phrase)

    def _on_custom_words_change(self, new_value: str):
        self.set_setting("custom_words", new_value)
        _rebuild_custom_re(new_value)

    def create_settings(self):
        try:
            items = self._inner_create_settings()
        except Exception:
            items = []
        if hasattr(self, '_author_helper'):
            return self._author_helper.prepend_settings(items)
        return items

    def _inner_create_settings(self):
        mode = self.get_setting("censor_mode", 0)

        items = [
            Header(text="Censorship Settings"),
            Selector(
                key="censor_mode",
                text="Censorship mode",
                default=0,
                items=["Symbol (per character)", "Phrase (whole word)"],
                icon="msg_block2",
                on_change=self._on_mode_change,
            ),
            Divider(),
        ]

        if mode == 0:
            items.append(
                Input(
                    key="censor_symbol",
                    text="Censorship symbol",
                    default="#",
                    subtext="Each letter will be replaced with this symbol",
                    icon="msg_edit",
                    on_change=self._on_symbol_change,
                )
            )
        else:
            items.append(
                Input(
                    key="censor_phrase",
                    text="Replacement phrase",
                    default="[censored]",
                    subtext="The word will be replaced with this phrase",
                    icon="msg_edit",
                    on_change=self._on_phrase_change,
                )
            )

        items.extend([
            Divider(),
            Header(text="Custom Words"),
            EditText(
                key="custom_words",
                hint="One word per line...",
                default="",
                multiline=True,
                max_length=5000,
            ),
        ])

        if hasattr(self, "_author_helper"):


            return self._author_helper.prepend_settings(items)


        return items
