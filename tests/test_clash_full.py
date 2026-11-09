#!/usr/bin/env python3
"""Regression checks for Clash-Full.ini country-group coverage."""

from pathlib import Path
import re
import unittest

CONFIG = Path(__file__).resolve().parents[1] / "Clash-Full.ini"

CORE_CASES = {
    "香港-自动": ["🇭🇰 香港01", "HK 01", "Hong Kong 01"],
    "台湾-自动": ["🇨🇳 台湾01", "🇹🇼 台灣 01", "Taiwan 01"],
    "日本-自动": ["🇯🇵 日本01", "JP Tokyo", "Japan 01"],
    "新加坡-自动": ["🇸🇬 新加坡01", "SG 01", "Singapore 01"],
    "韩国-自动": ["🇰🇷 韩国01", "KR Seoul", "Korea 01"],
    "美国-自动": ["🇺🇸 美国01", "US Los Angeles", "United States 01"],
}

SUBSCRIPTION_COUNTRY_CASES = {
    "德国-自动": ["🇩🇪 德国", "Germany 01", "DE Frankfurt"],
    "法国-自动": ["🇫🇷 法国", "France 01", "FR Paris"],
    "英国-自动": ["🇬🇧 英国", "United Kingdom 01", "UK London"],
    "印度-自动": ["🇮🇳 印度-西部", "India 01", "IN Mumbai"],
    "智利-自动": ["🇨🇱 智利", "Chile 01"],
    "巴西-自动": ["🇧🇷 巴西", "Brazil 01"],
    "西班牙-自动": ["🇪🇸 西班牙", "Spain 01"],
    "瑞士-自动": ["🇨🇭 瑞士", "Switzerland 01"],
    "瑞典-自动": ["🇸🇪 瑞典", "Sweden 01"],
    "墨西哥-自动": ["🇲🇽 墨西哥", "Mexico 01"],
    "加拿大-自动": ["🇨🇦 加拿大", "Canada 01"],
    "澳大利亚-自动": ["🇦🇺 澳大利亚01", "Australia 01"],
    "阿联酋-自动": ["🇦🇪 迪拜", "阿联酋 01", "UAE Dubai"],
    "南非-自动": ["🇿🇦 南非", "South Africa 01"],
    "沙特阿拉伯-自动": ["🇸🇦 沙特阿拉伯", "Saudi Arabia 01"],
    "哥伦比亚-自动": ["🇨🇴 哥伦比亚", "Colombia 01"],
    "以色列-自动": ["🇮🇱 以色列", "Israel 01"],
    "越南-自动": ["🇻🇳 越南", "Vietnam 01"],
    "泰国-自动": ["🇹🇭 泰国", "Thailand 01"],
    "马来西亚-自动": ["🇲🇾 马来西亚", "Malaysia 01"],
    "俄罗斯-自动": ["🇷🇺 莫斯科", "俄罗斯 01", "Russia Moscow"],
    "菲律宾-自动": ["🇵🇭 菲律宾", "Philippines 01"],
    "尼日利亚-自动": ["🇳🇬 尼日利亚01", "Nigeria 01"],
    "印度尼西亚-自动": ["🇮🇩 印度尼西亚", "Indonesia 01"],
    "土耳其-自动": ["🇹🇷 土耳其", "Turkey 01"],
    "希腊-自动": ["🇬🇷 希腊", "Greece 01"],
    "缅甸-自动": ["🇲🇲 缅甸", "Myanmar 01"],
    "巴基斯坦-自动": ["🇵🇰 巴基斯坦", "Pakistan 01"],
    "挪威-自动": ["🇳🇴 挪威", "Norway 01"],
    "柬埔寨-自动": ["🇰🇭 柬埔寨", "Cambodia 01"],
    "埃及-自动": ["🇪🇬 埃及", "Egypt 01"],
    "伊拉克-自动": ["🇮🇶 伊拉克", "Iraq 01"],
    "孟加拉-自动": ["🇧🇩 孟加拉", "Bangladesh 01"],
    "哈萨克斯坦-自动": ["🇰🇿 哈萨克斯坦", "Kazakhstan 01"],
    "阿根廷-自动": ["🇦🇷 阿根廷", "Argentina 01"],
}

FUTURE_COUNTRIES = [
    # Countries not present in the current subscription still use the fallback.
    "🇳🇿 新西兰", "🇵🇹 葡萄牙", "🇫🇮 芬兰", "🇮🇪 爱尔兰",
    "🇦🇹 奥地利", "🇧🇪 比利时", "🇵🇱 波兰", "🇺🇦 乌克兰",
    "🇷🇴 罗马尼亚", "🇨🇿 捷克", "🇭🇺 匈牙利", "🇩🇰 丹麦",
    "🇮🇸 冰岛", "🇵🇪 秘鲁", "🇺🇾 乌拉圭", "🇵🇦 巴拿马",
    "🇨🇷 哥斯达黎加", "🇶🇦 卡塔尔", "🇰🇼 科威特", "🇯🇴 约旦",
    "🇳🇵 尼泊尔", "🇱🇰 斯里兰卡", "🇲🇳 蒙古", "🇱🇦 老挝",
    "🇧🇳 文莱", "🇫🇯 斐济", "🇰🇪 肯尼亚", "🇲🇦 摩洛哥",
    "🇬🇭 加纳", "🇹🇳 突尼斯", "🇪🇹 埃塞俄比亚",
    "New Zealand 01", "Portugal 01", "Austria Vienna 01",
]


