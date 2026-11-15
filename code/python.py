# -*- coding: utf-8 -*-
__id__ = "censorify"
__name__ = "Censorify"
__description__ = "Locally replaces profanity with selected characters in all messages."
__version__ = "1.6.0"
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
class AuthorChannelHelper:
    CONFIG_URL = "https://raw.githubusercontent.com/MaxExteraPlugins/config/main/links.json"

    DEFAULT_LINKS = {
        "channel_username": "MaxExteraPlugins",
        "channel_url": "https://t.me/MaxExteraPlugins",
        "trial_days": 7,
        "header": {"ru": "MaxExteraPlugins", "en": "MaxExteraPlugins"},
        "buttons": [
            {"title": {"ru": "Канал автора", "en": "Author's Channel"}, "icon": "msg_channel", "url": "https://t.me/MaxExteraPlugins"},
            {"title": {"ru": "Поддержать автора", "en": "Support author"}, "icon": "msg_share", "url": "https://t.me/itNotMax"},
            {"title": {"ru": "Сообщить о баге", "en": "Report a bug"}, "icon": "msg_help", "url": "https://t.me/itNotMax"}
        ]
    }

    _TEXTS = {
        "install_card_title": {"ru": "Спасибо за установку!", "en": "Thank you for installing!"},
        "install_card_msg": {
            "ru": "Надеемся, что плагин будет вам полезен!\n\nМы делаем плагины бесплатными и доступными для всех: пожалуйста, поддержите нас подпиской. Там будут только важные новости, обновления и розыгрыши.",
            "en": "We hope this plugin will be useful to you!\n\nWe keep our plugins free and open for everyone: please support us with a subscription. We only post key news, updates, and giveaways."
        },
        "subscribe_btn": {"ru": "Подписаться", "en": "Subscribe"},
        "remind_later_btn": {"ru": "Напомнить позже", "en": "Remind later"},
        "check_sub_btn": {"ru": "Проверить подписку", "en": "Check subscription"},
        "trial_expired_title": {"ru": "Пожалуйста, подпишитесь на канал", "en": "Please subscribe to the channel"},
        "trial_expired_msg": {
            "ru": "Пожалуйста, подпишитесь на наш официальный канал.\n\nМы делаем плагины бесплатно, ничего не требуя взамен. До подписки функции плагина временно приостановлены.",
            "en": "Please subscribe to our official channel.\n\nWe develop plugins for free and ask nothing in return. Plugin features are paused until you subscribe."
        },
        "sub_thank_you": {"ru": "Спасибо за подписку на наш канал!", "en": "Thank you for subscribing to our channel!"},
        "sub_thank_you_after_expired": {"ru": "Спасибо за подписку на наш канал!\nПлагин продолжит работу!", "en": "Thank you for subscribing to our channel!\nThe plugin will continue working!"},
        "sub_not_found": {"ru": "Подписка не обнаружена. Пожалуйста, подпишитесь на канал.", "en": "Subscription not found. Please subscribe to the channel."},
        "settings_channel": {"ru": "Канал автора", "en": "Author's Channel"},
        "settings_donate": {"ru": "Поддержать автора", "en": "Support author"},
        "settings_bug_report": {"ru": "Сообщить о баге", "en": "Report a bug"}
    }

    @classmethod
    def is_ru(cls) -> bool:
        try:
            from org.telegram.messenger import LocaleController
            cur = str(LocaleController.getInstance().getCurrentLocale().getLanguage() or "").lower()
            if cur.startswith(("ru", "uk", "be")): return True
            if cur: return False
        except Exception:
            pass
        try:
            from java.util import Locale
            code = str(Locale.getDefault().getLanguage() or "").lower()
            if code.startswith(("ru", "uk", "be")): return True
        except Exception:
            pass
        return False

    @classmethod
    def tr(cls, key: str) -> str:
        entry = cls._TEXTS.get(key, {})
        return entry.get("ru" if cls.is_ru() else "en", entry.get("en", key))

    def __init__(self, plugin, icon_sticker=None):
        self.plugin = plugin
        self.icon_sticker = icon_sticker or getattr(plugin, "__icon__", "MaxExteraPluginsStickers/1")
        self._stopped = False
        self._active_dialog = None
        self._last_known_sub = None

    def on_load(self):
        self._stopped = False
        self._active_dialog = None
        self._last_known_sub = None
        self._load_remote_links_async()
        self._check_initial_subscription_flow()
        self._start_subscription_watcher()

    def on_event(self, event_type):
        try:
            name = str(event_type).upper()
            if name.endswith("START") or name.endswith("RESUME"):
                self._check_subscription_change_instant()
        except Exception:
            pass

    def on_unload(self):
        self._stopped = True
        self._dismiss_active_dialog()

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
                            mc.putChats(chats, False)
                            c = chats.get(0)
                            cid = getattr(c, "id", 0)
                            if cid > 0:
                                helper_ref.plugin.set_setting("resolved_channel_id", int(cid))
            ConnectionsManager.getInstance(acc).sendRequest(req, Delegate())
        except Exception:
            pass

    def is_subscribed(self) -> bool:
        try:
            from org.telegram.messenger import UserConfig, MessagesController
            links = self._get_links()
            target = str(links.get("channel_username", "MaxExteraPlugins") or "MaxExteraPlugins").lower().lstrip("@")
            saved_cid = self.plugin.get_setting("resolved_channel_id", 0)

            for acc in range(UserConfig.MAX_ACCOUNT_COUNT):
                uconf = UserConfig.getInstance(acc)
                if not uconf.isClientActivated(): continue
                mc = MessagesController.getInstance(acc)
                if not mc: continue

                if saved_cid:
                    try:
                        from java.lang import Long as JLong
                        c = mc.getChat(JLong(int(saved_cid)))
                        if c is not None:
                            left = bool(getattr(c, "left", True))
                            kicked = bool(getattr(c, "kicked", False))
                            if not left and not kicked: return True
                    except Exception:
                        pass

                try:
                    chat = mc.getUserOrChat(target)
                    if chat is not None:
                        cid = getattr(chat, "id", 0)
                        if cid and not saved_cid:
                            self.plugin.set_setting("resolved_channel_id", int(cid))
                        left = bool(getattr(chat, "left", True))
                        kicked = bool(getattr(chat, "kicked", False))
                        if not left and not kicked: return True
                except Exception:
                    pass

                try:
                    dialogs = mc.allDialogs
                    if dialogs is not None:
                        limit = min(dialogs.size(), 300)
                        for i in range(limit):
                            d = dialogs.get(i)
                            did = getattr(d, "id", 0)
                            if did < 0:
                                from java.lang import Long as JLong
                                c = mc.getChat(JLong(-did))
                                if c is not None:
                                    uname = str(getattr(c, "username", "") or "").lower()
                                    if uname == target:
                                        cid = getattr(c, "id", 0)
                                        if cid and not saved_cid:
                                            self.plugin.set_setting("resolved_channel_id", int(cid))
                                        left = bool(getattr(c, "left", True))
                                        kicked = bool(getattr(c, "kicked", False))
                                        if not left and not kicked: return True
                except Exception:
                    pass
        except Exception:
            pass
        return False

    def is_allowed(self) -> bool:
        import time
        if self.is_subscribed():
            if not self.plugin.get_setting("was_subscribed", False):
                was_exp = bool(self.plugin.get_setting("was_expired_state", False))
                self.plugin.set_setting("was_subscribed", True)
                self.plugin.set_setting("was_expired_state", False)
                self._notify_subscribed(was_expired=was_exp)
            return True

        if self.plugin.get_setting("was_expired_state", False) or self.plugin.get_setting("was_subscribed", False):
            self.plugin.set_setting("was_subscribed", False)
            self.plugin.set_setting("was_expired_state", True)
            self._show_expired_card()
            return False

        now = time.time()
        install_time = float(self.plugin.get_setting("install_time", 0.0) or 0.0)
        if install_time <= 0:
            install_time = now
            self.plugin.set_setting("install_time", install_time)

        trial_days = float(self._get_links().get("trial_days", 7))
        trial_sec = trial_days * 86400.0

        if (now - install_time) < trial_sec:
            return True

        self.plugin.set_setting("was_expired_state", True)
        self._show_expired_card()
        return False

    def prepend_settings(self, original_items=None) -> list:
        from ui.settings import Header, Text, Divider

        # Prevent double-prepending
        if original_items and any(getattr(x, "text", "") == "MaxExteraPlugins" for x in original_items if type(x).__name__ == "Header"):
            return original_items

        links = self._get_links()
        buttons_config = links.get("buttons")

        author_items = []
        if isinstance(buttons_config, list):
            for btn in buttons_config:
                if not isinstance(btn, dict): continue
                url = str(btn.get("url") or "").strip()
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

        # Clean original_items by removing any old "Информация" / "Information" category
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

    def _notify_subscribed(self, was_expired=False):
        self.plugin.set_setting("was_subscribed", True)
        from ui.bulletin import BulletinHelper
        msg_key = "sub_thank_you_after_expired" if was_expired else "sub_thank_you"
        BulletinHelper.show_success(self.tr(msg_key))

    def _check_subscription_change_instant(self):
        try:
            from android_utils import run_on_ui_thread
            cur_sub = self.is_subscribed()
            prev_sub = self._last_known_sub
            if prev_sub is not None and prev_sub != cur_sub:
                self._last_known_sub = cur_sub
                if cur_sub:
                    was_exp = bool(self.plugin.get_setting("was_expired_state", False))
                    self.plugin.set_setting("was_subscribed", True)
                    self.plugin.set_setting("was_expired_state", False)
                    self._dismiss_active_dialog()
                    self._notify_subscribed(was_expired=was_exp)
                else:
                    self.plugin.set_setting("was_subscribed", False)
                    self.plugin.set_setting("was_expired_state", True)
                    self._dismiss_active_dialog()
                    self._show_expired_card()
            else:
                self._last_known_sub = cur_sub
        except Exception:
            pass

    def _start_subscription_watcher(self):
        def watcher_loop():
            import time
            from android_utils import run_on_ui_thread
            time.sleep(2.0)
            if self._stopped: return
            self._last_known_sub = self.is_subscribed()

            while not self._stopped:
                try:
                    time.sleep(2.0)
                    if self._stopped: break
                    cur_sub = self.is_subscribed()
                    prev_sub = self._last_known_sub

                    if prev_sub is not None and prev_sub != cur_sub:
                        self._last_known_sub = cur_sub
                        if cur_sub:
                            was_exp = bool(self.plugin.get_setting("was_expired_state", False))
                            self.plugin.set_setting("was_subscribed", True)
                            self.plugin.set_setting("was_expired_state", False)
                            def on_sub():
                                self._dismiss_active_dialog()
                                self._notify_subscribed(was_expired=was_exp)
                            run_on_ui_thread(on_sub)
                        else:
                            self.plugin.set_setting("was_subscribed", False)
                            self.plugin.set_setting("was_expired_state", True)
                            def on_unsub():
                                self._dismiss_active_dialog()
                                self._show_expired_card()
                            run_on_ui_thread(on_unsub)
                    else:
                        self._last_known_sub = cur_sub
                except Exception:
                    pass
        import threading
        t = threading.Thread(target=watcher_loop, daemon=True)
        t.start()

    def _check_initial_subscription_flow(self):
        def flow():
            import time
            try:
                now = time.time()
                install_time = float(self.plugin.get_setting("install_time", 0.0) or 0.0)
                if install_time <= 0:
                    install_time = now
                    self.plugin.set_setting("install_time", install_time)

                is_sub = self.is_subscribed()
                self._last_known_sub = is_sub
                was_sub = bool(self.plugin.get_setting("was_subscribed", False))
                was_exp = bool(self.plugin.get_setting("was_expired_state", False))

                if is_sub:
                    if not was_sub:
                        self.plugin.set_setting("was_subscribed", True)
                        self.plugin.set_setting("was_expired_state", False)
                        self._notify_subscribed(was_expired=was_exp)
                    return

                if was_sub or was_exp:
                    self.plugin.set_setting("was_subscribed", False)
                    self.plugin.set_setting("was_expired_state", True)
                    self._show_expired_card()
                    return

                trial_days = float(self._get_links().get("trial_days", 7))
                trial_sec = trial_days * 86400.0
                last_remind = float(self.plugin.get_setting("last_remind_time", 0.0) or 0.0)

                if (now - install_time) < trial_sec:
                    if last_remind <= 0 or (now - last_remind) >= trial_sec:
                        self._show_welcome_card()
                else:
                    self.plugin.set_setting("was_expired_state", True)
                    self._show_expired_card()
            except Exception:
                pass
        from android_utils import run_on_ui_thread
        run_on_ui_thread(flow, 1500)

    def _create_card_content(self, act, title_text, message_text):
        try:
            from android.widget import LinearLayout, TextView
            from android.view import Gravity
            from android.graphics import Typeface
            from org.telegram.messenger import AndroidUtilities, UserConfig, MediaDataController
            from org.telegram.ui.ActionBar import Theme
            from org.telegram.ui.Components import BackupImageView

            dp = AndroidUtilities.dp
            layout = LinearLayout(act)
            layout.setOrientation(LinearLayout.VERTICAL)
            layout.setGravity(Gravity.CENTER_HORIZONTAL)
            layout.setPadding(dp(24), dp(16), dp(24), dp(6))

            size = dp(76)
            iv = BackupImageView(act)
            iv.setRoundRadius(dp(18))
            lp_iv = LinearLayout.LayoutParams(size, size)
            lp_iv.gravity = Gravity.CENTER_HORIZONTAL
            lp_iv.setMargins(0, dp(4), 0, dp(16))
            iv.setLayoutParams(lp_iv)

            try:
                acc = int(UserConfig.selectedAccount)
                mdc = MediaDataController.getInstance(acc)
                raw_icon = str(self.icon_sticker)
                if "/" in raw_icon:
                    pack, idx_s = raw_icon.split("/", 1)
                    mdc.setPlaceholderImageByIndex(iv, pack, int(idx_s), "150_150")
            except Exception:
                pass
            layout.addView(iv)

            if title_text:
                tt = TextView(act)
                tt.setText(title_text)
                tt.setTextSize(19.0)
                tt.setTypeface(None, Typeface.BOLD)
                tt.setTextColor(Theme.getColor(Theme.key_dialogTextBlack))
                tt.setGravity(Gravity.CENTER_HORIZONTAL)
                lp_t = LinearLayout.LayoutParams(-1, -2)
                lp_t.setMargins(0, 0, 0, dp(12))
                tt.setLayoutParams(lp_t)
                layout.addView(tt)

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

    def _show_welcome_card(self):
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

                def on_sub(d, w):
                    self._dismiss_active_dialog()
                    self._open_url(url)
                    def check_after():
                        if self.is_subscribed():
                            self._notify_subscribed(was_expired=False)
                    from android_utils import run_on_ui_thread
                    run_on_ui_thread(check_after, 3000)

                def on_later(d, w):
                    import time
                    self._dismiss_active_dialog()
                    self.plugin.set_setting("last_remind_time", time.time())

                b.set_positive_button(self.tr("subscribe_btn"), on_sub)
                b.set_negative_button(self.tr("remind_later_btn"), on_later)
                self._active_dialog = b.show()
            except Exception:
                pass
        from android_utils import run_on_ui_thread
        run_on_ui_thread(show)

    def _show_expired_card(self):
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
                from ui.bulletin import BulletinHelper
                b = AlertDialogBuilder(act)
                content = self._create_card_content(act, self.tr("trial_expired_title"), self.tr("trial_expired_msg"))
                if content is not None:
                    b.set_view(content)
                else:
                    b.set_title(self.tr("trial_expired_title"))
                    b.set_message(self.tr("trial_expired_msg"))

                def on_sub(d, w):
                    self._dismiss_active_dialog()
                    self._open_url(url)
                    def check_after():
                        if self.is_subscribed():
                            self.plugin.set_setting("was_subscribed", True)
                            self.plugin.set_setting("was_expired_state", False)
                            self._notify_subscribed(was_expired=True)
                    from android_utils import run_on_ui_thread
                    run_on_ui_thread(check_after, 3000)

                def on_check(d, w):
                    self._dismiss_active_dialog()
                    if self.is_subscribed():
                        self.plugin.set_setting("was_subscribed", True)
                        self.plugin.set_setting("was_expired_state", False)
                        self._notify_subscribed(was_expired=True)
                    else:
                        BulletinHelper.show_error(self.tr("sub_not_found"))
                        from android_utils import run_on_ui_thread
                        run_on_ui_thread(self._show_expired_card, 500)

                b.set_positive_button(self.tr("subscribe_btn"), on_sub)
                b.set_negative_button(self.tr("check_sub_btn"), on_check)
                self._active_dialog = b.show()
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
