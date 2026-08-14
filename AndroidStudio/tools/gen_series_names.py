import re
from pathlib import Path

text = Path(r"c:\Users\Admin\Projects\RadioMan\screens\handbook\chips.py").read_text(encoding="utf-8")
m = re.search(r"series_names = \{([^}]+)\}", text, re.DOTALL)
entries = re.findall(r"'([^']+)': '([^']+)'", m.group(1))
lines = [
    "package com.lemanrus.radioman.data",
    "",
    "object SeriesNames {",
    "    private val names = mapOf(",
]
for k, v in entries:
    lines.append(f'        "{k}" to "{v}",')
lines.extend([
    "    )",
    "",
    '    fun getDisplayName(key: String): String = names[key]',
    '        ?: "Серия ${key.removePrefix(\"series\").replace(\"_ipv\", \"ИПВ\")}"',
    "",
    "    fun sortedKeys(allKeys: Set<String>): List<String> = allKeys.sortedWith(",
    "        compareBy(",
    '            { key -> if (key.replace("series", "").replace("_ipv", "").all { it.isDigit() }) 0 else 1 },',
    "            { key ->",
    '                val n = key.replace("series", "").replace("_ipv", "9999")',
    "                if (n.all { it.isDigit() }) n.toIntOrNull() ?: Int.MAX_VALUE else Int.MAX_VALUE",
    "            },",
    "            { it }",
    "        )",
    "    )",
    "}",
])
out = Path(r"c:\Users\Admin\Projects\RadioMan\AndroidStudio\app\src\main\java\com\lemanrus\radioman\data\SeriesNames.kt")
out.write_text("\n".join(lines), encoding="utf-8")
print(f"Generated {len(entries)} entries")