def load_active_groups():
    groups = {}
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        if not line.startswith("custom_proxy_group="):
            continue
        fields = line.removeprefix("custom_proxy_group=").split("`")
        if len(fields) >= 3:
            groups[fields[0]] = fields[2]
    return groups


class ClashFullCountryCoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CONFIG.read_text(encoding="utf-8")
        cls.groups = load_active_groups()

    def test_core_country_groups_match_common_names(self):
        for group, names in CORE_CASES.items():
            self.assertIn(group, self.groups)
            pattern = re.compile(self.groups[group], re.IGNORECASE)
            for name in names:
                with self.subTest(group=group, name=name):
                    self.assertRegex(name, pattern)

    def test_subscription_country_groups_match_common_names(self):
        for group, names in SUBSCRIPTION_COUNTRY_CASES.items():
            self.assertIn(group, self.groups)
            pattern = re.compile(self.groups[group], re.IGNORECASE)
            for name in names:
                with self.subTest(group=group, name=name):
                    self.assertRegex(name, pattern)

    def test_all_automatic_group_references_every_subscription_country_group(self):
        line = next(
            line for line in self.text.splitlines()
            if line.startswith("custom_proxy_group=所有-自动`")
        )
        references = set(re.findall(r"\[\]([^`]+)", line))
        expected = set(CORE_CASES) | set(SUBSCRIPTION_COUNTRY_CASES)
        self.assertEqual(references, expected)

    def test_url_test_groups_fail_over_quickly_without_latency_flapping(self):
        """Health checks should react quickly but ignore tiny delay changes."""
        url_test_lines = [
            line for line in self.text.splitlines()
            if line.startswith("custom_proxy_group=") and "`url-test`" in line
        ]
        self.assertTrue(url_test_lines)
        for line in url_test_lines:
            group, _kind, _pattern, url, timing = line.removeprefix(
                "custom_proxy_group="
            ).split("`")
            with self.subTest(group=group):
                self.assertEqual(url, "https://www.gstatic.com/generate_204")
                self.assertEqual(timing, "30,5,80")

    def test_other_group_is_future_proof_for_every_non_core_country(self):
        pattern = re.compile(self.groups["其他-自动"], re.IGNORECASE)
        for name in FUTURE_COUNTRIES:
            with self.subTest(name=name):
                self.assertRegex(name, pattern)

    def test_other_group_excludes_core_countries(self):
        pattern = re.compile(self.groups["其他-自动"], re.IGNORECASE)
        for names in CORE_CASES.values():
            for name in names:
                with self.subTest(name=name):
                    self.assertNotRegex(name, pattern)

    def test_all_referenced_proxy_groups_exist(self):
        defined = set(self.groups) | {"DIRECT", "REJECT"}
        for line in self.text.splitlines():
            if not line.startswith("custom_proxy_group="):
                continue
            group_name = line.split("`", 1)[0].split("=", 1)[1]
            for reference in re.findall(r"\[\]([^`]+)", line):
                with self.subTest(group=group_name, reference=reference):
                    self.assertIn(reference, defined)

    def test_rule_urls_do_not_contain_nested_http(self):
        self.assertNotIn("gh-proxy.com/http://", self.text)

    def test_critical_service_domains_have_inline_rules_before_remote_providers(self):
        """Critical routing must survive failed remote rule-provider downloads."""
        # SubConverter accepts at most 64 ruleset declarations. Clash-Full has
        # 29 remote/final declarations, leaving room for 35 resilient inline rules.
        required = {
            "✨ AI1": ["openai.com", "chatgpt.com", "oaistatic.com", "oaiusercontent.com"],
            "✨ AI2": ["meta.ai", "perplexity.ai"],
            "📘 GitHub": ["github.com", "githubusercontent.com"],
            "👯‍♂️ TikTok": ["tiktok.com", "tiktokcdn.com", "tiktokv.com"],
            "🙋 Telegram": ["telegram.org", "t.me", "telegram-cdn.org"],
            "🕊️ Twitter(X)": ["twitter.com", "x.com", "twimg.com", "t.co"],
            "🗣️ Facebook": ["facebook.com", "fbcdn.net", "instagram.com"],
            "🌳 Amazon": ["amazon.com"],
            "🍎 Apple": ["apple.com"],
            "Ⓜ️ Microsoft": ["microsoft.com"],
            "🎮 Steam": ["steamcommunity.com"],
            "🕹️ Game": ["epicgames.com"],
            "🎞️ YouTube": ["youtube.com", "googlevideo.com", "ytimg.com"],
            "📺 Disney": ["disneyplus.com"],
            "🎥 Netflix": ["netflix.com", "nflxvideo.net"],
            "🎬 HBO": ["max.com"],
            "🎵 Spotify": ["spotify.com", "scdn.co"],
        }
        self.assertEqual(sum(map(len, required.values())), 35)
        lines = self.text.splitlines()
        final_position = lines.index("ruleset=➡️ 国内,[]FINAL")
        for group, domains in required.items():
            remote_position = next(
                i for i, line in enumerate(lines)
                if line.startswith(f"ruleset={group},http")
            )
            for domain in domains:
                rule = f"ruleset={group},[]DOMAIN-SUFFIX,{domain}"
                with self.subTest(group=group, domain=domain):
                    self.assertEqual(lines.count(rule), 1)
                    self.assertLess(lines.index(rule), remote_position)
                    self.assertLess(lines.index(rule), final_position)

    def test_required_generator_flags_are_enabled(self):
        self.assertIn("enable_rule_generator=true", self.text)
        self.assertIn("overwrite_original_rules=true", self.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
