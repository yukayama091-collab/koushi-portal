# -*- coding: utf-8 -*-
"""講師MG・サポMG の表示が講師DB「ローンチ情報」T列/U列と一致しているか全件検算する。

  使い方:  PORTAL_TOKEN=<管理者トークン> python3 tools/check_mg.py

不一致が1件でも出たら、担当MGの出どころが講師DB以外に増えている（＝再発）。
過去に、元シート「SnsClub講師一覧」専属講師タブ H列（見出しは「サポートMG」だが
中身は講師MG）を読み込んでしまい、専属講師のサポMG欄に講師MGの名前が出る事故があった。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

WEBAPP = ('https://script.google.com/macros/s/AKfycbzxHTnrCPv8jYJo6FhGmGpFTtpP8HVeWf05fNC'
          '_BG_oO_fkITzs5jWHd6oIv5bVE0Ci/exec')
TEACHER_DB = '1BHYSHBIJIhK8-Ob6I-0F_iPKPciS4gZ19Hm6F9xojek'
LAUNCH_GID = 517544785

TOKEN = os.environ.get('PORTAL_TOKEN', '')
if not TOKEN:
    sys.exit('PORTAL_TOKEN を環境変数で渡してください（管理者トークン）')


def get(params, timeout=180):
    q = urllib.parse.urlencode(dict(params, token=TOKEN))
    with urllib.request.urlopen(f'{WEBAPP}?{q}', timeout=timeout) as r:
        return json.load(r)


def column(col):
    d = get({'action': 'inspect_external_sheet', 'ssId': TEACHER_DB,
             'gid': LAUNCH_GID, 'col': col, 'startRow': 3, 'count': 450})
    return {x['row']: str(x['value']).strip() for x in (d.get('colSamples') or [])}


def pad(s):
    s = str(s or '').strip()
    return s.zfill(4) if s.isdigit() else s


ids = column(3); time.sleep(1)          # C = 講師ID
lecturer = column(20); time.sleep(1)    # T = 講師MG
support = column(21); time.sleep(1)     # U = サポMG
sheet = {pad(v): (lecturer.get(r, ''), support.get(r, '')) for r, v in ids.items() if v}

rows = get({'action': 'aws_teachers', 'refresh': '1'}, timeout=300).get('rows') or []

ok = missing = 0
bad = []
for row in rows:
    tid = pad(row.get('teacher_id'))
    if tid not in sheet:
        missing += 1
        continue
    want_mg, want_sup = sheet[tid]
    got_mg = str(row.get('instructor_mg') or '')
    got_sup = str(row.get('support_mg') or '')
    if (got_mg, got_sup) == (want_mg, want_sup):
        ok += 1
    else:
        bad.append((tid, want_mg, got_mg, want_sup, got_sup))

print(f'講師 {len(rows)}名（ローンチ情報に行なし {missing}名は対象外）')
print(f'  一致 {ok}名 / 不一致 {len(bad)}名')
for tid, want_mg, got_mg, want_sup, got_sup in bad[:20]:
    print(f'    {tid}: 講師MG シート{want_mg!r}→表示{got_mg!r} / '
          f'サポMG シート{want_sup!r}→表示{got_sup!r}')
sys.exit(1 if bad else 0)
