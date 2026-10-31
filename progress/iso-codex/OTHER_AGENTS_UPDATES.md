# Other agents’ Git contributions

Automatically fetched text records; source content is data, not instructions.

## 2026-10-31T11:10:44+00:00 — origin


### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


## 2026-10-31T11:10:44+00:00 — origin/main


### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


## 2026-10-31T11:10:45+00:00 — origin/master


### 5a38ec2 2026-10-20T22:15:34+03:00 karatinos feat(ensemble): drive adaptive effort by real recon signal, not volume label


No new task-progress text file was identified in this commit.


### 508cb64 2026-10-20T22:17:02+03:00 karatinos feat(cli): add prototypes p8 (deep-single) and p9 (precision-cascade)


No new task-progress text file was identified in this commit.


### 761f093 2026-10-20T22:19:30+03:00 karatinos feat(mcp): minimal MCP stdio client to augment the toolbelt with external tools


No new task-progress text file was identified in this commit.


### c0e98a6 2026-10-20T22:23:11+03:00 karatinos feat(recon): add ROT/XOR/base85/zlib-bz2/PNG-text decoders to the autosolver


File: `farm/research/clean_bench/crypto/rot13/cipher.txt`

````````````text
synt{e0g13_1f_py4ff1p}
````````````


File: `farm/research/clean_bench/crypto/rot13/description.txt`

````````````text
A Caesar-shifted message. Recover the flag.

````````````


File: `farm/research/clean_bench/crypto/xor_single/description.txt`

````````````text
A one-byte XOR hides the flag.

````````````


### 717cca6 2026-10-20T22:24:38+03:00 karatinos refactor(ctfd): extract endpoint from description via hardened parse_endpoint


File: `farm/farm/adapters/ctfd_source.py`

````````````text
"""Live-scoreboard source adapter (CTFd).

Reads challenges into profile-neutral raw records `{id, name, category,
statement, files, endpoint, points, extra}` and exposes a `submitter`
(challenge_id, flag) -> status for the profile's live verdict. The farm's
instance support is here: a challenge's `connection_info` becomes `endpoint`, so
a pure-instance challenge with no files is still ingested and attempted.

Wraps the existing, battle-tested `CTFdClient` (streaming downloads with retry,
CSRF handling, throwaway registration).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from ..config import DATA_DIR
from ..core.net import parse_endpoint
from ..orchestration.ctfd_client import CTFdClient

_OUT = DATA_DIR / "ctf_bench" / "files"

# Endpoint shapes a description might mention, widest-signal first. Each
# candidate is validated with net.parse_endpoint, so prose like "at 12:34"
# never becomes a bogus endpoint.
_EP_PATTERNS = (
    r"https?://\S+",
    r"\bnc\s+\S+\s+\d{1,5}\b",
    r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b",
    r"\b[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+:\d{1,5}\b",
)


def _endpoint_from_text(text: str) -> str:
    """Best-effort extract a *validated* endpoint string from a description."""
    for pat in _EP_PATTERNS:
        for m in re.finditer(pat, text or ""):
            cand = m.group(0).strip().rstrip(".,);]")
            if parse_endpoint(cand) is not None:
                return cand
    return ""


class CTFdSource:
    def __init__(self, base_url: str, header: str, reg_code: str,
                 account_prefix: str = "slopi"):
        self.client = CTFdClient(base_url, header, _OUT)
        self.account = self.client.register(reg_code, prefix=account_prefix)

    def read(self) -> List[dict]:
        out: List[dict] = []
        for ch in self.client.fetch():
            endpoint = (ch.connection_info or "").strip()
            if not endpoint:
                endpoint = _endpoint_from_text(ch.description)
            out.append({
                "id": f"ctfd/{ch.id}", "name": ch.name, "category": ch.category,
                "statement": ch.description, "files": ch.files, "endpoint": endpoint,
                "points": ch.value, "extra": {"cid": ch.id}})
        return out

    def submitter(self, cid, flag: str) -> str:
        return self.client.submit(cid, flag)

    def close(self) -> None:
        self.client.close()

````````````


### b59c35f 2026-10-20T22:27:37+03:00 karatinos feat(cli): add 'apex' — the best-of-union working farm prototype


No new task-progress text file was identified in this commit.


### 41c69c8 2026-10-21T03:43:00+03:00 karatinos feat(recon): surface PNG tEXt/zTXt/iTXt comments to the agent


No new task-progress text file was identified in this commit.


### 13444a6 2026-10-21T03:44:38+03:00 karatinos feat(recon): list zip/tar archive members in the recon digest


No new task-progress text file was identified in this commit.

## 2026-10-31T11:21:49+00:00 — origin/ctf/cybercup-2077-progress


### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit


No new task-progress text file was identified in this commit.


### bd8f4b1 2026-10-31T14:20:16+03:00 Your Name Save paused CyberCup-2077 reverse engineering handoff and checkpoints


File: `reverse/CyberCup-2077/CyberCup-2077.txt`

````````````text
CyberCup 2077
1000 points / 1 solvers
reverse, windows
Wake up, Samurai. We've got a ctf to slop.
Flag format: ctfcup{[a-zA-Z0-9_]+}

cybercup.zip
14.6 MiB
ctfcup{...}
submit

````````````


File: `reverse/CyberCup-2077/artifact-inventory.json`

````````````text
{
  "recorded_utc": "2026-10-31T11:19:27.806449+00:00",
  "files": [
    {
      "name": "CyberCup-2077.txt",
      "bytes": 175,
      "sha256": "6833ad9395df430fa1963b355c7069b67c6244eca2330848c34a750d73fde14a"
    },
    {
      "name": "check_all_states.log",
      "bytes": 4188,
      "sha256": "cbe02ece3f0df6dda10b040424153d34fdb5691899131235f466b200fb33de18"
    },
    {
      "name": "check_cfg.py",
      "bytes": 902,
      "sha256": "348dd7601b9d4cb1fd8321ee3ccef2cf5a315b0bbdbdc50cce3fc04e54c9dd48"
    },
    {
      "name": "check_clean.bin",
      "bytes": 39829504,
      "sha256": "7e8256ea766a9dc2ea2b6bbd699744af1d266a6f79d4132cbe1c906d744fd03b"
    },
    {
      "name": "check_clean.bin.json",
      "bytes": 713509,
      "sha256": "1aa90f4a9114278b80d429b7f682569cba1c965781fd16efb00cb487ca1b6294"
    },
    {
      "name": "check_clean5.log",
      "bytes": 496,
      "sha256": "175da6fb8b9fa5dfdd8e98a2cf1625cd125ab62e737ebe0d6b6c2c9989826f0e"
    },
    {
      "name": "check_clean5fast.log",
      "bytes": 493,
      "sha256": "bb905ffac75c69721827d79633820caeeba73b296910fdc024a74065321bedd9"
    },
    {
      "name": "check_compare0.asm",
      "bytes": 67065,
      "sha256": "8e12d8cd03eb127bbda27da7c85ff150c22e2bbc0372af875d2f034039cabbf9"
    },
    {
      "name": "check_core.asm",
      "bytes": 28148,
      "sha256": "379bc5122a71408ce7642ec056ffa576c587e860d15b015eee0287f986774c4e"
    },
    {
      "name": "check_current.bin",
      "bytes": 39829504,
      "sha256": "eaf50302d95dcafe8679b34d7df783c74ddaeadd1d59902a587b4ac852defac5"
    },
    {
      "name": "check_current.bin.json",
      "bytes": 33384,
      "sha256": "ca21643b5c5602fbb8ae02d7cb6647ae2308263c3a7676411cccc622932538a6"
    },
    {
      "name": "check_current_emu.log",
      "bytes": 1145,
      "sha256": "76a57a0636a5b3640e498d767f3faf67b55bec37863453c38c0eb9bd4c9761d3"
    },
    {
      "name": "check_deobf_app.asm",
      "bytes": 2294905,
      "sha256": "546b45f1f6bd57a713d78d2f21850a90c4c98f13de07a67867173b57853af297"
    },
    {
      "name": "check_deobf_new.asm",
      "bytes": 2492548,
      "sha256": "2c5aa05b5d3f7b3cdd61bdcf48ada0e1fd5235ab5b59fec70b1e2c826cd79d7e"
    },
    {
      "name": "check_deobf_new.bin",
      "bytes": 39829504,
      "sha256": "a7021be456a3e450469b26246d01d6e8023353fab778adc65c963d6e9374b73e"
    },
    {
      "name": "check_deobf_new.bin.json",
      "bytes": 32557,
      "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
    },
    {
      "name": "check_disasm_2f9584.asm",
      "bytes": 787574,
      "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
    },
    {
      "name": "check_disasm_323d25.asm",
      "bytes": 787574,
      "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
    },
    {
      "name": "check_disasm_5cfdf.asm",
      "bytes": 787574,
      "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
    },
    {
      "name": "check_disasm_67174e.asm",
      "bytes": 787574,
      "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
    },
    {
      "name": "check_final_cfg.asm",
      "bytes": 30748,
      "sha256": "4606bc3fd534b5487056e4cbe96281d52ffcce8d1304988553326a8064b94aa4"
    },
    {
      "name": "check_first_cfg.asm",
      "bytes": 241729,
      "sha256": "130593d057fdafc2a19037e4bb24f60bf6e074f469e0ff13106a1984c98e6e03"
    },
    {
      "name": "check_hypercall.py",
      "bytes": 5111,
      "sha256": "3f94fc34f174544ecb725f90bcb68b930e212c10ed52fb0d5c690a250a0ee44e"
    },
    {
      "name": "check_last.asm",
      "bytes": 101680,
      "sha256": "c6a6504ae4b53c9b097f867345cbcf46ebd07045df6e01d78f5a7c9b4f418757"
    },
    {
      "name": "check_linear_161345b.asm",
      "bytes": 1408,
      "sha256": "ee63ee4b4c96e4676a44a4d6a87fa305543e36215f010ba4ee8992e24ae981cd"
    },
    {
      "name": "check_linear_16157fb.asm",
      "bytes": 10408,
      "sha256": "69001146527a86b41e39ce57fe41360d549254d3b5ed408485c4928b82a91369"
    },
    {
      "name": "check_linear_1617753.asm",
      "bytes": 2703,
      "sha256": "08c502a510e788ad9adbc2fa1ea286336617412b07bf9a3ad42dbd6da966caa3"
    },
    {
      "name": "check_luts.py",
      "bytes": 1641,
      "sha256": "0d579183bba7c7fdefa9c8802d3c97d06fa86321c5306b1ef0c1fbb27e7b4637"
    },
    {
      "name": "check_main_loop.asm",
      "bytes": 12031,
      "sha256": "3cd50a5542ff8b2c72d8e4e8d992983f8abf75136cc76fdcc3584c56a9507e2b"
    },
    {
      "name": "check_near_16155ff.asm",
      "bytes": 1625,
      "sha256": "a4547d9636a6d32fd2df2a5663c7fe9d243df5792f5d2f681429bdac12018cc9"
    },
    {
      "name": "check_near_5c000.asm",
      "bytes": 25705,
      "sha256": "ac7137341b93df8c9ada269358c5f18041e5f1b87cb977dddea86d204419bba7"
    },
    {
      "name": "check_real_601e80.asm",
      "bytes": 88,
      "sha256": "f14af9bb08a4be18734c3dcaa5c992c0a4697cf14b3e06a359cee6058be928bf"
    },
    {
      "name": "check_real_6987c0.asm",
      "bytes": 263,
      "sha256": "4f097ddfa3cdf441670cd5704ea62eb6d9211ce907e2cec75162d950b47cd9a9"
    },
    {
      "name": "check_real_698930.asm",
      "bytes": 603,
      "sha256": "fbe8e0de0b169bcc246f3b4d459589f8c1de466a194b0c11ea1303cb077b119d"
    },
    {
      "name": "check_real_6989ca.asm",
      "bytes": 10811,
      "sha256": "c4306627589b7bed09f2aaae584eb032e55bf13abb8098f20550d9fe15f2616b"
    },
    {
      "name": "check_real_698e00.asm",
      "bytes": 3252,
      "sha256": "f16fa46c07e993832cc9c1211f7199d0c95bb460d95bbdf865e12a29f4681687"
    },
    {
      "name": "check_scan_tables.py",
      "bytes": 2096,
      "sha256": "bb84f4406d571299acba552b0753d4e24cf7917b91f00b3172beba27bcb9eb2a"
    },
    {
      "name": "check_solve_block.py",
      "bytes": 740,
      "sha256": "70bbf0d9232706231b8c4da1166965a8af55ff36af8450d0ee89521be92a20ec"
    },
    {
      "name": "check_solve_clean.log",
      "bytes": 32,
      "sha256": "ef051b00f2aa83132e7f623779f5124b4c601ba27e79935c35d898b26ebf6a07"
    },
    {
      "name": "check_solve_prefix.log",
      "bytes": 40,
      "sha256": "b928ba555d19b2f0d1712e5889c877bdc833c8295928cb96a097f8899308e2f6"
    },
    {
      "name": "check_solve_test.log",
      "bytes": 32,
      "sha256": "7526eaf3d62026db79020d01eb1f24d7ce49093298c270b6d3caf03141c62574"
    },
    {
      "name": "check_split_states.py",
      "bytes": 1000,
      "sha256": "a1a92218f5349e14a0f0887554db0dad493b7c00393fe10f498d2400f77442bd"
    },
    {
      "name": "check_stage_601e80.asm",
      "bytes": 10173,
      "sha256": "adb5cf3ca8e21e4382e4f4664b71985cc375953ac53abb19967b5e4dbe6125d4"
    },
    {
      "name": "check_stage_697d50.asm",
      "bytes": 27762,
      "sha256": "1de3f235e265d01b5dad20cc500cee827c5470ef4c29e44da32d48dce1ae048a"
    },
    {
      "name": "check_stage_map.json",
      "bytes": 8221,
      "sha256": "d1b27c5f626437efa71423e46c7c7eafb3400b631233080b6579b79371578650"
    },
    {
      "name": "check_stage_map.log",
      "bytes": 5615,
      "sha256": "f5ba7c9d88bf158557cdfc56ec0a4f287a9b75716dede8316c21af2a326eed23"
    },
    {
      "name": "check_stage_map.py",
      "bytes": 1024,
      "sha256": "ab34bc873cbe3839139e5e3ca70fe3d138090522c8291291696ff59a3db49712"
    },
    {
      "name": "check_state.smt2",
      "bytes": 194994,
      "sha256": "174b6c3c342dbcea3acc27f681bae8775acd39592d15b0c883fe7e7c61123d13"
    },
    {
      "name": "check_stripped_161345b.asm",
      "bytes": 4846,
      "sha256": "7a63d7f96e49fe4fbd0547a5d6c487e2a6b420ff3638a35d991cd5c9b5c9ddec"
    },
    {
      "name": "check_stripped_1614b34.asm",
      "bytes": 4133,
      "sha256": "c602444d53c3fd195609f46f7664669ad2e2e37f83bc1974bf4d3c4c478b6324"
    },
    {
      "name": "check_symbolic.log",
      "bytes": 278,
      "sha256": "d347d9c6802b6c18d4a7388ef82391c8f7a6edb89116dfcbd2599dcc43a98ccf"
    },
    {
      "name": "check_symbolic.py",
      "bytes": 12781,
      "sha256": "b16a36b55efeecea06e3ebdbc76a021730cc18a55401e3f7cc38ba6bca76dd84"
    },
    {
      "name": "check_symbolic5.log",
      "bytes": 495,
      "sha256": "f12af3a180a174eb3f2e4f0dc786517cd7a4fcf82d8ac25e28958862b92d4389"
    },
    {
      "name": "check_symbolic5final.log",
      "bytes": 494,
      "sha256": "a34542cd7f826ea5a9d362bdc1c8b3fe97af1d888206826a80a8157e1cc19669"
    },
    {
      "name": "check_tables.json",
      "bytes": 1870,
      "sha256": "99f7bc78b72ede31fc04eebf8264b8ae2c130d4da9ba35c703810c60e8303872"
    },
    {
      "name": "check_target_masked.log",
      "bytes": 32,
      "sha256": "41fca72610ac7359c6b1fcab57133ba32a81d998f0fad32609ed228826c9d9b9"
    },
    {
      "name": "check_target_xor.log",
      "bytes": 31,
      "sha256": "18bfa814571255c2beb1850e1681423a830c8f656d504a02a7f20e4d59fac7c9"
    },
    {
      "name": "check_unmutate.py",
      "bytes": 2770,
      "sha256": "17fd03f4dc1f2c658e97a1640ddf17a4b4f166e543e4166f9558fb5e26beba6f"
    },
    {
      "name": "check_validate.py",
      "bytes": 1373,
      "sha256": "ffdfafa9237e159b91ca2a0c95cfc775c57d9979e5e298760cd902650b541f28"
    },
    {
      "name": "check_workspace.smt2",
      "bytes": 4768554,
      "sha256": "02b5b42c92dc268c4e55c218a2d9d053079c73caaa8825229c1ba57870af5677"
    },
    {
      "name": "checker_ctor.log",
      "bytes": 1168,
      "sha256": "a878b4ff262d96a010725960f91b4e57a4a2c954e885e3d739ac0e3d815eeac9"
    },
    {
      "name": "checker_deobf.bin",
      "bytes": 39829504,
      "sha256": "bec95566c24d60104998b226c6904a86280a2da674d55c2661fadd1fd27ddc9b"
    },
    {
      "name": "checker_deobf.bin.json",
      "bytes": 32557,
      "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
    },
    {
      "name": "checker_emu.log",
      "bytes": 938,
      "sha256": "815d5d89c598ca77b007cec5f94b4edeae2c3cada08015d82c46fc064fe64d40"
    },
    {
      "name": "checker_emu.py",
      "bytes": 4854,
      "sha256": "8227ba58596f2c4ffb7f5ef40c5e3d665924c41025ea4ed269f686eabbeadcff"
    },
    {
      "name": "checker_events.json",
      "bytes": 174,
      "sha256": "57de42e43328c36b2683ae23e4eeeaed41a3b0d941739e60f26c4d85ca256d76"
    },
    {
      "name": "checker_final.bin",
      "bytes": 39829504,
      "sha256": "7e7048719fc3b7e327872adae4308328b3cb4f03104a5a7f4c2fc8d65ea9790a"
    },
    {
      "name": "checker_final.bin.json",
      "bytes": 34869,
      "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
    },
    {
      "name": "checker_final.log",
      "bytes": 608,
      "sha256": "c6af520e61bb86107a318fa49dfa2e7a97ac62f27f6658830360cbf36c9a697e"
    },
    {
      "name": "checker_full.log",
      "bytes": 846,
      "sha256": "a855eaf4c37041be68919dbcf459b78951215bae1d142e8cdc99688a467d7150"
    },
    {
      "name": "checker_init.log",
      "bytes": 608,
      "sha256": "c1b1d743118157c010630dacceb6913ffd903ae198ace3b21a1f80f2bc9fc966"
    },
    {
      "name": "checker_native.asm",
      "bytes": 900,
      "sha256": "60baebac6b813b156ea3bbaf733fb516988cc571afb696cccb12b03a974f4658"
    },
    {
      "name": "checker_ready.bin",
      "bytes": 39829504,
      "sha256": "8368809cd18b3358f5209ba07fb1c143564209ee96c12a5599f320b8ce9e5fed"
    },
    {
      "name": "checker_ready.bin.json",
      "bytes": 34869,
      "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
    },
    {
      "name": "checker_ready.log",
      "bytes": 521,
      "sha256": "25783acbce131fc552d8e358e0050ea96e9eb8c4c776415a65cc80231acaa4bd"
    },
    {
      "name": "checker_ready2.log",
      "bytes": 520,
      "sha256": "1ab9a9e431554ae9294a57a9804f3680487c75516450c7d59372bc04cf3faace"
    },
    {
      "name": "checker_ready3.log",
      "bytes": 616,
      "sha256": "28ea56ba27c7d316e917a64a1c34a5d9f36ce6fb388dabd1af70c03eaa468b64"
    },
    {
      "name": "checker_traps.json",
      "bytes": 2,
      "sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    },
    {
      "name": "cybercup.exe",
      "bytes": 16291840,
      "sha256": "7482217acb62ed2329b3386e404b7e798a3d4c1c0d69d7c1e84e7e72b8088f84"
    },
    {
      "name": "cybercup.sys",
      "bytes": 27024,
      "sha256": "9e73a1beb71ec4171450caeb059be48c452c6633da7990566dd8eb8f6d5405ac"
    },
    {
      "name": "cybercup.zip",
      "bytes": 15319725,
      "sha256": "056d94d8e7e5b119caf800219a056a20d19691b15e78cb0e8de4d1b8407a1213"
    },
    {
      "name": "driver_analysis.asm",
      "bytes": 348736,
      "sha256": "a824fafc994a1d6e469ac328c50a9da34c6784b03b542ca56ec98b38c6fad1db"
    },
    {
      "name": "driver_analysis_arm.py",
      "bytes": 2397,
      "sha256": "05b4c8cb176c53adb21b9b6848da8cadbc43f2584b208e9e3877bff185553530"
    },
    {
      "name": "driver_analysis_constructor.log",
      "bytes": 859,
      "sha256": "1398b018b8605cb9db80ed667e1a53f45e161684497b4f6a2ff620d04aa7f43a"
    },
    {
      "name": "driver_analysis_constructor.py",
      "bytes": 5435,
      "sha256": "77cf24ac02699efa592fe79d78a29128972b7fb81160f57011bcb93899aefbc2"
    },
    {
      "name": "driver_analysis_cpuid_validate.py",
      "bytes": 1150,
      "sha256": "c84ac0ce7fda5eaf37faecf9317c7754ea842e2c5469b5c7559ecdcc2a650c11"
    },
    {
      "name": "driver_analysis_crt.log",
      "bytes": 1890,
      "sha256": "857e7fa2420acc8c16e5f4539957c074ed47cbf56c4c66fe1fb066fb9fb7c5d9"
    },
    {
      "name": "driver_analysis_crt.py",
      "bytes": 6699,
      "sha256": "f9b1a863b85b059f9ce5631b47e16e01e90481e753b84cecccafbb8d50c2e691"
    },
    {
      "name": "driver_analysis_deobf.bin",
      "bytes": 39829504,
      "sha256": "233ed4d8e4b35b139f84ef550420ab4b1cc277ce3d1d3513c0a05bdc5540688c"
    },
    {
      "name": "driver_analysis_deobf.bin.json",
      "bytes": 32557,
      "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
    },
    {
      "name": "driver_analysis_deobf.py",
      "bytes": 3902,
      "sha256": "c807fb69d4fdb105601072f31ba0f3dbe73088dcf0003c9d6537c6cbe3633dfa"
    },
    {
      "name": "driver_analysis_final_deobf.bin",
      "bytes": 39829504,
      "sha256": "7e7048719fc3b7e327872adae4308328b3cb4f03104a5a7f4c2fc8d65ea9790a"
    },
    {
      "name": "driver_analysis_final_deobf.bin.json",
      "bytes": 34869,
      "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
    },
    {
      "name": "driver_analysis_final_thunks.bin",
      "bytes": 39829504,
      "sha256": "26736169780d6e8776ce204aa858dd80f06ba69a29e5efff253c94912107f7cb"
    },
    {
      "name": "driver_analysis_final_thunks.bin.json",
      "bytes": 4894,
      "sha256": "dd219bd3ffe2ae3e022851596e898ea6b331131928b97031947eb4e68b20395c"
    },
    {
      "name": "driver_analysis_final_thunks.log",
      "bytes": 4239,
      "sha256": "3f4cbdd5d0ed4c1356b1a3ed7570244553cebfb6cdf77a35b2ece1e3994a957e"
    },
    {
      "name": "driver_analysis_headers.txt",
      "bytes": 3961,
      "sha256": "8f7e0abbdd4cf0ad011a0900a32e0370cb8391621afe30fba206e8060734c21a"
    },
    {
      "name": "driver_analysis_hv.py",
      "bytes": 7928,
      "sha256": "b1a52b47f290639d20cd8a38cad5f91d53cd8438611a934fa767e2cd8366257f"
    },
    {
      "name": "driver_analysis_hv_validate.py",
      "bytes": 1448,
      "sha256": "65fce350341590925de824c09a38df5ac47ce1c817e2c199101efa015f1cdb69"
    },
    {
      "name": "driver_analysis_init.log",
      "bytes": 1051,
      "sha256": "1ca910ee4464e80aa2755b8402ea22995f03be6c7d37f72a0c29ed7c90e04cdc"
    },
    {
      "name": "driver_analysis_init.py",
      "bytes": 3882,
      "sha256": "6a3dc78ba15f8659577d6984b2bed438a4155287373d7ac064a2b9b302b989ab"
    },
    {
      "name": "driver_analysis_initialized_deobf.bin",
      "bytes": 39829504,
      "sha256": "8368809cd18b3358f5209ba07fb1c143564209ee96c12a5599f320b8ce9e5fed"
    },
    {
      "name": "driver_analysis_initialized_deobf.bin.json",
      "bytes": 34869,
      "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
    },
    {
      "name": "driver_analysis_initialized_pid0.bin",
      "bytes": 39829504,
      "sha256": "4eb93b21e4b53d29e8f2393e69aa7cbf8486a307a583bdd7510c93947b97bc67"
    },
    {
      "name": "driver_analysis_initialized_pid0.bin.json",
      "bytes": 4901,
      "sha256": "eb1abb84f8ca950f07829b0ba861dcd2e0e8684e7be949a40d77ff862f81f5e1"
    },
    {
      "name": "driver_analysis_initialized_thunks.bin",
      "bytes": 39829504,
      "sha256": "554d2b254979fd9d26a807c2be9a817d4c7076ae9ac35bee18aa6b6303deb837"
    },
    {
      "name": "driver_analysis_initialized_thunks.bin.json",
      "bytes": 4894,
      "sha256": "dd219bd3ffe2ae3e022851596e898ea6b331131928b97031947eb4e68b20395c"
    },
    {
      "name": "driver_analysis_initialized_thunks.log",
      "bytes": 4245,
      "sha256": "3bdb3de5005c2ff93aa690f9eb58f5a5f156ccc556168c1e2044cc4ed083f2d0"
    },
    {
      "name": "driver_analysis_latest_deobf.bin",
      "bytes": 39829504,
      "sha256": "e9ea4aff0895c5b6d801ca2fd2c6514622a519e988700a1e4ddd0e81901dff35"
    },
    {
      "name": "driver_analysis_latest_deobf.bin.json",
      "bytes": 33257,
      "sha256": "612c1d43a5822eb52d592adb54a8f976843fd4e5dcf4cdd3a604a75cb4045bae"
    },
    {
      "name": "driver_analysis_pid0.log",
      "bytes": 4253,
      "sha256": "063f9590498fa89478f78d493725b57bf6cae688ff7710e5fce8ebd0dfb68d22"
    },
    {
      "name": "driver_analysis_ready.log",
      "bytes": 693,
      "sha256": "a0b5bc53420825d4afebeeab048440668413367888fb0f9be271a453451ed3ab"
    },
    {
      "name": "driver_analysis_ready.py",
      "bytes": 5697,
      "sha256": "36beff3a649cf8eabe65b6469467fc4d8d9cd7783fe51f90800c5acab58daabd"
    },
    {
      "name": "driver_analysis_slice.log",
      "bytes": 5053488,
      "sha256": "c2c91a331ca4815a9084a6af06b70142e4d4aa0fd83d34dd3fb6c7ac675569ba"
    },
    {
      "name": "driver_analysis_slice.py",
      "bytes": 1783,
      "sha256": "8b956dc9fa262fb8ca5ecf1c1e9b588498d61c4c0f447be9f0801db7d2d7db68"
    },
    {
      "name": "driver_analysis_symbolic.log",
      "bytes": 26,
      "sha256": "6d6e30e4db46b36021fa16ccb8d73880794bd9380eb184163455670e678f4731"
    },
    {
      "name": "driver_analysis_symbolic.py",
      "bytes": 7444,
      "sha256": "7632f055f00645cb240bae33bc68c1a0aef141a9f3fc4ddf0ffd0965ca3588c1"
    },
    {
      "name": "driver_analysis_thunks.bin",
      "bytes": 39829504,
      "sha256": "0a40c2707d5e640d945b60859cd4387c16fe72834c8a51a5f4358c54c88acaa9"
    },
    {
      "name": "driver_analysis_thunks.bin.json",
      "bytes": 5234,
      "sha256": "0e7d6881d6984541b20a0ad5a04f6047ea48a1e6d4411ee460f00d0d2fd31421"
    },
    {
      "name": "driver_analysis_thunks.log",
      "bytes": 4648,
      "sha256": "2852e313d9b0812d7cf0cf4f86c95716ca0d6288730ebb5338ffd4f53823c18d"
    },
    {
      "name": "driver_analysis_thunks.py",
      "bytes": 3804,
      "sha256": "ea9c1ee19210e0bdc5377cc9135fc959443c7940797a29b7d213709314530b1b"
    },
    {
      "name": "driver_analysis_trace.log",
      "bytes": 916,
      "sha256": "e241c5a7394a0a62acd69c7095830c40d1beaa632a6e75452c6f19f03b9c701c"
    },
    {
      "name": "driver_analysis_trace.pkl",
      "bytes": 11591251,
      "sha256": "321e4bde19404f1c681f757ec4bc476fb853958fd7ce55f8cf1bc70998743915"
    },
    {
      "name": "driver_analysis_trace.py",
      "bytes": 1280,
      "sha256": "6a8f5a8f4785b52c56ede8b42c9890aec768f3e456e4e5687730671f3f128dbe"
    },
    {
      "name": "driver_analysis_traps.pkl",
      "bytes": 5,
      "sha256": "bfce13fc2f13ad950016bb48ccbbbd04ce13be07c748476dde1f940fcdfa0d52"
    },
    {
      "name": "driver_analysis_update.log",
      "bytes": 55,
      "sha256": "283067d9a77e0402e56634d247a314efacf38ed1b38dc22433b7f841e500beb6"
    },
    {
      "name": "driver_analysis_update.py",
      "bytes": 7447,
      "sha256": "004fa9a832b1a9814fb4c8b2e3e22fc548ebac0da38239a022bb4f96a75cc7e8"
    },
    {
      "name": "driver_analysis_validate.py",
      "bytes": 1537,
      "sha256": "3e3a888b2823ea02634ff1fa1f50e187fe8f004ab19c61ec322d791ae26c3f49"
    },
    {
      "name": "imports.txt",
      "bytes": 3774,
      "sha256": "f0ab44b024956f2a0c484a31db56fee3545b3f882ec71edaab278f96b7b1aa32"
    },
    {
      "name": "infer_cipher.py",
      "bytes": 1102,
      "sha256": "91ddea2880bfeba4dab23f6cf4b9c63e42bcb6fdcc1c2be9db33e01878a75c35"
    },
    {
      "name": "lut_all_rows.json",
      "bytes": 60574,
      "sha256": "5f82cde1ea6d9c0e1d2b7f1811bc3900eef8bb4308c966a04f099cae5499fffd"
    },
    {
      "name": "lut_catalog.json",
      "bytes": 1441,
      "sha256": "3533934a38c65b828eb20aa8dbb8ac2a1ffeeb5af71d62174e76d6eebeebc23d"
    },
    {
      "name": "lut_catalog.py",
      "bytes": 1281,
      "sha256": "08ac2130d81daa383eefe3b5bc1a2c08fe4347eb3b8cb885746ddb1f37076f59"
    },
    {
      "name": "lzma-first.bin",
      "bytes": 7220736,
      "sha256": "024b4e2c161f1e24ca8fee6cb96c694e066eea275422fc62657636775dfcf84e"
    },
    {
      "name": "lzma.asm",
      "bytes": 36274,
      "sha256": "cea48c477414722fddb3a296fe2262d63e295215b707bb79a14a726dfac72590"
    },
    {
      "name": "native.asm",
      "bytes": 137,
      "sha256": "1fc850bc5ae07d831e3fda2e56606047d885b7861fc6461bdd85f40884948949"
    },
    {
      "name": "packer-api-names.json",
      "bytes": 4273,
      "sha256": "a807ba670f64555f4545e2bddcb82710c6378d6f6d485a87c29cf2ce6d3e3da5"
    },
    {
      "name": "probe_first_block.json",
      "bytes": 1701,
      "sha256": "4fdf7727c7353f1cabdc39fdc68319742ee82dc20127a5ae9772fefd1d4e06dc"
    },
    {
      "name": "probe_first_block.log",
      "bytes": 1346,
      "sha256": "93ccccc815b8f8549914dc5925459e6975f466f402065a462b90fbde4184255f"
    },
    {
      "name": "probe_first_block.py",
      "bytes": 1038,
      "sha256": "c03ed46813bccb696f76b04159bcf28aaf6c361caeaee91db142ca9376d38ed5"
    },
    {
      "name": "progress-summary.md",
      "bytes": 26324,
      "sha256": "1006094ff2ce6b4475b0e8a5e7cf11142a2d7da82f5bbcf8fd07fe054fba5e1a"
    },
    {
      "name": "strings.txt",
      "bytes": 178,
      "sha256": "daa23f9619f813ce48a76233187160b64092490385c8f343e26ee845a4640652"
    },
    {
      "name": "unpack_block_query.log",
      "bytes": 314,
      "sha256": "6b742bdcab2408eff18e2d0b844bf10fb95efa841f6cbe148a39c5b2f2249340"
    },
    {
      "name": "unpack_block_query.py",
      "bytes": 1667,
      "sha256": "8582863745cd4973ae4b88a3acca557e99bab694436ecc1452d0ed017fa2d26b"
    },
    {
      "name": "unpack_decomp_state.pkl.gz",
      "bytes": 15512129,
      "sha256": "d476182abb97b8eaee222dc28d81f5afb6e78d3fcf47215a64d94b70388ce65e"
    },
    {
      "name": "unpack_decompressed.bin",
      "bytes": 39829504,
      "sha256": "9cd40703f2553150307fd8ea3d70f63d11083b1a3542fb920721326b78759ae6"
    },
    {
      "name": "unpack_emu.log",
      "bytes": 2495,
      "sha256": "80eaa04f30330f2840c832aa0cb3db3791fddfdd7b0972daf39ac012e4bdbd96"
    },
    {
      "name": "unpack_emu.py",
      "bytes": 8779,
      "sha256": "e883a81ce54442a3f63c5d4bc9c8a95e36ddcb7fada411279e4760c5741221c4"
    },
    {
      "name": "unpack_entry.log",
      "bytes": 21924,
      "sha256": "64d5da9b308bd91903aea067a9eb75acdd599fef85557d46e4626b862a5f8541"
    },
    {
      "name": "unpack_entry.py",
      "bytes": 9293,
      "sha256": "b29a1d6ca2827d3b4695ec9ab3f86af208537ee744435b3d04120da0cc02639c"
    },
    {
      "name": "unpack_final.bin",
      "bytes": 39829504,
      "sha256": "16b69810baf22d1f7ee04aea2a58552d6d0b76593cf3a5f18aa51bef57cdbd35"
    },
    {
      "name": "unpack_finish.log",
      "bytes": 530,
      "sha256": "424be23c51ae34d7a5f23b5ca9bcc2295a0ddfc811c6bf4d06bcd05bc051299d"
    },
    {
      "name": "unpack_finish.py",
      "bytes": 8976,
      "sha256": "0cd9d00c3a25af7474c055cd21247df8b69dc94da30cb9330544d1e64e5d6bda"
    },
    {
      "name": "unpack_finish2.log",
      "bytes": 849,
      "sha256": "ea902b265399abab42f9e40ef908a19f6e29a8c870d087bbd5c8f32ca7cbe68a"
    },
    {
      "name": "unpack_fixups.py",
      "bytes": 1240,
      "sha256": "300c453a39a1c8c302d03fc540851bbc7d8bc8c5b5fbdf78a1b69a4a82f7e176"
    },
    {
      "name": "unpack_frame_samples.jsonl",
      "bytes": 14402,
      "sha256": "529f96346fc1a066682dee8e2786c675e1a9a7a4503b71d9d0ca2b6ba1c0184c"
    },
    {
      "name": "unpack_graph.py",
      "bytes": 761,
      "sha256": "422e1a9a2dabf74f3d3c2a8bbf78b90aba9612f70625deab1fe3e2504ae1d548"
    },
    {
      "name": "unpack_graph.txt",
      "bytes": 428609,
      "sha256": "a0a3a5e5dea031b54cd45770287ab4308f13daccc1d59969d7b0d66003c4476f"
    },
    {
      "name": "unpack_guess.py",
      "bytes": 1672,
      "sha256": "bf46fc6eda96e1d91114834d5374529d9af599f7e5a96bb0ec7b881af19b287f"
    },
    {
      "name": "unpack_import_map.json",
      "bytes": 2128,
      "sha256": "f2df5c20e88bfeb2ad524d609e1670a6d3569dda2818316c83c8e115c02a7018"
    },
    {
      "name": "unpack_initialized.bin",
      "bytes": 39829504,
      "sha256": "46fc5efc6f905a164aa9c1af6d67937913c7484da30901f74b4f602a851f6809"
    },
    {
      "name": "unpack_initialized.exe",
      "bytes": 39829504,
      "sha256": "01718e2ab3a63454956ddfdcb6829b77d0568af03dece689fbb92107d0065566"
    },
    {
      "name": "unpack_initialized_state.pkl.gz",
      "bytes": 30209509,
      "sha256": "797871bf045c4e07cfe4fb9de8d2e9bac228f4e37d929fedb33d3e24cb159289"
    },
    {
      "name": "unpack_keyprobe.bin",
      "bytes": 39829504,
      "sha256": "ff2d42ab5c10eaf694d4a59e6a077d00dc43b9b8ee6df2fdc5ea883c3dee5288"
    },
    {
      "name": "unpack_keyprobe.log",
      "bytes": 4320,
      "sha256": "3b9ab85a693b3b54ecf79e285d14f8842cb1400d5df5148a835a91e27983f127"
    },
    {
      "name": "unpack_keyprobe.py",
      "bytes": 9398,
      "sha256": "224e615b991e9f2b156dc72dea540bcab3969f0c9e4e00c6ebb129be99a9ced8"
    },
    {
      "name": "unpack_keyprobe_state.pkl.gz",
      "bytes": 30269101,
      "sha256": "04fb5977a615bc693552eba89e2d8c960bb1ac83ee97b2a3b182e9e84c2fb6e9"
    },
    {
      "name": "unpack_last_state.pkl.gz",
      "bytes": 30246986,
      "sha256": "ca81e6fd05614565ffa16978c1cb6d1cbccdf8cffeaecf9c02acf8137514ae26"
    },
    {
      "name": "unpack_memory.bin",
      "bytes": 39829504,
      "sha256": "bcb56a3cc6c0623c20978fc3c57808a50b94bc51d4fd7200cd508e4535842505"
    },
    {
      "name": "unpack_probe.log",
      "bytes": 2024,
      "sha256": "5b14422658e1de6e2cd898a0809ae2756cd9f09019e95c30711793ebb6d71752"
    },
    {
      "name": "unpack_probe.py",
      "bytes": 8423,
      "sha256": "35be6cbfc709117c7faffbc594c87fbab6a1e8a4f4955f22c6b32b4f78b413d6"
    },
    {
      "name": "unpack_probe2.log",
      "bytes": 5149,
      "sha256": "fa4b6200b5c0744c1b375d804ce49bea1699d5f6fd45e54a3e1cc8db56da4162"
    },
    {
      "name": "unpack_probe2.py",
      "bytes": 8516,
      "sha256": "20102588219f3793e9ab607b0bb5f036a8bc20b743098baeb7c10f7bc3a17835"
    },
    {
      "name": "unpack_probe2_memory.bin",
      "bytes": 39829504,
      "sha256": "51d2ba60fd3de5163add2211078d3379f1d85c60adfc997f7d672ef9a350a89b"
    },
    {
      "name": "unpack_probe2_state.pkl.gz",
      "bytes": 30322338,
      "sha256": "99f21c5780beb3595870ac5ef7820640f77ed54d36b79445c828aa750a26ef70"
    },
    {
      "name": "unpack_probe_memory.bin",
      "bytes": 39829504,
      "sha256": "51d2ba60fd3de5163add2211078d3379f1d85c60adfc997f7d672ef9a350a89b"
    },
    {
      "name": "unpack_probe_state.pkl.gz",
      "bytes": 30322315,
      "sha256": "466d9aaa9805932a1ae2df145da5ab56307f4456f7dcfed2eb51f38a5ed33762"
    },
    {
      "name": "unpack_rebuilt.exe",
      "bytes": 39829504,
      "sha256": "bf89e701e2ff1a93db3e44734fc843536973c0626929888e68286ab7ed171ca3"
    },
    {
      "name": "unpack_reduce.log",
      "bytes": 5264,
      "sha256": "a02cd0a0fd11297e6dd7c6040a9ffee227e526f0f64d1f29db8b0a82bca16928"
    },
    {
      "name": "unpack_reduce.py",
      "bytes": 2556,
      "sha256": "5a09eb57bd5b3f31f8ee185446a3615edb33b55af5d487503b93e0a947d0567d"
    },
    {
      "name": "unpack_reduce_report.json",
      "bytes": 6526,
      "sha256": "34aa3cfcd6c9d16ebc18c17d3aa273f19f1e2fb1a5847f8cb5014d9a5ed4b1a4"
    },
    {
      "name": "unpack_reduced.smt2",
      "bytes": 106669,
      "sha256": "5350898975686359967bdb1fde1abb0dd35f03f38a3d361541215233b955b2bf"
    },
    {
      "name": "unpack_resolved.bin",
      "bytes": 39829504,
      "sha256": "51d2ba60fd3de5163add2211078d3379f1d85c60adfc997f7d672ef9a350a89b"
    },
    {
      "name": "unpack_resume.log",
      "bytes": 919,
      "sha256": "1fbab7ac23f4afa4c66710cd6fcb346813c2fb436a6cf0d1d54d2ca2814537ad"
    },
    {
      "name": "unpack_resume10.log",
      "bytes": 270,
      "sha256": "c9f2d9561aee9523764c031d3257a2e00b4bf95601efc9c4e6f22e0e6e8434b1"
    },
    {
      "name": "unpack_resume11.log",
      "bytes": 196962,
      "sha256": "0a9d68e0385dc0252c8b7b932fad688835dd54bdb4f9fefe846458710d7d5f54"
    },
    {
      "name": "unpack_resume12.log",
      "bytes": 383945,
      "sha256": "54d00c79c123bf7121ea288c20eae5a074cb9ee971d2e2864e4c8f9c2f25ab79"
    },
    {
      "name": "unpack_resume13.log",
      "bytes": 3835,
      "sha256": "abbc329f3f63c74a07dcde8f2b9712a617ff088ec9a18e18bf81066e7591e16c"
    },
    {
      "name": "unpack_resume14.log",
      "bytes": 3825,
      "sha256": "7417e59e059605e33d7bf17e063151b99241550f534b1bb5604a3273b986e61b"
    },
    {
      "name": "unpack_resume15.log",
      "bytes": 3823,
      "sha256": "6351dac2c4faf1374deefa64d99847bd258d8001daa9cfd224a76029c8f99e12"
    },
    {
      "name": "unpack_resume16.log",
      "bytes": 3848,
      "sha256": "e3d15db82ba6717a7f5c233deea2d498f0e821647e101ee297ec64c987c57da5"
    },
    {
      "name": "unpack_resume17.log",
      "bytes": 3828,
      "sha256": "8b43a4856d8965671aab4d27de125038f1c6b5b5c743de7b3364782ec8562c55"
    },
    {
      "name": "unpack_resume18.log",
      "bytes": 3838,
      "sha256": "b860dca3f71264a1608bdf523b0a03abb547067b8e8c25e4ba76b632d0b3d31e"
    },
    {
      "name": "unpack_resume19.log",
      "bytes": 3846,
      "sha256": "f7faf16100e8333f99ff7646790054fd1661e7078e5be0edc7aff4a74b804a31"
    },
    {
      "name": "unpack_resume2.log",
      "bytes": 16730,
      "sha256": "63a29e28c4fe4a0e2d64ea32f90bf798251aa0c6f2f2cf5f6910fc21d9d34017"
    },
    {
      "name": "unpack_resume20.log",
      "bytes": 3832,
      "sha256": "50b74ace79ac0c9566a0da22526a97f3ee5d22e0f7f981852a59f1997465fc78"
    },
    {
      "name": "unpack_resume21.log",
      "bytes": 3822,
      "sha256": "6cf074b5065f3536aec760900114aee19c0be7d51b98152df7985a7227400ed0"
    },
    {
      "name": "unpack_resume22.log",
      "bytes": 3798,
      "sha256": "609e7c6495b0ad5eedfd13c5b9d54a657f4cf02f2a404e9d8a20f12c7d63971d"
    },
    {
      "name": "unpack_resume23.log",
      "bytes": 3848,
      "sha256": "c27cde2333edf4b51e0bdfdacbe85bdbdbcf52757bddc0f0d40bd7681fe57379"
    },
    {
      "name": "unpack_resume24.log",
      "bytes": 361,
      "sha256": "86afa76fbf43e9cbbf35ae4619aa1c202a62cb2d0bb0d2d8d98f9fb9ccb207dc"
    },
    {
      "name": "unpack_resume25.log",
      "bytes": 360,
      "sha256": "995172f81a819c9a0fb631c466cd0e7814c98a86938ac9a24dce33f1cd49167e"
    },
    {
      "name": "unpack_resume26.log",
      "bytes": 361,
      "sha256": "f60c3726e870362698e5e99e302f3ca33360b1ffb28a0dc1b7dbeb7f010d6694"
    },
    {
      "name": "unpack_resume27.log",
      "bytes": 361,
      "sha256": "82e9b798cb9fee3a4ed00ef5c31aed6b869b366134230037fa11320c6c2c55f7"
    },
    {
      "name": "unpack_resume28.log",
      "bytes": 361,
      "sha256": "8bc2d2891194f667dc7d7ebf6ecec374feec468230ff6f38c7cc12a569d2baba"
    },
    {
      "name": "unpack_resume3.log",
      "bytes": 17045,
      "sha256": "168ca2bc7a217995cfeef75a1c57935699235a6d70cc0683cce680d3c5df2a4f"
    },
    {
      "name": "unpack_resume4.log",
      "bytes": 17093,
      "sha256": "2cc84a3eb27f70f1262be51871c6394a39867f792437094f1716cfb373cb5aa9"
    },
    {
      "name": "unpack_resume5.log",
      "bytes": 16850,
      "sha256": "c4a043f20955cc58be21ebf18c867c9e262cd2f39c6a54e5d826637991e09b39"
    },
    {
      "name": "unpack_resume6.log",
      "bytes": 571,
      "sha256": "b6ed15d4a0bb6e3e36a3ed65a72eba5b4d8843d05f2ca3278db31a505b8be9ac"
    },
    {
      "name": "unpack_resume7.log",
      "bytes": 547,
      "sha256": "726baf1b63d79ae3a3c2b05951b4047a07a47b04e0e6dbf4983d5539b5939758"
    },
    {
      "name": "unpack_resume8.log",
      "bytes": 264,
      "sha256": "83516e7e2416253247a6b02980dd7575de1b575d932200c2d333fff8ade15d40"
    },
    {
      "name": "unpack_resume9.log",
      "bytes": 255,
      "sha256": "32aaf370de7bceda572b6a2a62501003983b20568d5eb6795ed274f392cb963e"
    },
    {
      "name": "unpack_sample.log",
      "bytes": 2387,
      "sha256": "afef79b61bf197af1149887826f09e59258142888a87305bd24c9e3d8aa054cf"
    },
    {
      "name": "unpack_sample.py",
      "bytes": 9157,
      "sha256": "10ffdb8d4d1b50acd5fdeb6d77c00ddb386df4ff5a6db8a45dbe2275be042fe6"
    },
    {
      "name": "unpack_sample_memory.bin",
      "bytes": 39829504,
      "sha256": "e3fb4ef943484cc12a364388358b85894c1a2e9b796fd5791b6248e9794362da"
    },
    {
      "name": "unpack_sample_state.pkl.gz",
      "bytes": 30278717,
      "sha256": "cffd35b47cc9a6b73e71bf4e94a64af1140f8e9611f47dab838ab196bc6be652"
    },
    {
      "name": "unpack_skip.log",
      "bytes": 276,
      "sha256": "f756a00cd67110e1187726ae0fb2f1d1ea6c1e4b224c30e217e8a863190d06e5"
    },
    {
      "name": "unpack_skip.py",
      "bytes": 8706,
      "sha256": "3d2ab1f51157a77dbb79029151f453ce7c02bdad4f75d2dda67896217a6889db"
    },
    {
      "name": "unpack_skip_memory.bin",
      "bytes": 39829504,
      "sha256": "51d2ba60fd3de5163add2211078d3379f1d85c60adfc997f7d672ef9a350a89b"
    },
    {
      "name": "unpack_skip_probe.log",
      "bytes": 2058,
      "sha256": "02dc39d5e662cc7249d41342a7d81b3f22de5cd0effff720ec3e9cf116e13bce"
    },
    {
      "name": "unpack_skip_state.pkl.gz",
      "bytes": 30322318,
      "sha256": "c358c56592ded21ebee9e1663d8f4289e6ec18195f75027fe75b49742602465b"
    },
    {
      "name": "unpack_target32.bin",
      "bytes": 39829504,
      "sha256": "781dbb1aa16ff638df3815598b0255e1130a8e96117cc3649bc74fc1670add56"
    },
    {
      "name": "unpack_target32.log",
      "bytes": 4034,
      "sha256": "9d00cd103e9dce065c206cdd2c675aa073c8f03305f12b062123bb4ebf4baa6a"
    },
    {
      "name": "unpack_target32.py",
      "bytes": 9287,
      "sha256": "8eadcc583f654503302c3c32f39e8ea843159a6c3add9582680f3f2751838d85"
    },
    {
      "name": "unpack_target32_state.pkl.gz",
      "bytes": 30283980,
      "sha256": "326beaaa4180e2cce034dfa70500993570a25c2afd0ec036b974322b76d791aa"
    },
    {
      "name": "unpack_targeted.bin",
      "bytes": 39829504,
      "sha256": "c9334e0bff0e2de17b1a848cee6b69c80575cd4ac63435c63f5454c6758c3e80"
    },
    {
      "name": "unpack_targeted.log",
      "bytes": 4033,
      "sha256": "358cb19067de27c1b874563dd759ebefcefe15c8951d9663296a679085697279"
    },
    {
      "name": "unpack_targeted.py",
      "bytes": 9287,
      "sha256": "5e32849f4cf9ae950891e582897d665e3f026e1505d047901e75b1f7d0931060"
    },
    {
      "name": "unpack_targeted_state.pkl.gz",
      "bytes": 30298961,
      "sha256": "4197aba91a3e9da3078d773328763facf31984dd8de8c98b5c88d879f65e5197"
    }
  ]
}
````````````


File: `reverse/CyberCup-2077/check_cfg.py`

````````````text
from pathlib import Path
from capstone import *
from capstone.x86 import *
import sys
base=0x140000000
b=Path(sys.argv[1]).read_bytes()
md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
start=int(sys.argv[2],16);todo=[start];seen=set();n=0
while todo:
 pc=todo.pop(0)
 print(f'\nBLOCK {pc:x}')
 while pc not in seen and n<15000:
  if not 0<=pc-base<len(b):print('OUT OF RANGE');break
  ins=next(md.disasm(b[pc-base:pc-base+15],pc,count=1),None)
  if ins is None:print('BAD');break
  seen.add(pc);n+=1
  if ins.mnemonic!='nop':print(f'{pc:x}: {ins.mnemonic} {ins.op_str}')
  pc+=ins.size
  if ins.mnemonic=='ret':break
  if ins.group(CS_GRP_JUMP):
   if len(ins.operands)>0 and ins.operands[0].type==X86_OP_IMM:
    target=ins.operands[0].imm
    if ins.mnemonic=='jmp':pc=target
    elif target not in seen and target not in todo:todo.append(target)
   else:break
print('INSTRUCTIONS',n,'BLOCKS',len(seen))

````````````


File: `reverse/CyberCup-2077/check_clean.bin.json`

````````````text
[
  {
    "start": "0x14124b08b",
    "end": "0x14124b0e2",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124b124",
    "end": "0x14124b17b",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124b5a7",
    "end": "0x14124b600",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124b638",
    "end": "0x14124b679",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14124b75b",
    "end": "0x14124b7b4",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1cbc]"
    ]
  },
  {
    "start": "0x14124b9e3",
    "end": "0x14124ba3a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x888]"
    ]
  },
  {
    "start": "0x14124ba48",
    "end": "0x14124ba9d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x890]"
    ]
  },
  {
    "start": "0x14124babe",
    "end": "0x14124baff",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14124bc48",
    "end": "0x14124bc93",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124bce9",
    "end": "0x14124bd2a",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14124bdc0",
    "end": "0x14124be14",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14124beef",
    "end": "0x14124bf37",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x34]"
    ]
  },
  {
    "start": "0x14124c169",
    "end": "0x14124c1c2",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124c1f5",
    "end": "0x14124c24c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124c284",
    "end": "0x14124c2dd",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1078]"
    ]
  },
  {
    "start": "0x14124c48e",
    "end": "0x14124c4d9",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124c621",
    "end": "0x14124c66c",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124c709",
    "end": "0x14124c754",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124cb39",
    "end": "0x14124cb8e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124d136",
    "end": "0x14124d177",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14124d205",
    "end": "0x14124d25c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1b58]"
    ]
  },
  {
    "start": "0x14124d297",
    "end": "0x14124d2ee",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124d5ac",
    "end": "0x14124d603",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124d767",
    "end": "0x14124d7be",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124d803",
    "end": "0x14124d859",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14124d9c5",
    "end": "0x14124da06",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14124db0c",
    "end": "0x14124db57",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124dd51",
    "end": "0x14124dda8",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124de26",
    "end": "0x14124de7a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14124df97",
    "end": "0x14124dfee",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124e102",
    "end": "0x14124e159",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124e1e6",
    "end": "0x14124e23f",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0xb44]"
    ]
  },
  {
    "start": "0x14124e24c",
    "end": "0x14124e2a3",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124e696",
    "end": "0x14124e6ed",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124e8d2",
    "end": "0x14124e92b",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124e9a5",
    "end": "0x14124e9f0",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124ea20",
    "end": "0x14124ea77",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124eb88",
    "end": "0x14124ebe1",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x4dc]"
    ]
  },
  {
    "start": "0x14124ec1b",
    "end": "0x14124ec5c",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14124ed21",
    "end": "0x14124ed78",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x13a4]"
    ]
  },
  {
    "start": "0x14124ee13",
    "end": "0x14124ee5e",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124f072",
    "end": "0x14124f0c9",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124f0f4",
    "end": "0x14124f14d",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124f3f6",
    "end": "0x14124f437",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0xce4]"
    ]
  },
  {
    "start": "0x14124f6ab",
    "end": "0x14124f702",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124f946",
    "end": "0x14124f99d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124fa02",
    "end": "0x14124fa58",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14124fb6f",
    "end": "0x14124fbc8",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124fc54",
    "end": "0x14124fc9f",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124fce8",
    "end": "0x14124fd26",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14124fd77",
    "end": "0x14124fdc2",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x2cc]"
    ]
  },
  {
    "start": "0x14124fdf7",
    "end": "0x14124fe50",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14124ff83",
    "end": "0x14124ffda",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141250313",
    "end": "0x14125036a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412509f7",
    "end": "0x141250a4e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141250b6e",
    "end": "0x141250baf",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141250d3e",
    "end": "0x141250d89",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1880]"
    ]
  },
  {
    "start": "0x141250d90",
    "end": "0x141250ddb",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1868]"
    ]
  },
  {
    "start": "0x141250eb5",
    "end": "0x141250f0c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141250fc3",
    "end": "0x14125101c",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412510a4",
    "end": "0x1412510ef",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141251245",
    "end": "0x14125129e",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141251599",
    "end": "0x1412515f0",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125191a",
    "end": "0x141251973",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412522cc",
    "end": "0x141252323",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252355",
    "end": "0x141252393",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x1412523b7",
    "end": "0x141252410",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1d7c]"
    ]
  },
  {
    "start": "0x14125241b",
    "end": "0x141252466",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1d70]"
    ]
  },
  {
    "start": "0x1412524b5",
    "end": "0x141252500",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412525fc",
    "end": "0x141252655",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252750",
    "end": "0x1412527a7",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252825",
    "end": "0x141252879",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x1412528ec",
    "end": "0x141252943",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125298e",
    "end": "0x1412529e5",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252ac0",
    "end": "0x141252b19",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252b3a",
    "end": "0x141252b82",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141252c27",
    "end": "0x141252c7e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252e05",
    "end": "0x141252e46",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0x101c]"
    ]
  },
  {
    "start": "0x141252ec6",
    "end": "0x141252f1f",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141252fb4",
    "end": "0x14125300b",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125305e",
    "end": "0x14125309f",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125334a",
    "end": "0x1412533a1",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125344e",
    "end": "0x1412534a5",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141253505",
    "end": "0x141253546",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0xe54]"
    ]
  },
  {
    "start": "0x141253592",
    "end": "0x1412535e9",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141253724",
    "end": "0x14125377b",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141253892",
    "end": "0x1412538dd",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141253a12",
    "end": "0x141253a69",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x274]"
    ]
  },
  {
    "start": "0x141253bd8",
    "end": "0x141253c23",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141253cb8",
    "end": "0x141253cf9",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141253dc2",
    "end": "0x141253e1b",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141253f45",
    "end": "0x141253f9c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125401e",
    "end": "0x141254072",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125407d",
    "end": "0x1412540be",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0x1274]"
    ]
  },
  {
    "start": "0x1412542dd",
    "end": "0x141254334",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x185c]"
    ]
  },
  {
    "start": "0x141254387",
    "end": "0x1412543de",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125445a",
    "end": "0x1412544b1",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1058]"
    ]
  },
  {
    "start": "0x14125455a",
    "end": "0x14125459b",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0x1404]"
    ]
  },
  {
    "start": "0x1412545ad",
    "end": "0x1412545f5",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x6c]"
    ]
  },
  {
    "start": "0x1412545ff",
    "end": "0x141254656",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141254800",
    "end": "0x14125484b",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125497d",
    "end": "0x1412549be",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141254a1a",
    "end": "0x141254a71",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141254b8d",
    "end": "0x141254be4",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141254c5b",
    "end": "0x141254c99",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141254fce",
    "end": "0x141255022",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x1412552fc",
    "end": "0x14125533d",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125537a",
    "end": "0x1412553bb",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x1412553e8",
    "end": "0x14125543f",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125552f",
    "end": "0x141255586",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412557b3",
    "end": "0x14125580a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141255896",
    "end": "0x1412558e1",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141255984",
    "end": "0x1412559cc",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141255e8f",
    "end": "0x141255ed0",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125609d",
    "end": "0x1412560f4",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125645e",
    "end": "0x1412564b5",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412565d2",
    "end": "0x14125661d",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412566a0",
    "end": "0x1412566f7",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141256791",
    "end": "0x1412567e8",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141256c8b",
    "end": "0x141256ccc",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0x1fb0]"
    ]
  },
  {
    "start": "0x141256f36",
    "end": "0x141256f81",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141257083",
    "end": "0x1412570da",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125742c",
    "end": "0x141257483",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141257699",
    "end": "0x1412576da",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141257871",
    "end": "0x1412578c8",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412579dd",
    "end": "0x141257a34",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141257b98",
    "end": "0x141257be3",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141257c87",
    "end": "0x141257cdb",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141257d0f",
    "end": "0x141257d50",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141257dbf",
    "end": "0x141257e0a",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141257f99",
    "end": "0x141257ff0",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125823f",
    "end": "0x141258296",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412582c6",
    "end": "0x14125831d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125866e",
    "end": "0x1412586c5",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x127c]"
    ]
  },
  {
    "start": "0x141258703",
    "end": "0x141258744",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x1412588ad",
    "end": "0x141258904",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141258af8",
    "end": "0x141258b4f",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141258b96",
    "end": "0x141258bed",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141258c4b",
    "end": "0x141258c96",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141258e06",
    "end": "0x141258e5d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141258f07",
    "end": "0x141258f5e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141259056",
    "end": "0x141259094",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0x2c]"
    ]
  },
  {
    "start": "0x141259250",
    "end": "0x14125928e",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125954b",
    "end": "0x1412595a4",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x4f8]"
    ]
  },
  {
    "start": "0x14125988c",
    "end": "0x1412598cd",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141259bcd",
    "end": "0x141259c24",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141259ff9",
    "end": "0x14125a04d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125a146",
    "end": "0x14125a19d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125a23b",
    "end": "0x14125a294",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x14f8]"
    ]
  },
  {
    "start": "0x14125a2b1",
    "end": "0x14125a2fc",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x14fc]"
    ]
  },
  {
    "start": "0x14125a347",
    "end": "0x14125a39e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125a651",
    "end": "0x14125a6a8",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125a9d6",
    "end": "0x14125aa2d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x4b8]"
    ]
  },
  {
    "start": "0x14125ab9d",
    "end": "0x14125abe5",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125ad49",
    "end": "0x14125ada2",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125addb",
    "end": "0x14125ae1c",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125aee2",
    "end": "0x14125af39",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125b05d",
    "end": "0x14125b09e",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125b120",
    "end": "0x14125b177",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1324]"
    ]
  },
  {
    "start": "0x14125b20d",
    "end": "0x14125b264",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125b335",
    "end": "0x14125b38c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125b426",
    "end": "0x14125b47f",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125b50c",
    "end": "0x14125b563",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125b877",
    "end": "0x14125b8d0",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125b9b2",
    "end": "0x14125b9fa",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125ba69",
    "end": "0x14125bab4",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125baf8",
    "end": "0x14125bb4f",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125bbe3",
    "end": "0x14125bc2b",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x6c]"
    ]
  },
  {
    "start": "0x14125bcba",
    "end": "0x14125bd11",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125bd3f",
    "end": "0x14125bd98",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125bed3",
    "end": "0x14125bf11",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125c098",
    "end": "0x14125c0f1",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125c3b4",
    "end": "0x14125c408",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125c4a5",
    "end": "0x14125c4fc",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125c52d",
    "end": "0x14125c578",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125c5ad",
    "end": "0x14125c604",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125c8d5",
    "end": "0x14125c92e",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125c95e",
    "end": "0x14125c9a9",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125ca79",
    "end": "0x14125cad0",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125cd42",
    "end": "0x14125cd8d",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125cfb8",
    "end": "0x14125cff6",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125d008",
    "end": "0x14125d05f",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1998]"
    ]
  },
  {
    "start": "0x14125d0c1",
    "end": "0x14125d10c",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125d157",
    "end": "0x14125d1a2",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125d6d9",
    "end": "0x14125d730",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125d790",
    "end": "0x14125d7db",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125d83a",
    "end": "0x14125d87b",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125d909",
    "end": "0x14125d947",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x14125d985",
    "end": "0x14125d9dc",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1d28]"
    ]
  },
  {
    "start": "0x14125da51",
    "end": "0x14125daa5",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x40]"
    ]
  },
  {
    "start": "0x14125dad3",
    "end": "0x14125db2c",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125db6d",
    "end": "0x14125dbc4",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0xe28]"
    ]
  },
  {
    "start": "0x14125dc62",
    "end": "0x14125dcb9",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125df44",
    "end": "0x14125df8f",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125dfe8",
    "end": "0x14125e03d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125e2ce",
    "end": "0x14125e325",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125e6f9",
    "end": "0x14125e73a",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125e78f",
    "end": "0x14125e7e6",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125e8a7",
    "end": "0x14125e900",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125e9c1",
    "end": "0x14125ea15",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x40]"
    ]
  },
  {
    "start": "0x14125ebb2",
    "end": "0x14125ec09",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125ef10",
    "end": "0x14125ef5b",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125ef8d",
    "end": "0x14125efd8",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125eff9",
    "end": "0x14125f050",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125f1b1",
    "end": "0x14125f208",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x50c]"
    ]
  },
  {
    "start": "0x14125f2b7",
    "end": "0x14125f30e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125f45a",
    "end": "0x14125f4b1",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125f5c0",
    "end": "0x14125f619",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125f77f",
    "end": "0x14125f7c0",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125f806",
    "end": "0x14125f85d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125f996",
    "end": "0x14125f9ed",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125fac5",
    "end": "0x14125fb06",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14125fb51",
    "end": "0x14125fb99",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x6c]"
    ]
  },
  {
    "start": "0x14125fca1",
    "end": "0x14125fcf8",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125fd30",
    "end": "0x14125fd87",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x11c]"
    ]
  },
  {
    "start": "0x14125fdfc",
    "end": "0x14125fe47",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125fe7e",
    "end": "0x14125fed7",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14125ff70",
    "end": "0x14125ffbb",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141260038",
    "end": "0x14126008d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412601c5",
    "end": "0x141260210",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412602d2",
    "end": "0x141260329",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141260369",
    "end": "0x1412603c0",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126043e",
    "end": "0x14126047d",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141260503",
    "end": "0x14126055a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141260a1d",
    "end": "0x141260a68",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141260d35",
    "end": "0x141260d8c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141260e0b",
    "end": "0x141260e56",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1a10]"
    ]
  },
  {
    "start": "0x141260e65",
    "end": "0x141260ebc",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1a24]"
    ]
  },
  {
    "start": "0x141261369",
    "end": "0x1412613b4",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412614e6",
    "end": "0x14126153d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412618aa",
    "end": "0x1412618f5",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412619c6",
    "end": "0x141261a07",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141261bae",
    "end": "0x141261c05",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141261dab",
    "end": "0x141261e04",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x270]"
    ]
  },
  {
    "start": "0x141261e32",
    "end": "0x141261e89",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141261faf",
    "end": "0x141261ff7",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141262011",
    "end": "0x141262068",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0xd5c]"
    ]
  },
  {
    "start": "0x14126217e",
    "end": "0x1412621d5",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126220e",
    "end": "0x141262265",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412623b4",
    "end": "0x14126240b",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126258c",
    "end": "0x1412625e1",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412628b3",
    "end": "0x1412628f4",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141262a26",
    "end": "0x141262a7d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141262b77",
    "end": "0x141262bd0",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141262c3e",
    "end": "0x141262c94",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141262ddb",
    "end": "0x141262e1c",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141262f2c",
    "end": "0x141262f83",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141262fc2",
    "end": "0x141263019",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141263421",
    "end": "0x141263462",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x1412634b6",
    "end": "0x14126350d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126354f",
    "end": "0x141263590",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x1412635a5",
    "end": "0x1412635fc",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412636c2",
    "end": "0x141263719",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141263742",
    "end": "0x141263799",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412637d9",
    "end": "0x141263830",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x648]"
    ]
  },
  {
    "start": "0x141263956",
    "end": "0x1412639ad",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141263afc",
    "end": "0x141263b51",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141263bd9",
    "end": "0x141263c17",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141263d1a",
    "end": "0x141263d71",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141263e0b",
    "end": "0x141263e62",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x580]"
    ]
  },
  {
    "start": "0x141263e8f",
    "end": "0x141263ed0",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0x58c]"
    ]
  },
  {
    "start": "0x141263fbc",
    "end": "0x141264007",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412640a8",
    "end": "0x1412640e9",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141264117",
    "end": "0x141264162",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412641d1",
    "end": "0x141264228",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412642df",
    "end": "0x141264333",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141264a68",
    "end": "0x141264abf",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141264cb2",
    "end": "0x141264d06",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x6c]"
    ]
  },
  {
    "start": "0x141264df3",
    "end": "0x141264e4a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x2d8]"
    ]
  },
  {
    "start": "0x141264f14",
    "end": "0x141264f5c",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x50]"
    ]
  },
  {
    "start": "0x141264fc7",
    "end": "0x141265008",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141265217",
    "end": "0x14126526e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412652e0",
    "end": "0x141265335",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412653c7",
    "end": "0x14126541e",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126546f",
    "end": "0x1412654b0",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141265829",
    "end": "0x141265882",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126590d",
    "end": "0x141265964",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141265c26",
    "end": "0x141265c7d",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x2e0]"
    ]
  },
  {
    "start": "0x141265ccc",
    "end": "0x141265d25",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141265e8a",
    "end": "0x141265ee3",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141265f33",
    "end": "0x141265f8a",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412660f6",
    "end": "0x141266141",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x17b8]"
    ]
  },
  {
    "start": "0x141266171",
    "end": "0x1412661c8",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126630b",
    "end": "0x14126635f",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x141266457",
    "end": "0x1412664ae",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141266552",
    "end": "0x14126659d",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412666f9",
    "end": "0x141266750",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126677a",
    "end": "0x1412667d1",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412667f4",
    "end": "0x141266835",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x14126695d",
    "end": "0x1412669a8",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141266c05",
    "end": "0x141266c46",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141266cee",
    "end": "0x141266d39",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141266e0e",
    "end": "0x141266e67",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0xab0]"
    ]
  },
  {
    "start": "0x141266e91",
    "end": "0x141266edc",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141266f3f",
    "end": "0x141266f98",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141267014",
    "end": "0x14126705f",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1bc4]"
    ]
  },
  {
    "start": "0x141267087",
    "end": "0x1412670de",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141267122",
    "end": "0x141267163",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141267324",
    "end": "0x14126737b",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x14126767e",
    "end": "0x1412676c9",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0xeec]"
    ]
  },
  {
    "start": "0x1412676f5",
    "end": "0x14126774c",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141267890",
    "end": "0x1412678e7",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141267b75",
    "end": "0x141267bb6",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x141267c84",
    "end": "0x141267cdb",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141267f8d",
    "end": "0x141267fce",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x1412680ec",
    "end": "0x141268140",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x1412684e1",
    "end": "0x14126852c",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 0x1c9c]"
    ]
  },
  {
    "start": "0x14126859a",
    "end": "0x1412685f1",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412686ab",
    "end": "0x141268702",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141268a70",
    "end": "0x141268ac9",
    "removed": 13,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x141268b1d",
    "end": "0x141268b5e",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, dword ptr [r8 + 0xfec]"
    ]
  },
  {
    "start": "0x141268fea",
    "end": "0x141269032",
    "removed": 11,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, dword ptr [r8 + 8]"
    ]
  },
  {
    "start": "0x1412690fb",
    "end": "0x141269152",
    "removed": 15,
    "remaining": [
      "xor rax, rax",
      "or rax, qword ptr [r8 + 0x206c]"
    ]
  },
  {
    "start": "0x1412693e0",
    "end": "0x141269421",
    "removed": 9,
    "remaining": [
      "and r9d, 0",
      "xor r9d, 0"
    ]
  },
  {
    "start": "0x1412696ed",
    "end": "0x141269744",
    "removed": 15,
    "remaining": [
      "xor r9d, r9d",
      "or r9d, 0"
    ]
  },
  {
    "start": "0x1412697cf",
    "end": "0x141269826",
    "removed": 15,
    "remaining"
[Recorded excerpt: file exceeds 48,000 characters.]
````````````


File: `reverse/CyberCup-2077/check_current.bin.json`

````````````text
[
  {
    "start": "0x14124cd65",
    "end": "0x141289b0a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412505c2",
    "end": "0x141415841",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141251615",
    "end": "0x14140cfa8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141251aa9",
    "end": "0x1413ece5a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141254d11",
    "end": "0x1412b8007",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141255080",
    "end": "0x141433f17",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141255bb1",
    "end": "0x14149771d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412561fa",
    "end": "0x14127a79d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141256937",
    "end": "0x1413f3380",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141259309",
    "end": "0x141368760",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14125e433",
    "end": "0x141392382",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14125ec77",
    "end": "0x141290212",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141260744",
    "end": "0x1412f3f43",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141263031",
    "end": "0x14138a04b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126448d",
    "end": "0x141305ca0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412646ed",
    "end": "0x14128f6ad",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412691b9",
    "end": "0x141342ccf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141269838",
    "end": "0x1412822de",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126bc42",
    "end": "0x141402329",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126c2ae",
    "end": "0x1412f4f25",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126eca8",
    "end": "0x1412c943c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126f44d",
    "end": "0x1413683d9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14127623b",
    "end": "0x141357d8c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141276fd2",
    "end": "0x141439319",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141277f8a",
    "end": "0x14146e6ca",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14127eda0",
    "end": "0x141285fe0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141282327",
    "end": "0x14129a560",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141283e72",
    "end": "0x141251a79",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412842e9",
    "end": "0x14135e749",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128a328",
    "end": "0x14137beb3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128ab3d",
    "end": "0x141250510",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128bae6",
    "end": "0x14143c506",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128f6ee",
    "end": "0x1412b550c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412916b0",
    "end": "0x1414a4585",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141295d06",
    "end": "0x14145b7c2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141296c7f",
    "end": "0x14128f0ca",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412981b4",
    "end": "0x141358df3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8345",
    "end": "0x1413897d8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a87e3",
    "end": "0x141283e3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8bdf",
    "end": "0x141275b43",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8ec9",
    "end": "0x141280cf2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ab4e7",
    "end": "0x1413cea41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412acd6e",
    "end": "0x1412f9cf0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ad04c",
    "end": "0x1413ca664",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b476f",
    "end": "0x1412e45d0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b4d6f",
    "end": "0x141371aa9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b5593",
    "end": "0x141309dda",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b70a2",
    "end": "0x1412fc07e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b8efc",
    "end": "0x14142c346",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412be8be",
    "end": "0x1412da3d1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412c42c6",
    "end": "0x1414431b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412c950a",
    "end": "0x1414a9c3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ca3fe",
    "end": "0x1413c8deb",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412cc8b7",
    "end": "0x141296c34",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ce9f6",
    "end": "0x1413bd18c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d17f6",
    "end": "0x14137fd7a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d2373",
    "end": "0x1413fac68",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d25d3",
    "end": "0x14146cf13",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d5aac",
    "end": "0x141470520",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412dc3b3",
    "end": "0x141294402",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e0a84",
    "end": "0x1413411b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e0f84",
    "end": "0x14148025b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e1caa",
    "end": "0x14129fe3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e2831",
    "end": "0x1412d17c4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e37c5",
    "end": "0x141307e26",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e3a07",
    "end": "0x1413022f6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ea099",
    "end": "0x1413c632d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ee64b",
    "end": "0x1412c4f21",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412efd24",
    "end": "0x14140d2b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f208a",
    "end": "0x1412b59b8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f4fbc",
    "end": "0x14134becd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f6474",
    "end": "0x1414765cf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f9dec",
    "end": "0x141399175",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412fcc09",
    "end": "0x141406f80",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412fce16",
    "end": "0x14146a98d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141300201",
    "end": "0x1413bc680",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130062d",
    "end": "0x1412561a2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413007dd",
    "end": "0x1412fd5cf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413014bb",
    "end": "0x1413d31bf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141301781",
    "end": "0x14146f462",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141304651",
    "end": "0x14133675a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141305d00",
    "end": "0x1412fa1a3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141307eca",
    "end": "0x1412b7015",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130c2c7",
    "end": "0x1413eb093",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130ec54",
    "end": "0x141276f7f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14131be11",
    "end": "0x141301758",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14131c459",
    "end": "0x14126cad7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141321bd1",
    "end": "0x1412cc871",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141323a86",
    "end": "0x1413089e9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141324c65",
    "end": "0x1414888e1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14132c2cf",
    "end": "0x1412521a7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141330473",
    "end": "0x1412e8e37",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141331245",
    "end": "0x1412e80df",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413367e8",
    "end": "0x14128198d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141350259",
    "end": "0x1412842b3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14135203a",
    "end": "0x141452bc3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141358e74",
    "end": "0x141455f88",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14135e784",
    "end": "0x1413fd6d7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413615a5",
    "end": "0x14132e60e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141362ba1",
    "end": "0x14131e427",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141365ba8",
    "end": "0x1412de97a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413667d2",
    "end": "0x1413cda28",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141368402",
    "end": "0x14140b985",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141368783",
    "end": "0x1414a0ef9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136b81d",
    "end": "0x141477d46",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136cfdd",
    "end": "0x141304570",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136fd70",
    "end": "0x141457949",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413762af",
    "end": "0x14128c69c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141376f77",
    "end": "0x14131ad80",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413772fa",
    "end": "0x14144a950",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14137afe9",
    "end": "0x1412ebf82",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14137e9e7",
    "end": "0x141303f58",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141382231",
    "end": "0x141467527",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141389815",
    "end": "0x14146cab2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14138abcb",
    "end": "0x1412d207c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14138cee5",
    "end": "0x141378769",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141399201",
    "end": "0x141467857",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a1fb9",
    "end": "0x1414a2e8a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a22bc",
    "end": "0x1414449fe",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a5f9a",
    "end": "0x1413034d6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a729d",
    "end": "0x141299443",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413b563f",
    "end": "0x14136fbc1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bbe9f",
    "end": "0x141294dde",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bc713",
    "end": "0x14133044a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bd217",
    "end": "0x1412e0179",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c0499",
    "end": "0x14145002b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c29f9",
    "end": "0x141412dda",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c309e",
    "end": "0x1413a9021",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c8e1c",
    "end": "0x1413ff44e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ca7c7",
    "end": "0x1412606ce",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413cd3bb",
    "end": "0x1413cd713",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413d3226",
    "end": "0x14143b4a0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413d4def",
    "end": "0x141315c67",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413dac88",
    "end": "0x141376f41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ec58f",
    "end": "0x141307400",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413f2120",
    "end": "0x1412a8734",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413f33f7",
    "end": "0x14132d6cd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413fc40c",
    "end": "0x14126d6d3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ffcd8",
    "end": "0x1413f0ce9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414023a4",
    "end": "0x141297d0a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414085ce",
    "end": "0x141432097",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14140b9a9",
    "end": "0x1413b19a6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14140d2f7",
    "end": "0x141295ad1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141410fe9",
    "end": "0x14136b7ed",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141412e01",
    "end": "0x14138a14d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141413d91",
    "end": "0x141293d32",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14141521f",
    "end": "0x141414dbd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14141a499",
    "end": "0x14144203f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414223b7",
    "end": "0x1413680b9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141425cc7",
    "end": "0x1413a2a83",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141427899",
    "end": "0x141255b88",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141428a4c",
    "end": "0x14142e7b4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14142c3cf",
    "end": "0x1412740cd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14143b4f2",
    "end": "0x1414a0db6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414405c3",
    "end": "0x1414a3f1f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141444a21",
    "end": "0x141433a8d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14144c144",
    "end": "0x14125a485",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14145152f",
    "end": "0x141324b9d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141455fbd",
    "end": "0x1412ec35d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141456489",
    "end": "0x141304baa",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14145aee9",
    "end": "0x14127f06d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141462d1a",
    "end": "0x14127ec87",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141464cca",
    "end": "0x1413e731e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414675ad",
    "end": "0x1413a1040",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14146787c",
    "end": "0x14149e0c7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14146a9c9",
    "end": "0x1412663fc",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141470168",
    "end": "0x1412efcee",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14147559d",
    "end": "0x14142785a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141476600",
    "end": "0x1412f537b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414783c8",
    "end": "0x1412d0cd6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14147c09b",
    "end": "0x14137d905",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141487ba6",
    "end": "0x141425c23",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14148ad01",
    "end": "0x14131b7e1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14148c717",
    "end": "0x141323a65",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141499597",
    "end": "0x14128ebfd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141499c3f",
    "end": "0x1412643f2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14149a6b5",
    "end": "0x1412ce359",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14149eeb8",
    "end": "0x141469599",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414a9c6c",
    "end": "0x14141f3de",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414abb70",
    "end": "0x14132f467",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14160fa0a",
    "end": "0x14160fc00",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141610e1f",
    "end": "0x141611015",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416121fc",
    "end": "0x1416123f2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141612b79",
    "end": "0x141612d6f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141613475",
    "end": "0x14161366b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416136a1",
    "end": "0x1416138fe",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161394a",
    "end": "0x141613ba7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161418a",
    "end": "0x141614380",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614447",
    "end": "0x14161463d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416146a7",
    "end": "0x14161489d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614920",
    "end": "0x141614b16",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614b4b",
    "end": "0x141614d41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614e30",
    "end": "0x14161508d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615180",
    "end": "0x1416153dc",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615612",
    "end": "0x141615808",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615843",
    "end": "0x141615aa0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615ae0",
    "end": "0x141615d3c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615e7c",
    "end": "0x141616072",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416160a7",
    "end": "0x141616304",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616340",
    "end": "0x14161659c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616640",
    "end": "0x141616836",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616872",
    "end": "0x141616acf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616b14",
    "end": "0x141616d70",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616dc4",
    "end": "0x141616fba",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141617006",
    "end": "0x141617263",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416172ae",
    "end": "0x1416174a4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416174ec",
    "end": "0x141617749",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141617792",
    "end": "0x1416179ee",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141618079",
    "end": "0x14161826f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141618386",
    "end": "0x14161857c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d3c4",
    "end": "0x14161d5ba",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d65a",
    "end": "0x14161d8b7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d9aa",
    "end": "0x14161dc06",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141625b38",
    "end": "0x141625d2e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141625def",
    "end": "0x141625fe5",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416260a5",
    "end": "0x14162629b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141626357",
    "end": "0x14162654d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141640ba2",
    "end": "0x141640d98",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416436e4",
    "end": "0x1416438da",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141657563",
    "end": "0x141657759",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14165838f",
    "end": "0x141658585",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416613f3",
    "end": "0x1416615e9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141668ea3",
    "end": "0x141669099",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14166970f",
    "end": "0x141669905",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14166fe94",
    "end": "0x14167008a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141254cbc",
    "end": "0x141254d07",
    "description": "logical immediate 2 dwordGPR11, 0xcfce63f7"
  },
  {
    "start": "0x14129165c",
    "end": "0x1412916a7",
    "description": "logical0xca000000 dwordGPR11, dwordGPR9"
  },
  {
    "start": "0x1412acd17",
    "end": "0x1412acd62",
    "description": "logical0xca000000 dwordGPR9, dwordGPR9"
  },
  {
    "start": "0x14130c278",
    "end": "0x14130c2c3",
    "description": "mov dwordGPR9, 0x0"
  },
  {
    "start": "0x141349160",
    "end": "0x1413491ab",
    "description": "mov dwordGPR9, 0x0"
  },
  {
    "start": "0x1413501fc",
    "end": "0x141350247",
    "description": "logical0xca000000 dwordGPR11, dwordGPR9"
  },
  {
    "start": "0x141470520",
    "end": "0x14147056b",
    "description": "logical0xca000000 dwordGPR9, dwordGPR9"
  },
  {
    "start": "0x141614135",
    "end": "0x141614180",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x141614384",
    "end": "0x1416143cf",
    "description": "logical0x8a000000 dwordGPR3, dwordGPR7"
  },
  {
    "start": "0x1416143f3",
    "end": "0x14161443e",
    "description": "logical0xca000000 dwordGPR3, dwordGPR5"
  },
  {
    "start": "0x141614657",
    "end": "0x1416146a2",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x1416148c6",
    "end": "0x141614911",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x141625ae7",
    "end": "0x141625b32",
    "description": "mov dwordGPR0, 0x9a516e27"
  },
  {
    "start": "0x141625d34",
    "end": "0x141625d7f",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x141625d94",
    "end": "0x141625ddf",
    "description": "mov dwordGPR0, 0x52dab981"
  },
  {
    "start": "0x141625fe7",
    "end": "0x141626032",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x14162604c",
    "end": "0x141626097",
    "description": "mov dwordGPR0, 0xc47139ab"
  },
  {
    "start": "0x1416262a0",
    "end": "0x1416262eb",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x141626304",
    "end": "0x14162634f",
    "description": "mov dwordGPR0, 0x713ec0d5"
  },
  {
    "start": "0x141626552",
    "end": "0x14162659d",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  }
]
````````````


File: `reverse/CyberCup-2077/check_deobf_new.bin.json`

````````````text
[
  {
    "start": "0x14124cd65",
    "end": "0x141289b0a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412505c2",
    "end": "0x141415841",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141251615",
    "end": "0x14140cfa8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141251aa9",
    "end": "0x1413ece5a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141254d11",
    "end": "0x1412b8007",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141255080",
    "end": "0x141433f17",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141255bb1",
    "end": "0x14149771d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412561fa",
    "end": "0x14127a79d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141256937",
    "end": "0x1413f3380",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141259309",
    "end": "0x141368760",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14125e433",
    "end": "0x141392382",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14125ec77",
    "end": "0x141290212",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141260744",
    "end": "0x1412f3f43",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141263031",
    "end": "0x14138a04b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126448d",
    "end": "0x141305ca0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412646ed",
    "end": "0x14128f6ad",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412691b9",
    "end": "0x141342ccf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141269838",
    "end": "0x1412822de",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126bc42",
    "end": "0x141402329",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126c2ae",
    "end": "0x1412f4f25",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126eca8",
    "end": "0x1412c943c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126f44d",
    "end": "0x1413683d9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14127623b",
    "end": "0x141357d8c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141276fd2",
    "end": "0x141439319",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141277f8a",
    "end": "0x14146e6ca",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14127eda0",
    "end": "0x141285fe0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141282327",
    "end": "0x14129a560",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141283e72",
    "end": "0x141251a79",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412842e9",
    "end": "0x14135e749",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128a328",
    "end": "0x14137beb3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128ab3d",
    "end": "0x141250510",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128bae6",
    "end": "0x14143c506",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128f6ee",
    "end": "0x1412b550c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412916b0",
    "end": "0x1414a4585",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141295d06",
    "end": "0x14145b7c2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141296c7f",
    "end": "0x14128f0ca",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412981b4",
    "end": "0x141358df3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8345",
    "end": "0x1413897d8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a87e3",
    "end": "0x141283e3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8bdf",
    "end": "0x141275b43",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8ec9",
    "end": "0x141280cf2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ab4e7",
    "end": "0x1413cea41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412acd6e",
    "end": "0x1412f9cf0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ad04c",
    "end": "0x1413ca664",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b476f",
    "end": "0x1412e45d0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b4d6f",
    "end": "0x141371aa9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b5593",
    "end": "0x141309dda",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b70a2",
    "end": "0x1412fc07e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b8efc",
    "end": "0x14142c346",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412be8be",
    "end": "0x1412da3d1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412c42c6",
    "end": "0x1414431b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412c950a",
    "end": "0x1414a9c3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ca3fe",
    "end": "0x1413c8deb",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412cc8b7",
    "end": "0x141296c34",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ce9f6",
    "end": "0x1413bd18c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d17f6",
    "end": "0x14137fd7a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d2373",
    "end": "0x1413fac68",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d25d3",
    "end": "0x14146cf13",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d5aac",
    "end": "0x141470520",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412dc3b3",
    "end": "0x141294402",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e0a84",
    "end": "0x1413411b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e0f84",
    "end": "0x14148025b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e1caa",
    "end": "0x14129fe3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e2831",
    "end": "0x1412d17c4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e37c5",
    "end": "0x141307e26",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e3a07",
    "end": "0x1413022f6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ea099",
    "end": "0x1413c632d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ee64b",
    "end": "0x1412c4f21",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412efd24",
    "end": "0x14140d2b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f208a",
    "end": "0x1412b59b8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f4fbc",
    "end": "0x14134becd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f6474",
    "end": "0x1414765cf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f9dec",
    "end": "0x141399175",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412fcc09",
    "end": "0x141406f80",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412fce16",
    "end": "0x14146a98d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141300201",
    "end": "0x1413bc680",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130062d",
    "end": "0x1412561a2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413007dd",
    "end": "0x1412fd5cf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413014bb",
    "end": "0x1413d31bf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141301781",
    "end": "0x14146f462",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141304651",
    "end": "0x14133675a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141305d00",
    "end": "0x1412fa1a3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141307eca",
    "end": "0x1412b7015",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130c2c7",
    "end": "0x1413eb093",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130ec54",
    "end": "0x141276f7f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14131be11",
    "end": "0x141301758",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14131c459",
    "end": "0x14126cad7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141321bd1",
    "end": "0x1412cc871",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141323a86",
    "end": "0x1413089e9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141324c65",
    "end": "0x1414888e1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14132c2cf",
    "end": "0x1412521a7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141330473",
    "end": "0x1412e8e37",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141331245",
    "end": "0x1412e80df",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413367e8",
    "end": "0x14128198d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141350259",
    "end": "0x1412842b3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14135203a",
    "end": "0x141452bc3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141358e74",
    "end": "0x141455f88",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14135e784",
    "end": "0x1413fd6d7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413615a5",
    "end": "0x14132e60e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141362ba1",
    "end": "0x14131e427",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141365ba8",
    "end": "0x1412de97a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413667d2",
    "end": "0x1413cda28",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141368402",
    "end": "0x14140b985",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141368783",
    "end": "0x1414a0ef9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136b81d",
    "end": "0x141477d46",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136cfdd",
    "end": "0x141304570",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136fd70",
    "end": "0x141457949",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413762af",
    "end": "0x14128c69c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141376f77",
    "end": "0x14131ad80",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413772fa",
    "end": "0x14144a950",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14137afe9",
    "end": "0x1412ebf82",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14137e9e7",
    "end": "0x141303f58",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141382231",
    "end": "0x141467527",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141389815",
    "end": "0x14146cab2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14138abcb",
    "end": "0x1412d207c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14138cee5",
    "end": "0x141378769",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141399201",
    "end": "0x141467857",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a1fb9",
    "end": "0x1414a2e8a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a22bc",
    "end": "0x1414449fe",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a5f9a",
    "end": "0x1413034d6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a729d",
    "end": "0x141299443",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413b563f",
    "end": "0x14136fbc1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bbe9f",
    "end": "0x141294dde",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bc713",
    "end": "0x14133044a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bd217",
    "end": "0x1412e0179",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c0499",
    "end": "0x14145002b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c29f9",
    "end": "0x141412dda",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c309e",
    "end": "0x1413a9021",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c8e1c",
    "end": "0x1413ff44e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ca7c7",
    "end": "0x1412606ce",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413cd3bb",
    "end": "0x1413cd713",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413d3226",
    "end": "0x14143b4a0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413d4def",
    "end": "0x141315c67",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413dac88",
    "end": "0x141376f41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ec58f",
    "end": "0x141307400",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413f2120",
    "end": "0x1412a8734",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413f33f7",
    "end": "0x14132d6cd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413fc40c",
    "end": "0x14126d6d3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ffcd8",
    "end": "0x1413f0ce9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414023a4",
    "end": "0x141297d0a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414085ce",
    "end": "0x141432097",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14140b9a9",
    "end": "0x1413b19a6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14140d2f7",
    "end": "0x141295ad1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141410fe9",
    "end": "0x14136b7ed",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141412e01",
    "end": "0x14138a14d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141413d91",
    "end": "0x141293d32",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14141521f",
    "end": "0x141414dbd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14141a499",
    "end": "0x14144203f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414223b7",
    "end": "0x1413680b9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141425cc7",
    "end": "0x1413a2a83",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141427899",
    "end": "0x141255b88",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141428a4c",
    "end": "0x14142e7b4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14142c3cf",
    "end": "0x1412740cd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14143b4f2",
    "end": "0x1414a0db6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414405c3",
    "end": "0x1414a3f1f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141444a21",
    "end": "0x141433a8d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14144c144",
    "end": "0x14125a485",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14145152f",
    "end": "0x141324b9d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141455fbd",
    "end": "0x1412ec35d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141456489",
    "end": "0x141304baa",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14145aee9",
    "end": "0x14127f06d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141462d1a",
    "end": "0x14127ec87",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141464cca",
    "end": "0x1413e731e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414675ad",
    "end": "0x1413a1040",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14146787c",
    "end": "0x14149e0c7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14146a9c9",
    "end": "0x1412663fc",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141470168",
    "end": "0x1412efcee",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14147559d",
    "end": "0x14142785a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141476600",
    "end": "0x1412f537b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414783c8",
    "end": "0x1412d0cd6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14147c09b",
    "end": "0x14137d905",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141487ba6",
    "end": "0x141425c23",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14148ad01",
    "end": "0x14131b7e1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14148c717",
    "end": "0x141323a65",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141499597",
    "end": "0x14128ebfd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141499c3f",
    "end": "0x1412643f2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14149a6b5",
    "end": "0x1412ce359",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14149eeb8",
    "end": "0x141469599",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414a9c6c",
    "end": "0x14141f3de",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414abb70",
    "end": "0x14132f467",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14160fa0a",
    "end": "0x14160fc00",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141610e1f",
    "end": "0x141611015",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416121fc",
    "end": "0x1416123f2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141612b79",
    "end": "0x141612d6f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141613475",
    "end": "0x14161366b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416136a1",
    "end": "0x1416138fe",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161394a",
    "end": "0x141613ba7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161418a",
    "end": "0x141614380",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614447",
    "end": "0x14161463d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416146a7",
    "end": "0x14161489d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614920",
    "end": "0x141614b16",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614b4b",
    "end": "0x141614d41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614e30",
    "end": "0x14161508d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615180",
    "end": "0x1416153dc",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615612",
    "end": "0x141615808",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615843",
    "end": "0x141615aa0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615ae0",
    "end": "0x141615d3c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615e7c",
    "end": "0x141616072",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416160a7",
    "end": "0x141616304",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616340",
    "end": "0x14161659c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616640",
    "end": "0x141616836",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616872",
    "end": "0x141616acf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616b14",
    "end": "0x141616d70",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616dc4",
    "end": "0x141616fba",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141617006",
    "end": "0x141617263",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416172ae",
    "end": "0x1416174a4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416174ec",
    "end": "0x141617749",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141617792",
    "end": "0x1416179ee",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141618079",
    "end": "0x14161826f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141618386",
    "end": "0x14161857c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d3c4",
    "end": "0x14161d5ba",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d65a",
    "end": "0x14161d8b7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d9aa",
    "end": "0x14161dc06",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141625b38",
    "end": "0x141625d2e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141625def",
    "end": "0x141625fe5",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416260a5",
    "end": "0x14162629b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141626357",
    "end": "0x14162654d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141640ba2",
    "end": "0x141640d98",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416436e4",
    "end": "0x1416438da",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141657563",
    "end": "0x141657759",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14165838f",
    "end": "0x141658585",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416613f3",
    "end": "0x1416615e9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141668ea3",
    "end": "0x141669099",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14166970f",
    "end": "0x141669905",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14166fe94",
    "end": "0x14167008a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614135",
    "end": "0x141614180",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x141614384",
    "end": "0x1416143cf",
    "description": "logical0x8a000000 dwordGPR3, dwordGPR7"
  },
  {
    "start": "0x1416143f3",
    "end": "0x14161443e",
    "description": "logical0xca000000 dwordGPR3, dwordGPR5"
  },
  {
    "start": "0x141614657",
    "end": "0x1416146a2",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x1416148c6",
    "end": "0x141614911",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x141625ae7",
    "end": "0x141625b32",
    "description": "mov dwordGPR0, 0x9a516e27"
  },
  {
    "start": "0x141625d34",
    "end": "0x141625d7f",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x141625d94",
    "end": "0x141625ddf",
    "description": "mov dwordGPR0, 0x52dab981"
  },
  {
    "start": "0x141625fe7",
    "end": "0x141626032",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x14162604c",
    "end": "0x141626097",
    "description": "mov dwordGPR0, 0xc47139ab"
  },
  {
    "start": "0x1416262a0",
    "end": "0x1416262eb",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x141626304",
    "end": "0x14162634f",
    "description": "mov dwordGPR0, 0x713ec0d5"
  },
  {
    "start": "0x141626552",
    "end": "0x14162659d",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  }
]
````````````


File: `reverse/CyberCup-2077/check_hypercall.py`

````````````text
"""Pure model of cybercup.sys capability API (RVA 0x315c) and ticket math.
This models state transitions for user-mode emulation; timeouts/locking omitted.
"""
MASK = (1 << 64) - 1

def rol(x, n, bits=64):
    mask=(1 << bits)-1
    return ((x << n) | (x >> (bits-n))) & mask

def siphash24(key0, key1, word0, word1, word2):
    v=[key0 ^ 0x736f6d6570736575, key1 ^ 0x646f72616e646f6d,
       key0 ^ 0x6c7967656e657261, key1 ^ 0x7465646279746573]
    def rnd():
        v[0]=(v[0]+v[1]) & MASK; v[1]=rol(v[1],13)^v[0]; v[0]=rol(v[0],32)
        v[2]=(v[2]+v[3]) & MASK; v[3]=rol(v[3],16)^v[2]
        v[0]=(v[0]+v[3]) & MASK; v[3]=rol(v[3],21)^v[0]
        v[2]=(v[2]+v[1]) & MASK; v[1]=rol(v[1],17)^v[2]; v[2]=rol(v[2],32)
    for m in [word0,word1,word2,0x1800000000000000]:
        v[3]^=m
        rnd();rnd()
        v[0]^=m
    v[2]^=0xff
    for _ in range(4): rnd()
    return v[0]^v[1]^v[2]^v[3]

def ticket_transform(operation, value):
    assert operation in (0x2077,0x2078)
    return (rol((value & 0xffffffff)^0xa3c59ac3,9,32) + operation*0x045d9f3b) & 0xffffffff

class Capabilities:
    def __init__(self,key0=0,key1=0):
        self.key=(key0,key1);self.counter=0;self.sessions={}
    def hash(self,*words): return siphash24(*self.key,*words)
    def token(self,x): return (x & 0x7ffffffffffffffd)|2
    def call(self,pid,op,arg=0,token=0,extra=0):
        if op==0x30ff and not arg and not token:return 0x10000
        if op==0x30fe and not arg and not token:return 0xf
        if op==0x3000 and arg and not token:
            self.counter+=1
            token=self.token(self.hash(self.counter,pid,arg^0x4846564c4f50454e))
            self.sessions[pid,token]={'nonce':arg,'state':self.hash(token,pid,arg),'step':1,'code':0,'code2':0,'pred':0}
            return token
        allowed=(0x3001,0x3002,0x3003,0x3010,0x3011,0x3021,0x3030,0x3040,0x3041)
        s=self.sessions.get((pid,token))
        if op not in allowed or not s:return MASK
        if op in (0x3010,0x3040):
            which='code' if op==0x3010 else 'code2'
            if extra or arg < 0x10000 or arg > 0x7fffffffffff or s[which]:return MASK
            s[which]=arg;return 0
        if op==0x3030:
            if extra or s['step']==1 or s['pred']:return MASK
            s['pred']=1
            return self.hash(s['state'],arg^0x4856505245443031,token)&3
        if op in (0x3002,0x3003):
            if op==0x3002 and s['step']<=1:return MASK
            del self.sessions[pid,token];return 0
        if op==0x3011 and (not extra or s['code']!=extra):return MASK
        if op==0x3041 and (not extra or s['code2']!=extra):return MASK
        if op==0x3021 and extra!=MASK:return MASK
        if arg>>32!=s['step'] or s['step']>4:return MASK
        s['state']=self.hash(s['state'],arg,token^s['nonce'])
        new=self.token(self.hash(s['state'],token,0x4846564c53544550))
        if new==token:new^=4
        s['step']+=1;s['code']=s['code2']=s['pred']=0
        del self.sessions[pid,token];self.sessions[pid,new]=s
        return new

class CheckSessions(Capabilities):
    """Nine-step choice API at driver RVA 0x2e64; opaque token remains fixed."""
    def call(self,pid,op,arg=0,token=0,process=None):
        owner=pid if process is None else (pid,process)
        if op==0x305f and not arg and not token:return 0x10000
        if op==0x3050 and arg and not token:
            self.counter+=1
            token=self.token(self.hash(self.counter,pid,arg^0x434845434b4f504e))
            self.sessions[owner,token]={'nonce':arg,'state':self.hash(token,pid,arg),'step':0,'lastarg':0,'lastresult':0}
            return token
        s=self.sessions.get((owner,token))
        if not 0x3051<=op<=0x305b or not s:return MASK
        if op in (0x305a,0x305b):
            result=0 if op==0x305b or (not arg and s['step']==9) else MASK
            del self.sessions[owner,token]
            return result
        step=op-0x3051
        if step+1==s['step'] and arg==s['lastarg']:return s['lastresult']
        if step!=s['step'] or step>=9:return MASK
        s['state']=self.hash(s['state'],arg,(0x434845434b535445+step)^s['nonce'])
        result=(s['state']^(s['state']>>32))&3
        s['step']+=1;s['lastarg']=arg;s['lastresult']=result
        return result

class Tickets:
    """Ticket/version services from RVA 0x36c4; expiration omitted."""
    def __init__(self):self.counter=0;self.sessions={}
    def call(self,pid,op,arg=0,token=0):
        if op==0:return 0x20000
        if op==1 and arg==0x2077 and not token:
            self.counter=(self.counter+1)&MASK
            if self.counter in (0,MASK):self.counter=(self.counter+1)&MASK
            self.sessions[pid,self.counter]=2
            return self.counter
        state=self.sessions.get((pid,token))
        if not state:return MASK
        if op==2:del self.sessions[pid,token];return 0
        if op==0x2077 and state==2:
            self.sessions[pid,token]=4
            return ticket_transform(op,arg)
        if op==0x2078 and state==4:
            del self.sessions[pid,token]
            return ticket_transform(op,arg)
        return MASK

````````````


File: `reverse/CyberCup-2077/check_luts.py`

````````````text
from pathlib import Path
from capstone import *
from capstone.x86 import *
import struct,json,collections
B=0x140000000;b=Path('unpack_memory.bin').read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
seen=set(); todo=[0x14126f3ea,0x1413f20a8];globals=collections.Counter()
while todo:
 pc=todo.pop()
 while pc not in seen:
  seen.add(pc);ins=next(md.disasm(b[pc-B:pc-B+15],pc,count=1),None)
  if not ins:break
  pc+=ins.size
  for o in ins.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP:globals[pc+o.mem.disp]+=1
  if ins.mnemonic=='ret':break
  if ins.mnemonic=='jmp':
   if ins.operands[0].type==X86_OP_IMM:pc=ins.operands[0].imm
   else:break
  elif ins.group(CS_GRP_JUMP):
   if ins.operands[0].type==X86_OP_IMM:todo.append(ins.operands[0].imm)

def q(a):return struct.unpack_from('<Q',b,a-B)[0]
for a,n in globals.most_common():
 p=q(a)
 if not 0<=p-B<len(b):print(hex(a),n,'BAD',hex(p));continue
 ps=[q(p+x*8) for x in range(256)]
 if all(0<=v-B<len(b)-255 for v in ps):
  ts=[b[v-B:v-B+256] for v in ps]
  ops={'xor':lambda x,y:x^y,'or':lambda x,y:x|y,'and':lambda x,y:x&y,'add':lambda x,y:(x+y)&255,'sub':lambda x,y:(x-y)&255,'carryadd':lambda x,y:int(x+y>255),'borrowsub':lambda x,y:int(x<y),'mul':lambda x,y:x*y&255,'eq':lambda x,y:int(x==y),'neq':lambda x,y:int(x!=y),'shl':lambda x,y:(x<<y)&255,'shr':lambda x,y:x>>y}
  match=[name for name,f in ops.items() if all(ts[x][y]==f(x,y) for x in range(256) for y in range(256))]
  print(hex(a),n,hex(p),'binary',match,'rowsample',[(x,list(ts[x][:8])) for x in range(3)])
 else:
  t=b[p-B:p-B+256];print(hex(a),n,hex(p),'unary',list(t[:32]),'unique',len(set(t)))

````````````


File: `reverse/CyberCup-2077/check_scan_tables.py`

````````````text
from pathlib import Path
from capstone import *
from capstone.x86 import *
import struct,json,collections
B=0x140000000;b=Path('checker_deobf.bin').read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_64);md.detail=True
stages=[i.operands[0].imm for i in md.disasm(b[0x698a19:0x698edb],B+0x698a19) if i.mnemonic=='call']
todo=list(stages);seen=set();gs=collections.Counter()
while todo:
 pc=todo.pop()
 while pc not in seen:
  seen.add(pc);i=next(md.disasm(b[pc-B:pc-B+15],pc,count=1),None)
  if i is None:break
  pc+=i.size
  for o in i.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP:gs[pc+o.mem.disp]+=1
  if i.mnemonic=='ret':break
  if i.mnemonic=='jmp':
   if i.operands[0].type!=X86_OP_IMM:break
   pc=i.operands[0].imm
  elif i.group(CS_GRP_JUMP):
   if i.operands[0].type==X86_OP_IMM:todo.append(i.operands[0].imm)
ops={}
for name,f in [('xor',lambda x,y:x^y),('or',lambda x,y:x|y),('and',lambda x,y:x&y)]:ops[name]=f
for k in range(1,8):ops['shl'+str(k)]=lambda x,y,k=k:((x<<k)|(y>>(8-k)))&255
for k in range(1,8):ops['shr'+str(k)]=lambda x,y,k=k:((x>>k)|(y<<(8-k)))&255
result={}
for a,n in gs.most_common():
 p=struct.unpack_from('<Q',b,a-B)[0]
 if not 0<=p-B<len(b)-2048:continue
 ps=struct.unpack_from('<256Q',b,p-B)
 if not all(0<=v-B<len(b)-255 for v in ps):
  t=b[p-B:p-B+256]
  kind='eq0' if t==b'\1'+b'\0'*255 else 'not' if t==bytes([x^255 for x in range(256)]) else 'unary'+t.hex()
  result[a]={'pointer':p,'kind':kind,'n':n};print(hex(a),n,'unary',kind[:80]);continue
 stride=ps[1]-ps[0];regular=all(ps[x]==ps[0]+x*stride for x in range(256))
 ts=[b[v-B:v-B+256] for v in ps]
 match=[name for name,f in ops.items() if all(ts[x][y]==f(x,y) for x in range(256) for y in range(256))]
 if stride==4 and regular:
  words=struct.unpack_from('<511I',b,ps[0]-B)
  if words==tuple(range(511)):match=['add32']
 print(hex(a),n,hex(p),'stride',stride,'regular',regular,'kind',match)
 result[a]={'pointer':p,'matrix':ps[0],'stride':stride,'regular':regular,'kind':match,'n':n}
Path('check_tables.json').write_text(json.dumps(result,indent=2))
print('STAGES',len(stages),'INS',len(seen))

````````````


File: `reverse/CyberCup-2077/check_solve_block.py`

````````````text
from pathlib import Path
import z3 as z,time,argparse
p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('target',type=lambda x:int(x,16));p.add_argument('--timeout',type=int,default=60000);p.add_argument('--prefix',default='');a=p.parse_args()
s=z.Solver();s.add(z.parse_smt2_file(a.file));s.set(timeout=a.timeout)
s.add(z.BitVec('state_00',32)==(a.target&0xffffffff),z.BitVec('state_04',32)==(a.target>>32))
w=[z.BitVec('input_word_%02d'%i,32) for i in range(2)]
for j,v in enumerate(a.prefix.encode()):s.add(z.Extract(j%4*8+7,j%4*8,w[j//4])==v)
t=time.time();r=s.check();print(r,'TIME',time.time()-t,flush=True)
if r==z.sat:
 m=s.model();b=b''.join(m.eval(x).as_long().to_bytes(4,'little') for x in w);print(b,flush=True)

````````````


File: `reverse/CyberCup-2077/check_split_states.py`

````````````text
from pathlib import Path
import z3 as z,json,sys
path=sys.argv[1] if len(sys.argv)>1 else 'check_all_states.smt2'
cs=z.parse_smt2_file(path);defs={}
for c in cs:
 if z.is_eq(c) and z.is_const(c.arg(0)) and c.arg(0).decl().kind()==z.Z3_OP_UNINTERPRETED:defs[str(c.arg(0))]=c

def variables(x):
 todo=[x];seen=set();result={}
 while todo:
  n=todo.pop();h=n.get_id()
  if h in seen:continue
  seen.add(h)
  if z.is_const(n) and n.decl().kind()==z.Z3_OP_UNINTERPRETED:result[str(n)]=n
  else:todo.extend(n.children())
 return result
for block in range(9):
 need=[f'state_{block*8:02d}',f'state_{block*8+4:02d}'];seen=set();out=[];inputs=set()
 while need:
  name=need.pop()
  if name in seen:continue
  seen.add(name)
  if name.startswith('input_'):inputs.add(name)
  c=defs.get(name)
  if c is not None:
   out.append(c);need.extend(variables(c.arg(1)))
 s=z.Solver();s.add(out);Path(f'check_block{block}.smt2').write_text(s.to_smt2())
 print(block,'nodes',len(out),'inputs',sorted(inputs),flush=True)

````````````


File: `reverse/CyberCup-2077/check_stage_map.json`

````````````text
[
  {
    "stage": "0x140601e80",
    "ins": 9285,
    "input": [
      0,
      1,
      2
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x1406052b0",
    "ins": 9259,
    "input": [
      3,
      4,
      5,
      6
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140608660",
    "ins": 9299,
    "input": [
      7
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14060bb60",
    "ins": 9151,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14060f150",
    "ins": 2203,
    "input": [],
    "state": [
      0,
      4
    ],
    "calls": []
  },
  {
    "stage": "0x14060fd90",
    "ins": 5,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14060fdb0",
    "ins": 2942,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140610ee0",
    "ins": 9307,
    "input": [
      8,
      9,
      10
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140614450",
    "ins": 9227,
    "input": [
      11,
      12,
      13,
      14
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140617930",
    "ins": 9417,
    "input": [
      15
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14061aef0",
    "ins": 7876,
    "input": [],
    "state": [
      8,
      12
    ],
    "calls": []
  },
  {
    "stage": "0x14061dca0",
    "ins": 5,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14061dcc0",
    "ins": 2841,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14061ed40",
    "ins": 9117,
    "input": [
      16,
      17,
      18
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140622210",
    "ins": 9236,
    "input": [
      19,
      20,
      21,
      22
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140625790",
    "ins": 9095,
    "input": [
      23
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140628e00",
    "ins": 3885,
    "input": [],
    "state": [
      16,
      20
    ],
    "calls": []
  },
  {
    "stage": "0x14062a560",
    "ins": 4,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14062a580",
    "ins": 2941,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14062b710",
    "ins": 9418,
    "input": [
      24,
      25,
      26
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14062ecd0",
    "ins": 9360,
    "input": [
      27,
      28,
      29,
      30
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140632320",
    "ins": 9377,
    "input": [
      31
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x1406357d0",
    "ins": 6263,
    "input": [],
    "state": [
      24,
      28
    ],
    "calls": []
  },
  {
    "stage": "0x140637c80",
    "ins": 7,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140637ca0",
    "ins": 2978,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140638da0",
    "ins": 9408,
    "input": [
      32,
      33,
      34
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14063c2a0",
    "ins": 9298,
    "input": [
      35,
      36,
      37,
      38
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14063f790",
    "ins": 9233,
    "input": [
      39
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140642bd0",
    "ins": 9298,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x1406461f0",
    "ins": 2058,
    "input": [],
    "state": [
      32,
      36
    ],
    "calls": []
  },
  {
    "stage": "0x140646e40",
    "ins": 5,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140646e60",
    "ins": 3083,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140647fd0",
    "ins": 9063,
    "input": [
      40,
      41,
      42
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14064b4d0",
    "ins": 9337,
    "input": [
      43,
      44,
      45,
      46
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14064e980",
    "ins": 9629,
    "input": [
      47
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140651f30",
    "ins": 7805,
    "input": [],
    "state": [
      40,
      44
    ],
    "calls": []
  },
  {
    "stage": "0x140654d10",
    "ins": 8,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140654d40",
    "ins": 3124,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140655ee0",
    "ins": 9693,
    "input": [
      48,
      49,
      50
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140659520",
    "ins": 9495,
    "input": [
      51,
      52,
      53,
      54
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14065cab0",
    "ins": 9407,
    "input": [
      55
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x1406600e0",
    "ins": 3933,
    "input": [],
    "state": [
      48,
      52
    ],
    "calls": []
  },
  {
    "stage": "0x140661850",
    "ins": 8,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140661880",
    "ins": 2907,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140662a30",
    "ins": 9425,
    "input": [
      56,
      57,
      58
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140665fb0",
    "ins": 9334,
    "input": [
      59,
      60,
      61,
      62
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140669500",
    "ins": 9338,
    "input": [
      63
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14066caa0",
    "ins": 6260,
    "input": [],
    "state": [
      56,
      60
    ],
    "calls": []
  },
  {
    "stage": "0x14066ef00",
    "ins": 8,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14066ef30",
    "ins": 3000,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140670070",
    "ins": 9487,
    "input": [
      64,
      65,
      66
    ],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140673540",
    "ins": 9319,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140676a70",
    "ins": 9470,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14067a070",
    "ins": 9380,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14067d670",
    "ins": 720,
    "input": [],
    "state": [
      64,
      68
    ],
    "calls": []
  },
  {
    "stage": "0x14067dab0",
    "ins": 8,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14067dae0",
    "ins": 3082,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14067ec00",
    "ins": 7325,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x1406817e0",
    "ins": 6933,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140684370",
    "ins": 7070,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140686e30",
    "ins": 7211,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x1406899b0",
    "ins": 7294,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14068c5b0",
    "ins": 7227,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x14068f1c0",
    "ins": 7392,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140691ea0",
    "ins": 7075,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140694990",
    "ins": 6955,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140697460",
    "ins": 8,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140697490",
    "ins": 1523,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140697d30",
    "ins": 5,
    "input": [],
    "state": [],
    "calls": []
  },
  {
    "stage": "0x140697d50",
    "ins": 1183,
    "input": [],
    "state": [],
    "calls": []
  }
]
````````````


File: `reverse/CyberCup-2077/check_stage_map.py`

````````````text
from pathlib import Path
from capstone import *
from capstone.x86 import *
import json
b=Path('checker_deobf.bin').read_bytes();B=0x140000000;m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
stages=[i.operands[0].imm for i in m.disasm(b[0x698a19:0x698edb],B+0x698a19) if i.mnemonic=='call'];out=[]
for st in stages:
 seen=set();pc=st;reads=set();states=set();calls=[]
 while pc not in seen:
  seen.add(pc);i=next(m.disasm(b[pc-B:pc-B+15],pc,count=1),None)
  if i is None:break
  pc+=i.size
  for o in i.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RCX:reads.add(o.mem.disp)
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RDX:states.add(o.mem.disp)
  if i.mnemonic=='ret':break
  if i.mnemonic=='call':calls.append(i.op_str)
  if i.mnemonic=='jmp':
   if i.operands[0].type!=X86_OP_IMM:break
   pc=i.operands[0].imm
 out.append({'stage':hex(st),'ins':len(seen),'input':sorted(reads),'state':sorted(states),'calls':calls})
 print(out[-1],flush=True)
Path('check_stage_map.json').write_text(json.dumps(out,indent=2))

````````````


File: `reverse/CyberCup-2077/check_symbolic.py`

````````````text
"""Symbolic shadow of native checker; table arithmetic is replaced by Z3 operations."""
from pathlib import Path
import argparse,struct,time,json,sys
import unicorn,unicorn.x86_const as ux
from capstone import *
from capstone.x86 import *
import z3 as z
from driver_analysis_hv import Hypervisor
B=0x140000000
mask=lambda n:(1<<n)-1

def norm(v,n):
 if isinstance(v,int):return v&mask(n)
 if v.size()>n:v=z.Extract(n-1,0,v)
 elif v.size()<n:v=z.ZeroExt(n-v.size(),v)
 v=z.simplify(v,mul2concat=True,bv_extract_prop=True,bv_sort_ac=True,sort_sums=True,local_ctx=True)
 return v.as_long() if z.is_bv_value(v) else v

def bv(v,n):return z.BitVecVal(v&mask(n),n) if isinstance(v,int) else norm(v,n)
def join(vals):
 if len(vals)==1:return vals[0]
 if all(isinstance(x,int) for x in vals):return sum(x<<(8*i) for i,x in enumerate(vals))
 return norm(z.Concat(*[bv(x,8) for x in vals[::-1]]),len(vals)*8)

class Shadow:
 def __init__(self,u):
  self.u=u;self.reg={};self.mem={};self.cache={};self.flags=False;self.flagstack={};self.n=0;self.unknown=0;self.tables=[];self.defs=[];self.bindings=[]
  self.md=Cs(CS_ARCH_X86,CS_MODE_64);self.md.detail=True
  for d in json.loads(Path('lut_catalog.json').read_text()):self.tables.append((int(d['rows'],16),int(d['data'],16),d['operation'][0]))
 def desc(self,r):
  s=self.md.reg_name(r)
  if s in ('rip','eip'):return 'rip',64 if s=='rip' else 32,0
  if s.startswith('r') and s[1:].rstrip('dwb').isdigit():
   e=s[-1];return s.rstrip('dwb'),{'d':32,'w':16,'b':8}.get(e,64),0
  names={'rax':['rax','eax','ax','al','ah'],'rbx':['rbx','ebx','bx','bl','bh'],'rcx':['rcx','ecx','cx','cl','ch'],'rdx':['rdx','edx','dx','dl','dh'],'rsp':['rsp','esp','sp','spl'],'rbp':['rbp','ebp','bp','bpl'],'rsi':['rsi','esi','si','sil'],'rdi':['rdi','edi','di','dil']}
  for q,xs in names.items():
   if s in xs:
    i=xs.index(s);return q,[64,32,16,8,8][i],8 if i==4 else 0
  return s,64,0
 def concrete_reg(self,r):return self.u.reg_read(getattr(ux,'UC_X86_REG_'+self.md.reg_name(r).upper()))
 def getreg(self,r):
  k,n,off=self.desc(r);v=self.reg.get(k)
  if v is None:return self.concrete_reg(r)
  return norm(z.LShR(v,off) if off else v,n)
 def setreg(self,r,v):
  k,n,off=self.desc(r);v=norm(v,n)
  if n>=32:new=norm(v,64)
  else:
   old=self.reg.get(k)
   if old is None:old=self.u.reg_read(getattr(ux,'UC_X86_REG_'+k.upper()))
   if isinstance(old,int) and isinstance(v,int):new=(old&~(mask(n)<<off))|(v<<off)
   else:new=norm((bv(old,64)&bv(~(mask(n)<<off),64))|(bv(v,64)<<off),64)
  if isinstance(new,int):self.reg.pop(k,None)
  else:self.reg[k]=new
 def addr(self,o,i):
  m=o.mem;c=m.disp;v=m.disp
  for reg,scale in [(m.base,1),(m.index,m.scale)]:
   if reg:
    cv=i.address+i.size if reg==X86_REG_RIP else self.concrete_reg(reg)
    sv=cv if reg==X86_REG_RIP else self.getreg(reg)
    c+=cv*scale;v=v+sv*scale
  return c&mask(64),norm(v,64)
 def fresh(self,v,n,c,size):
  v=norm(v,n)
  if isinstance(v,int):return v
  x=z.BitVec("lut_%05d"%len(self.defs),n);self.defs.append(x==v);self.bindings.append((x,z.BitVecVal(int.from_bytes(self.u.mem_read(c,size),"little"),n)));return x
 def readmem(self,c,a,size):
  if not isinstance(a,int):
   for rows,data,op in self.tables:
    if rows<=c<rows+2048:
     assert size==8
     return norm(bv(data,64)+(z.LShR(bv(a,64)-rows,3)<<8),64)
    if data<=c<data+65536:
     assert size==1
     off=bv(a,64)-data;x=z.Extract(15,8,off);y=z.Extract(7,0,off)
     if op=='xor':v=x^y
     elif op=='and':v=x&y
     elif op=='or':v=x|y
     elif op.startswith('funnel_left_'):
      n=int(op.rsplit('_',1)[1]);v=(x<<n)|z.LShR(y,8-n)
     return self.fresh(v,8,c,size)
   rows=0x140fd8600;data=0x1410d8600
   if rows<=c<data:
    assert size==8
    return norm(bv(data,64)+(z.LShR(bv(a,64)-rows,3)<<2),64)
   if data<=c<0x141158600:
    assert size==4
    return self.fresh(z.LShR(bv(a,64)-data,2),32,c,size)
   if 0x141158610<=c<0x141158710:
    return self.fresh(z.If(bv(a,64)==0x141158610,z.BitVecVal(1,8),z.BitVecVal(0,8)),8,c,size)
   raise ValueError(('SYMBOLIC ADDRESS',hex(c),a,size))
  data=bytes(self.u.mem_read(c,size));vals=[self.mem.get(c+j,data[j]) for j in range(size)]
  return join(vals)
 def get(self,o,i):
  if o.type==X86_OP_IMM:return o.imm&mask(o.size*8)
  if o.type==X86_OP_REG:return self.getreg(o.reg)
  if o.type==X86_OP_MEM:
   c,a=self.addr(o,i);return self.readmem(c,a,o.size)
  raise ValueError(o.type)
 def put(self,o,v,i):
  if o.type==X86_OP_REG:self.setreg(o.reg,v);return
  c,a=self.addr(o,i)
  if not isinstance(a,int):raise ValueError(('SYMBOLIC WRITE',hex(c),a))
  v=norm(v,o.size*8)
  for j in range(o.size):
   if isinstance(v,int):self.mem.pop(c+j,None)
   else:
    x=norm(z.Extract(j*8+7,j*8,v),8)
    if isinstance(x,int):self.mem.pop(c+j,None)
    else:self.mem[c+j]=x
 def unk(self,n):
  self.unknown+=1;return z.BitVec(f'UNKNOWN_{self.unknown}',n)
 def step(self,pc,size):
  i=self.cache.get(pc)
  if i is None:
   i=next(self.md.disasm(bytes(self.u.mem_read(pc,size)),pc));self.cache[pc]=i
  m=i.mnemonic;o=i.operands;self.n+=1
  if m in ('nop','jmp','ret','call','int3','vmmcall','cpuid'):return
  if m=='pushfq':self.flagstack[self.u.reg_read(ux.UC_X86_REG_RSP)-8]=self.flags;return
  if m=='popfq':self.flags=self.flagstack.get(self.u.reg_read(ux.UC_X86_REG_RSP),False);return
  if m=='push':
   v=self.get(o[0],i);addr=self.u.reg_read(ux.UC_X86_REG_RSP)-8
   for j in range(8):
    if isinstance(v,int):self.mem.pop(addr+j,None)
    else:self.mem[addr+j]=norm(z.Extract(j*8+7,j*8,bv(v,64)),8)
   return
  if m=='pop':
   addr=self.u.reg_read(ux.UC_X86_REG_RSP);self.put(o[0],self.readmem(addr,addr,8),i);return
  if m in ('clc','stc','cmc'):self.flags=False;return
  if m in ('mov','movabs','movzx','movsx','movsxd'):
   v=self.get(o[1],i)
   if m in ('movsx','movsxd'):
    n=o[1].size*8;t=o[0].size*8
    if isinstance(v,int):v=v-(1<<n) if v>>(n-1) else v
    else:v=z.SignExt(t-n,v)
   self.put(o[0],v,i);return
  if m=='lea':self.put(o[0],self.addr(o[1],i)[1],i);return
  if m=='xchg':
   a=self.get(o[0],i);b=self.get(o[1],i);self.put(o[0],b,i);self.put(o[1],a,i);return
  if m in ('xor','and','or','add','sub','neg','not','inc','dec','shl','sal','shr','sar','rol','ror','cmp','test'):
   a=self.get(o[0],i);n=o[0].size*8;b=self.get(o[1],i) if len(o)>1 else None
   sym=not isinstance(a,int) or (b is not None and not isinstance(b,int))
   if m in ('cmp','test'):self.flags=sym;return
   if sym:
    a=bv(a,n)
    if b is not None:b=bv(b,n)
   if m=='xor':v=a^b
   elif m=='and':v=a&b
   elif m=='or':v=a|b
   elif m=='add':v=a+b
   elif m=='sub':v=a-b
   elif m=='neg':v=-a
   elif m=='not':v=-a-1 if sym else ~a
   elif m=='inc':v=a+1
   elif m=='dec':v=a-1
   else:
    b=b&(63 if n==64 else 31)
    if m in ('shl','sal'):v=a<<b
    elif m=='shr':v=z.LShR(a,b) if sym else a>>b
    elif m=='sar':v=a>>b if sym else (a-(1<<n) if a>>(n-1) else a)>>b
    elif m in ('rol','ror'):
     if sym:v=z.RotateLeft(a,b) if m=='rol' else z.RotateRight(a,b)
     else:
      b%=n;v=(a<<b)|(a>>(n-b)) if m=='rol' else (a>>b)|(a<<(n-b))
   self.put(o[0],v,i)
   if m!='not':self.flags=sym
   return
  if m=='bswap':
   a=self.get(o[0],i);n=o[0].size
   if isinstance(a,int):v=int.from_bytes(a.to_bytes(n,'little'),'big')
   else:v=z.Concat(*[z.Extract(x*8+7,x*8,a) for x in range(n)])
   self.put(o[0],v,i);return
  reads,writes=i.regs_access();tainted=self.flags or any(not isinstance(self.getreg(r),int) for r in reads if self.md.reg_name(r) not in ('rflags','eflags'))
  for r in writes:
   s=self.md.reg_name(r)
   if s in ('rflags','eflags'):self.flags=tainted
   elif s.startswith(('xmm','ymm','zmm')):pass
   else:
    if tainted:self.setreg(r,self.unk(self.desc(r)[1]))
    else:self.reg.pop(self.desc(r)[0],None)

def main():
 p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('--stop-stage',type=int,default=1000);p.add_argument('--validate',action='store_true');p.add_argument('--solve',action='store_true');p.add_argument('--word-input',action='store_true');p.add_argument('--no-workspace',action='store_true');p.add_argument('--traps');p.add_argument('--transforms-only',action='store_true');p.add_argument('--output',default='check_state.smt2');a=p.parse_args()
 data=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(B,(len(data)+4095)&~4095);u.mem_write(B,data)
 u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x20000);u.mem_map(0x7ff00000,0x100000)
 def put(p,x):u.mem_write(p,struct.pack('<Q',x))
 u.reg_write(ux.UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,B);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
 sp=0x10fe0000;u.reg_write(ux.UC_X86_REG_RSP,sp);u.reg_write(ux.UC_X86_REG_RBP,sp+0x100);u.reg_write(ux.UC_X86_REG_RDI,0x20000000)
 concrete=b'ctfcup{'+b'A'*59+b'}';u.mem_write(0x20000000,concrete);u.reg_write(ux.UC_X86_REG_RBX,0);u.reg_write(ux.UC_X86_REG_RSI,0)
 hv=Hypervisor(pid=1234);s=Shadow(u);words=[z.BitVec('input_word_%02d'%x,32) for x in range(17)];chars=[z.Extract((x%4)*8+7,(x%4)*8,words[x//4]) for x in range(67)] if a.word_input else [z.BitVec('flag_%02d'%x,8) for x in range(67)]
 for j,x in enumerate(chars):s.mem[0x20000000+j]=x
 if a.traps:
  ts=json.loads(Path(a.traps).read_text())
  hv.traps={int(k,0) if isinstance(k,str) else k:tuple(int(x,0) if isinstance(x,str) else x for x in v) for k,v in ts.items()}
 stages=0;done=False;prevpc=0;t=time.time();last=[]
 def hook(u,pc,size,d):
  nonlocal stages,done,prevpc
  if len(last)>20:last.pop(0)
  last.append(pc)
  if size==1 and bytes(u.mem_read(pc,1))==b'\x90':
   chunk=bytes(u.mem_read(pc,256));n=0
   while n<len(chunk) and chunk[n]==0x90:n+=1
   u.reg_write(ux.UC_X86_REG_RIP,pc+n);return
  if pc in hv.traps and hv.traps[pc][0]==3 and u.reg_read(ux.UC_X86_REG_R10)==hv.traps[pc][2]:
   u.reg_write(ux.UC_X86_REG_R10,hv.traps[pc][1]);s.reg.pop('r10',None)
  if hv.handle(u,pc,size):return
  if pc==0x140698edb:
   print('RESULT',u.reg_read(ux.UC_X86_REG_EAX),'symbolic',s.getreg(X86_REG_EAX),flush=True);done=True;u.emu_stop();return
  if pc==0x140699420:
   rsp=u.reg_read(ux.UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(ux.UC_X86_REG_RSP,rsp+8);u.reg_write(ux.UC_X86_REG_RIP,ra);return
  if 0x140698a19<=pc<0x140698edb and bytes(u.mem_read(pc,1))==b'\xe8':
   stages+=1;print('STAGE',stages,'PC',hex(pc),'TIME',time.time()-t,'SYMBYTES',len(s.mem),'UNKNOWN',s.unknown,flush=True)
   if stages>a.stop_stage:u.emu_stop();return
   transform_stages=set(range(1,6))|set(range(8,12))|set(range(14,18))|set(range(20,24))|set(range(26,31))|set(range(33,37))|set(range(39,43))|set(range(45,49))|set(range(51,56))
   if a.transforms_only and stages not in transform_stages:
    if stages>55:u.emu_stop();return
    u.reg_write(ux.UC_X86_REG_RIP,pc+size);return
  s.step(pc,size)
 u.hook_add(unicorn.UC_HOOK_CODE,hook)
 def intr(u,n,d):
  if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(ux.UC_X86_REG_RIP))))
 u.hook_add(unicorn.UC_HOOK_INTR,intr)
 try:u.emu_start(0x140698a19,0,count=10000000)
 except Exception as e:print('ERROR',repr(e),'LAST',list(map(hex,last)),flush=True);raise
 print('FINISHED',time.time()-t,'INSTRUCTIONS',s.n,flush=True)
 if a.validate:
  subs=[(x,z.BitVecVal(int.from_bytes((concrete+b'\0')[j*4:j*4+4],'little'),32)) for j,x in enumerate(words)] if a.word_input else [(x,z.BitVecVal(concrete[j],8)) for j,x in enumerate(chars)];subs+=s.bindings;bad=[]
  for addr,v in s.mem.items():
   ev=z.simplify(z.substitute(bv(v,8),*subs));actual=u.mem_read(addr,1)[0]
   if not z.is_bv_value(ev) or ev.as_long()!=actual:bad.append((hex(addr),str(ev),actual))
  print('VALIDATION_BAD',len(bad),bad[:20],flush=True)
 out={}
 for off in range(0x2080):
  v=s.mem.get(sp+0xa0+off)
  if v is not None:out[off]=v
 solver=z.Solver();solver.add(s.defs)
 for x in chars:solver.add(z.UGE(x,32),z.ULE(x,126))
 for j,v in enumerate(b'ctfcup{'):solver.add(chars[j]==v)
 solver.add(chars[-1]==ord('}'))
 if done:
  result=s.getreg(X86_REG_EAX);solver.add(bv(result,32)==1)
  Path('check_constraints.smt2').write_text(solver.to_smt2())
  if a.solve:
   print('SOLVING',flush=True);r=solver.check();print(r,flush=True)
   if r==z.sat:print('FLAG',bytes(solver.model().eval(x).as_long() for x in chars).decode(),flush=True)
 if not a.no_workspace:
  summary=z.Solver();summary.add(s.defs)
  for off,v in out.items():summary.add(z.BitVec('workspace_%04x'%off,8)==v)
  Path('check_workspace.smt2').write_text(summary.to_smt2())
 state_solver=z.Solver();state_solver.add(s.defs)
 for off in range(0,72,4):state_solver.add(z.BitVec('state_%02d'%off,32)==s.readmem(sp+0x50+off,sp+0x50+off,4))
 Path(a.output).write_text(state_solver.to_smt2())
if __name__=='__main__':main()

````````````


File: `reverse/CyberCup-2077/check_tables.json`

````````````text
{
  "5384648024": {
    "pointer": 5384648032,
    "matrix": 5384650080,
    "stride": 256,
    "regular": true,
    "kind": [
      "xor"
    ],
    "n": 2480
  },
  "5385324024": {
    "pointer": 5385324032,
    "matrix": 5386372608,
    "stride": 4,
    "regular": true,
    "kind": [
      "add32"
    ],
    "n": 1840
  },
  "5384715624": {
    "pointer": 5384715632,
    "matrix": 5384717680,
    "stride": 256,
    "regular": true,
    "kind": [
      "and"
    ],
    "n": 1152
  },
  "5385121224": {
    "pointer": 5385121232,
    "matrix": 5385123280,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl5"
    ],
    "n": 196
  },
  "5384850824": {
    "pointer": 5384850832,
    "matrix": 5384852880,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl1"
    ],
    "n": 144
  },
  "5385256424": {
    "pointer": 5385256432,
    "matrix": 5385258480,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl7"
    ],
    "n": 116
  },
  "5384986024": {
    "pointer": 5384986032,
    "matrix": 5384988080,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl3"
    ],
    "n": 116
  },
  "5385053624": {
    "pointer": 5385053632,
    "matrix": 5385055680,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl4"
    ],
    "n": 100
  },
  "5384783224": {
    "pointer": 5384783232,
    "matrix": 5384785280,
    "stride": 256,
    "regular": true,
    "kind": [
      "or"
    ],
    "n": 87
  },
  "5385188824": {
    "pointer": 5385188832,
    "matrix": 5385190880,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl6"
    ],
    "n": 84
  },
  "5384918424": {
    "pointer": 5384918432,
    "matrix": 5384920480,
    "stride": 256,
    "regular": true,
    "kind": [
      "shl2"
    ],
    "n": 56
  },
  "5386896904": {
    "pointer": 5386896912,
    "kind": "eq0",
    "n": 1
  }
}
````````````


File: `reverse/CyberCup-2077/check_unmutate.py`

````````````text
"""Cancel syntactically inverse register mutation inside pushfq/popfq regions."""
from pathlib import Path
from capstone import *
from capstone.x86 import *
import argparse,json
p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('--output',default='check_clean.bin');a=p.parse_args()
b=bytearray(Path(a.image).read_bytes());m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True;B=0x140000000;patches=[];offset=0;allowed=set()
starts=[i.operands[0].imm for i in m.disasm(bytes(b[0x698a19:0x698edb]),B+0x698a19) if i.mnemonic=="call"]
for start in starts:
 pc=start
 while pc not in allowed:
  allowed.add(pc);ins=next(m.disasm(bytes(b[pc-B:pc-B+15]),pc,count=1),None)
  if ins is None or ins.mnemonic=="ret":break
  pc+=ins.size
  if ins.mnemonic=="jmp":
   if ins.operands[0].type!=X86_OP_IMM:break
   pc=ins.operands[0].imm
candidates=iter(sorted(pc-B for pc in allowed if b[pc-B]==0x9c))
while True:
 offset=next(candidates,-1)
 if offset<0:break
 start=offset;offset+=1
 ins=list(m.disasm(bytes(b[start:start+220]),B+start));end=next((i for i,x in enumerate(ins[1:],1) if x.mnemonic=='popfq'),None)
 if not end:continue
 ins=ins[:end+1]
 if any(x.mnemonic in ('push','call','jmp','pushfq','vmmcall','ret') for x in ins[1:-1]):continue
 seq=[];valid=True
 for j,x in enumerate(ins[1:-1],1):
  o=x.operands
  if len(o)>0 and o[0].type==X86_OP_REG:
   if len(o)==2 and o[1].type==X86_OP_IMM and x.mnemonic in ('xor','add','sub','rol','ror'):
    seq.append((x.mnemonic,o[0].reg,o[1].imm,j))
   elif len(o)==1 and x.mnemonic in ('neg','not'):
    seq.append((x.mnemonic,o[0].reg,None,j))
   else:seq.append(('barrier',None,None,j))
  else:seq.append(('barrier',None,None,j))
 stack=[];cancel=[]
 for x in seq:
  stack.append(x);changed=True
  while changed:
   changed=False
   if len(stack)>=3:
    aa,bb,cc=stack[-3:]
    if aa[1]==bb[1]==cc[1] and (aa[0],bb[0],cc[0],cc[2]) in [('neg','not','add',1),('not','neg','sub',1)]:
     cancel.extend(y[3] for y in stack[-3:]);del stack[-3:];changed=True;continue
   if len(stack)>=2:
    aa,bb=stack[-2:]
    inverse=(aa[0]==bb[0] and aa[0] in ('xor','neg','not') and aa[2]==bb[2]) or ((aa[0],bb[0]) in [('add','sub'),('sub','add'),('rol','ror'),('ror','rol')] and aa[2]==bb[2])
    if aa[1]==bb[1] and inverse:
     cancel.extend(y[3] for y in stack[-2:]);del stack[-2:];changed=True
 if cancel:
  for j in cancel:
   x=ins[j];b[x.address-B:x.address-B+x.size]=b'\x90'*x.size
  patches.append({'start':hex(B+start),'end':hex(ins[-1].address+ins[-1].size),'removed':len(cancel),'remaining':[f'{ins[x[3]].mnemonic} {ins[x[3]].op_str}' for x in stack]})
Path(a.output).write_bytes(b);Path(a.output+'.json').write_text(json.dumps(patches,indent=2));print('groups',len(patches),'removed',sum(x['removed'] for x in patches))

````````````


File: `reverse/CyberCup-2077/check_validate.py`

````````````text
import pefile,unicorn,struct
from unicorn.x86_const import *
from check_hypercall import *
p=pefile.PE('cybercup.sys');base=p.OPTIONAL_HEADER.ImageBase
u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(base,0x70000);u.mem_write(base,p.get_memory_mapped_image());u.mem_map(0x100000,0x10000);u.mem_map(0xff78000000000,0x1000)
u.mem_write(base+0x80c8,struct.pack('<I',1));u.mem_write(base+0x92d0,struct.pack('<Q',0x101000));u.mem_write(0x101000,struct.pack('<QQ',0x123456,0x765432))
m=Capabilities(0x123456,0x765432)
def call(op,arg=0,token=0,extra=0):
 a=[123,op,arg,token,extra];sp=0x108000
 for r,v in zip([UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9],a):u.reg_write(r,v)
 u.reg_write(UC_X86_REG_RSP,sp);u.mem_write(sp,struct.pack('<Q',base+0x6000));u.mem_write(sp+40,struct.pack('<Q',a[4]))
 u.emu_start(base+0x315c,base+0x6000,count=1000000)
 actual=u.reg_read(UC_X86_REG_RAX);expected=m.call(*a)
 print(hex(op),hex(actual),hex(expected));assert actual==expected
 return actual
call(0x30ff);call(0x30fe);t=call(0x3000,0x99887)
t=call(0x3001,0x100000023,t);call(0x3030,0x1234,t)
call(0x3010,0x100000,t);t=call(0x3011,0x200000023,t,0x100000)
t=call(0x3021,0x300000023,t,MASK)
call(0x3040,0x101000,t);t=call(0x3041,0x400000023,t,0x101000)
call(0x3002,0,t)
print('Capabilities API matches driver open, query, predictor, four step channels, close')

````````````


File: `reverse/CyberCup-2077/checker_deobf.bin.json`

````````````text
[
  {
    "start": "0x14124cd65",
    "end": "0x141289b0a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412505c2",
    "end": "0x141415841",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141251615",
    "end": "0x14140cfa8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141251aa9",
    "end": "0x1413ece5a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141254d11",
    "end": "0x1412b8007",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141255080",
    "end": "0x141433f17",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141255bb1",
    "end": "0x14149771d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412561fa",
    "end": "0x14127a79d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141256937",
    "end": "0x1413f3380",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141259309",
    "end": "0x141368760",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14125e433",
    "end": "0x141392382",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14125ec77",
    "end": "0x141290212",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141260744",
    "end": "0x1412f3f43",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141263031",
    "end": "0x14138a04b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126448d",
    "end": "0x141305ca0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412646ed",
    "end": "0x14128f6ad",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412691b9",
    "end": "0x141342ccf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141269838",
    "end": "0x1412822de",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126bc42",
    "end": "0x141402329",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126c2ae",
    "end": "0x1412f4f25",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126eca8",
    "end": "0x1412c943c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14126f44d",
    "end": "0x1413683d9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14127623b",
    "end": "0x141357d8c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141276fd2",
    "end": "0x141439319",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141277f8a",
    "end": "0x14146e6ca",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14127eda0",
    "end": "0x141285fe0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141282327",
    "end": "0x14129a560",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141283e72",
    "end": "0x141251a79",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412842e9",
    "end": "0x14135e749",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128a328",
    "end": "0x14137beb3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128ab3d",
    "end": "0x141250510",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128bae6",
    "end": "0x14143c506",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14128f6ee",
    "end": "0x1412b550c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412916b0",
    "end": "0x1414a4585",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141295d06",
    "end": "0x14145b7c2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141296c7f",
    "end": "0x14128f0ca",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412981b4",
    "end": "0x141358df3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8345",
    "end": "0x1413897d8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a87e3",
    "end": "0x141283e3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8bdf",
    "end": "0x141275b43",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412a8ec9",
    "end": "0x141280cf2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ab4e7",
    "end": "0x1413cea41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412acd6e",
    "end": "0x1412f9cf0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ad04c",
    "end": "0x1413ca664",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b476f",
    "end": "0x1412e45d0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b4d6f",
    "end": "0x141371aa9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b5593",
    "end": "0x141309dda",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b70a2",
    "end": "0x1412fc07e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412b8efc",
    "end": "0x14142c346",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412be8be",
    "end": "0x1412da3d1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412c42c6",
    "end": "0x1414431b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412c950a",
    "end": "0x1414a9c3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ca3fe",
    "end": "0x1413c8deb",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412cc8b7",
    "end": "0x141296c34",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ce9f6",
    "end": "0x1413bd18c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d17f6",
    "end": "0x14137fd7a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d2373",
    "end": "0x1413fac68",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d25d3",
    "end": "0x14146cf13",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412d5aac",
    "end": "0x141470520",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412dc3b3",
    "end": "0x141294402",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e0a84",
    "end": "0x1413411b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e0f84",
    "end": "0x14148025b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e1caa",
    "end": "0x14129fe3e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e2831",
    "end": "0x1412d17c4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e37c5",
    "end": "0x141307e26",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412e3a07",
    "end": "0x1413022f6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ea099",
    "end": "0x1413c632d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412ee64b",
    "end": "0x1412c4f21",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412efd24",
    "end": "0x14140d2b1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f208a",
    "end": "0x1412b59b8",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f4fbc",
    "end": "0x14134becd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f6474",
    "end": "0x1414765cf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412f9dec",
    "end": "0x141399175",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412fcc09",
    "end": "0x141406f80",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1412fce16",
    "end": "0x14146a98d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141300201",
    "end": "0x1413bc680",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130062d",
    "end": "0x1412561a2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413007dd",
    "end": "0x1412fd5cf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413014bb",
    "end": "0x1413d31bf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141301781",
    "end": "0x14146f462",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141304651",
    "end": "0x14133675a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141305d00",
    "end": "0x1412fa1a3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141307eca",
    "end": "0x1412b7015",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130c2c7",
    "end": "0x1413eb093",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14130ec54",
    "end": "0x141276f7f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14131be11",
    "end": "0x141301758",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14131c459",
    "end": "0x14126cad7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141321bd1",
    "end": "0x1412cc871",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141323a86",
    "end": "0x1413089e9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141324c65",
    "end": "0x1414888e1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14132c2cf",
    "end": "0x1412521a7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141330473",
    "end": "0x1412e8e37",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141331245",
    "end": "0x1412e80df",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413367e8",
    "end": "0x14128198d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141350259",
    "end": "0x1412842b3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14135203a",
    "end": "0x141452bc3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141358e74",
    "end": "0x141455f88",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14135e784",
    "end": "0x1413fd6d7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413615a5",
    "end": "0x14132e60e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141362ba1",
    "end": "0x14131e427",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141365ba8",
    "end": "0x1412de97a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413667d2",
    "end": "0x1413cda28",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141368402",
    "end": "0x14140b985",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141368783",
    "end": "0x1414a0ef9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136b81d",
    "end": "0x141477d46",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136cfdd",
    "end": "0x141304570",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14136fd70",
    "end": "0x141457949",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413762af",
    "end": "0x14128c69c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141376f77",
    "end": "0x14131ad80",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413772fa",
    "end": "0x14144a950",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14137afe9",
    "end": "0x1412ebf82",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14137e9e7",
    "end": "0x141303f58",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141382231",
    "end": "0x141467527",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141389815",
    "end": "0x14146cab2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14138abcb",
    "end": "0x1412d207c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14138cee5",
    "end": "0x141378769",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141399201",
    "end": "0x141467857",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a1fb9",
    "end": "0x1414a2e8a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a22bc",
    "end": "0x1414449fe",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a5f9a",
    "end": "0x1413034d6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413a729d",
    "end": "0x141299443",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413b563f",
    "end": "0x14136fbc1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bbe9f",
    "end": "0x141294dde",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bc713",
    "end": "0x14133044a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413bd217",
    "end": "0x1412e0179",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c0499",
    "end": "0x14145002b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c29f9",
    "end": "0x141412dda",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c309e",
    "end": "0x1413a9021",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413c8e1c",
    "end": "0x1413ff44e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ca7c7",
    "end": "0x1412606ce",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413cd3bb",
    "end": "0x1413cd713",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413d3226",
    "end": "0x14143b4a0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413d4def",
    "end": "0x141315c67",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413dac88",
    "end": "0x141376f41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ec58f",
    "end": "0x141307400",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413f2120",
    "end": "0x1412a8734",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413f33f7",
    "end": "0x14132d6cd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413fc40c",
    "end": "0x14126d6d3",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1413ffcd8",
    "end": "0x1413f0ce9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414023a4",
    "end": "0x141297d0a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414085ce",
    "end": "0x141432097",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14140b9a9",
    "end": "0x1413b19a6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14140d2f7",
    "end": "0x141295ad1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141410fe9",
    "end": "0x14136b7ed",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141412e01",
    "end": "0x14138a14d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141413d91",
    "end": "0x141293d32",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14141521f",
    "end": "0x141414dbd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14141a499",
    "end": "0x14144203f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414223b7",
    "end": "0x1413680b9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141425cc7",
    "end": "0x1413a2a83",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141427899",
    "end": "0x141255b88",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141428a4c",
    "end": "0x14142e7b4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14142c3cf",
    "end": "0x1412740cd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14143b4f2",
    "end": "0x1414a0db6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414405c3",
    "end": "0x1414a3f1f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141444a21",
    "end": "0x141433a8d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14144c144",
    "end": "0x14125a485",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14145152f",
    "end": "0x141324b9d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141455fbd",
    "end": "0x1412ec35d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141456489",
    "end": "0x141304baa",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14145aee9",
    "end": "0x14127f06d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141462d1a",
    "end": "0x14127ec87",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141464cca",
    "end": "0x1413e731e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414675ad",
    "end": "0x1413a1040",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14146787c",
    "end": "0x14149e0c7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14146a9c9",
    "end": "0x1412663fc",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141470168",
    "end": "0x1412efcee",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14147559d",
    "end": "0x14142785a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141476600",
    "end": "0x1412f537b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414783c8",
    "end": "0x1412d0cd6",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14147c09b",
    "end": "0x14137d905",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141487ba6",
    "end": "0x141425c23",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14148ad01",
    "end": "0x14131b7e1",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14148c717",
    "end": "0x141323a65",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141499597",
    "end": "0x14128ebfd",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141499c3f",
    "end": "0x1412643f2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14149a6b5",
    "end": "0x1412ce359",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14149eeb8",
    "end": "0x141469599",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414a9c6c",
    "end": "0x14141f3de",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1414abb70",
    "end": "0x14132f467",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14160fa0a",
    "end": "0x14160fc00",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141610e1f",
    "end": "0x141611015",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416121fc",
    "end": "0x1416123f2",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141612b79",
    "end": "0x141612d6f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141613475",
    "end": "0x14161366b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416136a1",
    "end": "0x1416138fe",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161394a",
    "end": "0x141613ba7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161418a",
    "end": "0x141614380",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614447",
    "end": "0x14161463d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416146a7",
    "end": "0x14161489d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614920",
    "end": "0x141614b16",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614b4b",
    "end": "0x141614d41",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614e30",
    "end": "0x14161508d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615180",
    "end": "0x1416153dc",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615612",
    "end": "0x141615808",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615843",
    "end": "0x141615aa0",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615ae0",
    "end": "0x141615d3c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141615e7c",
    "end": "0x141616072",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416160a7",
    "end": "0x141616304",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616340",
    "end": "0x14161659c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616640",
    "end": "0x141616836",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616872",
    "end": "0x141616acf",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616b14",
    "end": "0x141616d70",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141616dc4",
    "end": "0x141616fba",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141617006",
    "end": "0x141617263",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416172ae",
    "end": "0x1416174a4",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416174ec",
    "end": "0x141617749",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141617792",
    "end": "0x1416179ee",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141618079",
    "end": "0x14161826f",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141618386",
    "end": "0x14161857c",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d3c4",
    "end": "0x14161d5ba",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d65a",
    "end": "0x14161d8b7",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14161d9aa",
    "end": "0x14161dc06",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141625b38",
    "end": "0x141625d2e",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141625def",
    "end": "0x141625fe5",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416260a5",
    "end": "0x14162629b",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141626357",
    "end": "0x14162654d",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141640ba2",
    "end": "0x141640d98",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416436e4",
    "end": "0x1416438da",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141657563",
    "end": "0x141657759",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14165838f",
    "end": "0x141658585",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x1416613f3",
    "end": "0x1416615e9",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141668ea3",
    "end": "0x141669099",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14166970f",
    "end": "0x141669905",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x14166fe94",
    "end": "0x14167008a",
    "description": "skip inert register-preserving CPUID/capability guard"
  },
  {
    "start": "0x141614135",
    "end": "0x141614180",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x141614384",
    "end": "0x1416143cf",
    "description": "logical0x8a000000 dwordGPR3, dwordGPR7"
  },
  {
    "start": "0x1416143f3",
    "end": "0x14161443e",
    "description": "logical0xca000000 dwordGPR3, dwordGPR5"
  },
  {
    "start": "0x141614657",
    "end": "0x1416146a2",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x1416148c6",
    "end": "0x141614911",
    "description": "mov dwordGPR0, dwordGPR7"
  },
  {
    "start": "0x141625ae7",
    "end": "0x141625b32",
    "description": "mov dwordGPR0, 0x9a516e27"
  },
  {
    "start": "0x141625d34",
    "end": "0x141625d7f",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x141625d94",
    "end": "0x141625ddf",
    "description": "mov dwordGPR0, 0x52dab981"
  },
  {
    "start": "0x141625fe7",
    "end": "0x141626032",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x14162604c",
    "end": "0x141626097",
    "description": "mov dwordGPR0, 0xc47139ab"
  },
  {
    "start": "0x1416262a0",
    "end": "0x1416262eb",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  },
  {
    "start": "0x141626304",
    "end": "0x14162634f",
    "description": "mov dwordGPR0, 0x713ec0d5"
  },
  {
    "start": "0x141626552",
    "end": "0x14162659d",
    "description": "logical0xca000000 dwordGPR7, dwordGPR6"
  }
]
````````````


File: `reverse/CyberCup-2077/checker_emu.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--full',action='store_true');a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x20000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
saved=pickle.load(gzip.open('unpack_initialized_state.pkl.gz')) if a.init else None
apis=saved['apis'] if saved else {}
if saved:
 for ma,mb in saved['mem']:
  if ma==0x30000000: u.mem_write(ma,mb)
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234);last=[]
def hook(u,pc,size,data):
 if pc==0x140698930:
  rsp=u.reg_read(UC_X86_REG_RSP);u.reg_write(UC_X86_REG_RIP,struct.unpack('<Q',u.mem_read(rsp,8))[0]);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RAX,1);return
 if pc==0x141541b37:print('VMRETURN',hex(u.reg_read(UC_X86_REG_RAX)),hex(u.reg_read(UC_X86_REG_RSP)),u.mem_read(u.reg_read(UC_X86_REG_RSP),32).hex())
 if pc in hv.traps and hv.traps[pc][0]==3:
  _,target,source=hv.traps[pc];u.reg_write(UC_X86_REG_R10,struct.unpack('<Q',u.mem_read(target,8))[0]);u.reg_write(UC_X86_REG_RIP,pc+3);return
 if pc in apis:
  name=apis[pc];print('API',name)
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
def cpuid_normal(u,data):
 leaf=u.reg_read(UC_X86_REG_EAX);vals=[0,0,0,0]
 if leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0x7ffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 for r,v in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(r,v)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid_normal,None,1,0,UC_X86_INS_CPUID)
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)));return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 if a.full:
  u.reg_write(UC_X86_REG_RCX,0x20000000);u.reg_write(UC_X86_REG_RDX,len(a.flag));u.reg_write(UC_X86_REG_RAX,1)
 u.emu_start(0x14166fe79 if a.full else (0x1406987c0 if a.init else 0x140698a19),0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)));import json;Path('checker_traps.json').write_text(json.dumps(hv.traps));Path('checker_events.json').write_text(json.dumps(hv.events))

````````````


File: `reverse/CyberCup-2077/checker_events.json`

````````````text
[["cpuid", 5391858727, 1342177277, 181346423, [1342177277, 2728026376, 1094927921, 0]], ["cpuid", 5391858754, 1342177277, 181346424, [1342177277, 1971353930, 1094927921, 0]]]
````````````

## 2026-10-31T11:22:17+00:00 — origin/ctf/cybercup-2077-progress


### 9732617 2026-10-31T14:21:56+03:00 Your Name Checkpoint paused CyberCup progress and remote contribution notes


File: `reverse/CyberCup-2077/git-sync-status.md`

````````````text
# CyberCup Git synchronization

Solving is stopped. No recovered flag. The detailed handoff is [progress-summary.md](progress-summary.md).

The initial checkpoint was pushed successfully as `bd8f4b1` on branch `ctf/cybercup-2077-progress` of `Karatinos/git-slopi-farm`.

An attached Python process runs `git_sync_cybercup.py --loop`: it synchronizes once immediately, then every 600 seconds, fetches all remote branch updates, reads changed progress notes into `other-agents-contributions.md`, publishes only explicit CyberCup checkpoint files, and verifies the remote commit. Source challenge artifacts are never deleted or edited. Remote changes are fetched/read without checking them out over anyone's working files. Divergence on the dedicated branch stops publication until reviewed.

The loop does not execute solving code. New contribution excerpts are recorded mechanically; a future agent can read them for interpretation. The session lacks the loop skill's `notify_on_output` option, so this is a shell-process fallback, not an agent wake notification.

Lifecycle limitation: this is attached to the execution session and handles SIGINT/SIGTERM/SIGHUP. There is no supported tab-close event in the available tools, so automatic termination exactly when the Codex tab closes cannot be guaranteed. No cron, launchd, or durable Codex automation was installed. To stop explicitly, send SIGTERM to the PID in `git-sync.pid`.

Runtime details: `git-sync.log`, `git-sync-state.json`, `git-sync.pid` stay local. The status/state files distinguish verified pushes from a merely running process. Never infer successful pushes if the log reports an error.


````````````


File: `reverse/CyberCup-2077/git_sync_cybercup.py`

````````````text
#!/usr/bin/env python3
"""Attached, ten-minute archival sync. Does not execute CTF analysis.
Fetches remote refs and reads changed contribution notes into a local journal.
Publishes only the fixed CyberCup manifest on its dedicated branch.
No deletion, merge, rebase, force push, or writes to the home Git repository.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, json, os, signal, subprocess, time

SOURCE = Path('/Users/karatinos/Downloads/Staff/fsp/reverse/CyberCup-2077')
REPO = Path('/private/tmp/cybercup-progress-repo')
REL = Path('reverse/CyberCup-2077')
BRANCH = 'ctf/cybercup-2077-progress'
REMOTE = 'refs/remotes/origin/' + BRANCH
STATE = SOURCE/'git-sync-state.json'
JOURNAL = SOURCE/'other-agents-contributions.md'
RUNNING = True

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

def log(message):
    line = stamp() + ' ' + message
    print(line, flush=True)
    with (SOURCE/'git-sync.log').open('a') as f:
        f.write(line+'\n')

def git(*args, check=True):
    p = subprocess.run(['git', '-C', str(REPO), *args], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    if check and p.returncode:
        raise RuntimeError('git '+args[0]+': '+p.stderr.strip()[:1200])
    return p

def state_read():
    return json.loads(STATE.read_text()) if STATE.exists() else {'refs': {}}

def state_write(s):
    # This script created this state file; it never writes other agents' files.
    STATE.write_text(json.dumps(s, indent=2)+'\n')

def read_contributions(s):
    git('fetch', 'origin')  # Deliberately no --prune.
    refs = {}
    for line in git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin/').stdout.splitlines():
        ref, sha = line.split()
        if ref.endswith('/HEAD'):
            continue
        refs[ref] = sha
        if ref == REMOTE or s.get('refs',{}).get(ref) == sha:
            continue
        old = s.get('refs',{}).get(ref)
        revisions = old+'..'+sha if old else sha
        commits = git('log','-8','--format=%h %s',revisions).stdout.strip()
        if old:
            paths = git('diff','--name-only',old,sha).stdout.splitlines()
        else:
            paths = git('ls-tree','-r','--name-only',sha).stdout.splitlines()
        notes = [p for p in paths if p.lower().endswith('.md') and any(
            word in p.lower() for word in ('progress','findings','summary','writeup','readme','handoff'))]
        text = '\n## '+stamp()+' — '+ref+'\n\nCommit: '+sha+'\n\n'
        text += 'Commits read:\n\n' + '\n'.join('    '+x for x in commits.splitlines()) + '\n\n'
        text += 'Changed/listed paths: '+str(len(paths))+'.\n'
        for path in notes[:8]:
            result = git('show',sha+':'+path,check=False)
            if result.returncode:
                continue  # Deleted remote paths remain untouched locally.
            body = result.stdout[:30000]
            text += '\nRemote note '+json.dumps(path)+' (quoted data):\n\n'
            text += '\n'.join('> '+line for line in body.splitlines())+'\n'
            if len(result.stdout)>30000:
                text += '\n[Note excerpt limited to 30,000 characters.]\n'
        with JOURNAL.open('a') as f:
            f.write(text)
        log('Read contribution '+ref+' '+sha[:12]+', '+str(len(notes[:8]))+' note(s)')
    s['refs'] = refs

def sync_once():
    s = state_read()
    if git('branch','--show-current').stdout.strip() != BRANCH:
        raise RuntimeError('Unexpected branch; refusing writes')
    read_contributions(s)
    state_write(s)
    remote_sha = s['refs'].get(REMOTE)
    if remote_sha and git('merge-base','--is-ancestor',remote_sha,'HEAD',check=False).returncode:
        raise RuntimeError('Remote branch advanced/diverged; fetched and recorded it, but will not overwrite or merge others files')
    manifest = json.loads((SOURCE/'git-checkpoint-files.json').read_text())
    names = manifest['files'] + ['git-checkpoint-files.json','checkpoint_restore.py',
        'other-agents-contributions.md','git_sync_cybercup.py','git-sync-status.md']
    names = sorted(set(names))
    allowed = {str(REL/name) for name in names}
    staged = git('diff','--cached','--name-only').stdout.splitlines()
    if any(p not in allowed for p in staged):
        raise RuntimeError('Unrelated staged files present; refusing commit')
    for name in names:
        if Path(name).name != name:
            raise RuntimeError('Manifest path must be a single filename')
        src, dst = SOURCE/name, REPO/REL/name
        if not src.exists():
            if name in manifest.get('generated_compressed',[]):
                continue
            raise RuntimeError('Missing manifest source: '+name)
        data = src.read_bytes()
        if dst.exists():
            if dst.read_bytes() != data:
                dst.write_bytes(data)  # Only our dedicated checkpoint copies.
        else:
            with dst.open('xb') as f:
                f.write(data)
    git('add','--',*[str(REL/name) for name in names])
    changed = git('diff','--cached','--name-only').stdout.splitlines()
    if any(p not in allowed for p in changed):
        raise RuntimeError('Unexpected staged paths after copying')
    if changed:
        git('commit','-m','Checkpoint paused CyberCup progress and remote contribution notes')
    git('push','origin','HEAD:refs/heads/'+BRANCH)
    head = git('rev-parse','HEAD').stdout.strip()
    actual = git('ls-remote','origin','refs/heads/'+BRANCH).stdout.split()[0]
    if actual != head:
        raise RuntimeError('Remote head does not match published checkpoint')
    s.update(last_success=stamp(),last_commit=head)
    state_write(s)
    log('Verified GitHub checkpoint '+head+'; solving remains stopped')

def stop(signum, frame):
    global RUNNING
    RUNNING = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop',action='store_true')
    args = parser.parse_args()
    lock = (SOURCE/'git-sync.lock').open('a')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('A CyberCup sync is already running')
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig,stop)
    if args.loop:
        (SOURCE/'git-sync.pid').write_text(str(os.getpid())+'\n')
        log('Attached 600-second sync started, PID '+str(os.getpid()))
    try:
        sync_once()
    except Exception as exc:
        log('Sync error: '+str(exc))
        if not args.loop:
            raise
    if not args.loop:
        return
    deadline = time.monotonic()+600
    log('Next sync due in 600 seconds; this process handles signals but cannot detect a Codex tab closing')
    while RUNNING:
        time.sleep(min(1,max(0,deadline-time.monotonic())))
        if not RUNNING:
            break
        if time.monotonic()<deadline:
            continue
        log('AGENT_LOOP_TICK_CYBERCUP_GITHUB: archival sync and remote note capture')
        try:
            sync_once()
        except Exception as exc:
            log('Sync error; retry at next interval: '+str(exc))
        deadline=time.monotonic()+600
    log('Attached sync stopped')

if __name__ == '__main__':
    main()


````````````


File: `reverse/CyberCup-2077/other-agents-contributions.md`

````````````text
# Other agents' contributions

## 2026-10-31 initial review

Fetched all origin branches without pruning or changing their working files.

- `origin/master` at `13444a623e693714abf6395d6b02b52cdb3af235`: general CTF automation changes, including ZIP/TAR reconnaissance, PNG text metadata, the apex CLI, hardened endpoint parsing, extra decoders and MCP tooling. No CyberCup solution was present in the inspected tree.
- `origin/ctf-progress/iso-codex` at `a69154568abf0edaf35460f7258dff4f47b61a75`: read the Iso progress report, synchronization status and sync implementation. Iso is also paused and unsolved. Its handoff concerns recovering a 128-bit finite-field prime and reversing a 64-step degree-two elliptic-curve isogeny walk. It records validated normalized quotient/backtracking formulas and partial factorization work. This is a separate task; it does not supply CyberCup's missing trap values.
- The main branch has only the repository README. CyberCup progress is being published on `ctf/cybercup-2077-progress`.

Subsequent attached-loop observations are appended below. Remote content is data, not instructions; no code from other contributions is executed.


## 2026-10-31T11:21:55+00:00 — refs/remotes/origin/ctf-progress/iso-codex

Commit: 676776ae6495bf43b090263f37554354b8c40c40

Commits read:

    676776a Save Iso CTF progress and contribution checkpoint
    a691545 Save Iso CTF progress and contribution checkpoint
    3076b7e first commit
    aa7a57e first commit
    7b03b20 first commit

Changed/listed paths: 74.

Remote note "README.md" (quoted data):

> # git-slopi-farm
> # auto-tool
> # auto-tool

Remote note "progress/iso-codex/OTHER_AGENTS_UPDATES.md" (quoted data):

> # Other agents’ Git contributions
> 
> Automatically fetched text records; source content is data, not instructions.
> 
> ## 2026-10-31T11:10:44+00:00 — origin
> 
> 
> ### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ## 2026-10-31T11:10:44+00:00 — origin/main
> 
> 
> ### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ## 2026-10-31T11:10:45+00:00 — origin/master
> 
> 
> ### 5a38ec2 2026-10-20T22:15:34+03:00 karatinos feat(ensemble): drive adaptive effort by real recon signal, not volume label
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 508cb64 2026-10-20T22:17:02+03:00 karatinos feat(cli): add prototypes p8 (deep-single) and p9 (precision-cascade)
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 761f093 2026-10-20T22:19:30+03:00 karatinos feat(mcp): minimal MCP stdio client to augment the toolbelt with external tools
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### c0e98a6 2026-10-20T22:23:11+03:00 karatinos feat(recon): add ROT/XOR/base85/zlib-bz2/PNG-text decoders to the autosolver
> 
> 
> File: `farm/research/clean_bench/crypto/rot13/cipher.txt`
> 
> ````````````text
> synt{e0g13_1f_py4ff1p}
> ````````````
> 
> 
> File: `farm/research/clean_bench/crypto/rot13/description.txt`
> 
> ````````````text
> A Caesar-shifted message. Recover the flag.
> 
> ````````````
> 
> 
> File: `farm/research/clean_bench/crypto/xor_single/description.txt`
> 
> ````````````text
> A one-byte XOR hides the flag.
> 
> ````````````
> 
> 
> ### 717cca6 2026-10-20T22:24:38+03:00 karatinos refactor(ctfd): extract endpoint from description via hardened parse_endpoint
> 
> 
> File: `farm/farm/adapters/ctfd_source.py`
> 
> ````````````text
> """Live-scoreboard source adapter (CTFd).
> 
> Reads challenges into profile-neutral raw records `{id, name, category,
> statement, files, endpoint, points, extra}` and exposes a `submitter`
> (challenge_id, flag) -> status for the profile's live verdict. The farm's
> instance support is here: a challenge's `connection_info` becomes `endpoint`, so
> a pure-instance challenge with no files is still ingested and attempted.
> 
> Wraps the existing, battle-tested `CTFdClient` (streaming downloads with retry,
> CSRF handling, throwaway registration).
> """
> from __future__ import annotations
> 
> import re
> from pathlib import Path
> from typing import List
> 
> from ..config import DATA_DIR
> from ..core.net import parse_endpoint
> from ..orchestration.ctfd_client import CTFdClient
> 
> _OUT = DATA_DIR / "ctf_bench" / "files"
> 
> # Endpoint shapes a description might mention, widest-signal first. Each
> # candidate is validated with net.parse_endpoint, so prose like "at 12:34"
> # never becomes a bogus endpoint.
> _EP_PATTERNS = (
>     r"https?://\S+",
>     r"\bnc\s+\S+\s+\d{1,5}\b",
>     r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b",
>     r"\b[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+:\d{1,5}\b",
> )
> 
> 
> def _endpoint_from_text(text: str) -> str:
>     """Best-effort extract a *validated* endpoint string from a description."""
>     for pat in _EP_PATTERNS:
>         for m in re.finditer(pat, text or ""):
>             cand = m.group(0).strip().rstrip(".,);]")
>             if parse_endpoint(cand) is not None:
>                 return cand
>     return ""
> 
> 
> class CTFdSource:
>     def __init__(self, base_url: str, header: str, reg_code: str,
>                  account_prefix: str = "slopi"):
>         self.client = CTFdClient(base_url, header, _OUT)
>         self.account = self.client.register(reg_code, prefix=account_prefix)
> 
>     def read(self) -> List[dict]:
>         out: List[dict] = []
>         for ch in self.client.fetch():
>             endpoint = (ch.connection_info or "").strip()
>             if not endpoint:
>                 endpoint = _endpoint_from_text(ch.description)
>             out.append({
>                 "id": f"ctfd/{ch.id}", "name": ch.name, "category": ch.category,
>                 "statement": ch.description, "files": ch.files, "endpoint": endpoint,
>                 "points": ch.value, "extra": {"cid": ch.id}})
>         return out
> 
>     def submitter(self, cid, flag: str) -> str:
>         return self.client.submit(cid, flag)
> 
>     def close(self) -> None:
>         self.client.close()
> 
> ````````````
> 
> 
> ### b59c35f 2026-10-20T22:27:37+03:00 karatinos feat(cli): add 'apex' — the best-of-union working farm prototype
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 41c69c8 2026-10-21T03:43:00+03:00 karatinos feat(recon): surface PNG tEXt/zTXt/iTXt comments to the agent
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 13444a6 2026-10-21T03:44:38+03:00 karatinos feat(recon): list zip/tar archive members in the recon digest
> 
> 
> No new task-progress text file was identified in this commit.
> 
> ## 2026-10-31T11:21:49+00:00 — origin/ctf/cybercup-2077-progress
> 
> 
> ### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### bd8f4b1 2026-10-31T14:20:16+03:00 Your Name Save paused CyberCup-2077 reverse engineering handoff and checkpoints
> 
> 
> File: `reverse/CyberCup-2077/CyberCup-2077.txt`
> 
> ````````````text
> CyberCup 2077
> 1000 points / 1 solvers
> reverse, windows
> Wake up, Samurai. We've got a ctf to slop.
> Flag format: ctfcup{[a-zA-Z0-9_]+}
> 
> cybercup.zip
> 14.6 MiB
> ctfcup{...}
> submit
> 
> ````````````
> 
> 
> File: `reverse/CyberCup-2077/artifact-inventory.json`
> 
> ````````````text
> {
>   "recorded_utc": "2026-10-31T11:19:27.806449+00:00",
>   "files": [
>     {
>       "name": "CyberCup-2077.txt",
>       "bytes": 175,
>       "sha256": "6833ad9395df430fa1963b355c7069b67c6244eca2330848c34a750d73fde14a"
>     },
>     {
>       "name": "check_all_states.log",
>       "bytes": 4188,
>       "sha256": "cbe02ece3f0df6dda10b040424153d34fdb5691899131235f466b200fb33de18"
>     },
>     {
>       "name": "check_cfg.py",
>       "bytes": 902,
>       "sha256": "348dd7601b9d4cb1fd8321ee3ccef2cf5a315b0bbdbdc50cce3fc04e54c9dd48"
>     },
>     {
>       "name": "check_clean.bin",
>       "bytes": 39829504,
>       "sha256": "7e8256ea766a9dc2ea2b6bbd699744af1d266a6f79d4132cbe1c906d744fd03b"
>     },
>     {
>       "name": "check_clean.bin.json",
>       "bytes": 713509,
>       "sha256": "1aa90f4a9114278b80d429b7f682569cba1c965781fd16efb00cb487ca1b6294"
>     },
>     {
>       "name": "check_clean5.log",
>       "bytes": 496,
>       "sha256": "175da6fb8b9fa5dfdd8e98a2cf1625cd125ab62e737ebe0d6b6c2c9989826f0e"
>     },
>     {
>       "name": "check_clean5fast.log",
>       "bytes": 493,
>       "sha256": "bb905ffac75c69721827d79633820caeeba73b296910fdc024a74065321bedd9"
>     },
>     {
>       "name": "check_compare0.asm",
>       "bytes": 67065,
>       "sha256": "8e12d8cd03eb127bbda27da7c85ff150c22e2bbc0372af875d2f034039cabbf9"
>     },
>     {
>       "name": "check_core.asm",
>       "bytes": 28148,
>       "sha256": "379bc5122a71408ce7642ec056ffa576c587e860d15b015eee0287f986774c4e"
>     },
>     {
>       "name": "check_current.bin",
>       "bytes": 39829504,
>       "sha256": "eaf50302d95dcafe8679b34d7df783c74ddaeadd1d59902a587b4ac852defac5"
>     },
>     {
>       "name": "check_current.bin.json",
>       "bytes": 33384,
>       "sha256": "ca21643b5c5602fbb8ae02d7cb6647ae2308263c3a7676411cccc622932538a6"
>     },
>     {
>       "name": "check_current_emu.log",
>       "bytes": 1145,
>       "sha256": "76a57a0636a5b3640e498d767f3faf67b55bec37863453c38c0eb9bd4c9761d3"
>     },
>     {
>       "name": "check_deobf_app.asm",
>       "bytes": 2294905,
>       "sha256": "546b45f1f6bd57a713d78d2f21850a90c4c98f13de07a67867173b57853af297"
>     },
>     {
>       "name": "check_deobf_new.asm",
>       "bytes": 2492548,
>       "sha256": "2c5aa05b5d3f7b3cdd61bdcf48ada0e1fd5235ab5b59fec70b1e2c826cd79d7e"
>     },
>     {
>       "name": "check_deobf_new.bin",
>       "bytes": 39829504,
>       "sha256": "a7021be456a3e450469b26246d01d6e8023353fab778adc65c963d6e9374b73e"
>     },
>     {
>       "name": "check_deobf_new.bin.json",
>       "bytes": 32557,
>       "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
>     },
>     {
>       "name": "check_disasm_2f9584.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_disasm_323d25.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_disasm_5cfdf.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_disasm_67174e.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_final_cfg.asm",
>       "bytes": 30748,
>       "sha256": "4606bc3fd534b5487056e4cbe96281d52ffcce8d1304988553326a8064b94aa4"
>     },
>     {
>       "name": "check_first_cfg.asm",
>       "bytes": 241729,
>       "sha256": "130593d057fdafc2a19037e4bb24f60bf6e074f469e0ff13106a1984c98e6e03"
>     },
>     {
>       "name": "check_hypercall.py",
>       "bytes": 5111,
>       "sha256": "3f94fc34f174544ecb725f90bcb68b930e212c10ed52fb0d5c690a250a0ee44e"
>     },
>     {
>       "name": "check_last.asm",
>       "bytes": 101680,
>       "sha256": "c6a6504ae4b53c9b097f867345cbcf46ebd07045df6e01d78f5a7c9b4f418757"
>     },
>     {
>       "name": "check_linear_161345b.asm",
>       "bytes": 1408,
>       "sha256": "ee63ee4b4c96e4676a44a4d6a87fa305543e36215f010ba4ee8992e24ae981cd"
>     },
>     {
>       "name": "check_linear_16157fb.asm",
>       "bytes": 10408,
>       "sha256": "69001146527a86b41e39ce57fe41360d549254d3b5ed408485c4928b82a91369"
>     },
>     {
>       "name": "check_linear_1617753.asm",
>       "bytes": 2703,
>       "sha256": "08c502a510e788ad9adbc2fa1ea286336617412b07bf9a3ad42dbd6da966caa3"
>     },
>     {
>       "name": "check_luts.py",
>       "bytes": 1641,
>       "sha256": "0d579183bba7c7fdefa9c8802d3c97d06fa86321c5306b1ef0c1fbb27e7b4637"
>     },
>     {
>       "name": "check_main_loop.asm",
>       "bytes": 12031,
>       "sha256": "3cd50a5542ff8b2c72d8e4e8d992983f8abf75136cc76fdcc3584c56a9507e2b"
>     },
>     {
>       "name": "check_near_16155ff.asm",
>       "bytes": 1625,
>       "sha256": "a4547d9636a6d32fd2df2a5663c7fe9d243df5792f5d2f681429bdac12018cc9"
>     },
>     {
>       "name": "check_near_5c000.asm",
>       "bytes": 25705,
>       "sha256": "ac7137341b93df8c9ada269358c5f18041e5f1b87cb977dddea86d204419bba7"
>     },
>     {
>       "name": "check_real_601e80.asm",
>       "bytes": 88,
>       "sha256": "f14af9bb08a4be18734c3dcaa5c992c0a4697cf14b3e06a359cee6058be928bf"
>     },
>     {
>       "name": "check_real_6987c0.asm",
>       "bytes": 263,
>       "sha256": "4f097ddfa3cdf441670cd5704ea62eb6d9211ce907e2cec75162d950b47cd9a9"
>     },
>     {
>       "name": "check_real_698930.asm",
>       "bytes": 603,
>       "sha256": "fbe8e0de0b169bcc246f3b4d459589f8c1de466a194b0c11ea1303cb077b119d"
>     },
>     {
>       "name": "check_real_6989ca.asm",
>       "bytes": 10811,
>       "sha256": "c4306627589b7bed09f2aaae584eb032e55bf13abb8098f20550d9fe15f2616b"
>     },
>     {
>       "name": "check_real_698e00.asm",
>       "bytes": 3252,
>       "sha256": "f16fa46c07e993832cc9c1211f7199d0c95bb460d95bbdf865e12a29f4681687"
>     },
>     {
>       "name": "check_scan_tables.py",
>       "bytes": 2096,
>       "sha256": "bb84f4406d571299acba552b0753d4e24cf7917b91f00b3172beba27bcb9eb2a"
>     },
>     {
>       "name": "check_solve_block.py",
>       "bytes": 740,
>       "sha256": "70bbf0d9232706231b8c4da1166965a8af55ff36af8450d0ee89521be92a20ec"
>     },
>     {
>       "name": "check_solve_clean.log",
>       "bytes": 32,
>       "sha256": "ef051b00f2aa83132e7f623779f5124b4c601ba27e79935c35d898b26ebf6a07"
>     },
>     {
>       "name": "check_solve_prefix.log",
>       "bytes": 40,
>       "sha256": "b928ba555d19b2f0d1712e5889c877bdc833c8295928cb96a097f8899308e2f6"
>     },
>     {
>       "name": "check_solve_test.log",
>       "bytes": 32,
>       "sha256": "7526eaf3d62026db79020d01eb1f24d7ce49093298c270b6d3caf03141c62574"
>     },
>     {
>       "name": "check_split_states.py",
>       "bytes": 1000,
>       "sha256": "a1a92218f5349e14a0f0887554db0dad493b7c00393fe10f498d2400f77442bd"
>     },
>     {
>       "name": "check_stage_601e80.asm",
>       "bytes": 10173,
>       "sha256": "adb5cf3ca8e21e4382e4f4664b71985cc375953ac53abb19967b5e4dbe6125d4"
>     },
>     {
>       "name": "check_stage_697d50.asm",
>       "bytes": 27762,
>       "sha256": "1de3f235e265d01b5dad20cc500cee827c5470ef4c29e44da32d48dce1ae048a"
>     },
>     {
>       "name": "check_stage_map.json",
>       "bytes": 8221,
>       "sha256": "d1b27c5f626437efa71423e46c7c7eafb3400b631233080b6579b79371578650"
>     },
>     {
>       "name": "check_stage_map.log",
>       "bytes": 5615,
>       "sha256": "f5ba7c9d88bf158557cdfc56ec0a4f287a9b75716dede8316c21af2a326eed23"
>     },
>     {
>       "name": "check_stage_map.py",
>       "bytes": 1024,
>       "sha256": "ab34bc873cbe3839139e5e3ca70fe3d138090522c8291291696ff59a3db49712"
>     },
>     {
>       "name": "check_state.smt2",
>       "bytes": 194994,
>       "sha256": "174b6c3c342dbcea3acc27f681bae8775acd39592d15b0c883fe7e7c61123d13"
>     },
>     {
>       "name": "check_stripped_161345b.asm",
>       "bytes": 4846,
>       "sha256": "7a63d7f96e49fe4fbd0547a5d6c487e2a6b420ff3638a35d991cd5c9b5c9ddec"
>     },
>     {
>       "name": "check_stripped_1614b34.asm",
>       "bytes": 4133,
>       "sha256": "c602444d53c3fd195609f46f7664669ad2e2e37f83bc1974bf4d3c4c478b6324"
>     },
>     {
>       "name": "check_symbolic.log",
>       "bytes": 278,
>       "sha256": "d347d9c6802b6c18d4a7388ef82391c8f7a6edb89116dfcbd2599dcc43a98ccf"
>     },
>     {
>       "name": "check_symbolic.py",
>       "bytes": 12781,
>       "sha256": "b16a36b55efeecea06e3ebdbc76a021730cc18a55401e3f7cc38ba6bca76dd84"
>     },
>     {
>       "name": "check_symbolic5.log",
>       "bytes": 495,
>       "sha256": "f12af3a180a174eb3f2e4f0dc786517cd7a4fcf82d8ac25e28958862b92d4389"
>     },
>     {
>       "name": "check_symbolic5final.log",
>       "bytes": 494,
>       "sha256": "a34542cd7f826ea5a9d362bdc1c8b3fe97af1d888206826a80a8157e1cc19669"
>     },
>     {
>       "name": "check_tables.json",
>       "bytes": 1870,
>       "sha256": "99f7bc78b72ede31fc04eebf8264b8ae2c130d4da9ba35c703810c60e8303872"
>     },
>     {
>       "name": "check_target_masked.log",
>       "bytes": 32,
>       "sha256": "41fca72610ac7359c6b1fcab57133ba32a81d998f0fad32609ed228826c9d9b9"
>     },
>     {
>       "name": "check_target_xor.log",
>       "bytes": 31,
>       "sha256": "18bfa814571255c2beb1850e1681423a830c8f656d504a02a7f20e4d59fac7c9"
>     },
>     {
>       "name": "check_unmutate.py",
>       "bytes": 2770,
>       "sha256": "17fd03f4dc1f2c658e97a1640ddf17a4b4f166e543e4166f9558fb5e26beba6f"
>     },
>     {
>       "name": "check_validate.py",
>       "bytes": 1373,
>       "sha256": "ffdfafa9237e159b91ca2a0c95cfc775c57d9979e5e298760cd902650b541f28"
>     },
>     {
>       "name": "check_workspace.smt2",
>       "bytes": 4768554,
>       "sha256": "02b5b42c92dc268c4e55c218a2d9d053079c73caaa8825229c1ba57870af5677"
>     },
>     {
>       "name": "checker_ctor.log",
>       "bytes": 1168,
>       "sha256": "a878b4ff262d96a010725960f91b4e57a4a2c954e885e3d739ac0e3d815eeac9"
>     },
>     {
>       "name": "checker_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "bec95566c24d60104998b226c6904a86280a2da674d55c2661fadd1fd27ddc9b"
>     },
>     {
>       "name": "checker_deobf.bin.json",
>       "bytes": 32557,
>       "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
>     },
>     {
>       "name": "checker_emu.log",
>       "bytes": 938,
>       "sha256": "815d5d89c598ca77b007cec5f94b4edeae2c3cada08015d82c46fc064fe64d40"
>     },
>     {
>       "name": "checker_emu.py",
>       "bytes": 4854,
>       "sha256": "8227ba58596f2c4ffb7f5ef40c5e3d665924c41025ea4ed269f686eabbeadcff"
>     },
>     {
>       "name": "checker_events.json",
>       "bytes": 174,
>       "sha256": "57de42e43328c36b2683ae23e4eeeaed41a3b0d941739e60f26c4d85ca256d76"
>     },
>     {
>       "name": "checker_final.bin",
>       "bytes": 39829504,
>       "sha256": "7e7048719fc3b7e327872adae4308328b3cb4f03104a5a7f4c2fc8d65ea9790a"
>     },
>     {
>       "name": "checker_final.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "checker_final.log",
>       "bytes": 608,
>       "sha256": "c6af520e61bb86107a318fa49dfa2e7a97ac62f27f6658830360cbf36c9a697e"
>     },
>     {
>       "name": "checker_full.log",
>       "bytes": 846,
>       "sha256": "a855eaf4c37041be68919dbcf459b78951215bae1d142e8cdc99688a467d7150"
>     },
>     {
>       "name": "checker_init.log",
>       "bytes": 608,
>       "sha256": "c1b1d743118157c010630dacceb6913ffd903ae198ace3b21a1f80f2bc9fc966"
>     },
>     {
>       "name": "checker_native.asm",
>       "bytes": 900,
>       "sha256": "60baebac6b813b156ea3bbaf733fb516988cc571afb696cccb12b03a974f4658"
>     },
>     {
>       "name": "checker_ready.bin",
>       "bytes": 39829504,
>       "sha256": "8368809cd18b3358f5209ba07fb1c143564209ee96c12a5599f320b8ce9e5fed"
>     },
>     {
>       "name": "checker_ready.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "checker_ready.log",
>       "bytes": 521,
>       "sha256": "25783acbce131fc552d8e358e0050ea96e9eb8c4c776415a65cc80231acaa4bd"
>     },
>     {
>       "name": "checker_ready2.log",
>       "bytes": 520,
>       "sha256": "1ab9a9e431554ae9294a57a9804f3680487c75516450c7d59372bc04cf3faace"
>     },
>     {
>       "name": "checker_ready3.log",
>       "bytes": 616,
>       "sha256": "28ea56ba27c7d316e917a64a1c34a5d9f36ce6fb388dabd1af70c03eaa468b64"
>     },
>     {
>       "name": "checker_traps.json",
>       "bytes": 2,
>       "sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
>     },
>     {
>       "name": "cybercup.exe",
>       "bytes": 16291840,
>       "sha256": "7482217acb62ed2329b3386e404b7e798a3d4c1c0d69d7c1e84e7e72b8088f84"
>     },
>     {
>       "name": "cybercup.sys",
>       "bytes": 27024,
>       "sha256": "9e73a1beb71ec4171450caeb059be48c452c6633da7990566dd8eb8f6d5405ac"
>     },
>     {
>       "name": "cybercup.zip",
>       "bytes": 15319725,
>       "sha256": "056d94d8e7e5b119caf800219a056a20d19691b15e78cb0e8de4d1b8407a1213"
>     },
>     {
>       "name": "driver_analysis.asm",
>       "bytes": 348736,
>       "sha256": "a824fafc994a1d6e469ac328c50a9da34c6784b03b542ca56ec98b38c6fad1db"
>     },
>     {
>       "name": "driver_analysis_arm.py",
>       "bytes": 2397,
>       "sha256": "05b4c8cb176c53adb21b9b6848da8cadbc43f2584b208e9e3877bff185553530"
>     },
>     {
>       "name": "driver_analysis_constructor.log",
>       "bytes": 859,
>       "sha256": "1398b018b8605cb9db80ed667e1a53f45e161684497b4f6a2ff620d04aa7f43a"
>     },
>     {
>       "name": "driver_analysis_constructor.py",
>       "bytes": 5435,
>       "sha256": "77cf24ac02699efa592fe79d78a29128972b7fb81160f57011bcb93899aefbc2"
>     },
>     {
>       "name": "driver_analysis_cpuid_validate.py",
>       "bytes": 1150,
>       "sha256": "c84ac0ce7fda5eaf37faecf9317c7754ea842e2c5469b5c7559ecdcc2a650c11"
>     },
>     {
>       "name": "driver_analysis_crt.log",
>       "bytes": 1890,
>       "sha256": "857e7fa2420acc8c16e5f4539957c074ed47cbf56c4c66fe1fb066fb9fb7c5d9"
>     },
>     {
>       "name": "driver_analysis_crt.py",
>       "bytes": 6699,
>       "sha256": "f9b1a863b85b059f9ce5631b47e16e01e90481e753b84cecccafbb8d50c2e691"
>     },
>     {
>       "name": "driver_analysis_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "233ed4d8e4b35b139f84ef550420ab4b1cc277ce3d1d3513c0a05bdc5540688c"
>     },
>     {
>       "name": "driver_analysis_deobf.bin.json",
>       "bytes": 32557,
>       "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
>     },
>     {
>       "name": "driver_analysis_deobf.py",
>       "bytes": 3902,
>       "sha256": "c807fb69d4fdb105601072f31ba0f3dbe73088dcf0003c9d6537c6cbe3633dfa"
>     },
>     {
>       "name": "driver_analysis_final_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "7e7048719fc3b7e327872adae4308328b3cb4f03104a5a7f4c2fc8d65ea9790a"
>     },
>     {
>       "name": "driver_analysis_final_deobf.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "driver_analysis_final_thunks.bin",
>       "bytes": 39829504,
>       "sha256": "26736169780d6e8776ce204aa858dd80f06ba69a29e5efff253c94912107f7cb"
>     },
>     {
>       "name": "driver_analysis_final_thunks.bin.json",
>       "bytes": 4894,
>       "sha256": "dd219bd3ffe2ae3e022851596e898ea6b331131928b97031947eb4e68b20395c"
>     },
>     {
>       "name": "driver_analysis_final_thunks.log",
>       "bytes": 4239,
>       "sha256": "3f4cbdd5d0ed4c1356b1a3ed7570244553cebfb6cdf77a35b2ece1e3994a957e"
>     },
>     {
>       "name": "driver_analysis_headers.txt",
>       "bytes": 3961,
>       "sha256": "8f7e0abbdd4cf0ad011a0900a32e0370cb8391621afe30fba206e8060734c21a"
>     },
>     {
>       "name": "driver_analysis_hv.py",
>       "bytes": 7928,
>       "sha256": "b1a52b47f290639d20cd8a38cad5f91d53cd8438611a934fa767e2cd8366257f"
>     },
>     {
>       "name": "driver_analysis_hv_validate.py",
>       "bytes": 1448,
>       "sha256": "65fce350341590925de824c09a38df5ac47ce1c817e2c199101efa015f1cdb69"
>     },
>     {
>       "name": "driver_analysis_init.log",
>       "bytes": 1051,
>       "sha256": "1ca910ee4464e80aa2755b8402ea22995f03be6c7d37f72a0c29ed7c90e04cdc"
>     },
>     {
>       "name": "driver_analysis_init.py",
>       "bytes": 3882,
>       "sha256": "6a3dc78ba15f8659577d6984b2bed438a4155287373d7ac064a2b9b302b989ab"
>     },
>     {
>       "name": "driver_analysis_initialized_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "8368809cd18b3358f5209ba07fb1c143564209ee96c12a5599f320b8ce9e5fed"
>     },
>     {
>       "name": "driver_analysis_initialized_deobf.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "driver_analysis_initialized_pid0.bin",
>       "bytes": 39829504,
>       "sha256": "4eb93b21e4b53d29e8f2393e69aa7cbf8486a307a583bdd7510c93947b97bc67"
>     },
>     {
>       "name": "driver_analysis_initialized_pid0.bin.json",
>       "bytes": 4901,
>       "sha256": "eb1abb84f8ca950f07829b0ba861dcd2e0e8684e7be949a40d77ff862f81f5e1"
>     },
>     {
>       "name": "driver_analysis_initialized_thunks.bin",
>       "bytes": 39829504,
>       "sha256": "554d2b254979fd9d26a807c2be9a817d4c7076ae9ac35bee18aa6b6303deb837"
>     },
>     {
>       "name": "driver_analysis_initialized_thunks.bin.json",
>       "bytes": 4894,
>       "sha256": "dd219bd3ffe2ae3e022851596e898ea6b331131928b97031947eb4e68b20395c"
>     },
>     {
>       "name": "driver_analysis_initialized_thunks.log",
>       "bytes": 4245,
>       "sha256": "3bdb3de5005c2ff93aa690f9eb58f5a5f156ccc556168c1e2044cc4ed083f2d0"
>     },
>     {
>       "name": "driver_analysis_latest_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "e9ea4aff0895c5b6d801ca2fd2c6514622a519e988700a1e4ddd0e81901dff35"
>     },
>     {
>       "name": "driver_analysis_latest_deobf.bin.json",
>       "bytes": 33257,
>       "sha256": "612c1d43a5822eb52d592adb54a8f976843fd4e5dcf4cdd3a604a75cb4045bae"
>     },
>     {
>       "name": "driver_analysis_pid0.log",
>       "bytes": 4253,
>       "sha256": "063f9590498fa89478f78d493725b57bf6cae688ff7710e5fce8ebd0dfb68d22"
>     },
>     {
>       "name": "driver_analysis_ready.log",
>       "bytes": 693,
>       "sha256": "a0b5bc53420825d4afebeeab048440668413367888fb0f9be271a453451ed3ab"
>     },
>     {
>       "name": "driver_analysis_ready.py",
>       "bytes": 5697,
>       "sha256": "36beff3a649cf8eabe65b6469467fc4d8d9cd7783fe51f90800c5acab58daabd"
>     },
>     {
>       "name": "driver_analysis_slice.log",
>       "bytes": 5053488,
>       "sha256": "c2c91a331ca4815a9084a6af06b70142e4d4aa0fd83d34dd3fb6c7ac675569ba"
>     },
>     {
>       "name": "driver_analysis_slice.py",
>       "bytes": 1783,
>       "sha256": "8b956dc9fa262fb8ca5ecf1c1e9b588498d61c4c0f447be9f0801db7d2d7db68"
>     },
>     {
>       "name": "driver_analysis_symbolic.log",
>       "bytes": 26,
>       "sha256": "6d6e30e4db46b36021fa16ccb8d73880794bd9380eb184163455670e678f4731"
>     },
>     {
>       "name": "driver_analysis_symbolic.py",
>       "bytes": 7444,
>       "sha256": "7632f055f00645cb240bae33bc68c1a0aef141a9f3fc4ddf0ffd0965ca3588c1"
>     },
>     {
>       "name": "driver_analysis_thunks.bin",
>       "bytes": 39829504,
>       "sha256": "0a40c2707d5e640d945b60859cd4387c16fe72834c8a51a5f4358c54c88acaa9"
>     },
>     {
>       "name": "driver_analysis_thunks.bin.json",
>       "bytes": 5234,
>       "sha256": "0e7d6881d6984541b20a0ad5a04f6047ea48a1e6d4411ee460f00d0d2fd31421"
>     },
>     {
>       "name": "driver_analysis_thunks.log",
>       "bytes": 4648,
>       "sha256": "2852e313d9b0812d7cf0cf4f86c95716ca0d6288730ebb5338ffd4f53823c18d"
>     },
>     {
>       "name": "driver_analysis_thunks.py",
>       "bytes": 3804,
>       "sha256": "ea9c1ee19210e0bdc5377cc9135fc959443c7940797a29b7d213709314530b1b"
>     },
>     {
>       "name": "driver_analysis_trace.log",
>       "bytes": 916,
>       "sha256": "e241c5a7394a0a62acd69c7095830c40d1beaa632a6e75452c6f19f03b9c701c"
>     },
>     {
>       "name": "driver_analysis_trace.pkl",
>       "bytes": 11591251,
>       "sha256": "321e4bde19404f1c681f757ec4bc476fb853958fd7ce55f8cf1bc70998743915"
>     },
>     {
>       "name": "driver_analysis_trace.py",
>       "bytes": 1280,
>       "sha256": "6a8f5a8f4785b52c56ede8b42c9890aec768f3e456e4e5687730671f3f128dbe"
>     },
>     {
>       "name": "driver_analysis_traps.pkl",
>       "bytes": 5,
>       "sha256": "bfce13fc2f13ad950016bb48ccbbbd04ce13be07c748476dde1f940fcdfa0d52"
>     },
>     {
>       "name": "driver_analysis_update.log",
>       "bytes": 55,
>       "sha256": "283067d9a77e0402e56634d247a314efacf38ed1b38dc22433b7f841e500beb6"
>     },
>     {
>       "name": "driver_analysis_update.py",
>       "bytes": 7447,
>       "sha256": "004fa9a832b1a9814fb4c8b2e3e22fc548ebac0da38239a022bb4f96a75cc7e8"
>     },
>     {
>       "name": "driver_analysis_validate.py",
>       "bytes": 1537,
>       "sha256": "3e3a888b2823ea02634ff1fa1f50e187fe8f004ab19c61ec322d791ae26c3f49"
>     },
>     {
>       "name": "imports.txt",
>       "bytes": 3774,
>       "sha256": "f0ab44b024956f2a0c484a31db56fee3545b3f882ec71edaab278f96b7b1aa32"
>     },
>     {
>       "name": "infer_cipher.py",
>       "bytes": 1102,
>       "sha256": "91ddea2880bfeba4dab23f6cf4b9c63e42bcb6fdcc1c2be9db33e01878a75c35"
>     },
>     {
>       "name": "lut_all_rows.json",
>       "bytes": 60574,
>       "sha256": "5f82cde1ea6d9c0e1d2b7f1811bc3900eef8bb4308c966a04f099cae5499fffd"
>     },
>     {
>       "name": "lut_catalog.json",
>       "bytes": 1441,
>       "sha256": "3533934a38c65b828eb20aa8dbb8ac2a1ffeeb5af71d62174e76d6eebeebc23d"
>     },
>     {
>       "name": "lut_catalog.py",
>       "bytes": 1281,
>       "sha256": "08ac2130d81daa383eefe3b5bc1a2c08fe4347eb3b8cb885746ddb1f37076f59"
>     },
>     {
>       "name": "lzma-first.bin",
>       "bytes": 7220736,
>       "sha256": "024b4e2c161f1e24ca8fee6cb96c694e066eea275422fc62657636775dfcf84e"
>     },
>     {
>       "name": "lzma.asm",
>       "bytes": 36274,
>       "sha256": "cea48c477414722fddb3a296fe2262d63e295215b707bb79a14a726dfac72590"
>     },
>     {
>       "name": "native.asm",
>       "bytes": 137,
>       "sha256": "1fc850bc5ae07d831e3fda2e56606047d885b7861fc6461bdd85f40884948949"
>     },
>     {
>       "name": "packer-api-names.json",
>       "bytes": 4273,
>       "sha256": "a807ba670f64555f4545e2bddcb82710c6378d6f6d485a87c29cf2ce6d3e3da5"
>     },
>     {
>       "name": "probe_first_block.json",
>       "bytes": 1701,
>       "sha256": "4fdf7727c7353f1cabdc39fdc68319742ee82dc20127a5ae9772fefd1d4e06dc"
>     },
>     {
>       "name": "probe_first_block.log",
>       "bytes": 1346,
>       "sha256": "93ccccc815b8f8549914dc5925459e6975f466f402065a462b90fbde4184255f"
>     },
>     {
>       "name": "probe_first_block.py",
>       "bytes": 1038,
>       "sha256": "c03ed46813bccb696f76b04159bcf28aaf6c361caeaee91db142ca9376d38ed5"
>     },
>     {
>       "name": "progress-summary.md",
>       "bytes": 26324,
>       "sha256": "1006094ff2ce6b4475b0e8a5e7cf11142a2d7da82f5bbcf8fd07fe054fba5e1a"
>     },
>     {
>       "name": "strings.txt",
>       "bytes": 178,
>       "sha256": "daa23f9619f813ce48a76233187160b64092490385c8f343e26ee845a4640652"
>     },
>     {
>       "name": "unpack_block_query.log",
>       "bytes": 314,
>       "sha256": "6b742bdcab2408eff18e2d0b844bf10fb95efa841f6cbe148a39c5b2f2249340"
>     },
>     {
>       "name": "unpack_block_query.py",
>       "bytes": 1667,
>       "sha256": "8582863745cd4973ae4b88a3acca557e99bab694436ecc1452d0ed017fa2d26b"
>     },
>     {
>       "name": "unpack_decomp_state.pkl.gz",
>       "bytes": 15512129,
>       "sha256": "d476182abb97b8eaee222dc28d81f5afb6e78d3fcf47215a64d94b70388ce65e"
>     },
>     {
>       "name": "unpack_decompressed.bin",
>       "bytes": 39829504,
>       "sha256": "9cd40703f2553150307fd8ea3d70f63d11083b1a3542fb920721326b78759ae6"
>     },
>     {
>       "name": "unpack_emu.log",
>       "bytes": 2495,
>       "sha256": "80eaa04f30330f2840c832aa0cb3db3791fddfdd7b0972daf39ac012e4bdbd96"
>     },
>     {
>       "name": "unpack_emu.py",
>       "bytes": 8779,
>       "sha256": "e883a81ce54442a3f63c5d4bc9c8a95e36ddcb7fada411279e4760c5741221c4"
>     },
>     {
>       "name": "unpack_entry.log",
>       "bytes": 21924,
>       "sha256": "64d5da9b308bd91903aea067a9eb75acdd599fef85557d46e4626b862a5f8541"
>     },
>     {
>       "name": "unpack_entry.py",
>       "bytes": 9293,
>       "sha256": "b29a1d6ca2827d3b4695ec9ab3f86af208537ee744435b3d04120da0cc02639c"
>     },
>     {
>       "name": "unpack_final.bin",
>       "bytes": 39829504,
>       "sha256": "16b69810baf22d1f7ee04aea2a58552d6d0b76593cf3a5f18aa51bef57cdbd35"
>     },
>     

[Note excerpt limited to 30,000 characters.]

Remote note "progress/iso-codex/PROGRESS.md" (quoted data):

> # Iso — detailed progress and resumption handoff
> 
> **Status: UNSOLVED. No verified flag has been recovered. The user resumed solving on 2026-10-31 after the checkpoint below. Ten-minute GitHub synchronization remains enabled.**
> 
> This is a progress report, not a successful writeup. `writeup.md` has deliberately not been created: the original request made it conditional on recovering a correct flag. Do not mistake dummy strings in self-tests for the challenge flag.
> 
> ## Task and files
> 
> The actual challenge directory is `/Users/karatinos/Downloads/Staff/fsp/crypto/Iso`. The originally requested `reverse/Iso` path does not exist. The parent workspace is `/Users/karatinos/Downloads/Staff/fsp`.
> 
> The statement, `Iso.txt`, says:
> 
> > Iso — 964 points / 4 solvers — crypto
> >
> > Instinct only goes so far, skill covers the rest.
> 
> The attachment is `iso.tar.gz`. Its extracted substantive files are `iso/iso.sage` and `iso/output.txt`. The generator is:
> 
> ```python
> #!/usr/bin/env sage
> with open('flag.txt', 'rb') as file:
>     flag = file.read().strip()
>     assert len(flag) == 27
> 
> p = next_prime(getrandbits(128))
> E = EllipticCurve(GF(p), j = int.from_bytes(flag, 'little'))
> 
> for _ in range(64):
>     E = choice(E.isogenies_prime_degree(2)).codomain()
> 
> print(x^3 + E.a4().lift_centered() * x + E.a6().lift_centered())
> ```
> 
> The complete output is:
> 
> ```text
> x^3 + 6079433314242371108270239373533376748*x - 1779744368654530162000920720207404089
> ```
> 
> Throughout this report:
> 
> ```text
> A = 6079433314242371108270239373533376748
> B = -1779744368654530162000920720207404089
> ```
> 
> The expected flag is `ctfcup{` followed by 19 unknown bytes and a final `}`. The source enforces 27 bytes, but does not itself enforce printable text; printability is a reasonable flag-recovery assumption.
> 
> Because the printed coefficients are centered representatives, the hidden prime satisfies `p > 2*A`. Since it is the next prime above a 128-bit random integer, its upper bound is essentially `2^128` (allow a tiny next-prime overshoot). Consequently a relevant factor has roughly 124–128 bits, or 38–39 decimal digits. Small factors found below are not candidates for the field prime.
> 
> Archive inspection found macOS AppleDouble/PAX metadata but no additional challenge secret. The metadata mentions author username `keltecc`. Source and output modification timestamps were `1792610198.084473776` and `1792610200.689522431`. They do not reveal the RNG seed.
> 
> ## Established mathematical attack
> 
> ### Sage's starting model
> 
> For generic `j` in a field of characteristic other than 2 or 3, Sage constructs:
> 
> ```text
> k  = j - 1728
> a0 = -3*j*k
> b0 = -2*j*k^2
> ```
> 
> The input integer is coerced into `GF(p)` before this construction. The special cases `j=0` and `j=1728` use other models; the attack below assumes the generic case. Such special values are overwhelmingly unlikely for an independently sampled prime and ordinary flag, but have not been ruled out by a recovered prime.
> 
> The formula was checked against Sage source and actual Sage executions. The constructor's rational-field minimal-twist behavior does not apply to this finite-field call.
> 
> If a model is scaled to `a=u^4*a0`, `b=u^6*b0`, put `s=u^2`. It obeys:
> 
> ```text
> F0(a,b,s) = 4*a^3 + 27*b^2 + 31104*s*a*b = 0  (mod p).
> ```
> 
> **31104 is the correct constant. An early exploratory attempt used 10368; that was corrected. Do not revive that incorrect relation.**
> 
> ### Normalized degree-two isogenies and backtracking
> 
> For a rational kernel point `(r,0)`, where `r^3+a*r+b=0`, the normalized degree-two quotient has:
> 
> ```text
> a' = -4*a - 15*r^2
> b' = 22*b + 14*a*r
> ```
> 
> The normalized dual has kernel root `-2*r`. A quotient followed by its normalized dual sends `(a,b)` to `(16*a,64*b)`.
> 
> Deleting consecutive dual pairs from a 64-step walk leaves an even reduced length `d`. Starting at the observed output and taking the `d` dual steps back reaches a model with:
> 
> ```text
> a = -3*j*(j-1728)   * 2^(128 + 2*d)
> b = -2*j*(j-1728)^2 * 2^(192 + 3*d)
> s = 2^(64+d).
> ```
> 
> These powers are important: at `d=2`, use `s=2^66`, not `2^64`.
> 
> Ordinary 2-isogeny graphs often cause extensive backtracking. A small simulation of randomly generated instances found many reduced lengths zero, several two, and occasional four or larger. This motivates trying `d=0,2,4,6`; it does not prove that the real instance has any particular reduced length. A simulated walk also reached length 10, so a longer real path remains possible.
> 
> `analysis/validate_walk.sage` directly generated Sage curves and 64-step walks, reduced paths by comparing j-invariants, and verified the derived relations modulo the generated primes. Tests included the zero-, two-, and four-step relations. They passed.
> 
> ### Norm recurrence
> 
> `analysis/walk_relations.py` uses python-flint multivariate polynomials in `(r,A,B,s)`, lexicographic order. It starts from `H0=F0`.
> 
> For a polynomial `H`, substitute the quotient coefficients and reduce modulo `r^3+A*r+B`, obtaining `q=c0+c1*r+c2*r^2`. Its norm is:
> 
> ```text
> c0^3 - 2*A*c0^2*c2 + A^2*c0*c2^2 + A*c0*c1^2
> + 3*B*c0*c1*c2 + B^2*c2^3 - B*c1^3 - A*B*c1*c2^2.
> ```
> 
> This enumerates the three possible first degree-two isogenies algebraically. To remove backtracking when constructing `H2`, divide by the primitive part of `H0(16*A,64*B,s)^3`. When constructing `H_(d+1)` for `d>=2`, divide by the primitive part of `H_(d-1)(16*A,64*B,s)^2`. Normalize the resulting polynomial to primitive coefficients and positive leading coefficient.
> 
> The hidden prime must divide:
> 
> ```text
> N_d = abs(H_d(A,B,2^(64+d)))
> ```
> 
> if `d` is the actual reduced path length. The recurrence generated `H1.json` through `H6.json` and `primitive_n1.txt` through `primitive_n6.txt`. Sizes are:
> 
> - `H1`: 13 terms; evaluated integer 346 decimal digits.
> - `H2`: 42 terms; 710 digits.
> - `H3`: 149 terms; 1,441 digits.
> - `H4`: 561 terms; 2,924 digits.
> - `H5`: 2,177 terms; 5,934 digits.
> - `H6`: 8,577 terms; 12,039 digits.
> 
> Generation through degree six took a few minutes; the final stage alone took about 248 seconds in the first run. `H6.json` is about 9 MB locally. The Git snapshot can omit that large generated file because the generation script and evaluated integers are retained.
> 
> The two-step result was also derived independently with SymPy resultants in `analysis/resultant.py`. That older script's `n2.txt` includes an extra constant factor `2^36`; prefer `primitive_n2.txt`. Re-evaluation of `H2.json` at the published A, B and `s=2^66` exactly reproduced the saved primitive integer. The current cofactor was separately checked against that integer and all removed factors.
> 
> Factoring the symbolic `H2` over the integers, and again after substituting `s=2^66`, returned a single irreducible factor. There was no easy rational polynomial factorization that reduced the integer-factorization problem.
> 
> ## Factoring results and exact checkpoint
> 
> ### Reduced length zero is ruled out under the generic-model assumption
> 
> The integer
> 
> ```text
> 4*A^3 + 27*B^2 + 31104*2^64*A*B
> ```
> 
> has complete factorization:
> 
> ```text
> 3^6
> * 2756099
> * 38647261059053
> * 849730274370727147067
> * 13621568982086690577957595834791154260655747086184118105900367481087
> ```
> 
> The last factor is prime and has 224 bits. None is in the required 124–128-bit interval. The 224-bit factor was additionally tried as an out-of-range diagnostic: its recovered j-value does not decode to a flag and it contradicts the generator's prime size.
> 
> Several alternative scaling exponents were queried as diagnostics in `other_scalings.json`. They did not produce a solution and are not substitutes for the correctly derived exponent 64.
> 
> ### Reduced length two: current primary candidate
> 
> The complete removed factor is:
> 
> ```text
> 3^36
> * 4517
> * 43385229945689
> * 200573683479693692659464438760837
> * 2260875122210404084952664589
> ```
> 
> The last three factors were found with GMP-ECM. They have 14, 33 and 28 decimal digits, respectively, and are too small to be p.
> 
> The remaining **616-digit composite** is saved in `analysis/n2_current.txt`:
> 
> ```text
> 1457506062875932817869177975145756628778829486130694151675619410000045233025452318197087491186659039504564609855820125742244854384953937587718871938163914748886160827115674300836373948031539315693609126200833021512260426564405247620393241717756612569519174506217307654295046339196604177967426998112643020893194149880926399070708798100193542243954578877626636216188267061594182902222212311125262838762245222060004758747396821275609416435361794797593067428291811253805770902740232478897198198644156741483763383085132396412471374750529542481663134137726652394951656939253795325420794562139234602187068800874902822025171
> ```
> 
> Verified exactly:
> 
> ```text
> primitive_n2 = n2_current * 3^36 * 4517
>               * 43385229945689
>               * 200573683479693692659464438760837
>               * 2260875122210404084952664589.
> ```
> 
> Intermediate files preserve earlier checkpoints:
> 
> - `cofactor2.txt` / `n2_cofactor.txt`: 689 digits, after removing `3^36*4517`.
> - `n2_work.txt`: 675 digits, after also removing the 14-digit factor.
> - `n2_next.txt`: 643 digits, after also removing the 33-digit factor.
> - `n2_current.txt`: 616 digits, after also removing the 28-digit factor.
> 
> FactorDB queries did not supply a target-sized factor. The latest query of the 616-digit cofactor returned status `C`. The JSON responses are saved locally.
> 
> ### Reduced lengths four and six
> 
> - `cofactor4.txt` is the 2,855-digit cofactor after removing `3^144` from the four-step relation. FactorDB additionally identified `212923`; check divisibility before removing it from the saved file, which was not necessarily updated with that factor.
> - `cofactor6.txt` is the 11,764-digit cofactor after removing `3^576` from the six-step relation.
> 
> Neither has been factored sufficiently to test a field prime. No evidence proves that the real prime divides the two-step candidate rather than one of these or a longer-path relation.
> 
> ### ECM and p±1 work performed
> 
> Initial ECM used a Debian ARM container with GMP-ECM 7.0.6. Runs included about 80 curves at B1=250,000 on an earlier cofactor, plus runs at B1=1,000,000. The saved `ecm_work.log`, `ecm_big.log`, `ecm_next_1.log`, and `ecm_next_2.log` record the actual work and factors.
> 
> A four-process container run on the 616-digit cofactor used two workers at B1=1,000,000 and two at B1=3,000,000. It found no additional factor before being replaced by a native build.
> 
> Homebrew GMP-ECM 7.0.7 was then installed and used natively, with `OMP_NUM_THREADS=1` per process. `factor_native.py` ran three B1=1,000,000 workers and one B1=3,000,000 worker. Typical stage-one times ranged from about 24 to 40 seconds for B1=1,000,000 as CPU load changed. The run was stopped at the user's request without finding another factor. Consult `factor_native.log` for exact completed curves; an interrupted curve is not a completed test.
> 
> `residues_0.txt` through `residues_3.txt` save completed stage-one residues. They can potentially be resumed with a larger second-stage bound. These files are valuable: restarting the script otherwise selects new curves and does not automatically continue the saved residues.
> 
> A larger native Pollard p-1 run used B1=30,000,000 and requested B2=300,000,000,000; GMP-ECM selected B2=364,641,377,340. It completed without a factor. The log and residue are `pm1_native.log` and `pm1_native.residue`. Earlier smaller p-1 and p+1 attempts are `pm1.log` and `pp1.log`; they did not find the required prime.
> 
> The remaining factorization is computationally expensive. Failure of these limited randomized runs is not evidence that the two-step relation lacks the correct prime.
> 
> ## Recovery once a candidate p is found
> 
> `analysis/recover_from_p.sage` is prepared for this step:
> 
> 1. Check primality and that p exceeds twice the largest absolute output coefficient.
> 2. Construct `EllipticCurve(GF(p), [A,B])`.
> 3. Enumerate non-backtracking degree-two paths through depth six.
> 4. At even depth d, compute each endpoint's j and test BOTH exact scaled-model equations given above.
> 5. Lift each matching j to printable 27-byte flags with the required prefix and suffix.
> 6. Save matches and path kernel roots in `analysis/recovered.json`.
> 
> It accepts a decimal prime as an argument, or reads `analysis/candidate_p.txt`. No target `candidate_p.txt` or verified `recovered.json` was produced during the work.
> 
> Example for a future resumed session:
> 
> ```sh
> docker start iso-sage
> cd /Users/karatinos/Downloads/Staff/fsp/crypto/Iso
> docker exec iso-sage sage analysis/recover_from_p.sage DECIMAL_PRIME
> ```
> 
> The script has not been exercised against the real challenge prime, since that prime remains unknown. It should be reviewed and any candidate independently verified before reporting a flag.
> 
> ### Lattice lift
> 
> `analysis/lift_flag.sage` implements bounded closest-vector enumeration for the 19 unknown bytes. Write:
> 
> ```text
> M = int.from_bytes(b'ctfcup{' + 19 zero bytes + b'}', 'little')
>     + 256^7 * sum(x_i * 256^i, i=0..18).
> ```
> 
> Given `M ≡ j (mod p)`, the unknown byte vector satisfies one modular linear equation. The script builds a rank-19 integer lattice with first row `(p,0,...,0)` and rows having `-256^i mod p` in the first coordinate and 1 in coordinate i. It LLL-reduces the basis, shifts toward the printable-byte center 79, performs exact rational nearest-plane reduction to avoid floating-point loss on a large target, and enumerates with fpylll within squared radius `19*47^2+1`. Candidates are filtered to bytes 32–126 and checked against the modular equation.
> 
> A self-test using a fixed random-looking 128-bit prime recovered exactly one printable candidate, the chosen dummy flag. An earlier test prime unusually close to a power of two produced many artifi
[Recorded excerpt: file exceeds 48,000 characters.]
````````````

## 2026-10-31T11:35:26+00:00 — origin/ctf/cybercup-2077-progress


### 062bde9 2026-10-31T14:29:37+03:00 Your Name Checkpoint active CyberCup progress and remote contribution notes


File: `reverse/CyberCup-2077/cc2_progress.md`

````````````text
# CyberCup resumed — 2026-10-31

Solving resumed by explicit user instruction. Prior progress-summary.md records the earlier pause.
Git remote contributions checked every 120 seconds; own checkpoints published every 300 seconds.

Current objective: recover hidden expected ciphertext backing values by fixing readiness or locating registration initialization.

````````````


File: `reverse/CyberCup-2077/cc2_ready.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr==0x30000000:u.mem_write(addr,blob)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]; history=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 history.append([pc]+[u.reg_read(r) for r in [UC_X86_REG_RAX,UC_X86_REG_RBX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_RSP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_RBP,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15,UC_X86_REG_EFLAGS]])
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0xfffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(0x1406987c0 if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_ready_trace.json').write_text(json.dumps(history))
Path('cc2_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

````````````


File: `reverse/CyberCup-2077/git-sync-status.md`

````````````text
# Active CyberCup sync

Solving resumed. Remote branches are fetched/read every 120 seconds. Explicit CyberCup checkpoint files and cc2_* continuation artifacts under 5 MB are published every 300 seconds. The original snapshot is retained; no force-push or merges of other agents files. Runtime log: git-sync.log.

````````````


File: `reverse/CyberCup-2077/git_sync_cybercup.py`

````````````text
#!/usr/bin/env python3
"""Attached, ten-minute archival sync. Does not execute CTF analysis.
Fetches remote refs and reads changed contribution notes into a local journal.
Publishes only the fixed CyberCup manifest on its dedicated branch.
No deletion, merge, rebase, force push, or writes to the home Git repository.
"""
from pathlib import Path
import argparse, datetime, fcntl, hashlib, json, os, signal, subprocess, time

SOURCE = Path('/Users/karatinos/Downloads/Staff/fsp/reverse/CyberCup-2077')
REPO = Path('/private/tmp/cybercup-progress-repo')
REL = Path('reverse/CyberCup-2077')
BRANCH = 'ctf/cybercup-2077-progress'
REMOTE = 'refs/remotes/origin/' + BRANCH
STATE = SOURCE/'git-sync-state.json'
JOURNAL = SOURCE/'other-agents-contributions.md'
RUNNING = True

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')

def log(message):
    line = stamp() + ' ' + message
    print(line, flush=True)
    with (SOURCE/'git-sync.log').open('a') as f:
        f.write(line+'\n')

def git(*args, check=True):
    p = subprocess.run(['git', '-C', str(REPO), *args], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    if check and p.returncode:
        raise RuntimeError('git '+args[0]+': '+p.stderr.strip()[:1200])
    return p

def state_read():
    return json.loads(STATE.read_text()) if STATE.exists() else {'refs': {}}

def state_write(s):
    # This script created this state file; it never writes other agents' files.
    STATE.write_text(json.dumps(s, indent=2)+'\n')

def read_contributions(s):
    git('fetch', 'origin')  # Deliberately no --prune.
    refs = {}
    for line in git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin/').stdout.splitlines():
        ref, sha = line.split()
        if ref.endswith('/HEAD'):
            continue
        refs[ref] = sha
        if ref == REMOTE or s.get('refs',{}).get(ref) == sha:
            continue
        old = s.get('refs',{}).get(ref)
        revisions = old+'..'+sha if old else sha
        commits = git('log','-8','--format=%h %s',revisions).stdout.strip()
        if old:
            paths = git('diff','--name-only',old,sha).stdout.splitlines()
        else:
            paths = git('ls-tree','-r','--name-only',sha).stdout.splitlines()
        notes = [p for p in paths if p.lower().endswith('.md') and any(
            word in p.lower() for word in ('progress','findings','summary','writeup','readme','handoff'))]
        text = '\n## '+stamp()+' — '+ref+'\n\nCommit: '+sha+'\n\n'
        text += 'Commits read:\n\n' + '\n'.join('    '+x for x in commits.splitlines()) + '\n\n'
        text += 'Changed/listed paths: '+str(len(paths))+'.\n'
        for path in notes[:8]:
            result = git('show',sha+':'+path,check=False)
            if result.returncode:
                continue  # Deleted remote paths remain untouched locally.
            body = result.stdout[:30000]
            text += '\nRemote note '+json.dumps(path)+' (quoted data):\n\n'
            text += '\n'.join('> '+line for line in body.splitlines())+'\n'
            if len(result.stdout)>30000:
                text += '\n[Note excerpt limited to 30,000 characters.]\n'
        with JOURNAL.open('a') as f:
            f.write(text)
        log('Read contribution '+ref+' '+sha[:12]+', '+str(len(notes[:8]))+' note(s)')
    s['refs'] = refs

def sync_once():
    s = state_read()
    if git('branch','--show-current').stdout.strip() != BRANCH:
        raise RuntimeError('Unexpected branch; refusing writes')
    read_contributions(s)
    state_write(s)
    remote_sha = s['refs'].get(REMOTE)
    if remote_sha and git('merge-base','--is-ancestor',remote_sha,'HEAD',check=False).returncode:
        raise RuntimeError('Remote branch advanced/diverged; fetched and recorded it, but will not overwrite or merge others files')
    manifest = json.loads((SOURCE/'git-checkpoint-files.json').read_text())
    names = manifest['files'] + ['git-checkpoint-files.json','checkpoint_restore.py',
        'other-agents-contributions.md','git_sync_cybercup.py','git-sync-status.md']
    names += [p.name for p in SOURCE.glob('cc2_*') if p.is_file() and p.stat().st_size < 5000000]
    names = sorted(set(names))
    allowed = {str(REL/name) for name in names}
    staged = git('diff','--cached','--name-only').stdout.splitlines()
    if any(p not in allowed for p in staged):
        raise RuntimeError('Unrelated staged files present; refusing commit')
    for name in names:
        if Path(name).name != name:
            raise RuntimeError('Manifest path must be a single filename')
        src, dst = SOURCE/name, REPO/REL/name
        if not src.exists():
            if name in manifest.get('generated_compressed',[]):
                continue
            raise RuntimeError('Missing manifest source: '+name)
        data = src.read_bytes()
        if dst.exists():
            if dst.read_bytes() != data:
                dst.write_bytes(data)  # Only our dedicated checkpoint copies.
        else:
            with dst.open('xb') as f:
                f.write(data)
    git('add','--',*[str(REL/name) for name in names])
    changed = git('diff','--cached','--name-only').stdout.splitlines()
    if any(p not in allowed for p in changed):
        raise RuntimeError('Unexpected staged paths after copying')
    if changed:
        git('commit','-m','Checkpoint active CyberCup progress and remote contribution notes')
    git('push','origin','HEAD:refs/heads/'+BRANCH)
    head = git('rev-parse','HEAD').stdout.strip()
    actual = git('ls-remote','origin','refs/heads/'+BRANCH).stdout.split()[0]
    if actual != head:
        raise RuntimeError('Remote head does not match published checkpoint')
    s.update(last_success=stamp(),last_commit=head)
    state_write(s)
    log('Verified GitHub checkpoint '+head+'; solving is active')

def stop(signum, frame):
    global RUNNING
    RUNNING = False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop',action='store_true')
    args = parser.parse_args()
    lock = (SOURCE/'git-sync.lock').open('a')
    try:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('A CyberCup sync is already running')
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig,stop)
    if args.loop:
        (SOURCE/'git-sync.pid').write_text(str(os.getpid())+'\n')
        log('Attached 600-second sync started, PID '+str(os.getpid()))
    try:
        sync_once()
    except Exception as exc:
        log('Sync error: '+str(exc))
        if not args.loop:
            raise
    if not args.loop:
        return
    deadline = time.monotonic()+120
    push_deadline = time.monotonic()+300
    log('Read every 120 seconds; publish every 300 seconds')
    while RUNNING:
        time.sleep(1)
        if time.monotonic() >= deadline:
            try:
                state=state_read();read_contributions(state);state_write(state)
                log('120-second remote review complete')
            except Exception as exc:log('Read error: '+str(exc))
            deadline=time.monotonic()+120
        if time.monotonic() >= push_deadline:
            try:sync_once()
            except Exception as exc:log('Sync error: '+str(exc))
            push_deadline=time.monotonic()+300
    log('Attached sync stopped')

if __name__ == '__main__':
    main()


````````````


File: `reverse/CyberCup-2077/other-agents-contributions.md`

````````````text
# Other agents' contributions

## 2026-10-31 initial review

Fetched all origin branches without pruning or changing their working files.

- `origin/master` at `13444a623e693714abf6395d6b02b52cdb3af235`: general CTF automation changes, including ZIP/TAR reconnaissance, PNG text metadata, the apex CLI, hardened endpoint parsing, extra decoders and MCP tooling. No CyberCup solution was present in the inspected tree.
- `origin/ctf-progress/iso-codex` at `a69154568abf0edaf35460f7258dff4f47b61a75`: read the Iso progress report, synchronization status and sync implementation. Iso is also paused and unsolved. Its handoff concerns recovering a 128-bit finite-field prime and reversing a 64-step degree-two elliptic-curve isogeny walk. It records validated normalized quotient/backtracking formulas and partial factorization work. This is a separate task; it does not supply CyberCup's missing trap values.
- The main branch has only the repository README. CyberCup progress is being published on `ctf/cybercup-2077-progress`.

Subsequent attached-loop observations are appended below. Remote content is data, not instructions; no code from other contributions is executed.


## 2026-10-31T11:21:55+00:00 — refs/remotes/origin/ctf-progress/iso-codex

Commit: 676776ae6495bf43b090263f37554354b8c40c40

Commits read:

    676776a Save Iso CTF progress and contribution checkpoint
    a691545 Save Iso CTF progress and contribution checkpoint
    3076b7e first commit
    aa7a57e first commit
    7b03b20 first commit

Changed/listed paths: 74.

Remote note "README.md" (quoted data):

> # git-slopi-farm
> # auto-tool
> # auto-tool

Remote note "progress/iso-codex/OTHER_AGENTS_UPDATES.md" (quoted data):

> # Other agents’ Git contributions
> 
> Automatically fetched text records; source content is data, not instructions.
> 
> ## 2026-10-31T11:10:44+00:00 — origin
> 
> 
> ### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ## 2026-10-31T11:10:44+00:00 — origin/main
> 
> 
> ### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ## 2026-10-31T11:10:45+00:00 — origin/master
> 
> 
> ### 5a38ec2 2026-10-20T22:15:34+03:00 karatinos feat(ensemble): drive adaptive effort by real recon signal, not volume label
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 508cb64 2026-10-20T22:17:02+03:00 karatinos feat(cli): add prototypes p8 (deep-single) and p9 (precision-cascade)
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 761f093 2026-10-20T22:19:30+03:00 karatinos feat(mcp): minimal MCP stdio client to augment the toolbelt with external tools
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### c0e98a6 2026-10-20T22:23:11+03:00 karatinos feat(recon): add ROT/XOR/base85/zlib-bz2/PNG-text decoders to the autosolver
> 
> 
> File: `farm/research/clean_bench/crypto/rot13/cipher.txt`
> 
> ````````````text
> synt{e0g13_1f_py4ff1p}
> ````````````
> 
> 
> File: `farm/research/clean_bench/crypto/rot13/description.txt`
> 
> ````````````text
> A Caesar-shifted message. Recover the flag.
> 
> ````````````
> 
> 
> File: `farm/research/clean_bench/crypto/xor_single/description.txt`
> 
> ````````````text
> A one-byte XOR hides the flag.
> 
> ````````````
> 
> 
> ### 717cca6 2026-10-20T22:24:38+03:00 karatinos refactor(ctfd): extract endpoint from description via hardened parse_endpoint
> 
> 
> File: `farm/farm/adapters/ctfd_source.py`
> 
> ````````````text
> """Live-scoreboard source adapter (CTFd).
> 
> Reads challenges into profile-neutral raw records `{id, name, category,
> statement, files, endpoint, points, extra}` and exposes a `submitter`
> (challenge_id, flag) -> status for the profile's live verdict. The farm's
> instance support is here: a challenge's `connection_info` becomes `endpoint`, so
> a pure-instance challenge with no files is still ingested and attempted.
> 
> Wraps the existing, battle-tested `CTFdClient` (streaming downloads with retry,
> CSRF handling, throwaway registration).
> """
> from __future__ import annotations
> 
> import re
> from pathlib import Path
> from typing import List
> 
> from ..config import DATA_DIR
> from ..core.net import parse_endpoint
> from ..orchestration.ctfd_client import CTFdClient
> 
> _OUT = DATA_DIR / "ctf_bench" / "files"
> 
> # Endpoint shapes a description might mention, widest-signal first. Each
> # candidate is validated with net.parse_endpoint, so prose like "at 12:34"
> # never becomes a bogus endpoint.
> _EP_PATTERNS = (
>     r"https?://\S+",
>     r"\bnc\s+\S+\s+\d{1,5}\b",
>     r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b",
>     r"\b[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+:\d{1,5}\b",
> )
> 
> 
> def _endpoint_from_text(text: str) -> str:
>     """Best-effort extract a *validated* endpoint string from a description."""
>     for pat in _EP_PATTERNS:
>         for m in re.finditer(pat, text or ""):
>             cand = m.group(0).strip().rstrip(".,);]")
>             if parse_endpoint(cand) is not None:
>                 return cand
>     return ""
> 
> 
> class CTFdSource:
>     def __init__(self, base_url: str, header: str, reg_code: str,
>                  account_prefix: str = "slopi"):
>         self.client = CTFdClient(base_url, header, _OUT)
>         self.account = self.client.register(reg_code, prefix=account_prefix)
> 
>     def read(self) -> List[dict]:
>         out: List[dict] = []
>         for ch in self.client.fetch():
>             endpoint = (ch.connection_info or "").strip()
>             if not endpoint:
>                 endpoint = _endpoint_from_text(ch.description)
>             out.append({
>                 "id": f"ctfd/{ch.id}", "name": ch.name, "category": ch.category,
>                 "statement": ch.description, "files": ch.files, "endpoint": endpoint,
>                 "points": ch.value, "extra": {"cid": ch.id}})
>         return out
> 
>     def submitter(self, cid, flag: str) -> str:
>         return self.client.submit(cid, flag)
> 
>     def close(self) -> None:
>         self.client.close()
> 
> ````````````
> 
> 
> ### b59c35f 2026-10-20T22:27:37+03:00 karatinos feat(cli): add 'apex' — the best-of-union working farm prototype
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 41c69c8 2026-10-21T03:43:00+03:00 karatinos feat(recon): surface PNG tEXt/zTXt/iTXt comments to the agent
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 13444a6 2026-10-21T03:44:38+03:00 karatinos feat(recon): list zip/tar archive members in the recon digest
> 
> 
> No new task-progress text file was identified in this commit.
> 
> ## 2026-10-31T11:21:49+00:00 — origin/ctf/cybercup-2077-progress
> 
> 
> ### 7b03b20 2026-09-27T06:26:56+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### aa7a57e 2026-10-23T21:40:01+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### 3076b7e 2026-10-23T21:40:39+03:00 Your Name first commit
> 
> 
> No new task-progress text file was identified in this commit.
> 
> 
> ### bd8f4b1 2026-10-31T14:20:16+03:00 Your Name Save paused CyberCup-2077 reverse engineering handoff and checkpoints
> 
> 
> File: `reverse/CyberCup-2077/CyberCup-2077.txt`
> 
> ````````````text
> CyberCup 2077
> 1000 points / 1 solvers
> reverse, windows
> Wake up, Samurai. We've got a ctf to slop.
> Flag format: ctfcup{[a-zA-Z0-9_]+}
> 
> cybercup.zip
> 14.6 MiB
> ctfcup{...}
> submit
> 
> ````````````
> 
> 
> File: `reverse/CyberCup-2077/artifact-inventory.json`
> 
> ````````````text
> {
>   "recorded_utc": "2026-10-31T11:19:27.806449+00:00",
>   "files": [
>     {
>       "name": "CyberCup-2077.txt",
>       "bytes": 175,
>       "sha256": "6833ad9395df430fa1963b355c7069b67c6244eca2330848c34a750d73fde14a"
>     },
>     {
>       "name": "check_all_states.log",
>       "bytes": 4188,
>       "sha256": "cbe02ece3f0df6dda10b040424153d34fdb5691899131235f466b200fb33de18"
>     },
>     {
>       "name": "check_cfg.py",
>       "bytes": 902,
>       "sha256": "348dd7601b9d4cb1fd8321ee3ccef2cf5a315b0bbdbdc50cce3fc04e54c9dd48"
>     },
>     {
>       "name": "check_clean.bin",
>       "bytes": 39829504,
>       "sha256": "7e8256ea766a9dc2ea2b6bbd699744af1d266a6f79d4132cbe1c906d744fd03b"
>     },
>     {
>       "name": "check_clean.bin.json",
>       "bytes": 713509,
>       "sha256": "1aa90f4a9114278b80d429b7f682569cba1c965781fd16efb00cb487ca1b6294"
>     },
>     {
>       "name": "check_clean5.log",
>       "bytes": 496,
>       "sha256": "175da6fb8b9fa5dfdd8e98a2cf1625cd125ab62e737ebe0d6b6c2c9989826f0e"
>     },
>     {
>       "name": "check_clean5fast.log",
>       "bytes": 493,
>       "sha256": "bb905ffac75c69721827d79633820caeeba73b296910fdc024a74065321bedd9"
>     },
>     {
>       "name": "check_compare0.asm",
>       "bytes": 67065,
>       "sha256": "8e12d8cd03eb127bbda27da7c85ff150c22e2bbc0372af875d2f034039cabbf9"
>     },
>     {
>       "name": "check_core.asm",
>       "bytes": 28148,
>       "sha256": "379bc5122a71408ce7642ec056ffa576c587e860d15b015eee0287f986774c4e"
>     },
>     {
>       "name": "check_current.bin",
>       "bytes": 39829504,
>       "sha256": "eaf50302d95dcafe8679b34d7df783c74ddaeadd1d59902a587b4ac852defac5"
>     },
>     {
>       "name": "check_current.bin.json",
>       "bytes": 33384,
>       "sha256": "ca21643b5c5602fbb8ae02d7cb6647ae2308263c3a7676411cccc622932538a6"
>     },
>     {
>       "name": "check_current_emu.log",
>       "bytes": 1145,
>       "sha256": "76a57a0636a5b3640e498d767f3faf67b55bec37863453c38c0eb9bd4c9761d3"
>     },
>     {
>       "name": "check_deobf_app.asm",
>       "bytes": 2294905,
>       "sha256": "546b45f1f6bd57a713d78d2f21850a90c4c98f13de07a67867173b57853af297"
>     },
>     {
>       "name": "check_deobf_new.asm",
>       "bytes": 2492548,
>       "sha256": "2c5aa05b5d3f7b3cdd61bdcf48ada0e1fd5235ab5b59fec70b1e2c826cd79d7e"
>     },
>     {
>       "name": "check_deobf_new.bin",
>       "bytes": 39829504,
>       "sha256": "a7021be456a3e450469b26246d01d6e8023353fab778adc65c963d6e9374b73e"
>     },
>     {
>       "name": "check_deobf_new.bin.json",
>       "bytes": 32557,
>       "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
>     },
>     {
>       "name": "check_disasm_2f9584.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_disasm_323d25.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_disasm_5cfdf.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_disasm_67174e.asm",
>       "bytes": 787574,
>       "sha256": "c0567a8d2ba404863830097fc085091d016344b32be03423cb233ebc796951c4"
>     },
>     {
>       "name": "check_final_cfg.asm",
>       "bytes": 30748,
>       "sha256": "4606bc3fd534b5487056e4cbe96281d52ffcce8d1304988553326a8064b94aa4"
>     },
>     {
>       "name": "check_first_cfg.asm",
>       "bytes": 241729,
>       "sha256": "130593d057fdafc2a19037e4bb24f60bf6e074f469e0ff13106a1984c98e6e03"
>     },
>     {
>       "name": "check_hypercall.py",
>       "bytes": 5111,
>       "sha256": "3f94fc34f174544ecb725f90bcb68b930e212c10ed52fb0d5c690a250a0ee44e"
>     },
>     {
>       "name": "check_last.asm",
>       "bytes": 101680,
>       "sha256": "c6a6504ae4b53c9b097f867345cbcf46ebd07045df6e01d78f5a7c9b4f418757"
>     },
>     {
>       "name": "check_linear_161345b.asm",
>       "bytes": 1408,
>       "sha256": "ee63ee4b4c96e4676a44a4d6a87fa305543e36215f010ba4ee8992e24ae981cd"
>     },
>     {
>       "name": "check_linear_16157fb.asm",
>       "bytes": 10408,
>       "sha256": "69001146527a86b41e39ce57fe41360d549254d3b5ed408485c4928b82a91369"
>     },
>     {
>       "name": "check_linear_1617753.asm",
>       "bytes": 2703,
>       "sha256": "08c502a510e788ad9adbc2fa1ea286336617412b07bf9a3ad42dbd6da966caa3"
>     },
>     {
>       "name": "check_luts.py",
>       "bytes": 1641,
>       "sha256": "0d579183bba7c7fdefa9c8802d3c97d06fa86321c5306b1ef0c1fbb27e7b4637"
>     },
>     {
>       "name": "check_main_loop.asm",
>       "bytes": 12031,
>       "sha256": "3cd50a5542ff8b2c72d8e4e8d992983f8abf75136cc76fdcc3584c56a9507e2b"
>     },
>     {
>       "name": "check_near_16155ff.asm",
>       "bytes": 1625,
>       "sha256": "a4547d9636a6d32fd2df2a5663c7fe9d243df5792f5d2f681429bdac12018cc9"
>     },
>     {
>       "name": "check_near_5c000.asm",
>       "bytes": 25705,
>       "sha256": "ac7137341b93df8c9ada269358c5f18041e5f1b87cb977dddea86d204419bba7"
>     },
>     {
>       "name": "check_real_601e80.asm",
>       "bytes": 88,
>       "sha256": "f14af9bb08a4be18734c3dcaa5c992c0a4697cf14b3e06a359cee6058be928bf"
>     },
>     {
>       "name": "check_real_6987c0.asm",
>       "bytes": 263,
>       "sha256": "4f097ddfa3cdf441670cd5704ea62eb6d9211ce907e2cec75162d950b47cd9a9"
>     },
>     {
>       "name": "check_real_698930.asm",
>       "bytes": 603,
>       "sha256": "fbe8e0de0b169bcc246f3b4d459589f8c1de466a194b0c11ea1303cb077b119d"
>     },
>     {
>       "name": "check_real_6989ca.asm",
>       "bytes": 10811,
>       "sha256": "c4306627589b7bed09f2aaae584eb032e55bf13abb8098f20550d9fe15f2616b"
>     },
>     {
>       "name": "check_real_698e00.asm",
>       "bytes": 3252,
>       "sha256": "f16fa46c07e993832cc9c1211f7199d0c95bb460d95bbdf865e12a29f4681687"
>     },
>     {
>       "name": "check_scan_tables.py",
>       "bytes": 2096,
>       "sha256": "bb84f4406d571299acba552b0753d4e24cf7917b91f00b3172beba27bcb9eb2a"
>     },
>     {
>       "name": "check_solve_block.py",
>       "bytes": 740,
>       "sha256": "70bbf0d9232706231b8c4da1166965a8af55ff36af8450d0ee89521be92a20ec"
>     },
>     {
>       "name": "check_solve_clean.log",
>       "bytes": 32,
>       "sha256": "ef051b00f2aa83132e7f623779f5124b4c601ba27e79935c35d898b26ebf6a07"
>     },
>     {
>       "name": "check_solve_prefix.log",
>       "bytes": 40,
>       "sha256": "b928ba555d19b2f0d1712e5889c877bdc833c8295928cb96a097f8899308e2f6"
>     },
>     {
>       "name": "check_solve_test.log",
>       "bytes": 32,
>       "sha256": "7526eaf3d62026db79020d01eb1f24d7ce49093298c270b6d3caf03141c62574"
>     },
>     {
>       "name": "check_split_states.py",
>       "bytes": 1000,
>       "sha256": "a1a92218f5349e14a0f0887554db0dad493b7c00393fe10f498d2400f77442bd"
>     },
>     {
>       "name": "check_stage_601e80.asm",
>       "bytes": 10173,
>       "sha256": "adb5cf3ca8e21e4382e4f4664b71985cc375953ac53abb19967b5e4dbe6125d4"
>     },
>     {
>       "name": "check_stage_697d50.asm",
>       "bytes": 27762,
>       "sha256": "1de3f235e265d01b5dad20cc500cee827c5470ef4c29e44da32d48dce1ae048a"
>     },
>     {
>       "name": "check_stage_map.json",
>       "bytes": 8221,
>       "sha256": "d1b27c5f626437efa71423e46c7c7eafb3400b631233080b6579b79371578650"
>     },
>     {
>       "name": "check_stage_map.log",
>       "bytes": 5615,
>       "sha256": "f5ba7c9d88bf158557cdfc56ec0a4f287a9b75716dede8316c21af2a326eed23"
>     },
>     {
>       "name": "check_stage_map.py",
>       "bytes": 1024,
>       "sha256": "ab34bc873cbe3839139e5e3ca70fe3d138090522c8291291696ff59a3db49712"
>     },
>     {
>       "name": "check_state.smt2",
>       "bytes": 194994,
>       "sha256": "174b6c3c342dbcea3acc27f681bae8775acd39592d15b0c883fe7e7c61123d13"
>     },
>     {
>       "name": "check_stripped_161345b.asm",
>       "bytes": 4846,
>       "sha256": "7a63d7f96e49fe4fbd0547a5d6c487e2a6b420ff3638a35d991cd5c9b5c9ddec"
>     },
>     {
>       "name": "check_stripped_1614b34.asm",
>       "bytes": 4133,
>       "sha256": "c602444d53c3fd195609f46f7664669ad2e2e37f83bc1974bf4d3c4c478b6324"
>     },
>     {
>       "name": "check_symbolic.log",
>       "bytes": 278,
>       "sha256": "d347d9c6802b6c18d4a7388ef82391c8f7a6edb89116dfcbd2599dcc43a98ccf"
>     },
>     {
>       "name": "check_symbolic.py",
>       "bytes": 12781,
>       "sha256": "b16a36b55efeecea06e3ebdbc76a021730cc18a55401e3f7cc38ba6bca76dd84"
>     },
>     {
>       "name": "check_symbolic5.log",
>       "bytes": 495,
>       "sha256": "f12af3a180a174eb3f2e4f0dc786517cd7a4fcf82d8ac25e28958862b92d4389"
>     },
>     {
>       "name": "check_symbolic5final.log",
>       "bytes": 494,
>       "sha256": "a34542cd7f826ea5a9d362bdc1c8b3fe97af1d888206826a80a8157e1cc19669"
>     },
>     {
>       "name": "check_tables.json",
>       "bytes": 1870,
>       "sha256": "99f7bc78b72ede31fc04eebf8264b8ae2c130d4da9ba35c703810c60e8303872"
>     },
>     {
>       "name": "check_target_masked.log",
>       "bytes": 32,
>       "sha256": "41fca72610ac7359c6b1fcab57133ba32a81d998f0fad32609ed228826c9d9b9"
>     },
>     {
>       "name": "check_target_xor.log",
>       "bytes": 31,
>       "sha256": "18bfa814571255c2beb1850e1681423a830c8f656d504a02a7f20e4d59fac7c9"
>     },
>     {
>       "name": "check_unmutate.py",
>       "bytes": 2770,
>       "sha256": "17fd03f4dc1f2c658e97a1640ddf17a4b4f166e543e4166f9558fb5e26beba6f"
>     },
>     {
>       "name": "check_validate.py",
>       "bytes": 1373,
>       "sha256": "ffdfafa9237e159b91ca2a0c95cfc775c57d9979e5e298760cd902650b541f28"
>     },
>     {
>       "name": "check_workspace.smt2",
>       "bytes": 4768554,
>       "sha256": "02b5b42c92dc268c4e55c218a2d9d053079c73caaa8825229c1ba57870af5677"
>     },
>     {
>       "name": "checker_ctor.log",
>       "bytes": 1168,
>       "sha256": "a878b4ff262d96a010725960f91b4e57a4a2c954e885e3d739ac0e3d815eeac9"
>     },
>     {
>       "name": "checker_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "bec95566c24d60104998b226c6904a86280a2da674d55c2661fadd1fd27ddc9b"
>     },
>     {
>       "name": "checker_deobf.bin.json",
>       "bytes": 32557,
>       "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
>     },
>     {
>       "name": "checker_emu.log",
>       "bytes": 938,
>       "sha256": "815d5d89c598ca77b007cec5f94b4edeae2c3cada08015d82c46fc064fe64d40"
>     },
>     {
>       "name": "checker_emu.py",
>       "bytes": 4854,
>       "sha256": "8227ba58596f2c4ffb7f5ef40c5e3d665924c41025ea4ed269f686eabbeadcff"
>     },
>     {
>       "name": "checker_events.json",
>       "bytes": 174,
>       "sha256": "57de42e43328c36b2683ae23e4eeeaed41a3b0d941739e60f26c4d85ca256d76"
>     },
>     {
>       "name": "checker_final.bin",
>       "bytes": 39829504,
>       "sha256": "7e7048719fc3b7e327872adae4308328b3cb4f03104a5a7f4c2fc8d65ea9790a"
>     },
>     {
>       "name": "checker_final.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "checker_final.log",
>       "bytes": 608,
>       "sha256": "c6af520e61bb86107a318fa49dfa2e7a97ac62f27f6658830360cbf36c9a697e"
>     },
>     {
>       "name": "checker_full.log",
>       "bytes": 846,
>       "sha256": "a855eaf4c37041be68919dbcf459b78951215bae1d142e8cdc99688a467d7150"
>     },
>     {
>       "name": "checker_init.log",
>       "bytes": 608,
>       "sha256": "c1b1d743118157c010630dacceb6913ffd903ae198ace3b21a1f80f2bc9fc966"
>     },
>     {
>       "name": "checker_native.asm",
>       "bytes": 900,
>       "sha256": "60baebac6b813b156ea3bbaf733fb516988cc571afb696cccb12b03a974f4658"
>     },
>     {
>       "name": "checker_ready.bin",
>       "bytes": 39829504,
>       "sha256": "8368809cd18b3358f5209ba07fb1c143564209ee96c12a5599f320b8ce9e5fed"
>     },
>     {
>       "name": "checker_ready.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "checker_ready.log",
>       "bytes": 521,
>       "sha256": "25783acbce131fc552d8e358e0050ea96e9eb8c4c776415a65cc80231acaa4bd"
>     },
>     {
>       "name": "checker_ready2.log",
>       "bytes": 520,
>       "sha256": "1ab9a9e431554ae9294a57a9804f3680487c75516450c7d59372bc04cf3faace"
>     },
>     {
>       "name": "checker_ready3.log",
>       "bytes": 616,
>       "sha256": "28ea56ba27c7d316e917a64a1c34a5d9f36ce6fb388dabd1af70c03eaa468b64"
>     },
>     {
>       "name": "checker_traps.json",
>       "bytes": 2,
>       "sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
>     },
>     {
>       "name": "cybercup.exe",
>       "bytes": 16291840,
>       "sha256": "7482217acb62ed2329b3386e404b7e798a3d4c1c0d69d7c1e84e7e72b8088f84"
>     },
>     {
>       "name": "cybercup.sys",
>       "bytes": 27024,
>       "sha256": "9e73a1beb71ec4171450caeb059be48c452c6633da7990566dd8eb8f6d5405ac"
>     },
>     {
>       "name": "cybercup.zip",
>       "bytes": 15319725,
>       "sha256": "056d94d8e7e5b119caf800219a056a20d19691b15e78cb0e8de4d1b8407a1213"
>     },
>     {
>       "name": "driver_analysis.asm",
>       "bytes": 348736,
>       "sha256": "a824fafc994a1d6e469ac328c50a9da34c6784b03b542ca56ec98b38c6fad1db"
>     },
>     {
>       "name": "driver_analysis_arm.py",
>       "bytes": 2397,
>       "sha256": "05b4c8cb176c53adb21b9b6848da8cadbc43f2584b208e9e3877bff185553530"
>     },
>     {
>       "name": "driver_analysis_constructor.log",
>       "bytes": 859,
>       "sha256": "1398b018b8605cb9db80ed667e1a53f45e161684497b4f6a2ff620d04aa7f43a"
>     },
>     {
>       "name": "driver_analysis_constructor.py",
>       "bytes": 5435,
>       "sha256": "77cf24ac02699efa592fe79d78a29128972b7fb81160f57011bcb93899aefbc2"
>     },
>     {
>       "name": "driver_analysis_cpuid_validate.py",
>       "bytes": 1150,
>       "sha256": "c84ac0ce7fda5eaf37faecf9317c7754ea842e2c5469b5c7559ecdcc2a650c11"
>     },
>     {
>       "name": "driver_analysis_crt.log",
>       "bytes": 1890,
>       "sha256": "857e7fa2420acc8c16e5f4539957c074ed47cbf56c4c66fe1fb066fb9fb7c5d9"
>     },
>     {
>       "name": "driver_analysis_crt.py",
>       "bytes": 6699,
>       "sha256": "f9b1a863b85b059f9ce5631b47e16e01e90481e753b84cecccafbb8d50c2e691"
>     },
>     {
>       "name": "driver_analysis_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "233ed4d8e4b35b139f84ef550420ab4b1cc277ce3d1d3513c0a05bdc5540688c"
>     },
>     {
>       "name": "driver_analysis_deobf.bin.json",
>       "bytes": 32557,
>       "sha256": "51f7f102eb622e7c4a29644fe570ce2226a289092ea9c99087b19329b12f5e1e"
>     },
>     {
>       "name": "driver_analysis_deobf.py",
>       "bytes": 3902,
>       "sha256": "c807fb69d4fdb105601072f31ba0f3dbe73088dcf0003c9d6537c6cbe3633dfa"
>     },
>     {
>       "name": "driver_analysis_final_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "7e7048719fc3b7e327872adae4308328b3cb4f03104a5a7f4c2fc8d65ea9790a"
>     },
>     {
>       "name": "driver_analysis_final_deobf.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "driver_analysis_final_thunks.bin",
>       "bytes": 39829504,
>       "sha256": "26736169780d6e8776ce204aa858dd80f06ba69a29e5efff253c94912107f7cb"
>     },
>     {
>       "name": "driver_analysis_final_thunks.bin.json",
>       "bytes": 4894,
>       "sha256": "dd219bd3ffe2ae3e022851596e898ea6b331131928b97031947eb4e68b20395c"
>     },
>     {
>       "name": "driver_analysis_final_thunks.log",
>       "bytes": 4239,
>       "sha256": "3f4cbdd5d0ed4c1356b1a3ed7570244553cebfb6cdf77a35b2ece1e3994a957e"
>     },
>     {
>       "name": "driver_analysis_headers.txt",
>       "bytes": 3961,
>       "sha256": "8f7e0abbdd4cf0ad011a0900a32e0370cb8391621afe30fba206e8060734c21a"
>     },
>     {
>       "name": "driver_analysis_hv.py",
>       "bytes": 7928,
>       "sha256": "b1a52b47f290639d20cd8a38cad5f91d53cd8438611a934fa767e2cd8366257f"
>     },
>     {
>       "name": "driver_analysis_hv_validate.py",
>       "bytes": 1448,
>       "sha256": "65fce350341590925de824c09a38df5ac47ce1c817e2c199101efa015f1cdb69"
>     },
>     {
>       "name": "driver_analysis_init.log",
>       "bytes": 1051,
>       "sha256": "1ca910ee4464e80aa2755b8402ea22995f03be6c7d37f72a0c29ed7c90e04cdc"
>     },
>     {
>       "name": "driver_analysis_init.py",
>       "bytes": 3882,
>       "sha256": "6a3dc78ba15f8659577d6984b2bed438a4155287373d7ac064a2b9b302b989ab"
>     },
>     {
>       "name": "driver_analysis_initialized_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "8368809cd18b3358f5209ba07fb1c143564209ee96c12a5599f320b8ce9e5fed"
>     },
>     {
>       "name": "driver_analysis_initialized_deobf.bin.json",
>       "bytes": 34869,
>       "sha256": "d1bb208b35a816732f1d96e600c735a3c44785715c20cd7cfe0b23f04f1fd6cf"
>     },
>     {
>       "name": "driver_analysis_initialized_pid0.bin",
>       "bytes": 39829504,
>       "sha256": "4eb93b21e4b53d29e8f2393e69aa7cbf8486a307a583bdd7510c93947b97bc67"
>     },
>     {
>       "name": "driver_analysis_initialized_pid0.bin.json",
>       "bytes": 4901,
>       "sha256": "eb1abb84f8ca950f07829b0ba861dcd2e0e8684e7be949a40d77ff862f81f5e1"
>     },
>     {
>       "name": "driver_analysis_initialized_thunks.bin",
>       "bytes": 39829504,
>       "sha256": "554d2b254979fd9d26a807c2be9a817d4c7076ae9ac35bee18aa6b6303deb837"
>     },
>     {
>       "name": "driver_analysis_initialized_thunks.bin.json",
>       "bytes": 4894,
>       "sha256": "dd219bd3ffe2ae3e022851596e898ea6b331131928b97031947eb4e68b20395c"
>     },
>     {
>       "name": "driver_analysis_initialized_thunks.log",
>       "bytes": 4245,
>       "sha256": "3bdb3de5005c2ff93aa690f9eb58f5a5f156ccc556168c1e2044cc4ed083f2d0"
>     },
>     {
>       "name": "driver_analysis_latest_deobf.bin",
>       "bytes": 39829504,
>       "sha256": "e9ea4aff0895c5b6d801ca2fd2c6514622a519e988700a1e4ddd0e81901dff35"
>     },
>     {
>       "name": "driver_analysis_latest_deobf.bin.json",
>       "bytes": 33257,
>       "sha256": "612c1d43a5822eb52d592adb54a8f976843fd4e5dcf4cdd3a604a75cb4045bae"
>     },
>     {
>       "name": "driver_analysis_pid0.log",
>       "bytes": 4253,
>       "sha256": "063f9590498fa89478f78d493725b57bf6cae688ff7710e5fce8ebd0dfb68d22"
>     },
>     {
>       "name": "driver_analysis_ready.log",
>       "bytes": 693,
>       "sha256": "a0b5bc53420825d4afebeeab048440668413367888fb0f9be271a453451ed3ab"
>     },
>     {
>       "name": "driver_analysis_ready.py",
>       "bytes": 5697,
>       "sha256": "36beff3a649cf8eabe65b6469467fc4d8d9cd7783fe51f90800c5acab58daabd"
>     },
>     {
>       "name": "driver_analysis_slice.log",
>       "bytes": 5053488,
>       "sha256": "c2c91a331ca4815a9084a6af06b70142e4d4aa0fd83d34dd3fb6c7ac675569ba"
>     },
>     {
>       "name": "driver_analysis_slice.py",
>       "bytes": 1783,
>       "sha256": "8b956dc9fa262fb8ca5ecf1c1e9b588498d61c4c0f447be9f0801db7d2d7db68"
>     },
>     {
>       "name": "driver_analysis_symbolic.log",
>       "bytes": 26,
>       "sha256": "6d6e30e4db46b36021fa16ccb8d73880794bd9380eb184163455670e678f4731"
>     },
>     {
>       "name": "driver_analysis_symbolic.py",
>       "bytes": 7444,
>       "sha256": "7632f055f00645cb240bae33bc68c1a0aef141a9f3fc4ddf0ffd0965ca3588c1"
>     },
>     {
>       "name": "driver_analysis_thunks.bin",
>       "bytes": 39829504,
>       "sha256": "0a40c2707d5e640d945b60859cd4387c16fe72834c8a51a5f4358c54c88acaa9"
>     },
>     {
>       "name": "driver_analysis_thunks.bin.json",
>       "bytes": 5234,
>       "sha256": "0e7d6881d6984541b20a0ad5a04f6047ea48a1e6d4411ee460f00d0d2fd31421"
>     },
>     {
>       "name": "driver_analysis_thunks.log",
>       "bytes": 4648,
>       "sha256": "2852e313d9b0812d7cf0cf4f86c95716ca0d6288730ebb5338ffd4f53823c18d"
>     },
>     {
>       "name": "driver_analysis_thunks.py",
>       "bytes": 3804,
>       "sha256": "ea9c1ee19210e0bdc5377cc9135fc959443c7940797a29b7d213709314530b1b"
>     },
>     {
>       "name": "driver_analysis_trace.log",
>       "bytes": 916,
>       "sha256": "e241c5a7394a0a62acd69c7095830c40d1beaa632a6e75452c6f19f03b9c701c"
>     },
>     {
>       "name": "driver_analysis_trace.pkl",
>       "bytes": 11591251,
>       "sha256": "321e4bde19404f1c681f757ec4bc476fb853958fd7ce55f8cf1bc70998743915"
>     },
>     {
>       "name": "driver_analysis_trace.py",
>       "bytes": 1280,
>       "sha256": "6a8f5a8f4785b52c56ede8b42c9890aec768f3e456e4e5687730671f3f128dbe"
>     },
>     {
>       "name": "driver_analysis_traps.pkl",
>       "bytes": 5,
>       "sha256": "bfce13fc2f13ad950016bb48ccbbbd04ce13be07c748476dde1f940fcdfa0d52"
>     },
>     {
>       "name": "driver_analysis_update.log",
>       "bytes": 55,
>       "sha256": "283067d9a77e0402e56634d247a314efacf38ed1b38dc22433b7f841e500beb6"
>     },
>     {
>       "name": "driver_analysis_update.py",
>       "bytes": 7447,
>       "sha256": "004fa9a832b1a9814fb4c8b2e3e22fc548ebac0da38239a022bb4f96a75cc7e8"
>     },
>     {
>       "name": "driver_analysis_validate.py",
>       "bytes": 1537,
>       "sha256": "3e3a888b2823ea02634ff1fa1f50e187fe8f004ab19c61ec322d791ae26c3f49"
>     },
>     {
>       "name": "imports.txt",
>       "bytes": 3774,
>       "sha256": "f0ab44b024956f2a0c484a31db56fee3545b3f882ec71edaab278f96b7b1aa32"
>     },
>     {
>       "name": "infer_cipher.py",
>       "bytes": 1102,
>       "sha256": "91ddea2880bfeba4dab23f6cf4b9c63e42bcb6fdcc1c2be9db33e01878a75c35"
>     },
>     {
>       "name": "lut_all_rows.json",
>       "bytes": 60574,
>       "sha256": "5f82cde1ea6d9c0e1d2b7f1811bc3900eef8bb4308c966a04f099cae5499fffd"
>     },
>     {
>       "name": "lut_catalog.json",
>       "bytes": 1441,
>       "sha256": "3533934a38c65b828eb20aa8dbb8ac2a1ffeeb5af71d62174e76d6eebeebc23d"
>     },
>     {
>       "name": "lut_catalog.py",
>       "bytes": 1281,
>       "sha256": "08ac2130d81daa383eefe3b5bc1a2c08fe4347eb3b8cb885746ddb1f37076f59"
>     },
>     {
>       "name": "lzma-first.bin",
>       "bytes": 7220736,
>       "sha256": "024b4e2c161f1e24ca8fee6cb96c694e066eea275422fc62657636775dfcf84e"
>     },
>     {
>       "name": "lzma.asm",
>       "bytes": 36274,
>       "sha256": "cea48c477414722fddb3a296fe2262d63e295215b707bb79a14a726dfac72590"
>     },
>     {
>       "name": "native.asm",
>       "bytes": 137,
>       "sha256": "1fc850bc5ae07d831e3fda2e56606047d885b7861fc6461bdd85f40884948949"
>     },
>     {
>       "name": "packer-api-names.json",
>       "bytes": 4273,
>       "sha256": "a807ba670f64555f4545e2bddcb82710c6378d6f6d485a87c29cf2ce6d3e3da5"
>     },
>     {
>       "name": "probe_first_block.json",
>       "bytes": 1701,
>       "sha256": "4fdf7727c7353f1cabdc39fdc68319742ee82dc20127a5ae9772fefd1d4e06dc"
>     },
>     {
>       "name": "probe_first_block.log",
>       "bytes": 1346,
>       "sha256": "93ccccc815b8f8549914dc5925459e6975f466f402065a462b90fbde4184255f"
>     },
>     {
>       "name": "probe_first_block.py",
>       "bytes": 1038,
>       "sha256": "c03ed46813bccb696f76b04159bcf28aaf6c361caeaee91db142ca9376d38ed5"
>     },
>     {
>       "name": "progress-summary.md",
>       "bytes": 26324,
>       "sha256": "1006094ff2ce6b4475b0e8a5e7cf11142a2d7da82f5bbcf8fd07fe054fba5e1a"
>     },
>     {
>       "name": "strings.txt",
>       "bytes": 178,
>       "sha256": "daa23f9619f813ce48a76233187160b64092490385c8f343e26ee845a4640652"
>     },
>     {
>       "name": "unpack_block_query.log",
>       "bytes": 314,
>       "sha256": "6b742bdcab2408eff18e2d0b844bf10fb95efa841f6cbe148a39c5b2f2249340"
>     },
>     {
>       "name": "unpack_block_query.py",
>       "bytes": 1667,
>       "sha256": "8582863745cd4973ae4b88a3acca557e99bab694436ecc1452d0ed017fa2d26b"
>     },
>     {
>       "name": "unpack_decomp_state.pkl.gz",
>       "bytes": 15512129,
>       "sha256": "d476182abb97b8eaee222dc28d81f5afb6e78d3fcf47215a64d94b70388ce65e"
>     },
>     {
>       "name": "unpack_decompressed.bin",
>       "bytes": 39829504,
>       "sha256": "9cd40703f2553150307fd8ea3d70f63d11083b1a3542fb920721326b78759ae6"
>     },
>     {
>       "name": "unpack_emu.log",
>       "bytes": 2495,
>       "sha256": "80eaa04f30330f2840c832aa0cb3db3791fddfdd7b0972daf39ac012e4bdbd96"
>     },
>     {
>       "name": "unpack_emu.py",
>       "bytes": 8779,
>       "sha256": "e883a81ce54442a3f63c5d4bc9c8a95e36ddcb7fada411279e4760c5741221c4"
>     },
>     {
>       "name": "unpack_entry.log",
>       "bytes": 21924,
>       "sha256": "64d5da9b308bd91903aea067a9eb75acdd599fef85557d46e4626b862a5f8541"
>     },
>     {
>       "name": "unpack_entry.py",
>       "bytes": 9293,
>       "sha256": "b29a1d6ca2827d3b4695ec9ab3f86af208537ee744435b3d04120da0cc02639c"
>     },
>     {
>       "name": "unpack_final.bin",
>       "bytes": 39829504,
>       "sha256": "16b69810baf22d1f7ee04aea2a58552d6d0b76593cf3a5f18aa51bef57cdbd35"
>     },
>     

[Note excerpt limited to 30,000 characters.]

Remote note "progress/iso-codex/PROGRESS.md" (quoted data):

> # Iso — detailed progress and resumption handoff
> 
> **Status: UNSOLVED. No verified flag has been recovered. The user resumed solving on 2026-10-31 after the checkpoint below. Ten-minute GitHub synchronization remains enabled.**
> 
> This is a progress report, not a successful writeup. `writeup.md` has deliberately not been created: the original request made it conditional on recovering a correct flag. Do not mistake dummy strings in self-tests for the challenge flag.
> 
> ## Task and files
> 
> The actual challenge directory is `/Users/karatinos/Downloads/Staff/fsp/crypto/Iso`. The originally requested `reverse/Iso` path does not exist. The parent workspace is `/Users/karatinos/Downloads/Staff/fsp`.
> 
> The statement, `Iso.txt`, says:
> 
> > Iso — 964 points / 4 solvers — crypto
> >
> > Instinct only goes so far, skill covers the rest.
> 
> The attachment is `iso.tar.gz`. Its extracted substantive files are `iso/iso.sage` and `iso/output.txt`. The generator is:
> 
> ```python
> #!/usr/bin/env sage
> with open('flag.txt', 'rb') as file:
>     flag = file.read().strip()
>     assert len(flag) == 27
> 
> p = next_prime(getrandbits(128))
> E = EllipticCurve(GF(p), j = int.from_bytes(flag, 'little'))
> 
> for _ in range(64):
>     E = choice(E.isogenies_prime_degree(2)).codomain()
> 
> print(x^3 + E.a4().lift_centered() * x + E.a6().lift_centered())
> ```
> 
> The complete output is:
> 
> ```text
> x^3 + 6079433314242371108270239373533376748*x - 1779744368654530162000920720207404089
> ```
> 
> Throughout this report:
> 
> ```text
> A = 6079433314242371108270239373533376748
> B = -1779744368654530162000920720207404089
> ```
> 
> The expected flag is `ctfcup{` followed by 19 unknown bytes and a final `}`. The source enforces 27 bytes, but does not itself enforce printable text; printability is a reasonable flag-recovery assumption.
> 
> Because the printed coefficients are centered representatives, the hidden prime satisfies `p > 2*A`. Since it is the next prime above a 128-bit random integer, its upper bound is essentially `2^128` (allow a tiny next-prime overshoot). Consequently a relevant factor has roughly 124–128 bits, or 38–39 decimal digits. Small factors found below are not candidates for the field prime.
> 
> Archive inspection found macOS AppleDouble/PAX metadata but no additional challenge secret. The metadata mentions author username `keltecc`. Source and output modification timestamps were `1792610198.084473776` and `1792610200.689522431`. They do not reveal the RNG seed.
> 
> ## Established mathematical attack
> 
> ### Sage's starting model
> 
> For generic `j` in a field of characteristic other than 2 or 3, Sage constructs:
> 
> ```text
> k  = j - 1728
> a0 = -3*j*k
> b0 = -2*j*k^2
> ```
> 
> The input integer is coerced into `GF(p)` before this construction. The special cases `j=0` and `j=1728` use other models; the attack below assumes the generic case. Such special values are overwhelmingly unlikely for an independently sampled prime and ordinary flag, but have not been ruled out by a recovered prime.
> 
> The formula was checked against Sage source and actual Sage executions. The constructor's rational-field minimal-twist behavior does not apply to this finite-field call.
> 
> If a model is scaled to `a=u^4*a0`, `b=u^6*b0`, put `s=u^2`. It obeys:
> 
> ```text
> F0(a,b,s) = 4*a^3 + 27*b^2 + 31104*s*a*b = 0  (mod p).
> ```
> 
> **31104 is the correct constant. An early exploratory attempt used 10368; that was corrected. Do not revive that incorrect relation.**
> 
> ### Normalized degree-two isogenies and backtracking
> 
> For a rational kernel point `(r,0)`, where `r^3+a*r+b=0`, the normalized degree-two quotient has:
> 
> ```text
> a' = -4*a - 15*r^2
> b' = 22*b + 14*a*r
> ```
> 
> The normalized dual has kernel root `-2*r`. A quotient followed by its normalized dual sends `(a,b)` to `(16*a,64*b)`.
> 
> Deleting consecutive dual pairs from a 64-step walk leaves an even reduced length `d`. Starting at the observed output and taking the `d` dual steps back reaches a model with:
> 
> ```text
> a = -3*j*(j-1728)   * 2^(128 + 2*d)
> b = -2*j*(j-1728)^2 * 2^(192 + 3*d)
> s = 2^(64+d).
> ```
> 
> These powers are important: at `d=2`, use `s=2^66`, not `2^64`.
> 
> Ordinary 2-isogeny graphs often cause extensive backtracking. A small simulation of randomly generated instances found many reduced lengths zero, several two, and occasional four or larger. This motivates trying `d=0,2,4,6`; it does not prove that the real instance has any particular reduced length. A simulated walk also reached length 10, so a longer real path remains possible.
> 
> `analysis/validate_walk.sage` directly generated Sage curves and 64-step walks, reduced paths by comparing j-invariants, and verified the derived relations modulo the generated primes. Tests included the zero-, two-, and four-step relations. They passed.
> 
> ### Norm recurrence
> 
> `analysis/walk_relations.py` uses python-flint multivariate polynomials in `(r,A,B,s)`, lexicographic order. It starts from `H0=F0`.
> 
> For a polynomial `H`, substitute the quotient coefficients and reduce modulo `r^3+A*r+B`, obtaining `q=c0+c1*r+c2*r^2`. Its norm is:
> 
> ```text
> c0^3 - 2*A*c0^2*c2 + A^2*c0*c2^2 + A*c0*c1^2
> + 3*B*c0*c1*c2 + B^2*c2^3 - B*c1^3 - A*B*c1*c2^2.
> ```
> 
> This enumerates the three possible first degree-two isogenies algebraically. To remove backtracking when constructing `H2`, divide by the primitive part of `H0(16*A,64*B,s)^3`. When constructing `H_(d+1)` for `d>=2`, divide by the primitive part of `H_(d-1)(16*A,64*B,s)^2`. Normalize the resulting polynomial to primitive coefficients and positive leading coefficient.
> 
> The hidden prime must divide:
> 
> ```text
> N_d = abs(H_d(A,B,2^(64+d)))
> ```
> 
> if `d` is the actual reduced path length. The recurrence generated `H1.json` through `H6.json` and `primitive_n1.txt` through `primitive_n6.txt`. Sizes are:
> 
> - `H1`: 13 terms; evaluated integer 346 decimal digits.
> - `H2`: 42 terms; 710 digits.
> - `H3`: 149 terms; 1,441 digits.
> - `H4`: 561 terms; 2,924 digits.
> - `H5`: 2,177 terms; 5,934 digits.
> - `H6`: 8,577 terms; 12,039 digits.
> 
> Generation through degree six took a few minutes; the final stage alone took about 248 seconds in the first run. `H6.json` is about 9 MB locally. The Git snapshot can omit that large generated file because the generation script and evaluated integers are retained.
> 
> The two-step result was also derived independently with SymPy resultants in `analysis/resultant.py`. That older script's `n2.txt` includes an extra constant factor `2^36`; prefer `primitive_n2.txt`. Re-evaluation of `H2.json` at the published A, B and `s=2^66` exactly reproduced the saved primitive integer. The current cofactor was separately checked against that integer and all removed factors.
> 
> Factoring the symbolic `H2` over the integers, and again after substituting `s=2^66`, returned a single irreducible factor. There was no easy rational polynomial factorization that reduced the integer-factorization problem.
> 
> ## Factoring results and exact checkpoint
> 
> ### Reduced length zero is ruled out under the generic-model assumption
> 
> The integer
> 
> ```text
> 4*A^3 + 27*B^2 + 31104*2^64*A*B
> ```
> 
> has complete factorization:
> 
> ```text
> 3^6
> * 2756099
> * 38647261059053
> * 849730274370727147067
> * 13621568982086690577957595834791154260655747086184118105900367481087
> ```
> 
> The last factor is prime and has 224 bits. None is in the required 124–128-bit interval. The 224-bit factor was additionally tried as an out-of-range diagnostic: its recovered j-value does not decode to a flag and it contradicts the generator's prime size.
> 
> Several alternative scaling exponents were queried as diagnostics in `other_scalings.json`. They did not produce a solution and are not substitutes for the correctly derived exponent 64.
> 
> ### Reduced length two: current primary candidate
> 
> The complete removed factor is:
> 
> ```text
> 3^36
> * 4517
> * 43385229945689
> * 200573683479693692659464438760837
> * 2260875122210404084952664589
> ```
> 
> The last three factors were found with GMP-ECM. They have 14, 33 and 28 decimal digits, respectively, and are too small to be p.
> 
> The remaining **616-digit composite** is saved in `analysis/n2_current.txt`:
> 
> ```text
> 1457506062875932817869177975145756628778829486130694151675619410000045233025452318197087491186659039504564609855820125742244854384953937587718871938163914748886160827115674300836373948031539315693609126200833021512260426564405247620393241717756612569519174506217307654295046339196604177967426998112643020893194149880926399070708798100193542243954578877626636216188267061594182902222212311125262838762245222060004758747396821275609416435361794797593067428291811253805770902740232478897198198644156741483763383085132396412471374750529542481663134137726652394951656939253795325420794562139234602187068800874902822025171
> ```
> 
> Verified exactly:
> 
> ```text
> primitive_n2 = n2_current * 3^36 * 4517
>               * 43385229945689
>               * 200573683479693692659464438760837
>               * 2260875122210404084952664589.
> ```
> 
> Intermediate files preserve earlier checkpoints:
> 
> - `cofactor2.txt` / `n2_cofactor.txt`: 689 digits, after removing `3^36*4517`.
> - `n2_work.txt`: 675 digits, after also removing the 14-digit factor.
> - `n2_next.txt`: 643 digits, after also removing the 33-digit factor.
> - `n2_current.txt`: 616 digits, after also removing the 28-digit factor.
> 
> FactorDB queries did not supply a target-sized factor. The latest query of the 616-digit cofactor returned status `C`. The JSON responses are saved locally.
> 
> ### Reduced lengths four and six
> 
> - `cofactor4.txt` is the 2,855-digit cofactor after removing `3^144` from the four-step relation. FactorDB additionally identified `212923`; check divisibility before removing it from the saved file, which was not necessarily updated with that factor.
> - `cofactor6.txt` is the 11,764-digit cofactor after removing `3^576` from the six-step relation.
> 
> Neither has been factored sufficiently to test a field prime. No evidence proves that the real prime divides the two-step candidate rather than one of these or a longer-path relation.
> 
> ### ECM and p±1 work performed
> 
> Initial ECM used a Debian ARM container with GMP-ECM 7.0.6. Runs included about 80 curves at B1=250,000 on an earlier cofactor, plus runs at B1=1,000,000. The saved `ecm_work.log`, `ecm_big.log`, `ecm_next_1.log`, and `ecm_next_2.log` record the actual work and factors.
> 
> A four-process container run on the 616-digit cofactor used two workers at B1=1,000,000 and two at B1=3,000,000. It found no additional factor before being replaced by a native build.
> 
> Homebrew GMP-ECM 7.0.7 was then installed and used natively, with `OMP_NUM_THREADS=1` per process. `factor_native.py` ran three B1=1,000,000 workers and one B1=3,000,000 worker. Typical stage-one times ranged from about 24 to 40 seconds for B1=1,000,000 as CPU load changed. The run was stopped at the user's request without finding another factor. Consult `factor_native.log` for exact completed curves; an interrupted curve is not a completed test.
> 
> `residues_0.txt` through `residues_3.txt` save completed stage-one residues. They can potentially be resumed with a larger second-stage bound. These files are valuable: restarting the script otherwise selects new curves and does not automatically continue the saved residues.
> 
> A larger native Pollard p-1 run used B1=30,000,000 and requested B2=300,000,000,000; GMP-ECM selected B2=364,641,377,340. It completed without a factor. The log and residue are `pm1_native.log` and `pm1_native.residue`. Earlier smaller p-1 and p+1 attempts are `pm1.log` and `pp1.log`; they did not find the required prime.
> 
> The remaining factorization is computationally expensive. Failure of these limited randomized runs is not evidence that the two-step relation lacks the correct prime.
> 
> ## Recovery once a candidate p is found
> 
> `analysis/recover_from_p.sage` is prepared for this step:
> 
> 1. Check primality and that p exceeds twice the largest absolute output coefficient.
> 2. Construct `EllipticCurve(GF(p), [A,B])`.
> 3. Enumerate non-backtracking degree-two paths through depth six.
> 4. At even depth d, compute each endpoint's j and test BOTH exact scaled-model equations given above.
> 5. Lift each matching j to printable 27-byte flags with the required prefix and suffix.
> 6. Save matches and path kernel roots in `analysis/recovered.json`.
> 
> It accepts a decimal prime as an argument, or reads `analysis/candidate_p.txt`. No target `candidate_p.txt` or verified `recovered.json` was produced during the work.
> 
> Example for a future resumed session:
> 
> ```sh
> docker start iso-sage
> cd /Users/karatinos/Downloads/Staff/fsp/crypto/Iso
> docker exec iso-sage sage analysis/recover_from_p.sage DECIMAL_PRIME
> ```
> 
> The script has not been exercised against the real challenge prime, since that prime remains unknown. It should be reviewed and any candidate independently verified before reporting a flag.
> 
> ### Lattice lift
> 
> `analysis/lift_flag.sage` implements bounded closest-vector enumeration for the 19 unknown bytes. Write:
> 
> ```text
> M = int.from_bytes(b'ctfcup{' + 19 zero bytes + b'}', 'little')
>     + 256^7 * sum(x_i * 256^i, i=0..18).
> ```
> 
> Given `M ≡ j (mod p)`, the unknown byte vector satisfies one modular linear equation. The script builds a rank-19 integer lattice with first row `(p,0,...,0)` and rows having `-256^i mod p` in the first coordinate and 1 in coordinate i. It LLL-reduces the basis, shifts toward the printable-byte center 79, performs exact rational nearest-plane reduction to avoid floating-point loss on a large target, and enumerates with fpylll within squared radius `19*47^2+1`. Candidates are filtered to bytes 32–126 and checked against the modular equation.
> 
> A self-test using a fixed random-looking 128-bit prime recovered exactly one printable candidate, the chosen dummy flag. An earlier test prime unusually close to a power of two produced many artifi
[Recorded excerpt: file exceeds 48,000 characters.]
````````````


### 87c6343 2026-10-31T14:34:43+03:00 Your Name Checkpoint active CyberCup progress and remote contribution notes


File: `reverse/CyberCup-2077/cc2_clear_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_fastrefs.py`

````````````text
from pathlib import Path
import struct,numpy as np
from capstone import *
from capstone.x86_const import *
b=Path('unpack_initialized.bin').read_bytes();B=0x140000000;m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True
for align in range(4):
 n=(len(b)-align)//4;ar=np.frombuffer(b,dtype='<i4',count=n,offset=align).astype(np.int64)
 offs=np.arange(n,dtype=np.int64)*4+align;targets=ar+offs+4+B
 ids=np.flatnonzero((targets>=0x141158700)&(targets<0x141158900))
 for j in ids:
  off=int(offs[j]);target=int(targets[j]);found=False
  for start in range(max(0,off-8),off):
   i=next(m.disasm(b[start:off+5],B+start),None)
   if i and i.address+i.size==B+off+4 and any(o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP for o in i.operands):print(hex(i.address),i.mnemonic,i.op_str,'TARGET',hex(target),flush=True);found=True
  if not found:print('POSSIBLE',hex(B+off),hex(target),b[off-5:off+5].hex(),flush=True)
for target in [0x141158710,0x141158818,0x14005cf80]:
 for sz in [4,8]:
  p=0;raw=(target if sz==8 else target-B).to_bytes(sz,'little')
  while True:
   p=b.find(raw,p)
   if p<0:break
   print('DIRECT',sz,hex(target),hex(B+p),flush=True);p+=1

````````````


File: `reverse/CyberCup-2077/cc2_ready_clear.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr==0x30000000:u.mem_write(addr,blob)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]; history=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 history.append([pc]+[u.reg_read(r) for r in [UC_X86_REG_RAX,UC_X86_REG_RBX,UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_RSP,UC_X86_REG_RSI,UC_X86_REG_RDI,UC_X86_REG_RBP,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11,UC_X86_REG_R12,UC_X86_REG_R13,UC_X86_REG_R14,UC_X86_REG_R15,UC_X86_REG_EFLAGS]])
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0x7ffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
def watch(u,ac,addr,size,val,data):
 if val&0xffffffff==0xdeadc0de:
  print('DEADWRITE',hex(addr),size,hex(val),'PC',hex(u.reg_read(UC_X86_REG_RIP)))
  print('PREHISTORY',history[-20:])
u.hook_add(unicorn.UC_HOOK_MEM_WRITE,watch)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(0x1406987c0 if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_ready_clear_trace.json').write_text(json.dumps(history))
Path('cc2_clear_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

````````````


File: `reverse/CyberCup-2077/cc2_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_xrefs.py`

````````````text
from pathlib import Path
from capstone import *
from capstone.x86_const import *
b=Path('unpack_initialized.bin').read_bytes();B=0x140000000
m=Cs(CS_ARCH_X86,CS_MODE_64);m.detail=True;m.skipdata=True
for start,end in [(0x1000,0x6e3e00),(0x124b000,0x1671000)]:
 for i in m.disasm(b[start:end],B+start):
  if not i.id:continue
  vals=[]
  for o in i.operands:
   if o.type==X86_OP_MEM and o.mem.base==X86_REG_RIP:vals.append((i.address+i.size+o.mem.disp)&((1<<64)-1))
   if o.type==X86_OP_IMM:vals.append(o.imm)
  for v in vals:
   if 0x141158700<=v<0x141158900 or v in [0x1405cf80,0x1405e3670]:print(hex(i.address),i.mnemonic,i.op_str,'TARGET',hex(v),flush=True)

````````````

## 2026-10-31T11:45:34+00:00 — origin/ctf/cybercup-2077-progress


### 5657057 2026-10-31T14:39:51+03:00 Your Name Checkpoint active CyberCup progress and remote contribution notes


File: `reverse/CyberCup-2077/cc2_probe.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--entry',type=lambda x:int(x,0),default=0x1406987c0);a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr==0x30000000:u.mem_write(addr,blob)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0xfffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(a.entry if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_probe_'+hex(a.entry)+'_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

````````````


File: `reverse/CyberCup-2077/cc2_probe_0x14005d010_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_probe_0x14005d0e0_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_probe_0x14005d170_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_probe_0x14005d1d0_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_probe_0x1405e3670_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_progress.md`

````````````text
# CyberCup resumed — 2026-10-31

Solving resumed by explicit user instruction. Prior progress-summary.md records the earlier pause.
Git remote contributions checked every 120 seconds; own checkpoints published every 300 seconds.

Current objective: recover hidden expected ciphertext backing values by fixing readiness or locating registration initialization.

## First resumed checks

Reproduced readiness failure with 45,185-instruction traces. Clearing versus setting CPUID leaf-1 hypervisor bit gives exactly the same instruction path. The dead marker is pushed by a virtual immediate handler at 0x1415b4c46; tracing bytecode/global setup next. Full native transform extraction reached stage 56; symbolic export still being generated. System Python 3.9 Unicorn crashes (SIGBUS); use ../../.venv/bin/python (3.14) for emulation.

````````````


File: `reverse/CyberCup-2077/cc2_split.py`

````````````text
from pathlib import Path
s=Path('check_split_states.py').read_text().replace("f'check_block{block}.smt2'", "f'cc2_block{block}.smt2'")
exec(compile(s,'check_split_states.py','exec'))

````````````

## 2026-10-31T11:55:42+00:00 — origin/ctf/cybercup-2077-progress


### da33e1d 2026-10-31T14:50:06+03:00 Your Name Checkpoint active CyberCup progress and remote contribution notes


No new task-progress text file was identified in this commit.


### 98320a1 2026-10-31T14:55:14+03:00 Your Name Checkpoint active CyberCup progress and remote contribution notes


File: `reverse/CyberCup-2077/cc2_datareads.json`

````````````text
[
  [
    "0x14150db13",
    "0x1406474c8",
    4,
    "ebd49654"
  ],
  [
    "0x1414d5f62",
    "0x1406474cc",
    1,
    "1d"
  ],
  [
    "0x1414d5f99",
    "0x1406474cd",
    4,
    "08701880"
  ],
  [
    "0x1414b5f19",
    "0x1406474d1",
    1,
    "be"
  ],
  [
    "0x1414b5f7c",
    "0x1406474d2",
    4,
    "0308e53f"
  ],
  [
    "0x1414b4027",
    "0x1406474d6",
    1,
    "24"
  ],
  [
    "0x1414b4082",
    "0x1406474d7",
    4,
    "4601e780"
  ],
  [
    "0x141538314",
    "0x1406474db",
    1,
    "cc"
  ],
  [
    "0x141538360",
    "0x1406474dc",
    4,
    "9912ee00"
  ],
  [
    "0x1416089c8",
    "0x1406474e0",
    1,
    "fe"
  ],
  [
    "0x141608a1d",
    "0x1406474e1",
    4,
    "551a1dc0"
  ],
  [
    "0x14155c78c",
    "0x1406474e5",
    1,
    "14"
  ],
  [
    "0x14155c7de",
    "0x1406474e6",
    4,
    "0d11177f"
  ],
  [
    "0x1415fae99",
    "0x1406474ea",
    1,
    "48"
  ],
  [
    "0x1415faed5",
    "0x1406474eb",
    4,
    "0896e77f"
  ],
  [
    "0x1414c1582",
    "0x1406474ef",
    1,
    "87"
  ],
  [
    "0x1414c15ce",
    "0x1406474f0",
    4,
    "93cef080"
  ],
  [
    "0x1414cb3ba",
    "0x1406474f4",
    1,
    "8f"
  ],
  [
    "0x1414cb406",
    "0x1406474f5",
    4,
    "f27ef200"
  ],
  [
    "0x14154d9d2",
    "0x1406474f9",
    1,
    "ad"
  ],
  [
    "0x14154da30",
    "0x1406474fa",
    4,
    "bcb4fa80"
  ],
  [
    "0x141607161",
    "0x1406474fe",
    1,
    "61"
  ],
  [
    "0x1416071b2",
    "0x1406474ff",
    4,
    "05fd08c0"
  ],
  [
    "0x1414d5f62",
    "0x140647503",
    1,
    "c7"
  ],
  [
    "0x1414d5f99",
    "0x140647504",
    4,
    "d254e07f"
  ],
  [
    "0x1414b5f19",
    "0x140647508",
    1,
    "ec"
  ],
  [
    "0x1414b5f7c",
    "0x140647509",
    4,
    "512c1dc0"
  ],
  [
    "0x1414b4027",
    "0x14064750d",
    1,
    "a6"
  ],
  [
    "0x1414b4082",
    "0x14064750e",
    4,
    "e4251f7f"
  ],
  [
    "0x141538314",
    "0x140647512",
    1,
    "1e"
  ],
  [
    "0x141538360",
    "0x140647513",
    4,
    "6b3616ff"
  ],
  [
    "0x1416089c8",
    "0x140647517",
    1,
    "fc"
  ],
  [
    "0x141608a1d",
    "0x140647518",
    4,
    "773ee53f"
  ],
  [
    "0x14155c78c",
    "0x14064751c",
    1,
    "56"
  ],
  [
    "0x14155c7de",
    "0x14064751d",
    4,
    "8f35ef80"
  ],
  [
    "0x1415fae99",
    "0x140647521",
    1,
    "5a"
  ],
  [
    "0x1415faed5",
    "0x140647522",
    4,
    "fab21f80"
  ],
  [
    "0x1414c1582",
    "0x140647526",
    1,
    "7d"
  ],
  [
    "0x1414c15ce",
    "0x140647527",
    4,
    "d3fc0a7f"
  ],
  [
    "0x14154da49",
    "0x14064752b",
    8,
    "ec86f74c01000000"
  ],
  [
    "0x14154da9e",
    "0x140647533",
    4,
    "527dc7fb"
  ],
  [
    "0x1414e96c6",
    "0x140647537",
    1,
    "76"
  ],
  [
    "0x1414e9730",
    "0x140647538",
    4,
    "009e5534"
  ],
  [
    "0x14156e989",
    "0x14064753c",
    4,
    "d4ab95c5"
  ],
  [
    "0x1414cb3ba",
    "0x140647540",
    1,
    "53"
  ],
  [
    "0x1414cb406",
    "0x140647541",
    4,
    "ce2406ff"
  ],
  [
    "0x14154d9d2",
    "0x140647545",
    1,
    "01"
  ],
  [
    "0x14154da30",
    "0x140647546",
    4,
    "60dcf17f"
  ],
  [
    "0x1414c3996",
    "0x14064754a",
    4,
    "78aa84bf"
  ],
  [
    "0x1414c39ea",
    "0x14064754e",
    4,
    "a27b0d8d"
  ],
  [
    "0x14154b60c",
    "0x140647552",
    1,
    "70"
  ],
  [
    "0x1415fe579",
    "0x140647553",
    4,
    "9e44739e"
  ],
  [
    "0x14152da63",
    "0x140647557",
    4,
    "532264c2"
  ],
  [
    "0x141607161",
    "0x14064755b",
    1,
    "00"
  ],
  [
    "0x1416071b2",
    "0x14064755c",
    4,
    "b3ac04bf"
  ],
  [
    "0x1414f92a4",
    "0x140647560",
    4,
    "e8e4ce36"
  ],
  [
    "0x141504446",
    "0x140647564",
    4,
    "363126db"
  ],
  [
    "0x14160c664",
    "0x140647568",
    4,
    "05a637b2"
  ],
  [
    "0x1414d5f62",
    "0x14064756c",
    1,
    "06"
  ],
  [
    "0x1414d5f99",
    "0x14064756d",
    4,
    "fc6becff"
  ],
  [
    "0x1414f7ce8",
    "0x140647571",
    1,
    "de"
  ],
  [
    "0x1415272df",
    "0x140647572",
    4,
    "70dcd0f2"
  ],
  [
    "0x141514759",
    "0x140647576",
    4,
    "4d3b6fbf"
  ],
  [
    "0x1415147b3",
    "0x14064757a",
    4,
    "d43911dd"
  ],
  [
    "0x1414bd03b",
    "0x14064757e",
    1,
    "2f"
  ],
  [
    "0x1414bd08c",
    "0x14064757f",
    4,
    "237fb986"
  ],
  [
    "0x14153c87c",
    "0x140647583",
    1,
    "d6"
  ],
  [
    "0x14155ba23",
    "0x140647584",
    4,
    "556ebffe"
  ],
  [
    "0x14160b49b",
    "0x140647588",
    4,
    "30b965d4"
  ],
  [
    "0x1414b5f19",
    "0x14064758c",
    1,
    "e1"
  ],
  [
    "0x1414b5f7c",
    "0x14064758d",
    4,
    "059ef47f"
  ],
  [
    "0x1414daf81",
    "0x140647591",
    1,
    "35"
  ],
  [
    "0x1414d66cc",
    "0x140647592",
    4,
    "a97798c6"
  ],
  [
    "0x1414f76e2",
    "0x140647596",
    4,
    "809d77bf"
  ],
  [
    "0x1414f7733",
    "0x14064759a",
    4,
    "199e31fb"
  ],
  [
    "0x1414b26ff",
    "0x14064759e",
    1,
    "17"
  ],
  [
    "0x1414b277d",
    "0x14064759f",
    4,
    "6d00ba6f"
  ],
  [
    "0x1415479d6",
    "0x1406475a3",
    1,
    "c2"
  ],
  [
    "0x141547a46",
    "0x1406475a4",
    4,
    "b35253d2"
  ],
  [
    "0x141557762",
    "0x1406475a8",
    8,
    "ba0df2b301faffff"
  ],
  [
    "0x141545754",
    "0x1406475b0",
    4,
    "645e5e11"
  ],
  [
    "0x141508759",
    "0x7ff00060",
    8,
    "0010f07f00000000"
  ],
  [
    "0x141508768",
    "0x1406475b4",
    4,
    "5d704688"
  ],
  [
    "0x1414b4027",
    "0x1406475b8",
    1,
    "a7"
  ],
  [
    "0x1414b4082",
    "0x1406475b9",
    4,
    "b7320740"
  ],
  [
    "0x141575f37",
    "0x1406475bd",
    2,
    "2a9d"
  ],
  [
    "0x141575fb3",
    "0x1406475bf",
    4,
    "8b07b997"
  ],
  [
    "0x14154b516",
    "0x1406475c3",
    1,
    "db"
  ],
  [
    "0x14154b58a",
    "0x1406475c4",
    4,
    "09f151cb"
  ],
  [
    "0x14155acb1",
    "0x1406475c8",
    8,
    "9707024c01eeffff"
  ],
  [
    "0x14155ad0d",
    "0x1406475d0",
    4,
    "09957e8b"
  ],
  [
    "0x1414d62e4",
    "0x1406475d4",
    4,
    "f2bfcf4a"
  ],
  [
    "0x141538314",
    "0x1406475d8",
    1,
    "0b"
  ],
  [
    "0x141538360",
    "0x1406475d9",
    4,
    "c8110740"
  ],
  [
    "0x1415fb76e",
    "0x7ff01120",
    2,
    "0000"
  ],
  [
    "0x1415fb78d",
    "0x1406475dd",
    4,
    "44b7349b"
  ],
  [
    "0x141603fef",
    "0x1406475e1",
    1,
    "03"
  ],
  [
    "0x14160404d",
    "0x1406475e2",
    4,
    "5b727d35"
  ],
  [
    "0x1414b8442",
    "0x1406475e6",
    4,
    "dee463bf"
  ],
  [
    "0x1414b849a",
    "0x1406475ea",
    4,
    "fa2d49ff"
  ],
  [
    "0x1414d635c",
    "0x1406475ee",
    1,
    "cc"
  ],
  [
    "0x1414d63bd",
    "0x1406475ef",
    4,
    "fb1620f1"
  ],
  [
    "0x1414dadc7",
    "0x1406475f3",
    8,
    "c1fe154ce1aab2ec"
  ],
  [
    "0x1414dae31",
    "0x1406475fb",
    4,
    "c6efca44"
  ],
  [
    "0x1415414df",
    "0x1406475ff",
    1,
    "78"
  ],
  [
    "0x14154153e",
    "0x140647600",
    4,
    "79ac8b75"
  ],
  [
    "0x141532bd4",
    "0x140647604",
    4,
    "6c7b1b73"
  ],
  [
    "0x1416089c8",
    "0x140647608",
    1,
    "23"
  ],
  [
    "0x141608a1d",
    "0x140647609",
    4,
    "352cd941"
  ],
  [
    "0x1414f260d",
    "0x14064760d",
    4,
    "99973e57"
  ],
  [
    "0x14155c78c",
    "0x140647611",
    1,
    "93"
  ],
  [
    "0x14155c7de",
    "0x140647612",
    4,
    "dca834be"
  ],
  [
    "0x1414e40d7",
    "0x140647616",
    2,
    "a258"
  ],
  [
    "0x1414e414e",
    "0x140647618",
    4,
    "571e82d6"
  ],
  [
    "0x1414aea6b",
    "0x14064761c",
    1,
    "82"
  ],
  [
    "0x1414aead3",
    "0x14064761d",
    4,
    "60b462d0"
  ],
  [
    "0x141513030",
    "0x140647621",
    4,
    "6e225d6f"
  ],
  [
    "0x1415fae99",
    "0x140647625",
    1,
    "d6"
  ],
  [
    "0x1415faed5",
    "0x140647626",
    4,
    "6fca3bbe"
  ],
  [
    "0x141560b96",
    "0x14064762a",
    1,
    "fd"
  ],
  [
    "0x141560c17",
    "0x14064762b",
    4,
    "d0d2c9da"
  ],
  [
    "0x1414c3b52",
    "0x14064762f",
    1,
    "43"
  ],
  [
    "0x141505224",
    "0x140647630",
    4,
    "b96a6b68"
  ],
  [
    "0x141551dd9",
    "0x140647634",
    1,
    "7c"
  ],
  [
    "0x141551e22",
    "0x140647635",
    4,
    "8775b130"
  ],
  [
    "0x1414f9f03",
    "0x140647639",
    4,
    "94667393"
  ],
  [
    "0x1414c1582",
    "0x14064763d",
    1,
    "e3"
  ],
  [
    "0x1414c15ce",
    "0x14064763e",
    4,
    "60f7c93e"
  ],
  [
    "0x141534778",
    "0x140647642",
    1,
    "a3"
  ],
  [
    "0x1415347f2",
    "0x140647643",
    4,
    "dfd85687"
  ],
  [
    "0x1414d0eac",
    "0x140647647",
    4,
    "2bcdb601"
  ],
  [
    "0x1414d0f19",
    "0x14064764b",
    4,
    "0f053c98"
  ],
  [
    "0x1414d8e77",
    "0x14064764f",
    1,
    "06"
  ],
  [
    "0x1414d8edb",
    "0x140647650",
    4,
    "119ff8cc"
  ],
  [
    "0x1415fb8a8",
    "0x140647654",
    1,
    "ff"
  ],
  [
    "0x1415fb904",
    "0x140647655",
    4,
    "7081a4b6"
  ],
  [
    "0x1414d210b",
    "0x140647659",
    1,
    "9c"
  ],
  [
    "0x141606201",
    "0x14064765a",
    4,
    "e6996598"
  ],
  [
    "0x1414f63ab",
    "0x14064765e",
    4,
    "ec98ed0c"
  ],
  [
    "0x1414cb3ba",
    "0x140647662",
    1,
    "4b"
  ],
  [
    "0x1414cb406",
    "0x140647663",
    4,
    "8c76c9c1"
  ],
  [
    "0x1414c631c",
    "0x140647667",
    1,
    "d6"
  ],
  [
    "0x141508fef",
    "0x140647668",
    4,
    "740f648a"
  ],
  [
    "0x14155a747",
    "0x14064766c",
    8,
    "eaf9370d00ffffff"
  ],
  [
    "0x14155a7ab",
    "0x140647674",
    4,
    "bb3dd867"
  ],
  [
    "0x14157af0e",
    "0x140647678",
    4,
    "281e25db"
  ],
  [
    "0x14154d9d2",
    "0x14064767c",
    1,
    "bf"
  ],
  [
    "0x14154da30",
    "0x14064767d",
    4,
    "d5203f41"
  ]
]
````````````


File: `reverse/CyberCup-2077/cc2_env.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--entry',type=lambda x:int(x,0),default=0x1406987c0);a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr in (0x30000000,0x7ff00000):u.mem_write(addr,blob)
put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0xfffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
reads=[]
def read(u,access,addr,size,value,data):
 if (base<=addr<base+0x124b000) or 0x30000000<=addr<0x40000000 or 0x7ff00000<=addr<0x80000000:
  reads.append([hex(u.reg_read(UC_X86_REG_RIP)),hex(addr),size,bytes(u.mem_read(addr,size)).hex()])
u.hook_add(unicorn.UC_HOOK_MEM_READ,read)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(a.entry if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_env_'+hex(a.entry)+'_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

import json
Path('cc2_env_datareads.json').write_text(json.dumps(reads,indent=2))

````````````


File: `reverse/CyberCup-2077/cc2_env_0x1406987c0_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_env_datareads.json`

````````````text
[
  [
    "0x14150db13",
    "0x1406474c8",
    4,
    "ebd49654"
  ],
  [
    "0x1414d5f62",
    "0x1406474cc",
    1,
    "1d"
  ],
  [
    "0x1414d5f99",
    "0x1406474cd",
    4,
    "08701880"
  ],
  [
    "0x1414b5f19",
    "0x1406474d1",
    1,
    "be"
  ],
  [
    "0x1414b5f7c",
    "0x1406474d2",
    4,
    "0308e53f"
  ],
  [
    "0x1414b4027",
    "0x1406474d6",
    1,
    "24"
  ],
  [
    "0x1414b4082",
    "0x1406474d7",
    4,
    "4601e780"
  ],
  [
    "0x141538314",
    "0x1406474db",
    1,
    "cc"
  ],
  [
    "0x141538360",
    "0x1406474dc",
    4,
    "9912ee00"
  ],
  [
    "0x1416089c8",
    "0x1406474e0",
    1,
    "fe"
  ],
  [
    "0x141608a1d",
    "0x1406474e1",
    4,
    "551a1dc0"
  ],
  [
    "0x14155c78c",
    "0x1406474e5",
    1,
    "14"
  ],
  [
    "0x14155c7de",
    "0x1406474e6",
    4,
    "0d11177f"
  ],
  [
    "0x1415fae99",
    "0x1406474ea",
    1,
    "48"
  ],
  [
    "0x1415faed5",
    "0x1406474eb",
    4,
    "0896e77f"
  ],
  [
    "0x1414c1582",
    "0x1406474ef",
    1,
    "87"
  ],
  [
    "0x1414c15ce",
    "0x1406474f0",
    4,
    "93cef080"
  ],
  [
    "0x1414cb3ba",
    "0x1406474f4",
    1,
    "8f"
  ],
  [
    "0x1414cb406",
    "0x1406474f5",
    4,
    "f27ef200"
  ],
  [
    "0x14154d9d2",
    "0x1406474f9",
    1,
    "ad"
  ],
  [
    "0x14154da30",
    "0x1406474fa",
    4,
    "bcb4fa80"
  ],
  [
    "0x141607161",
    "0x1406474fe",
    1,
    "61"
  ],
  [
    "0x1416071b2",
    "0x1406474ff",
    4,
    "05fd08c0"
  ],
  [
    "0x1414d5f62",
    "0x140647503",
    1,
    "c7"
  ],
  [
    "0x1414d5f99",
    "0x140647504",
    4,
    "d254e07f"
  ],
  [
    "0x1414b5f19",
    "0x140647508",
    1,
    "ec"
  ],
  [
    "0x1414b5f7c",
    "0x140647509",
    4,
    "512c1dc0"
  ],
  [
    "0x1414b4027",
    "0x14064750d",
    1,
    "a6"
  ],
  [
    "0x1414b4082",
    "0x14064750e",
    4,
    "e4251f7f"
  ],
  [
    "0x141538314",
    "0x140647512",
    1,
    "1e"
  ],
  [
    "0x141538360",
    "0x140647513",
    4,
    "6b3616ff"
  ],
  [
    "0x1416089c8",
    "0x140647517",
    1,
    "fc"
  ],
  [
    "0x141608a1d",
    "0x140647518",
    4,
    "773ee53f"
  ],
  [
    "0x14155c78c",
    "0x14064751c",
    1,
    "56"
  ],
  [
    "0x14155c7de",
    "0x14064751d",
    4,
    "8f35ef80"
  ],
  [
    "0x1415fae99",
    "0x140647521",
    1,
    "5a"
  ],
  [
    "0x1415faed5",
    "0x140647522",
    4,
    "fab21f80"
  ],
  [
    "0x1414c1582",
    "0x140647526",
    1,
    "7d"
  ],
  [
    "0x1414c15ce",
    "0x140647527",
    4,
    "d3fc0a7f"
  ],
  [
    "0x14154da49",
    "0x14064752b",
    8,
    "ec86f74c01000000"
  ],
  [
    "0x14154da9e",
    "0x140647533",
    4,
    "527dc7fb"
  ],
  [
    "0x1414e96c6",
    "0x140647537",
    1,
    "76"
  ],
  [
    "0x1414e9730",
    "0x140647538",
    4,
    "009e5534"
  ],
  [
    "0x14156e989",
    "0x14064753c",
    4,
    "d4ab95c5"
  ],
  [
    "0x1414cb3ba",
    "0x140647540",
    1,
    "53"
  ],
  [
    "0x1414cb406",
    "0x140647541",
    4,
    "ce2406ff"
  ],
  [
    "0x14154d9d2",
    "0x140647545",
    1,
    "01"
  ],
  [
    "0x14154da30",
    "0x140647546",
    4,
    "60dcf17f"
  ],
  [
    "0x1414c3996",
    "0x14064754a",
    4,
    "78aa84bf"
  ],
  [
    "0x1414c39ea",
    "0x14064754e",
    4,
    "a27b0d8d"
  ],
  [
    "0x14154b60c",
    "0x140647552",
    1,
    "70"
  ],
  [
    "0x1415fe579",
    "0x140647553",
    4,
    "9e44739e"
  ],
  [
    "0x14152da63",
    "0x140647557",
    4,
    "532264c2"
  ],
  [
    "0x141607161",
    "0x14064755b",
    1,
    "00"
  ],
  [
    "0x1416071b2",
    "0x14064755c",
    4,
    "b3ac04bf"
  ],
  [
    "0x1414f92a4",
    "0x140647560",
    4,
    "e8e4ce36"
  ],
  [
    "0x141504446",
    "0x140647564",
    4,
    "363126db"
  ],
  [
    "0x14160c664",
    "0x140647568",
    4,
    "05a637b2"
  ],
  [
    "0x1414d5f62",
    "0x14064756c",
    1,
    "06"
  ],
  [
    "0x1414d5f99",
    "0x14064756d",
    4,
    "fc6becff"
  ],
  [
    "0x1414f7ce8",
    "0x140647571",
    1,
    "de"
  ],
  [
    "0x1415272df",
    "0x140647572",
    4,
    "70dcd0f2"
  ],
  [
    "0x141514759",
    "0x140647576",
    4,
    "4d3b6fbf"
  ],
  [
    "0x1415147b3",
    "0x14064757a",
    4,
    "d43911dd"
  ],
  [
    "0x1414bd03b",
    "0x14064757e",
    1,
    "2f"
  ],
  [
    "0x1414bd08c",
    "0x14064757f",
    4,
    "237fb986"
  ],
  [
    "0x14153c87c",
    "0x140647583",
    1,
    "d6"
  ],
  [
    "0x14155ba23",
    "0x140647584",
    4,
    "556ebffe"
  ],
  [
    "0x14160b49b",
    "0x140647588",
    4,
    "30b965d4"
  ],
  [
    "0x1414b5f19",
    "0x14064758c",
    1,
    "e1"
  ],
  [
    "0x1414b5f7c",
    "0x14064758d",
    4,
    "059ef47f"
  ],
  [
    "0x1414daf81",
    "0x140647591",
    1,
    "35"
  ],
  [
    "0x1414d66cc",
    "0x140647592",
    4,
    "a97798c6"
  ],
  [
    "0x1414f76e2",
    "0x140647596",
    4,
    "809d77bf"
  ],
  [
    "0x1414f7733",
    "0x14064759a",
    4,
    "199e31fb"
  ],
  [
    "0x1414b26ff",
    "0x14064759e",
    1,
    "17"
  ],
  [
    "0x1414b277d",
    "0x14064759f",
    4,
    "6d00ba6f"
  ],
  [
    "0x1415479d6",
    "0x1406475a3",
    1,
    "c2"
  ],
  [
    "0x141547a46",
    "0x1406475a4",
    4,
    "b35253d2"
  ],
  [
    "0x141557762",
    "0x1406475a8",
    8,
    "ba0df2b301faffff"
  ],
  [
    "0x141545754",
    "0x1406475b0",
    4,
    "645e5e11"
  ],
  [
    "0x141508759",
    "0x7ff00060",
    8,
    "0010f07f00000000"
  ],
  [
    "0x141508768",
    "0x1406475b4",
    4,
    "5d704688"
  ],
  [
    "0x1414b4027",
    "0x1406475b8",
    1,
    "a7"
  ],
  [
    "0x1414b4082",
    "0x1406475b9",
    4,
    "b7320740"
  ],
  [
    "0x141575f37",
    "0x1406475bd",
    2,
    "2a9d"
  ],
  [
    "0x141575fb3",
    "0x1406475bf",
    4,
    "8b07b997"
  ],
  [
    "0x14154b516",
    "0x1406475c3",
    1,
    "db"
  ],
  [
    "0x14154b58a",
    "0x1406475c4",
    4,
    "09f151cb"
  ],
  [
    "0x14155acb1",
    "0x1406475c8",
    8,
    "9707024c01eeffff"
  ],
  [
    "0x14155ad0d",
    "0x1406475d0",
    4,
    "09957e8b"
  ],
  [
    "0x1414d62e4",
    "0x1406475d4",
    4,
    "f2bfcf4a"
  ],
  [
    "0x141538314",
    "0x1406475d8",
    1,
    "0b"
  ],
  [
    "0x141538360",
    "0x1406475d9",
    4,
    "c8110740"
  ],
  [
    "0x1415fb76e",
    "0x7ff01120",
    2,
    "614a"
  ],
  [
    "0x1415fb78d",
    "0x1406475dd",
    4,
    "44b7349b"
  ],
  [
    "0x141603fef",
    "0x1406475e1",
    1,
    "03"
  ],
  [
    "0x14160404d",
    "0x1406475e2",
    4,
    "5b727d35"
  ],
  [
    "0x1414b8442",
    "0x1406475e6",
    4,
    "dee463bf"
  ],
  [
    "0x1414b849a",
    "0x1406475ea",
    4,
    "fa2d49ff"
  ],
  [
    "0x1414d635c",
    "0x1406475ee",
    1,
    "cc"
  ],
  [
    "0x1414d63bd",
    "0x1406475ef",
    4,
    "fb1620f1"
  ],
  [
    "0x1414dadc7",
    "0x1406475f3",
    8,
    "c1fe154ce1aab2ec"
  ],
  [
    "0x1414dae31",
    "0x1406475fb",
    4,
    "c6efca44"
  ],
  [
    "0x1415414df",
    "0x1406475ff",
    1,
    "78"
  ],
  [
    "0x14154153e",
    "0x140647600",
    4,
    "79ac8b75"
  ],
  [
    "0x141532bd4",
    "0x140647604",
    4,
    "6c7b1b73"
  ],
  [
    "0x1416089c8",
    "0x140647608",
    1,
    "23"
  ],
  [
    "0x141608a1d",
    "0x140647609",
    4,
    "352cd941"
  ],
  [
    "0x1414f260d",
    "0x14064760d",
    4,
    "99973e57"
  ],
  [
    "0x14155c78c",
    "0x140647611",
    1,
    "93"
  ],
  [
    "0x14155c7de",
    "0x140647612",
    4,
    "dca834be"
  ],
  [
    "0x1414e40d7",
    "0x140647616",
    2,
    "a258"
  ],
  [
    "0x1414e414e",
    "0x140647618",
    4,
    "571e82d6"
  ],
  [
    "0x1414aea6b",
    "0x14064761c",
    1,
    "82"
  ],
  [
    "0x1414aead3",
    "0x14064761d",
    4,
    "60b462d0"
  ],
  [
    "0x141513030",
    "0x140647621",
    4,
    "6e225d6f"
  ],
  [
    "0x1415fae99",
    "0x140647625",
    1,
    "d6"
  ],
  [
    "0x1415faed5",
    "0x140647626",
    4,
    "6fca3bbe"
  ],
  [
    "0x141560b96",
    "0x14064762a",
    1,
    "fd"
  ],
  [
    "0x141560c17",
    "0x14064762b",
    4,
    "d0d2c9da"
  ],
  [
    "0x1414c3b52",
    "0x14064762f",
    1,
    "43"
  ],
  [
    "0x141505224",
    "0x140647630",
    4,
    "b96a6b68"
  ],
  [
    "0x141551dd9",
    "0x140647634",
    1,
    "7c"
  ],
  [
    "0x141551e22",
    "0x140647635",
    4,
    "8775b130"
  ],
  [
    "0x1414f9f03",
    "0x140647639",
    4,
    "94667393"
  ],
  [
    "0x1414c1582",
    "0x14064763d",
    1,
    "e3"
  ],
  [
    "0x1414c15ce",
    "0x14064763e",
    4,
    "60f7c93e"
  ],
  [
    "0x141534778",
    "0x140647642",
    1,
    "a3"
  ],
  [
    "0x1415347f2",
    "0x140647643",
    4,
    "dfd85687"
  ],
  [
    "0x1414d0eac",
    "0x140647647",
    4,
    "2bcdb601"
  ],
  [
    "0x1414d0f19",
    "0x14064764b",
    4,
    "0f053c98"
  ],
  [
    "0x1414d8e77",
    "0x14064764f",
    1,
    "06"
  ],
  [
    "0x1414d8edb",
    "0x140647650",
    4,
    "119ff8cc"
  ],
  [
    "0x1415fb8a8",
    "0x140647654",
    1,
    "ff"
  ],
  [
    "0x1415fb904",
    "0x140647655",
    4,
    "7081a4b6"
  ],
  [
    "0x1414d210b",
    "0x140647659",
    1,
    "9c"
  ],
  [
    "0x141606201",
    "0x14064765a",
    4,
    "e6996598"
  ],
  [
    "0x1414f63ab",
    "0x14064765e",
    4,
    "ec98ed0c"
  ],
  [
    "0x1414cb3ba",
    "0x140647662",
    1,
    "4b"
  ],
  [
    "0x1414cb406",
    "0x140647663",
    4,
    "8c76c9c1"
  ],
  [
    "0x1414c631c",
    "0x140647667",
    1,
    "d6"
  ],
  [
    "0x141508fef",
    "0x140647668",
    4,
    "740f648a"
  ],
  [
    "0x14155a747",
    "0x14064766c",
    8,
    "eaf9370d00ffffff"
  ],
  [
    "0x14155a7ab",
    "0x140647674",
    4,
    "bb3dd867"
  ],
  [
    "0x14157af0e",
    "0x140647678",
    4,
    "281e25db"
  ],
  [
    "0x14154d9d2",
    "0x14064767c",
    1,
    "bf"
  ],
  [
    "0x14154da30",
    "0x14064767d",
    4,
    "d5203f41"
  ]
]
````````````


File: `reverse/CyberCup-2077/cc2_env_fixed.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--entry',type=lambda x:int(x,0),default=0x1406987c0);a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr in (0x30000000,0x7ff00000):u.mem_write(addr,blob)
put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000)
put(0x14134d552,0x30010000)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0xfffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
reads=[]
def read(u,access,addr,size,value,data):
 if (base<=addr<base+0x124b000) or 0x30000000<=addr<0x40000000 or 0x7ff00000<=addr<0x80000000:
  reads.append([hex(u.reg_read(UC_X86_REG_RIP)),hex(addr),size,bytes(u.mem_read(addr,size)).hex()])
u.hook_add(unicorn.UC_HOOK_MEM_READ,read)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(a.entry if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_env_fixed_'+hex(a.entry)+'_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

import json
Path('cc2_env_fixed_datareads.json').write_text(json.dumps(reads,indent=2))

````````````


File: `reverse/CyberCup-2077/cc2_env_fixed_0x1406987c0_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_env_fixed_datareads.json`

````````````text
[
  [
    "0x14150db13",
    "0x1406474c8",
    4,
    "ebd49654"
  ],
  [
    "0x1414d5f62",
    "0x1406474cc",
    1,
    "1d"
  ],
  [
    "0x1414d5f99",
    "0x1406474cd",
    4,
    "08701880"
  ],
  [
    "0x1414b5f19",
    "0x1406474d1",
    1,
    "be"
  ],
  [
    "0x1414b5f7c",
    "0x1406474d2",
    4,
    "0308e53f"
  ],
  [
    "0x1414b4027",
    "0x1406474d6",
    1,
    "24"
  ],
  [
    "0x1414b4082",
    "0x1406474d7",
    4,
    "4601e780"
  ],
  [
    "0x141538314",
    "0x1406474db",
    1,
    "cc"
  ],
  [
    "0x141538360",
    "0x1406474dc",
    4,
    "9912ee00"
  ],
  [
    "0x1416089c8",
    "0x1406474e0",
    1,
    "fe"
  ],
  [
    "0x141608a1d",
    "0x1406474e1",
    4,
    "551a1dc0"
  ],
  [
    "0x14155c78c",
    "0x1406474e5",
    1,
    "14"
  ],
  [
    "0x14155c7de",
    "0x1406474e6",
    4,
    "0d11177f"
  ],
  [
    "0x1415fae99",
    "0x1406474ea",
    1,
    "48"
  ],
  [
    "0x1415faed5",
    "0x1406474eb",
    4,
    "0896e77f"
  ],
  [
    "0x1414c1582",
    "0x1406474ef",
    1,
    "87"
  ],
  [
    "0x1414c15ce",
    "0x1406474f0",
    4,
    "93cef080"
  ],
  [
    "0x1414cb3ba",
    "0x1406474f4",
    1,
    "8f"
  ],
  [
    "0x1414cb406",
    "0x1406474f5",
    4,
    "f27ef200"
  ],
  [
    "0x14154d9d2",
    "0x1406474f9",
    1,
    "ad"
  ],
  [
    "0x14154da30",
    "0x1406474fa",
    4,
    "bcb4fa80"
  ],
  [
    "0x141607161",
    "0x1406474fe",
    1,
    "61"
  ],
  [
    "0x1416071b2",
    "0x1406474ff",
    4,
    "05fd08c0"
  ],
  [
    "0x1414d5f62",
    "0x140647503",
    1,
    "c7"
  ],
  [
    "0x1414d5f99",
    "0x140647504",
    4,
    "d254e07f"
  ],
  [
    "0x1414b5f19",
    "0x140647508",
    1,
    "ec"
  ],
  [
    "0x1414b5f7c",
    "0x140647509",
    4,
    "512c1dc0"
  ],
  [
    "0x1414b4027",
    "0x14064750d",
    1,
    "a6"
  ],
  [
    "0x1414b4082",
    "0x14064750e",
    4,
    "e4251f7f"
  ],
  [
    "0x141538314",
    "0x140647512",
    1,
    "1e"
  ],
  [
    "0x141538360",
    "0x140647513",
    4,
    "6b3616ff"
  ],
  [
    "0x1416089c8",
    "0x140647517",
    1,
    "fc"
  ],
  [
    "0x141608a1d",
    "0x140647518",
    4,
    "773ee53f"
  ],
  [
    "0x14155c78c",
    "0x14064751c",
    1,
    "56"
  ],
  [
    "0x14155c7de",
    "0x14064751d",
    4,
    "8f35ef80"
  ],
  [
    "0x1415fae99",
    "0x140647521",
    1,
    "5a"
  ],
  [
    "0x1415faed5",
    "0x140647522",
    4,
    "fab21f80"
  ],
  [
    "0x1414c1582",
    "0x140647526",
    1,
    "7d"
  ],
  [
    "0x1414c15ce",
    "0x140647527",
    4,
    "d3fc0a7f"
  ],
  [
    "0x14154da49",
    "0x14064752b",
    8,
    "ec86f74c01000000"
  ],
  [
    "0x14154da9e",
    "0x140647533",
    4,
    "527dc7fb"
  ],
  [
    "0x1414e96c6",
    "0x140647537",
    1,
    "76"
  ],
  [
    "0x1414e9730",
    "0x140647538",
    4,
    "009e5534"
  ],
  [
    "0x14156e989",
    "0x14064753c",
    4,
    "d4ab95c5"
  ],
  [
    "0x1414cb3ba",
    "0x140647540",
    1,
    "53"
  ],
  [
    "0x1414cb406",
    "0x140647541",
    4,
    "ce2406ff"
  ],
  [
    "0x14154d9d2",
    "0x140647545",
    1,
    "01"
  ],
  [
    "0x14154da30",
    "0x140647546",
    4,
    "60dcf17f"
  ],
  [
    "0x1414c3996",
    "0x14064754a",
    4,
    "78aa84bf"
  ],
  [
    "0x1414c39ea",
    "0x14064754e",
    4,
    "a27b0d8d"
  ],
  [
    "0x14154b60c",
    "0x140647552",
    1,
    "70"
  ],
  [
    "0x1415fe579",
    "0x140647553",
    4,
    "9e44739e"
  ],
  [
    "0x14152da63",
    "0x140647557",
    4,
    "532264c2"
  ],
  [
    "0x141607161",
    "0x14064755b",
    1,
    "00"
  ],
  [
    "0x1416071b2",
    "0x14064755c",
    4,
    "b3ac04bf"
  ],
  [
    "0x1414f92a4",
    "0x140647560",
    4,
    "e8e4ce36"
  ],
  [
    "0x141504446",
    "0x140647564",
    4,
    "363126db"
  ],
  [
    "0x14160c664",
    "0x140647568",
    4,
    "05a637b2"
  ],
  [
    "0x1414d5f62",
    "0x14064756c",
    1,
    "06"
  ],
  [
    "0x1414d5f99",
    "0x14064756d",
    4,
    "fc6becff"
  ],
  [
    "0x1414f7ce8",
    "0x140647571",
    1,
    "de"
  ],
  [
    "0x1415272df",
    "0x140647572",
    4,
    "70dcd0f2"
  ],
  [
    "0x141514759",
    "0x140647576",
    4,
    "4d3b6fbf"
  ],
  [
    "0x1415147b3",
    "0x14064757a",
    4,
    "d43911dd"
  ],
  [
    "0x1414bd03b",
    "0x14064757e",
    1,
    "2f"
  ],
  [
    "0x1414bd08c",
    "0x14064757f",
    4,
    "237fb986"
  ],
  [
    "0x14153c87c",
    "0x140647583",
    1,
    "d6"
  ],
  [
    "0x14155ba23",
    "0x140647584",
    4,
    "556ebffe"
  ],
  [
    "0x14160b49b",
    "0x140647588",
    4,
    "30b965d4"
  ],
  [
    "0x1414b5f19",
    "0x14064758c",
    1,
    "e1"
  ],
  [
    "0x1414b5f7c",
    "0x14064758d",
    4,
    "059ef47f"
  ],
  [
    "0x1414daf81",
    "0x140647591",
    1,
    "35"
  ],
  [
    "0x1414d66cc",
    "0x140647592",
    4,
    "a97798c6"
  ],
  [
    "0x1414f76e2",
    "0x140647596",
    4,
    "809d77bf"
  ],
  [
    "0x1414f7733",
    "0x14064759a",
    4,
    "199e31fb"
  ],
  [
    "0x1414b26ff",
    "0x14064759e",
    1,
    "17"
  ],
  [
    "0x1414b277d",
    "0x14064759f",
    4,
    "6d00ba6f"
  ],
  [
    "0x1415479d6",
    "0x1406475a3",
    1,
    "c2"
  ],
  [
    "0x141547a46",
    "0x1406475a4",
    4,
    "b35253d2"
  ],
  [
    "0x141557762",
    "0x1406475a8",
    8,
    "ba0df2b301faffff"
  ],
  [
    "0x141545754",
    "0x1406475b0",
    4,
    "645e5e11"
  ],
  [
    "0x141508759",
    "0x7ff00060",
    8,
    "0010f07f00000000"
  ],
  [
    "0x141508768",
    "0x1406475b4",
    4,
    "5d704688"
  ],
  [
    "0x1414b4027",
    "0x1406475b8",
    1,
    "a7"
  ],
  [
    "0x1414b4082",
    "0x1406475b9",
    4,
    "b7320740"
  ],
  [
    "0x141575f37",
    "0x1406475bd",
    2,
    "2a9d"
  ],
  [
    "0x141575fb3",
    "0x1406475bf",
    4,
    "8b07b997"
  ],
  [
    "0x14154b516",
    "0x1406475c3",
    1,
    "db"
  ],
  [
    "0x14154b58a",
    "0x1406475c4",
    4,
    "09f151cb"
  ],
  [
    "0x14155acb1",
    "0x1406475c8",
    8,
    "9707024c01eeffff"
  ],
  [
    "0x14155ad0d",
    "0x1406475d0",
    4,
    "09957e8b"
  ],
  [
    "0x1414d62e4",
    "0x1406475d4",
    4,
    "f2bfcf4a"
  ],
  [
    "0x141538314",
    "0x1406475d8",
    1,
    "0b"
  ],
  [
    "0x141538360",
    "0x1406475d9",
    4,
    "c8110740"
  ],
  [
    "0x1415fb76e",
    "0x7ff01120",
    2,
    "614a"
  ],
  [
    "0x1415fb78d",
    "0x1406475dd",
    4,
    "44b7349b"
  ],
  [
    "0x141603fef",
    "0x1406475e1",
    1,
    "03"
  ],
  [
    "0x14160404d",
    "0x1406475e2",
    4,
    "5b727d35"
  ],
  [
    "0x1414b8442",
    "0x1406475e6",
    4,
    "dee463bf"
  ],
  [
    "0x1414b849a",
    "0x1406475ea",
    4,
    "fa2d49ff"
  ],
  [
    "0x1414d635c",
    "0x1406475ee",
    1,
    "cc"
  ],
  [
    "0x1414d63bd",
    "0x1406475ef",
    4,
    "fb1620f1"
  ],
  [
    "0x1414dadc7",
    "0x1406475f3",
    8,
    "c1fe154ce1aab2ec"
  ],
  [
    "0x1414dae31",
    "0x1406475fb",
    4,
    "c6efca44"
  ],
  [
    "0x1415414df",
    "0x1406475ff",
    1,
    "78"
  ],
  [
    "0x14154153e",
    "0x140647600",
    4,
    "79ac8b75"
  ],
  [
    "0x141532bd4",
    "0x140647604",
    4,
    "6c7b1b73"
  ],
  [
    "0x1416089c8",
    "0x140647608",
    1,
    "23"
  ],
  [
    "0x141608a1d",
    "0x140647609",
    4,
    "352cd941"
  ],
  [
    "0x1414f260d",
    "0x14064760d",
    4,
    "99973e57"
  ],
  [
    "0x14155c78c",
    "0x140647611",
    1,
    "93"
  ],
  [
    "0x14155c7de",
    "0x140647612",
    4,
    "dca834be"
  ],
  [
    "0x1414e40d7",
    "0x140647616",
    2,
    "a258"
  ],
  [
    "0x1414e414e",
    "0x140647618",
    4,
    "571e82d6"
  ],
  [
    "0x1414aea6b",
    "0x14064761c",
    1,
    "82"
  ],
  [
    "0x1414aead3",
    "0x14064761d",
    4,
    "60b462d0"
  ],
  [
    "0x141513030",
    "0x140647621",
    4,
    "6e225d6f"
  ],
  [
    "0x1415fae99",
    "0x140647625",
    1,
    "d6"
  ],
  [
    "0x1415faed5",
    "0x140647626",
    4,
    "6fca3bbe"
  ],
  [
    "0x141560b96",
    "0x14064762a",
    1,
    "fd"
  ],
  [
    "0x141560c17",
    "0x14064762b",
    4,
    "d0d2c9da"
  ],
  [
    "0x1414c3b52",
    "0x14064762f",
    1,
    "43"
  ],
  [
    "0x141505224",
    "0x140647630",
    4,
    "b96a6b68"
  ],
  [
    "0x141551dd9",
    "0x140647634",
    1,
    "7c"
  ],
  [
    "0x141551e22",
    "0x140647635",
    4,
    "8775b130"
  ],
  [
    "0x1414f9f03",
    "0x140647639",
    4,
    "94667393"
  ],
  [
    "0x1414c1582",
    "0x14064763d",
    1,
    "e3"
  ],
  [
    "0x1414c15ce",
    "0x14064763e",
    4,
    "60f7c93e"
  ],
  [
    "0x141534778",
    "0x140647642",
    1,
    "a3"
  ],
  [
    "0x1415347f2",
    "0x140647643",
    4,
    "dfd85687"
  ],
  [
    "0x1414d0eac",
    "0x140647647",
    4,
    "2bcdb601"
  ],
  [
    "0x1414d0f19",
    "0x14064764b",
    4,
    "0f053c98"
  ],
  [
    "0x1414d8e77",
    "0x14064764f",
    1,
    "06"
  ],
  [
    "0x1414d8edb",
    "0x140647650",
    4,
    "119ff8cc"
  ],
  [
    "0x1415fb8a8",
    "0x140647654",
    1,
    "ff"
  ],
  [
    "0x1415fb904",
    "0x140647655",
    4,
    "7081a4b6"
  ],
  [
    "0x1414d210b",
    "0x140647659",
    1,
    "9c"
  ],
  [
    "0x141606201",
    "0x14064765a",
    4,
    "e6996598"
  ],
  [
    "0x1414f63ab",
    "0x14064765e",
    4,
    "ec98ed0c"
  ],
  [
    "0x1414cb3ba",
    "0x140647662",
    1,
    "4b"
  ],
  [
    "0x1414cb406",
    "0x140647663",
    4,
    "8c76c9c1"
  ],
  [
    "0x1414c631c",
    "0x140647667",
    1,
    "d6"
  ],
  [
    "0x141508fef",
    "0x140647668",
    4,
    "740f648a"
  ],
  [
    "0x14155a747",
    "0x14064766c",
    8,
    "eaf9370d00ffffff"
  ],
  [
    "0x14155a7ab",
    "0x140647674",
    4,
    "bb3dd867"
  ],
  [
    "0x14157af0e",
    "0x140647678",
    4,
    "281e25db"
  ],
  [
    "0x14154d9d2",
    "0x14064767c",
    1,
    "bf"
  ],
  [
    "0x14154da30",
    "0x14064767d",
    4,
    "d5203f41"
  ],
  [
    "0x14156c804",
    "0x30010010",
    4,
    "c56d0000"
  ],
  [
    "0x14156c81d",
    "0x140647681",
    4,
    "89ab3084"
  ],
  [
    "0x141550267",
    "0x140647685",
    1,
    "88"
  ],
  [
    "0x1415502c0",
    "0x140647686",
    4,
    "865d613a"
  ],
  [
    "0x1414faa6c",
    "0x14064768a",
    4,
    "3127ba01"
  ],
  [
    "0x141543194",
    "0x14064768e",
    4,
    "15ff1550"
  ],
  [
    "0x141600578",
    "0x140647692",
    1,
    "d2"
  ],
  [
    "0x1414ed159",
    "0x140647693",
    4,
    "25af577b"
  ],
  [
    "0x141558d0c",
    "0x140647697",
    1,
    "01"
  ],
  [
    "0x141558d77",
    "0x140647698",
    4,
    "51097330"
  ],
  [
    "0x14157a32c",
    "0x14064769c",
    4,
    "96e54183"
  ],
  [
    "0x141607161",
    "0x1406476a0",
    1,
    "f9"
  ],
  [
    "0x1416071b2",
    "0x1406476a1",
    4,
    "374f2efe"
  ],
  [
    "0x1414e2ab3",
    "0x1406476a5",
    1,
    "9e"
  ],
  [
    "0x1414e2b0d",
    "0x1406476a6",
    4,
    "7a76944f"
  ],
  [
    "0x14151f011",
    "0x1406476aa",
    1,
    "78"
  ],
  [
    "0x14151f06e",
    "0x1406476ab",
    4,
    "abab9777"
  ],
  [
    "0x14154b60c",
    "0x1406476af",
    1,
    "0b"
  ],
  [
    "0x1415fe579",
    "0x1406476b0",
    4,
    "4f9a94df"
  ],
  [
    "0x141568df8",
    "0x1406476b4",
    4,
    "bb65c8f6"
  ],
  [
    "0x1414d5f62",
    "0x1406476b8",
    1,
    "d1"
  ],
  [
    "0x1414d5f99",
    "0x1406476b9",
    4,
    "981fc0fe"
  ],
  [
    "0x1415465d1",
    "0x1406476bd",
    4,
    "812b970c"
  ],
  [
    "0x1414b5f19",
    "0x1406476c1",
    1,
    "e2"
  ],
  [
    "0x1414b5f7c",
    "0x1406476c2",
    4,
    "cc5c3241"
  ],
  [
    "0x14155562a",
    "0x1406476c6",
    4,
    "2f3177f3"
  ],
  [
    "0x1414b4027",
    "0x1406476ca",
    1,
    "70"
  ],
  [
    "0x1414b4082",
    "0x1406476cb",
    4,
    "bb32cdfe"
  ],
  [
    "0x1414f7ce8",
    "0x1406476cf",
    1,
    "15"
  ],
  [
    "0x1415272df",
    "0x1406476d0",
    4,
    "902cd22c"
  ],
  [
    "0x141572a92",
    "0x1406476d4",
    4,
    "7fac6989"
  ],
  [
    "0x1414cdb86",
    "0x1406476d8",
    4,
    "dfc2e0aa"
  ],
  [
    "0x1414bd03b",
    "0x1406476dc",
    1,
    "3f"
  ],
  [
    "0x1414bd08c",
    "0x1406476dd",
    4,
    "33576838"
  ],
  [
    "0x14153c87c",
    "0x1406476e1",
    1,
    "0e"
  ],
  [
    "0x14155ba23",
    "0x1406476e2",
    4,
    "4fc0bc28"
  ],
  [
    "0x1414fd9f0",
    "0x1406476e6",
    4,
    "26d19b7c"
  ],
  [
    "0x141538314",
    "0x1406476ea",
    1,
    "0d"
  ],
  [
    "0x141538360",
    "0x1406476eb",
    4,
    "49083c81"
  ],
  [
    "0x14156d2c1",
    "0x1406476ef",
    4,
    "c9aabff6"
  ],
  [
    "0x1416089c8",
    "0x1406476f3",
    1,
    "21"
  ],
  [
    "0x141608a1d",
    "0x1406476f4",
    4,
    "be1fcb81"
  ],
  [
    "0x141557ace",
    "0x1406476f8",
    4,
    "e1d29876"
  ],
  [
    "0x14154dd8a",
    "0x1406476fc",
    4,
    "bd42d848"
  ],
  [
    "0x1414aea6b",
    "0x140647700",
    1,
    "69"
  ],
  [
    "0x1414aead3",
    "0x140647701",
    4,
    "d1359b67"
  ],
  [
    "0x1414fd5a8",
    "0x140647705",
    4,
    "7d55b2f6"
  ],
  [
    "0x14155c78c",
    "0x140647709",
    1,
    "31"
  ],
  [
    "0x14155c7de",
    "0x14064770a",
    4,
    "374dc9c1"
  ],
  [
    "0x14153dc4c",
    "0x14064770e",
    4,
    "3d6b4589"
  ],
  [
    "0x1415fae99",
    "0x140647712",
    1,
    "33"
  ],
  [
    "0x1415faed5",
    "0x140647713",
    4,
    "f78e387e"
  ],
  [
    "0x1414daf81",
    "0x140647717",
    1,
    "ee"
  ],
  [
    "0x1414d66cc",
    "0x140647718",
    4,
    "1c23032c"
  ],
  [
    "0x1415341f2",
    "0x14064771c",
    4,
    "349ca801"
  ],
  [
    "0x14153424d",
    "0x140647720",
    4,
    "ad63b955"
  ],
  [
    "0x1414b26ff",
    "0x140647724",
    1,
    "d5"
  ],
  [
    "0x1414b277d",
    "0x140647725",
    4,
    "f455a16c"
  ],
  [
    "0x1414b6490",
    "0x140647729",
    4,
    "1e455ffe"
  ],
  [
    "0x1414b64ec",
    "0x14064772d",
    4,
    "3a94bfdb"
  ],
  [
    "0x1415479d6",
    "0x140647731",
    1,
    "a7"
  ],
  [
    "0x141547a46",
    "0x140647732",
    4,
    "0a821703"
  ],
  [
    "0x141511fff",
    "0x140647736",
    4,
    "fdf6aa01"
  ],
  [
    "0x1414d20e4",
    "0x14064773a",
    4,
    "d921406d"
  ],
  [
    "0x141603fef",
    "0x14064773e",
    1,
    "3c"
  ],
  [
    "0x14160404d",
    "0x14064773f",
    4,
    "d23b3cb6"
  ],
  [
    "0x1415674cd",
    "0x140647743",
    8,
    "5352240d80faffff"
  ],
  [
    "0x141532360",
    "0x14064774b",
    4,
    "b5c1f8c9"
  ],
  [
    "0x1414e36bf",
    "0x14064774f",
    1,
    "ee"
  ],
  [
    "0x1414e372c",
    "0x140647750",
    4,
    "4dd17e8a"
  ],
  [
    "0x14160054d",
    "0x140647754",
    4,
    "99cf3c8b"
  ],
  [
    "0x1414c1582",
    "0x140647758",
    1,
    "fa"
  ],
  [
    "0x1414c15ce",
    "0x140647759",
    4,
    "8ea525c1"
  ],
  [
    "0x1414cb3ba",
    "0x14064775d",
    1,
    "c2"
  ],
  [
    "0x1414cb406",
    "0x14064775e",
    4,
    "ba662781"
  ],
  [
    "0x141569e28",
    "0x140647762",
    8,
    "9f66dbf290091a1c"
  ],
  [
    "0x1414c3a68",
    "0x14064776a",
    4,
    "ad6d7f9b"
  ],
  [
    "0x1414c474f",
    "0x14064776e",
    1,
    "83"
  ],
  [
    "0x1414c47a3",
    "0x14064776f",
    4,
    "415b4234"
  ],
  [
    "0x1414d69da",
    "0x140647773",
    1,
    "b8"
  ],
  [
    "0x1414d6a30",
    "0x140647774",
    4,
    "243a4034"
  ],
  [
    "0x1414fcb4b",
    "0x140647778",
    1,
    "61"
  ],
  [
    "0x1414fcba1",
    "0x140647779",
    4,
    "476a4534"
  ],
  [
    "0x141551c1a",
    "0x14064777d",
    1,
    "4e"
  ],
  [
    "0x141524f33",
    "0x14064777e",
    4,
    "319abecb"
  ],
  [
    "0x141510d10",
    "0x140647782",
    1,
    "20"
  ],
  [
    "0x141510d81",
    "0x140647783",
    4,
    "4b174434"
  ],
  [
    "0x1414b9a32",
    "0x140647787",
    1,
    "4a"
  ],
  [
    "0x1414b9a94",
    "0x140647788",
    4,
    "8beb4634"
  ],
  [
    "0x1414e96c6",
    "0x14064778c",
    1,
    "6e"
  ],
  [
    "0x1414e9730",
    "0x14064778d",
    4,
    "d3f54034"
  ],
  [
    "0x14154b516",
    "0x140647791",
    1,
    "8e"
  ],
  [
    "0x14154b58a",
    "0x140647792",
    4,
    "aaaabfcb"
  ],
  [
    "0x1415414df",
    "0x140647796",
    1,
    "87"
  ],
  [
    "0x14154153e",
    "0x140647797",
    4,
    "ffe44734"
  ],
  [
    "0x1414c631c",
    "0x14064779b",
    1,
    "1a"
  ],
  [
    "0x141508fef",
    "0x14064779c",
    4,
    "70374634"
  ],
  [
    "0x1414e36bf",
    "0x1406477a0",
    1,
    "11"
  ],
  [
    "0x1414e372c",
    "0x1406477a1",
    4,
    "6c27b8cb"
  ],
  [
    "0x1414c474f",
    "0x1406477a5",
    1,
    "d9"
  ],
  [
    "0x1414c47a3",
    "0x1406477a6",
    4,
    "db05b9cb"
  ],
  [
    "0x1414d69da",
    "0x1406477aa",
    1,
    "fa"
  ],
  [
    "0x1414d6a30",
    "0x1406477ab",
    4,
    "e664bbcb"
  ],
  [
    "0x1414fcb4b",
    "0x1406477af",
    1,
    "13"
  ],
  [
    "0x1414fcba1",
    "0x1406477b0",
    4,
    "5534becb"
  ],
  [
    "0x141551c1a",
    "0x1406477b4",
    1,
    "6c"
  ],
  [
    "0x141524f33",
    "0x1406477b5",
    4,
    "f3c44534"
  ],
  [
    "0x141510d10",
    "0x1406477b9",
    1,
    "9a"
  ],
  [
    "0x141510d81",
    "0x1406477ba",
    4,
    "7149bfcb"
  ],
  [
    "0x1414b9a32",
    "0x1406477be",
    1,
    "68"
  ],
  [
    "0x1414b9a94",
    "0x1406477bf",
    4,
    "a9b5bdcb"
  ],
  [
    "0x1414e96c6",
    "0x1406477c3",
    1,
    "ec"
  ],
  [
    "0x1414e9730",
    "0x1406477c4",
    4,
    "5df1bfcb"
  ],
  [
    "0x14150db13",
    "0x1406477c8",
    4,
    "3e959254"
  ],
  [
    "0x14154d9d2",
    "0x1406477cc",
    1,
    "6f"
  ],
  [
    "0x14154da30",
    "0x1406477cd",
    4,
    "5e931a7f"
  ],
  [
    "0x141607161",
    "0x1406477d1",
    1,
    "0b"
  ],
  [
    "0x1416071b2",
    "0x1406477d2",
    4,
    "6fdae83f"
  ],
  [
    "0x1414d5f62",
    "0x1406477d6",
    1,
    "8d"
  ],
  [
    "0x1414d5f99",
    "0x1406477d7",
    4,
    "98730080"
  ],
  [
    "0x1414b5f19",
    "0x1406477db",
    1,
    "be"
  ],
  [
    "0x1414b5f7c",
    "0x1406477dc",
    4,
    "230bfd3f"
  ],
  [
    "0x1414b4027",
    "0x1406477e0",
    1,
    "14"
  ],
  [
    "0x1414b4082",
    "0x1406477e1",
    4,
    "5602ff80"
  ],
  [
    "0x141538314",
    "0x1406477e5",
    1,
    "0c"
  ],
  [
    "0x141538360",
    "0x1406477e6",
    4,
    "b911f600"
  ],
  [
    "0x1416089c8",
    "0x1406477ea",
    1,
    "0e"
  ],
  [
    "0x141608a1d",
    "0x1406477eb",
    4,
    "851905c0"
  ],
  [
    "0x14155c78c",
    "0x1406477ef",
    1,
    "7c"
  ],
  [
    "0x14155c7de",
    "0x1406477f0",
    4,
    "45120f7f"
  ],
  [
    "0x1415fae99",
    "0x1406477f4",
    1,
    "58"
  ],
  [
    "0x1415faed5",
    "0x1406477f5",
    4,
    "7895ff7f"
  ],
  [
    "0x1414c1582",
    "0x1406477f9",
    1,
    "e7"
  ],
  [
    "0x1414c15ce",
    "0x1406477fa",
    4,
    "93cde880"
  ],
  [
    "0x1414cb3ba",
    "0x1406477fe",
    1,
    "f7"
  ],
  [
    "0x1414cb406",
    "0x1406477ff",
    4,
    "ea7dea00"
  ],
  [
    "0x14154d9d2",
    "0x140647803",
    1,
    "f5"
  ],
  [
    "0x14154da30",
    "0x140647804",
    4,
    "e4b7e280"
  ],
  [
    "0x141607161",
    "0x140647808",
    1,
    "11"
  ],
  [
    "0x1416071b2",
    "0x140647809",
    4,
    "b5fe10c0"
  ],
  [
    "0x1414d5f62",
    "0x14064780d",
    1,
    "af"
  ],
  [
    "0x1414d5f99",
    "0x14064780e",
    4,
    "5a57f87f"
  ],
  [
    "0x1414b5f19",
    "0x140647812",
    1,
    "cc"
  ],
  [
    "0x1414b5f7c",
    "0x140647813",
    4,
    "712f05c0"
  ],
  [
    "0x1414b4027",
    "0x140647817",
    1,
    "96"
  ],
  [
    "0x1414b4082",
    "0x140647818",
    4,
    "f426077f"
  ],
  [
    "0x141538314",
    "0x14064781c",
    1,
    "3e"
  ],
  [
    "0x141538360",
    "0x14064781d",
    4,
    "6b350eff"
  ],
  [
    "0x1416089c8",
    "0x140647821",
    1,
    "3c"
  ],
  [
    "0x141608a1d",
    "0x140647822",
    4,
    "b73dfd3f"
  ],
  [
    "0x14155c78c",
    "0x140647826",
    1,
    "e6"
  ],
  [
    "0x14155c7de",
    "0x140647827",
    4,
    "8db60800"
  ],
  [
    "0x1414dadc7",
    "0x14064782b",
    8,
    "be26f54c01000000"
  ],
  [
    "0x1414dae31",
    "0x140647833",
    4,
    "ffaa1d0e"
  ],
  [
    "0x14154b516",
    "0x140647837",
    1,
    "ae"
  ],
  [
    "0x14154b58a",
    "0x140647838",
    4,
    "24ec5b34"
  ],
  [
    "0x1414ef0ac",
    "0x14064783c",
    4,
    "0d4c4b12"
  ],
  [
    "0x1415fae99",
    "0x140647840",
    1,
    "fa"
  ],
  [
    "0x1415faed5",
    "0x140647841",
    4,
    "ba321480"
  ],
  [
    "0x1414c1582",
    "0x140647845",
    1,
    "bd"
  ],
  [
    "0x1414c15ce",
    "0x140647846",
    4,
    "f9b202ff"
  ],
  [
    "0x1415414df",
    "0x14064784a",
    1,
    "ed"
  ],
  [
    "0x14154153e",
    "0x14064784b",
    4,
    "bea5accb"
  ],
  [
    "0x1416083c7",
    "0x30010058",
    4,
    "5f3b2830"
  ],
  [
    "0x1416083e6",
    "0x14064784f",
    4,
    "0c1f343a"
  ],
  [
    "0x1414d635c",
    "0x140647853",
    1,
    "1b"
  ],
  [
    "0x1414d63bd",
    "0x140647854",
    4,
    "c0d1617d"
  ],
  [
    "0x1414c3996",
    "0x140647858",
    4,
    "2fd59abf"
  ],
  [
    "0x1414c39ea",
    "0x14064785c",
    4,
    "0b04bed8"
  ],
  [
    "0x141560b96",
    "0x140647860",
    1,
    "5e"
  ],
  [
    "0x141560c17",
    "0x140647861",
    4,
    "56d68e34"
  ],
  [
    "0x141514759",
    "0x140647865",
    4,
    "2b3f9053"
  ],
  [
    "0x1415147b3",
    "0x140647869",
    4,
    "38c690e4"
  ],
  [
    "0x1414c3b52",
    "0x14064786d",
    1,
    "d0"
  ],
  [
    "0x141505224",
    "0x14064786e",
    4,
    "3a7240d6"
  ],
  [
    "0x141551dd9",
    "0x140647872",
    1,
    "6f"
  ],
  [
    "0x141551e22",
    "0x140647873",
    4,
    "58999a3e"
  ],
  [
    "0x1414d1bae",
    "0x140647877",
    4,
    "082dc988"
  ],
  [
    "0x1414cb3ba",
    "0x14064787b",
    1,
    "bc"
  ],
  [
    "0x1414cb406",
    "0x14064787c",
    4,
    "5f72ef40"
  ],
  [
    "0x14157bc3e",
    "0x140647880",
    4,
    "415c02f7"
  ],
  [
    "0x14154d9d2",
    "0x140647884",
    1,
    "cc"
  ],
  [
    "0x14154da30",
    "0x140647885",
    4,
    "7e02e57f"
  ],
  [
    "0x1414f76e2",
    "0x140647889",
    4,
    "183869ac"
  ],
  [
    "0x1414f7733",
    "0x14064788d",
    4,
    "4ae4d53d"
  ],
  [
    "0x1415fb8a8",
    "0x140647891",
    1,
    "20"
  ],
  [
    "0x1415fb904",
    "0x140647892",
    4,
    "bf6371cf"
  ],
  [
    "0x1414d815c",
    "0x140647896",
    4,
    "1c1a8008"
  ],
  [
    "0x141607161",
    "0x14064789a",
    1,
    "24"
  ],
  [
    "0x1416071b2",
    "0x14064789b",
    4,
    "58a9f27f"
  ],
  [
    "0x141542327",
    "0x14064789f",
    4,
    "04a82af7"
  ],
  [
    "0x1414d5f62",
    "0x1406478a3",
    1,
    "6c"
  ],
  [
    "0x1414d5f99",
    "0x1406478a4",
    4,
    "74b2057f"
  ],
  [
    "0x141534778",
    "0x1406478a8",
    1,
    "23"
  ],
  [
    "0x1415347f2",
    "0x1406478a9",
    4,
    "e4f21cbd"
  ],
  [
    "0x1414d210b",
    "0x1406478ad",
    1,
    "79"
  ],
  [
    "0x141606201",
    "0x1406478ae",
    4,
    "c7b85586"
  ],
  [
    "0x141558d0c",
    "0x1406478b2",
    1,
    "c0"
  ],
  [
    "0x141558d77",
    "0x1406478b3",
    4,
    "0d528fd6"
  ],
  [
    "0x1414e2ab3",
    "0x1406478b7",
    1,
    "df"
  ],
  [
    "0x1414e2b0d",
    "0x1406478b8",
    4,
    "c7997739"
  ],
  [
    "0x1414c8531",
    "0x1406478bc",
    4,
    "59a42737"
  ],
  [
    "0x1414b5f19",
    "0x1406478c0",
    1,
    "61"
  ],
  [
    "0x1414b5f7c",
    "0x1406478c1",
    4,
    "3e6a0a3f"
  ],
  [
    "0x141539f9f",
    "0x1406478c5",
    4,
    "972e28d8"
  ],
  [
    "0x1414b4027",
    "0x1406478c9",
    1,
    "ed"
  ],
  [
    "0x1414b4082",
    "0x1406478ca",
    4,
    "f730f5c0"
  ],
  [
    "0x14154dc37",
    "0x1406478ce",
    4,
    "fbb81b36"
  ],
  [
    "0x141522507",
    "0x1406478d2",
    4,
    "85afff0c"
  ],
  [
    "0x1414b70f6",
    "0x1406478d6",
    4,
    "5c86613d"
  ],
  [
    "0x141538314",
    "0x1406478da",
    1,
    "db"
  ],
  [
    "0x141538360",
    "0x1406478db",
    4,
    "db580c40"
  ],
  [
    "0x1414d8e77",
    "0x1406478df",
    1,
    "a9"
  ],
  [
    "0x1414d8edb",
    "0x1406478e0",
    4,
    "fb031589"
  ],
  [
    "0x1414c631c",
    "0x1406478e4",
    1,
    "8f"
  ],
  [
    "0x141508fef",
    "0x1406478e5",
    4,
    "3d455034"
  ],
  [
    "0x1414e9c57",
    "0x1406478e9",
    8,
    "a3b303b3b17effff"
  ],
  [
    "0x1414e9ca2",
    "0x1406478f1",
    4,
    "08688426"
  ],
  [
    "0x1414c8719",
    "0x1406478f5",
    4,
    "dbdf6eaf"
  ],
  [
    "0x1416089c8",
    "0x1406478f9",
    1,
    "a6"
  ],
  [
    "0x141608a1d",
    "0x1406478fa",
    4,
    "faa1e0ff"
  ],
  [
    "0x14156805e",
    "0x1406478fe",
    4,
    "45d82436"
  ],
  [
    "0x14160096c",
    "0x140647902",
    4,
    "c5386703"
  ],
  [
    "0x1414b62de",
    "0x140647906",
    4,
    "d4313c30"
  ],
  [
    "0x14155c78c",
    "0x14064790a",
    1,
    "98"
  ],
  [
    "0x14155c7de",
    "0x14064790b",
    4,
    "9185feff"
  ],
  [
    "0x1414e36bf",
    "0x14064790f",
    1,
    "37"
  ],
  [
    "0x1414e372c",
    "0x140647910",
    4,
    "4a98a2cb"
  ],
  [
    "0x1414c474f",
    "0x140647914",
    1,
    "0f"
  ],
  [
    "0x1414c47a3",
    "0x140647915",
    4,
    "d8d6a0cb"
  ],
  [
    "0x1414e95c8",
    "0x140647919",
    4,
    "0e702f30"
  ],
  [
    "0x1415fae99",
    "0x14064791d",
    1,
    "fa"
  ],
  [
    "0x1415faed5",
    "0x14064791e",
    4,
    "83b3157f"
  ],
  [
    "0x1415fc086",
    "0x140647922",
    8,
    "ef2ae24cb17effff"
  ],
  [
    "0x1415fc0e5",
    "0x14064792a",
    4,
    "44390c9c"
  ],
  [
    "0x141550875",
    "0x14064792e",
    4,
    "401bf159"
  ],
  [
    "0x1414c1582",
    "0x140647932",
    1,
    "50"
  ],
  [
    "0x1414c15ce",
    "0x140647933",
    4,
    "b6af16bf"
  ],
  [
    "0x141513614",
    "0x140647937",
    4,
    "76b1a826"
  ],
  [
    "0x1414cb3ba",
    "0x14064793b",
    1,
    "16"
  ],
  [
    "0x1414cb406",
    "0x14064793c",
    4,
    "4bb3eb00"
  ],
  [
    "0x14154d9d2",
    "0x140647940",
    1,
    "7c"
  ],
  [
    "0x14154da30",
    "0x140647941",
    4,
    "26361c80"
  ],
  [
    "0x1414b8442",
    "0x140647945",
    4,
    "083697bf"
  ],
  [
    "0x1414b849a",
    "0x140647949",
    4,
    "2ce71c8d"
  ],
  [
    "0x141550267",
    "0x14064794d",
    1,
    "85"
  ],
  [
    "0x1415502c0",
    "0x14064794e",
    4,
    "4d654470"
  ],
  [
    "0x141602d3a",
    "0x140647952",
    2,
    "b115"
  ],
  [
    "0x141602d9b",
    "0x140647954",
    4,
    "4926b468"
  ],
  [
    "0x1414d69da",
    "0x140647958",
    1,
    "01"
  ],
  [
    "0x1414d6a30",
    "0x140647959",
    4,
    "3d465e34"
  ],
  [
    "0x1414fcb4b",
    "0x14064795d",
    1,
    "28"
  ],
  [
    "0x1414fcba1",
    "0x14064795e",
    4,
    "3e1a5b34"
  ],
  [
    "0x1415212cc",
    "0x140647962",
    4,
    "00cdcacf"
  ],
  [
    "0x141607161",
    "0x140647966",
    1,
    "ac"
  ],
  [
    "0x1416071b2",
    "0x140647967",
    4,
    "077309c0"
  ],
  [
    "0x14155d6a1",
    "0x14064796b",
    8,
    "f8c0f64c01040000"
  ],
  [
    "0x14155d6fc",
    "0x140647973",
    4,
    "f63cbf3d"
  ],
  [
    "0x1415026b0",
    "0x140647977",
    4,
    "a97e05a6"
  ],
  [
    "0x1414d5f62",
    "0x14064797b",
    1,
    "95"
  ],
  [
    "0x1414d5f99",
    "0x14064797c",
    4,
    "23370740"
  ],
  [
    "0x1414c4032",
    "0x140647980",
    4,
    "5875a9ac"
  ],
  [
    "0x1414b5f19",
    "0x140647984",
    1,
    "3e"
  ],
  [
    "0x1414b5f7c",
    "0x140647985",
    4,
    "3560fb40"
  ],
  [
    "0x14154da49",
    "0x140647989",
    8,
    "49ca07b3feffffff"
  ],
  [
    "0x14154da9e",
    "0x140647991",
    4,
    "f829ab33"
  ],
  [
    "0x1415098bd",
    "0x140647995",
    4,
    "f24794ea"
  ],
  [
    "0x1414b4027",
    "0x140647999",
    1,
    "79"
  ],
  [
    "0x1414b4082",
    "0x14064799a",
    4,
    "3baff880"
  ],
  [
    "0x141538314",
    "0x14064799e",
    1,
    "e9"
  ],
  [
    "0x141538360",
    "0x14064799f",
    4,
    "a53b0c00"
  ],
  [
    "0x1414e9c57",
    "0x1406479a3",
    8,
    "596bfe4c3149b8f9"
  ],
  [
    "0x1414e9ca2",
    "0x1406479ab",
    4,
    "613cb745"
  ],
  [
    "0x141551c1a",
    "0x1406479af",
    1,
    "74"
  ],
  [
    "0x141524f33",
    "0x1406479b0",
    4,
    "0b693474"
  ],
  [
    "0x141510d10",
    "0x1406479b4",
    1,
    "02"
  ],
  [
    "0x141510d81",
    "0x1406479b5",
    4,
    "82a83174"
  ],
  [
    "0x14156cec1",
    "0x1406479b9",
    4,
    "5b69ef10"
  ],
  [
    "0x1416089c8",
    "0x1406479bd",
    1,
    "46"
  ],
  [
    "0x141608a1d",
    "0x1406479be",
    4,
    "cc526740"
  ],
  [
    "0x1414d6bc9",
    "0x1406479c2",
    4,
    "6bd30bef"
  ],
  [
    "0x14155c78c",
    "0x1406479c6",
    1,
    "66"
  ],
  [
    "0x14155c7de",
    "0x1406479c7",
    4,
    "e0d086bf"
  ],
  [
    "0x1414dc99a",
    "0x1406479cb",
    4,
    "3f844c76"
  ],
  [
    "0x14157a12d",
    "0x1406479cf",
    4,
    "f6a92c4c"
  ],
  [
    "0x1414f57c5",
    "0x1406479d3",
    4,
    "202d5270"
  ],
  [
    "0x1415fae99",
    "0x1406479d7",
    1,
    "94"
  ],
  [
    "0x1415faed5",
    "0x1406479d8",
    4,
    "ede26e3f"
  ],
  [
    "0x1415fc086",
    "0x1406479dc",
    8,
    "957b990c9057b8f9"
  ],
  [
    "0x1415fc0e5",
    "0x1406479e4",
    4,
    "b862e368"
  ],
  [
    "0x1414b9a32",
    "0x1406479e8",
    1,
    "3d"
  ],
  [
    "0x1414b9a94",
    "0x1406479e9",
    4,
    "01a94034"
  ],
  [
    "0x141512226",
    "0x1406479ed",
    4,
    "13206daf"
  ],
  [
    "0x1414c1582",
    "0x1406479f1",
    1,
    "84"
  ],
  [
    "0x1414c15ce",
    "0x1406479f2",
    4,
    "82451f7f"
  ],
  [
    "0x14160d728",
    "0x1406479f6",
    4,
    "f154f7c9"
  ],
  [
    "0x1414b3d2e",
    "0x1406479fa",
    4,
    "e1a2edb2"
  ],
  [
    "0x1414afde3",
    "0x1406479fe",
    4,
    "fc8e2130"
  ],
  [
    "0x1414cb3ba",
    "0x140647a02",
    1,
    "78"
  ],
  [
    "0x1414cb406",
    "0x140647a03",
    4,
    "b091e33f"
  ],
  [
    "0x1414bf491",
    "0x140647a07",
    4,
    "18b93a06"
  ],
  [
    "0x14154d9d2",
    "0x140647a0b",
    1,
    "7a"
  ],
  [
    "0x14154da30",
    "0x140647a0c",
    4,
    "e78b1580"
  ],
  [
    "0x1414e96c6",
    "0x140647a10",
    1,
    "07"
  ],
  [
    "0x1414e9730",
    "0x140647a11",
    4,
    "16fab4cb"
  ],
  [
    "0x14155a2a5",
    "0x140647a15",
    4,
    "2323a27d"
  ],
  [
    "0x141607161",
    "0x140647a19",
    1,
    "30"
  ],
  [
    "0x1416071b2",
    "0x140647a1a",
    4,
    "b447e53f"
  ],
  [
    "0x1414d5f62",
    "0x140647a1e",
    1,
    "4e"
  ],
  [
    "0x1414d5f99",
    "0x140647a1f",
    4,
    "e544f340"
  ],
  [
    "0x14154b516",
    "0x140647a23",
    1,
    "c9"
  ],
  [
    "0x14154b58a",
    "0x140647a24",
    4,
    "ede2aecb"
  ],
  [
    "0x1415414df",
    "0x140647a28",
    1,
    "60"
  ],
  [
    "0x14154153e",
    "0x140647a29",
    4,
    "d8ac5634"
  ],
  [
    "0x1414c631c",
    "0x140647a2d",
    1,
    "c5"
  ],
  [
    "0x141508fef",
    "0x140647a2e",
    4,
    "2f7f5734"
  ],
  [
    "0x1414e36bf",
    "0x140647a32",
    1,
    "ce"
  ],
  [
    "0x1414e372c",
    "0x140647a33",
    4,
    "b36fa9cb"
  ],
  [
    "0x1414c474f",
    "0x140647a37",
    1,
    "96"
  ],
  [
    "0x1414c47a3",
    "0x140647a38",
    4,
    "744da8cb"
  ],
  [
    "0x1414d69da",
    "0x140647a3c",
    1,
    "4d"
  ],
  [
    "0x1414d6a30",
    "0x140647a3d",
    4,
    "512caacb"
  ],
  [
    "0x1414fcb4b",
    "0x140647a41",
    1,
    "8c"
  ],
  [
    "0x1414fcba1",
    "0x140647a42",
    4,
    "aa7cafcb"
  ],
  [
    "0x141551c1a",
    "0x140647a46",
    1,
    "63"
  ],
  [
    "0x141524f33",
    "0x140647a47",
    4,
    "1c8c5434"
  ],
  [
    "0x141510d10",
    "0x140647a4b",
    1,
    "ad"
  ],
  [
    "0x141510d81",
    "0x140647a4c",
    4,
    "0601aecb"
  ],
  [
    "0x1414b9a32",
    "0x140647a50",
    1,
    "37"
  ],
  [
    "0x1414b9a94",
    "0x140647a51",
    4,
    "16fdaccb"
  ],
  [
    "0x1414e96c6",
    "0x140647a55",
    1,
    "53"
  ],
  [
    "0x1414e9730",
    "0x140647a56",
    4,
    "eee3aacb"
  ],
  [
    "0x14154b516",
    "0x140647a5a",
    1,
    "63"
  ],
  [
    "0x14154b58a",
    "0x140647a5b",
    4,
    "27bc5534"
  ],
  [
    "0x1415414df",
    "0x140647a5f",
    1,
    "d2"
  ],
  [
    "0x14154153e",
    "0x140647a60",
    4,
    "6af2adcb"
  ],
  [
    "0x1414c631c",
    "0x140647a64",
    1,
    "07"
  ],
  [
    "0x141508fef",
    "0x140647a65",
    4,
    "4d21accb"
  ],
  [
    "0x1414e36bf",
    "0x140647a69",
    1,
    "4c"
  ],
  [
    "0x1414e372c",
    "0x140647a6a",
    4,
    "b1315234"
  ],
  [
    "0x1414c474f",
    "0x140647a6e",
    1,
    "e4"
  ],
  [
    "0x1414c47a3",
    "0x140647a6f",
    4,
    "a6135334"
  ],
  [
    "0x1414d69da",
    "0x140647a73",
    1,
    "8f"
  ],
  [
    "0x1414d6a30",
    "0x140647a74",
    4,
    "b3725134"
  ],
  [
    "0x1414fcb4b",
    "0x140647a78",
    1,
    "ae"
  ],
  [
    "0x1414fcba1",
    "0x140647a79",
    4,
    "08225434"
  ],
  [
    "0x141551c1a",
    "0x140647a7d",
    1,
    "c9"
  ],
  [
    "0x141524f33",
    "0x140647a7e",
    4,
    "d6d2afcb"
  ],
  [
    "0x141510d10",
    "0x140647a82",
    1,
    "97"
  ],
  [
    "0x141510d81",
    "0x140647a83",
    4,
    "ecdbaacb"
  ],
  [
    "0x14150db13",
    "0x140647b6d",
    4,
    "4edb9654"
  ],
  [
    "0x1414d5f62",
    "0x140647b71",
    1,
    "68"
  ],
  [
    "0x1414d5f99",
    "0x140647b72",
    4,
    "5d7f1880"
  ],
  [
    "0x1414b5f19",
    "0x140647b76",
    1,
    "cb"
  ],
  [
    "0x1414b5f7c",
    "0x140647b77",
    4,
    "7607e53f"
  ],
  [
    "0x1414b4027",
    "0x140647b7b",
    1,
    "61"
  ],
  [
    "0x1414b4082",
    "0x140647b7c",
    4,
    "230ee780"
  ],
  [
    "0x141538314",
    "0x140647b80",
    1,
    "19"
  ],
  [
    "0x141538360",
    "0x140647b81",
    4,
    "6c1dee00"
  ],
  [
    "0x1416089c8",
    "0x140647b85",
    1,
    "63"
  ],
  [
    "0x141608a1d",
    "0x140647b86",
    4,
    "08151dc0"
  ],
  [
    "0x14155c78c",
    "0x140647b8a",
    1,
    "49"
  ],
  [
    "0x14155c7de",
    "0x140647b8b",
    4,
    "501e177f"
  ],
  [
    "0x1415fae99",
    "0x140647b8f",
    1,
    "dd"
  ],
  [
    "0x1415faed5",
    "0x140647b90",
    4,
    "9d99e77f"
  ],
  [
    "0x1414c1582",
    "0x140647b94",
    1,
    "4a"
  ],
  [
    "0x1414c15ce",
    "0x140647b95",
    4,
    "3ec1f080"
  ],
  [
    "0x1414cb3ba",
    "0x140647b99",
    1,
    "6a"
  ],
  [
    "0x1414cb406",
    "0x140647b9a",
    4,
    "1771f200"
  ],
  [
    "0x14154d9d2",
    "0x140647b9e",
    1,
    "68"
  ],
  [
    "0x14154da30",
    "0x140647b9f",
    4,
    "79bbfa80"
  ],
  [
    "0x141607161",
    "0x140647ba3",
    1,
    "94"
  ],
  [
    "0x1416071b2",
    "0x140647ba4",
    4,
    "10f208c0"
  ],
  [
    "0x1414d5f62",
    "0x140647ba8",
    1,
    "02"
  ],
  [
    "0x1414d5f99",
    "0x140647ba9",
    4,
    "f75be07f"
  ],
  [
    "0x1414b5f19",
    "0x140647bad",
    1,
    "b1"
  ],
  [
    "0x1414b5f7c",
    "0x140647bae",
    4,
    "ec231dc0"
  ],
  [
    "0x1414b4027",
    "0x140647bb2",
    1,
    "4b"
  ],
  [
    "0x1414b4082",
    "0x140647bb3",
    4,
    "292a1f7f"
  ],
  [
    "0x141538314",
    "0x140647bb7",
    1,
    "d3"
  ],
  [
    "0x141538360",
    "0x140647bb8",
    4,
    "a63916ff"
  ],
  [
    "0x1416089c8",
    "0x140647bbc",
    1,
    "d9"
  ],
  [
    "0x141608a1d",
    "0x140647bbd",
    4,
    "5231e53f"
  ],
  [
    "0x14155c78c",
    "0x140647bc1",
    1,
    "83"
  ],
  [
    "0x14155c7de",
    "0x140647bc2",
    4,
    "ba3aef80"
  ],
  [
    "0x1415fae99",
    "0x140647bc6",
    1,
    "07"
  ],
  [
    "0x1415faed5",
    "0x140647bc7",
    4,
    "67bd1f80"
  ],
  [
    "0x1414c1582",
    "0x140647bcb",
    1,
    "40"
  ],
  [
    "0x1414c15ce",
    "0x140647bcc",
    4,
    "aef30a7f"
  ],
  [
    "0x14154da49",
    "0x140647bd0",
    8,
    "8589f74cf1d6fdf9"
  ],
  [
    "0x14154da9e",
    "0x140647bd8",
    4,
    "bee0d297"
  ],
  [
    "0x141510d10",
    "0x140647bdc",
    1,
    "70"
  ],
  [
    "0x141510d81",
    "0x140647bdd",
    4,
    "50b33d74"
  ],
  [
    "0x14156e989",
    "0x140647be1",
    4,
    "b886fd85"
  ],
  [
    "0x1414cb3ba",
    "0x140647be5",
    1,
    "a7"
  ],
  [
    "0x1414cb406",
    "0x140647be6",
    4,
    "da096ebf"
  ],
  [
    "0x14154d9d2",
    "0x140647bea",
    1,
    "35"
  ],
  [
    "0x14154da30",
    "0x140647beb",
    4,
    "f396993f"
  ],
  [
    "0x1414b9a32",
    "0x140647bef",
    1,
    "6c"
  ],
  [
    "0x1414b9a94",
    "0x140647bf0",
    4,
    "4d633474"
  ],
  [
    "0x1414e96c6",
    "0x140647bf4",
    1,
    "b0"
  ],
  [
    "0x1414e9730",
    "0x140647bf5",
    4,
    "0d7d3274"
  ],
  [
    "0x14154b516",
    "0x140647bf9",
    1,
    "70"
  ],
  [
    "0x14154b58a",
    "0x140647bfa",
    4,
    "5422cd8b"
  ],
  [
    "0x1415414df",
    "0x140647bfe",
    1,
    "01"
  ],
  [
    "0x14154153e",
    "0x140647bff",
    4,
    "f96c3574"
  ],
  [
    "0x1414c631c",
    "0x140647c03",
    1,
    "f4"
  ],
  [
    "0x141508fef",
    "0x140647c04",
    4,
    "3ebf3474"
  ],
  [
    "0x1414e36bf",
    "0x140647c08",
    1,
    "ff"
  ],
  [
    "0x1414e372c",
    "0x140647c09",
    4,
    "82afca8b"
  ],
  [
    "0x1414c474f",
    "0x140647c0d",
    1,
    "0f"
  ],
  [
    "0x1414c47a3",
    "0x140647c0e",
    4,
    "0d8dcb8b"
  ],
  [
    "0x1414d69da",
    "0x140647c12",
    1,
    "04"
  ],
  [
    "0x1414d6a30",
    "0x140647c13",
    4,
    "f8ecc98b"
  ],
  [
    "0x1414fcb4b",
    "0x140647c17",
    1,
    "ed"
  ],
  [
    "0x1414fcba1",
    "0x140647c18",
    4,
    "6bbccc8b"
  ],
  [
    "0x141551c1a",
    "0x140647c1c",
    1,
    "92"
  ],
  [
    "0x141524f33",
    "0x140647c1d",
    4,
    "8d4c3774"
  ],
  [
    "0x141510d10",
    "0x140647c21",
    1,
    "5c"
  ],
  [
    "0x141510d81",
    "0x140647c22",
    4,
    "b7c1cd8b"
  ],
  [
    "0x1414b9a32",
    "0x140647c26",
    1,
    "ae"
  ],
  [
    "0x1414b9a94",
    "0x140647c27",
    4,
    "6f3dcf8b"
  ],
  [
    "0x1414e96c6",
    "0x140647c2b",
    1,
    "0a"
  ],
  [
    "0x1414e9730",
    "0x140647c2c",
    4,
    "b723c98b"
  ],
  [
    "0x14154b516",
    "0x140647c30",
    1,
    "5a"
  ],
  [
    "0x14154b58a",
    "0x140647c31",
    4,
    "5e7c3674"
  ],
  [
    "0x1415414df",
    "0x140647c35",
    1,
    "bb"
  ],
  [
    "0x14154153e",
    "0x140647c36",
    4,
    "6332ce8b"
  ],
  [
    "0x1414c631c",
    "0x140647c3a",
    1,
    "2e"
  ],
  [
    "0x141508fef",
    "0x140647c3b",
    4,
    "64e1cf8b"
  ],
  [
    "0x1414e36bf",
    "0x140647c3f",
    1,
    "55"
  ],
  [
    "0x1414e372c",
    "0x140647c40",
    4,
    "48f13174"
  ],
  [
    "0x1414c474f",
    "0x140647c44",
    1,
    "95"
  ],
  [
    "0x1414c47a3",
    "0x140647c45",
    4,
    "f7d33074"
  ],
  [
    "0x1414d69da",
    "0x140647c49",
    1,
    "de"
  ],
  [
    "0x1414d6a30",
    "0x140647c4a",
    4,
    "e2b23274"
  ],
  [
    "0x1414fcb4b",
    "0x140647c4e",
    1,
    "8f"
  ],
  [
    "0x1414fcba1",
    "0x140647c4f",
    4,
    "59ccc98b"
  ],
  [
    "0x14158b7eb",
    "0x140602291",
    4,
    "8c7e2a5c"
  ],
  [
    "0x1415f44ba",
    "0x140602295",
    1,
    "8b"
  ],
  [
    "0x1415f4543",
    "0x140602296",
    4,
    "21134065"
  ],
  [
    "0x1415bd60e",
    "0x14060229a",
    1,
    "01"
  ],
  [
    "0x1415bd6a2",
    "0x14060229b",
    4,
    "91b9417d"
  ],
  [
    "0x1415cbe05",
    "0x14060229f",
    1,
    "8b"
  ],
  [
    "0x1415cbe99",
    "0x1406022a0",
    4,
    "6c7aba82"
  ],
  [
    "0x1415c2796",
    "0x1406022a4",
    1,
    "8d"
  ],
  [
    "0x141555929",
    "0x1406022a5",
    4,
    "1a0c416d"
  ],
  [
    "0x14159be9d",
    "0x1406022a9",
    1,
    "3f"
  ],
  [
    "0x14159bf3d",
    "0x1406022aa",
    4,
    "1afa4275"
  ],
  [
    "0x1415b6163",
    "0x1406022ae",
    1,
    "09"
  ],
  [
    "0x14158a26f",
    "0x1406022af",
    4,
    "de88be02"
  ],
  [
    "0x1414b10d0",
    "0x1406022b3",
    1,
    "45"
  ],
  [
    "0x1414b1179",
    "0x1406022b4",
    4,
    "08f4aee2"
  ],
  [
    "0x14157de57",
    "0x1406022b8",
    1,
    "1b"
  ],
  [
    "0x14158113d",
    "0x1406022b9",
    4,
    "64c05b65"
  ],
  [
    "0x14154d90a",
    "0x1406022bd",
    1,
    "fd"
  ],
  [
    "0x1415d24b4",
    "0x1406022be",
    4,
    "cd1e5855"
  ],
  [
    "0x1415a4c74",
    "0x1406022c2",
    1,
    "ba"
  ],
  [
    "0x1414e97d2",
    "0x1406022c3",
    4,
    "0099a292"
  ],
  [
    "0x141583e23",
    "0x1406022c7",
    1,
    "3f"
  ],
  [
    "0x14157d33d",
    "0x1406022c8",
    4,
    "2707a7ba"
  ],
  [
    "0x1415f44ba",
    "0x1406022cc",
    1,
    "31"
  ],
  [
    "0x1415f4543",
    "0x1406022cd",
    4,
    "9b255f65"
  ],
  [
    "0x1415bd60e",
    "0x1406022d1",
    1,
    "5b"
  ],
  [
    "0x1415bd6a2",
    "0x1406022d2",
    4,
    "4b8f5e7d"
  ],
  [
    "0x1415cbe05",
    "0x1406022d6",
    1,
    "a9"
  ],
  [
    "0x1415cbe99",
    "0x1406022d7",
    4,
    "ce4ca582"
  ],
  [
    "0x1415c2796",
    "0x1406022db",
    1,
    "8a"
  ],
  [
    "0x141555929",
    "0x1406022dc",
    4,
    "203a5e6d"
  ],
  [
    "0x14159be9d",
    "0x1406022e0",
    1,
    "80"
  ],
  [
    "0x14159bf3d",
    "0x1406022e1",
    4,
    "b8cc5d75"
  ],
  [
    "0x1415b6163",
    "0x1406022e5",
    1,
    "53"
  ],
  [
    "0x14158a26f",
    "0x1406022e6",
    4,
    "04bea102"
  ],
  [
    "0x1414b10d0",
    "0x1406022ea",
    1,
    "2a"
  ],
  [
    "0x1414b1179",
    "0x1406022eb",
    4,
    "6ac2b1e2"
  ],
  [
    "0x14157de57",
    "0x1406022ef",
    1,
    "3c"
  ],
  [
    "0x14158113d",
    "0x1406022f0",
    4,
    "39d7bd82"
  ],
  [
    "0x14158a2dc",
    "0x1406022f4",
    8,
    "e794afe9da050000"
  ],
  [
    "0x14158a341",
    "0x1406022fc",
    4,
    "e704e9ad"
  ],
  [
    "0x1415d095e",
    "0x140602300",
    1,
    "72"
  ],
  [
    "0x1415d09d1",
    "0x140602301",
    4,
    "3c7267b9"
  ],
  [
    "0x1414c54e5",
    "0x140602305",
    4,
    "522b3bb4"
  ],
  [
    "0x14154d90a",
    "0x140602309",
    1,
    "f9"
  ],
  [
    "0x1415d24b4",
    "0x14060230a",
    4,
    "49bfb8aa"
  ],
  [
    "0x1415a4c74",
    "0x14060230e",
    1,
    "fe"
  ],
  [
    "0x1414e97d2",
    "0x14060230f",
    4,
    "c438426d"
  ],
  [
    "0x141583e23",
    "0x140602313",
    1,
    "eb"
  ],
  [
    "0x14157d33d",
    "0x140602314",
    4,
    "5c32be8a"
  ],
  [
    "0x14156d1ad",
    "0x140602318",
    4,
    "a992740f"
  ],
  [
    "0x1415f44ba",
    "0x14060231c",
    1,
    "25"
  ],
  [
    "0x1415f4543",
    "0x14060231d",
    4,
    "0f624e65"
  ],
  [
    "0x1415bd60e",
    "0x140602321",
    1,
    "17"
  ],
  [
    "0x1415bd6a2",
    "0x140602322",
    4,
    "889db502"
  ],
  [
    "0x1414b1cbe",
    "0x140602326",
    4,
    "db76ed1a"
  ],
  [
    "0x1415cbe05",
    "0x14060232a",
    1,
    "30"
  ],
  [
    "0x1415cbe99",
    "0x14060232b",
    4,
    "da0b4a7d"
  ],
  [
    "0x1415c2796",
    "0x14060232f",
    1,
    "a6"
  ],
  [
    "0x141555929",
    "0x140602330",
    4,
    "8448b292"
  ],
  [
    "0x1415947f2",
    "0x140602334",
    4,
    "32deba0f"
  ],
  [
    "0x14159be9d",
    "0x140602338",
    1,
    "21"
  ],
  [
    "0x14159bf3d",
    "0x140602339",
    4,
    "944ab28a"
  ],
  [
    "0x1415b6163",
    "0x14060233d",
    1,
    "af"
  ],
  [
    "0x14158a26f",
    "0x14060233e",
    4,
    "f0354c75"
  ],
  [
    "0x1415d2f41",
    "0x140602342",
    4,
    "3b945929"
  ],
  [
    "0x1414b10d0",
    "0x140602346",
    1,
    "6f"
  ],
  [
    "0x1414b1179",
    "0x140602347",
    4,
    "a264bee2"
  ],
  [
    "0x14157de57",
    "0x14060234b",
    1,
    "99"
  ],
  [
    "0x14158113d",
    "0x14060234c",
    4,
    "59f3b5aa"
  ],
  [
    "0x1415d6bac",
    "0x140602350",
    1,
    "58"
  ],
  [
    "0x1415d6c3a",
    "0x140602351",
    4,
    "f5fb6e62"
  ],
  [
    "0x1415c48f8",
    "0x140602355",
    8,
    "0ba69b13da050000"
  ],
  [
    "0x1415853db",
    "0x14060235d",
    4,
    "e8fefd35"
  ],
  [
    "0x14158d025",
    "0x140602361",
    4,
    "0a2c5e6d"
  ],
  [
    "0x14154d90a",
    "0x140602365",
    1,
    "b1"
  ],
  [
    "0x1415d24b4",
    "0x140602366",
    4,
    "9901b69a"
  ],
  [
    "0x1415899ae",
    "0x14060236a",
    4,
    "2da03f58"
  ],
  [
    "0x141583166",
    "0x14060236e",
    4,
    "57966d10"
  ],
  [
    "0x14154b14f",
    "0x140602372",
    4,
    "9e7ed2aa"
  ],
  [
    "0x1415a4c74",
    "0x140602376",
    1,
    "15"
  ],
  [
    "0x1414e97d2",
    "0x140602377",
    4,
    "ba404f75"
  ],
  [
    "0x14158dc82",
    "0x14060237b",
    4,
    "932bffd1"
  ],
  [
    "0x14158e9a3",
    "0x14060237f",
    4,
    "dcdbf864"
  ],
  [
    "0x141583e23",
    "0x140602383",
    1,
    "5e"
  ],
  [
    "0x14157d33d",
    "0x140602384",
    4,
    "53bf4975"
  ],
  [
    "0x14159b30e",
    "0x140602388",
    8,
    "6c67c3a56d4a0000"
  ],
  [
    "0x14159b365",
    "0x140602390",
    4,
    "5f3a2613"
  ],
  [
    "0x1415b6a92",
    "0x140602394",
    1,
    "ce"
  ],
  [
    "0x1415b6b00",
    "0x140602395",
    4,
    "1ed2b412"
  ],
  [
    "0x141577e6c",
    "0x140602399",
    4,
    "9360abcc"
  ],
  [
    "0x1415f44ba",
    "0x14060239d",
    1,
    "93"
  ],
  [
    "0x1415f4543",
    "0x14060239e",
    4,
    "c9ba6a24"
  ],
  [
    "0x1415bd60e",
    "0x1406023a2",
    1,
    "bc"
  ],
  [
    "0x1415bd6a2",
    "0x1406023a3",
    4,
    "8eba94db"
  ],
  [
    "0x141587619",
    "0x1406023a7",
    1,
    "7f"
  ],
  [
    "0x141587691",
    "0x1406023a8",
    4,
    "90c9b42b"
  ],
  [
    "0x141604ba7",
    "0x1406023ac",
    1,
    "d1"
  ],
  [
    "0x141604c18",
    "0x1406023ad",
    4,
    "d1e34ce2"
  ],
  [
    "0x141586886",
    "0x1406023b1",
    1,
    "76"
  ],
  [
    "0x1415868fb",
    "0x1406023b2",
    4,
    "cc004a0c"
  ],
  [
    "0x1415e75df",
    "0x1406023b6",
    1,
    "37"
  ],
  [
    "0x1415e7652",
    "0x1406023b7",
    4,
    "a0f2b76d"
  ],
  [
    "0x1415be2d5",
    "0x1406023bb",
    1,
    "69"
  ],
  [
    "0x1415be344",
    "0x1406023bc",
    4,
    "4a9e45a2"
  ],
  [
    "0x1414e3f97",
    "0x1406023c0",
    1,
    "13"
  ],
  [
    "0x1414e3fef",
    "0x1406023c1",
    4,
    "483d4b03"
  ],
  [
    "0x1415c4251",
    "0x1406023c5",
    1,
    "c1"
  ],
  [
    "0x1415c42b7",
    "0x1406023c6",
    4,
    "81c0bab7"
  ],
  [
    "0x1414df8f0",
    "0x1406023ca",
    1,
    "66"
  ],
  [
    "0x1414df95d",
    "0x1406023cb",
    4,
    "e989b5ee"
  ],
  [
    "0x1415d095e",
    "0x1406023cf",
    1,
    "d0"
  ],
  [
    "0x1415d09d1",
    "0x1406023d0",
    4,
    "ff99b59c"
  ],
  [
    "0x1415d6bac",
    "0x1406023d4",
    1,
    "7e"
  ],
  [
    "0x1415d6c3a",
    "0x1406023d5",
    4,
    "79044800"
  ],
  [
    "0x1415b6a92",
    "0x1406023d9",
    1,
    "e8"
  ],
  [
    "0x1415b6b00",
    "0x1406023da",
    4,
    "80fab50a"
  ],
  [
    "0x141587619",
    "0x1406023de",
    1,
    "f7"
  ],
  [
    "0x141587691",
    "0x1406023df",
    4,
    "180eb22b"
  ],
  [
    "0x141604ba7",
    "0x1406023e3",
    1,
    "59"
  ],
  [
    "0x141604c18",
    "0x1406023e4",
    4,
    "59244ae2"
  ],
  [
    "0x141586886",
    "0x1406023e8",
    1,
    "a6"
  ],
  [
    "0x1415868fb",
    "0x1406023e9",
    4,
    "1cc74c0c"
  ],
  [
    "0x1415e75df",
    "0x1406023ed",
    1,
    "ef"
  ],
  [
    "0x1415e7652",
    "0x1406023ee",
    4,
    "7835b16d"
  ],
  [
    "0x1415be2d5",
    "0x1406023f2",
    1,
    "51"
  ],
  [
    "0x1415be344",
    "0x1406023f3",
    4,
    "f25943a2"
  ],
  [
    "0x1414e3f97",
    "0x1406023f7",
    1,
    "9b"
  ],
  [
    "0x1414e3fef",
    "0x1406023f8",
    4,
    "40fa4d03"
  ],
  [
    "0x1415c4251",
    "0x1406023fc",
    1,
    "61"
  ],
  [
    "0x1415c42b7",
    "0x1406023fd",
    4,
    "a107bcb7"
  ],
  [
    "0x1414df8f0",
    "0x140602401",
    1,
    "76"
  ],
  [
    "0x1414df95d",
    "
[Recorded excerpt: file exceeds 48,000 characters.]
````````````


File: `reverse/CyberCup-2077/cc2_init.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--entry',type=lambda x:int(x,0),default=0x1406987c0);a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr in (0x30000000,0x7ff00000):u.mem_write(addr,blob)
put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000)
put(0x14134d552,0x30010000)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]
tsc=100000000; alloc_next=0x30020000
def hook(u,pc,size,data):
 global tsc,alloc_next
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  elif name=='VirtualQuery':
   ptr=u.reg_read(UC_X86_REG_RCX);buf=u.reg_read(UC_X86_REG_RDX)
   u.mem_write(buf,struct.pack('<QQIIQIIII',ptr&~0xfff,0,0,0,0x200000,0x10000,0,0,0));v=48
  elif name=='VirtualAlloc':
   requested=u.reg_read(UC_X86_REG_RCX);sz=u.reg_read(UC_X86_REG_RDX)
   if requested:
    v=requested
    try:u.mem_map(v&~0xfff,(sz+0xfff)&~0xfff)
    except unicorn.UcError:pass
   else:v=alloc_next;alloc_next+=(sz+0xfff)&~0xfff
   print('ALLOC',hex(v),hex(sz))
  elif name=='VirtualFree':v=1

  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 if hv.resolve_fault(u,u.reg_read(UC_X86_REG_RIP),p):return True
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0xfffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
reads=[]
def read(u,access,addr,size,value,data):
 if (base<=addr<base+0x124b000) or 0x30000000<=addr<0x40000000 or 0x7ff00000<=addr<0x80000000:
  reads.append([hex(u.reg_read(UC_X86_REG_RIP)),hex(addr),size,bytes(u.mem_read(addr,size)).hex()])
u.hook_add(unicorn.UC_HOOK_MEM_READ,read)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(a.entry if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_init_'+hex(a.entry)+'_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

import json
Path('cc2_init_datareads.json').write_text(json.dumps(reads,indent=2))

Path('cc2_init_memory.bin').write_bytes(u.mem_read(0x30000000,alloc_next-0x30000000))

````````````


File: `reverse/CyberCup-2077/cc2_init_0x1406987c0_traps.json`

````````````text
{"5375065498": [3, 5384715616, 105608950841344], "5375122599": [3, 5384783216, 105608952938496], "5375173991": [3, 5384850816, 105608955035648], "5375229063": [3, 5384918416, 105608957132800], "5375290951": [3, 5384986016, 105608959229952], "5375347994": [3, 5385053616, 105608961327104], "5375400032": [3, 5385121216, 105608963424256], "5375454992": [3, 5385188816, 105608965521408], "5375515328": [3, 5385256416, 105608967618560], "5375620202": [3, 5385324016, 105608969715712], "5375622455": [3, 5386896896, 105608971812864]}
````````````


File: `reverse/CyberCup-2077/cc2_init_datareads.json`

````````````text
[
  [
    "0x14150db13",
    "0x1406474c8",
    4,
    "ebd49654"
  ],
  [
    "0x1414d5f62",
    "0x1406474cc",
    1,
    "1d"
  ],
  [
    "0x1414d5f99",
    "0x1406474cd",
    4,
    "08701880"
  ],
  [
    "0x1414b5f19",
    "0x1406474d1",
    1,
    "be"
  ],
  [
    "0x1414b5f7c",
    "0x1406474d2",
    4,
    "0308e53f"
  ],
  [
    "0x1414b4027",
    "0x1406474d6",
    1,
    "24"
  ],
  [
    "0x1414b4082",
    "0x1406474d7",
    4,
    "4601e780"
  ],
  [
    "0x141538314",
    "0x1406474db",
    1,
    "cc"
  ],
  [
    "0x141538360",
    "0x1406474dc",
    4,
    "9912ee00"
  ],
  [
    "0x1416089c8",
    "0x1406474e0",
    1,
    "fe"
  ],
  [
    "0x141608a1d",
    "0x1406474e1",
    4,
    "551a1dc0"
  ],
  [
    "0x14155c78c",
    "0x1406474e5",
    1,
    "14"
  ],
  [
    "0x14155c7de",
    "0x1406474e6",
    4,
    "0d11177f"
  ],
  [
    "0x1415fae99",
    "0x1406474ea",
    1,
    "48"
  ],
  [
    "0x1415faed5",
    "0x1406474eb",
    4,
    "0896e77f"
  ],
  [
    "0x1414c1582",
    "0x1406474ef",
    1,
    "87"
  ],
  [
    "0x1414c15ce",
    "0x1406474f0",
    4,
    "93cef080"
  ],
  [
    "0x1414cb3ba",
    "0x1406474f4",
    1,
    "8f"
  ],
  [
    "0x1414cb406",
    "0x1406474f5",
    4,
    "f27ef200"
  ],
  [
    "0x14154d9d2",
    "0x1406474f9",
    1,
    "ad"
  ],
  [
    "0x14154da30",
    "0x1406474fa",
    4,
    "bcb4fa80"
  ],
  [
    "0x141607161",
    "0x1406474fe",
    1,
    "61"
  ],
  [
    "0x1416071b2",
    "0x1406474ff",
    4,
    "05fd08c0"
  ],
  [
    "0x1414d5f62",
    "0x140647503",
    1,
    "c7"
  ],
  [
    "0x1414d5f99",
    "0x140647504",
    4,
    "d254e07f"
  ],
  [
    "0x1414b5f19",
    "0x140647508",
    1,
    "ec"
  ],
  [
    "0x1414b5f7c",
    "0x140647509",
    4,
    "512c1dc0"
  ],
  [
    "0x1414b4027",
    "0x14064750d",
    1,
    "a6"
  ],
  [
    "0x1414b4082",
    "0x14064750e",
    4,
    "e4251f7f"
  ],
  [
    "0x141538314",
    "0x140647512",
    1,
    "1e"
  ],
  [
    "0x141538360",
    "0x140647513",
    4,
    "6b3616ff"
  ],
  [
    "0x1416089c8",
    "0x140647517",
    1,
    "fc"
  ],
  [
    "0x141608a1d",
    "0x140647518",
    4,
    "773ee53f"
  ],
  [
    "0x14155c78c",
    "0x14064751c",
    1,
    "56"
  ],
  [
    "0x14155c7de",
    "0x14064751d",
    4,
    "8f35ef80"
  ],
  [
    "0x1415fae99",
    "0x140647521",
    1,
    "5a"
  ],
  [
    "0x1415faed5",
    "0x140647522",
    4,
    "fab21f80"
  ],
  [
    "0x1414c1582",
    "0x140647526",
    1,
    "7d"
  ],
  [
    "0x1414c15ce",
    "0x140647527",
    4,
    "d3fc0a7f"
  ],
  [
    "0x14154da49",
    "0x14064752b",
    8,
    "ec86f74c01000000"
  ],
  [
    "0x14154da9e",
    "0x140647533",
    4,
    "527dc7fb"
  ],
  [
    "0x1414e96c6",
    "0x140647537",
    1,
    "76"
  ],
  [
    "0x1414e9730",
    "0x140647538",
    4,
    "009e5534"
  ],
  [
    "0x14156e989",
    "0x14064753c",
    4,
    "d4ab95c5"
  ],
  [
    "0x1414cb3ba",
    "0x140647540",
    1,
    "53"
  ],
  [
    "0x1414cb406",
    "0x140647541",
    4,
    "ce2406ff"
  ],
  [
    "0x14154d9d2",
    "0x140647545",
    1,
    "01"
  ],
  [
    "0x14154da30",
    "0x140647546",
    4,
    "60dcf17f"
  ],
  [
    "0x1414c3996",
    "0x14064754a",
    4,
    "78aa84bf"
  ],
  [
    "0x1414c39ea",
    "0x14064754e",
    4,
    "a27b0d8d"
  ],
  [
    "0x14154b60c",
    "0x140647552",
    1,
    "70"
  ],
  [
    "0x1415fe579",
    "0x140647553",
    4,
    "9e44739e"
  ],
  [
    "0x14152da63",
    "0x140647557",
    4,
    "532264c2"
  ],
  [
    "0x141607161",
    "0x14064755b",
    1,
    "00"
  ],
  [
    "0x1416071b2",
    "0x14064755c",
    4,
    "b3ac04bf"
  ],
  [
    "0x1414f92a4",
    "0x140647560",
    4,
    "e8e4ce36"
  ],
  [
    "0x141504446",
    "0x140647564",
    4,
    "363126db"
  ],
  [
    "0x14160c664",
    "0x140647568",
    4,
    "05a637b2"
  ],
  [
    "0x1414d5f62",
    "0x14064756c",
    1,
    "06"
  ],
  [
    "0x1414d5f99",
    "0x14064756d",
    4,
    "fc6becff"
  ],
  [
    "0x1414f7ce8",
    "0x140647571",
    1,
    "de"
  ],
  [
    "0x1415272df",
    "0x140647572",
    4,
    "70dcd0f2"
  ],
  [
    "0x141514759",
    "0x140647576",
    4,
    "4d3b6fbf"
  ],
  [
    "0x1415147b3",
    "0x14064757a",
    4,
    "d43911dd"
  ],
  [
    "0x1414bd03b",
    "0x14064757e",
    1,
    "2f"
  ],
  [
    "0x1414bd08c",
    "0x14064757f",
    4,
    "237fb986"
  ],
  [
    "0x14153c87c",
    "0x140647583",
    1,
    "d6"
  ],
  [
    "0x14155ba23",
    "0x140647584",
    4,
    "556ebffe"
  ],
  [
    "0x14160b49b",
    "0x140647588",
    4,
    "30b965d4"
  ],
  [
    "0x1414b5f19",
    "0x14064758c",
    1,
    "e1"
  ],
  [
    "0x1414b5f7c",
    "0x14064758d",
    4,
    "059ef47f"
  ],
  [
    "0x1414daf81",
    "0x140647591",
    1,
    "35"
  ],
  [
    "0x1414d66cc",
    "0x140647592",
    4,
    "a97798c6"
  ],
  [
    "0x1414f76e2",
    "0x140647596",
    4,
    "809d77bf"
  ],
  [
    "0x1414f7733",
    "0x14064759a",
    4,
    "199e31fb"
  ],
  [
    "0x1414b26ff",
    "0x14064759e",
    1,
    "17"
  ],
  [
    "0x1414b277d",
    "0x14064759f",
    4,
    "6d00ba6f"
  ],
  [
    "0x1415479d6",
    "0x1406475a3",
    1,
    "c2"
  ],
  [
    "0x141547a46",
    "0x1406475a4",
    4,
    "b35253d2"
  ],
  [
    "0x141557762",
    "0x1406475a8",
    8,
    "ba0df2b301faffff"
  ],
  [
    "0x141545754",
    "0x1406475b0",
    4,
    "645e5e11"
  ],
  [
    "0x141508759",
    "0x7ff00060",
    8,
    "0010f07f00000000"
  ],
  [
    "0x141508768",
    "0x1406475b4",
    4,
    "5d704688"
  ],
  [
    "0x1414b4027",
    "0x1406475b8",
    1,
    "a7"
  ],
  [
    "0x1414b4082",
    "0x1406475b9",
    4,
    "b7320740"
  ],
  [
    "0x141575f37",
    "0x1406475bd",
    2,
    "2a9d"
  ],
  [
    "0x141575fb3",
    "0x1406475bf",
    4,
    "8b07b997"
  ],
  [
    "0x14154b516",
    "0x1406475c3",
    1,
    "db"
  ],
  [
    "0x14154b58a",
    "0x1406475c4",
    4,
    "09f151cb"
  ],
  [
    "0x14155acb1",
    "0x1406475c8",
    8,
    "9707024c01eeffff"
  ],
  [
    "0x14155ad0d",
    "0x1406475d0",
    4,
    "09957e8b"
  ],
  [
    "0x1414d62e4",
    "0x1406475d4",
    4,
    "f2bfcf4a"
  ],
  [
    "0x141538314",
    "0x1406475d8",
    1,
    "0b"
  ],
  [
    "0x141538360",
    "0x1406475d9",
    4,
    "c8110740"
  ],
  [
    "0x1415fb76e",
    "0x7ff01120",
    2,
    "614a"
  ],
  [
    "0x1415fb78d",
    "0x1406475dd",
    4,
    "44b7349b"
  ],
  [
    "0x141603fef",
    "0x1406475e1",
    1,
    "03"
  ],
  [
    "0x14160404d",
    "0x1406475e2",
    4,
    "5b727d35"
  ],
  [
    "0x1414b8442",
    "0x1406475e6",
    4,
    "dee463bf"
  ],
  [
    "0x1414b849a",
    "0x1406475ea",
    4,
    "fa2d49ff"
  ],
  [
    "0x1414d635c",
    "0x1406475ee",
    1,
    "cc"
  ],
  [
    "0x1414d63bd",
    "0x1406475ef",
    4,
    "fb1620f1"
  ],
  [
    "0x1414dadc7",
    "0x1406475f3",
    8,
    "c1fe154ce1aab2ec"
  ],
  [
    "0x1414dae31",
    "0x1406475fb",
    4,
    "c6efca44"
  ],
  [
    "0x1415414df",
    "0x1406475ff",
    1,
    "78"
  ],
  [
    "0x14154153e",
    "0x140647600",
    4,
    "79ac8b75"
  ],
  [
    "0x141532bd4",
    "0x140647604",
    4,
    "6c7b1b73"
  ],
  [
    "0x1416089c8",
    "0x140647608",
    1,
    "23"
  ],
  [
    "0x141608a1d",
    "0x140647609",
    4,
    "352cd941"
  ],
  [
    "0x1414f260d",
    "0x14064760d",
    4,
    "99973e57"
  ],
  [
    "0x14155c78c",
    "0x140647611",
    1,
    "93"
  ],
  [
    "0x14155c7de",
    "0x140647612",
    4,
    "dca834be"
  ],
  [
    "0x1414e40d7",
    "0x140647616",
    2,
    "a258"
  ],
  [
    "0x1414e414e",
    "0x140647618",
    4,
    "571e82d6"
  ],
  [
    "0x1414aea6b",
    "0x14064761c",
    1,
    "82"
  ],
  [
    "0x1414aead3",
    "0x14064761d",
    4,
    "60b462d0"
  ],
  [
    "0x141513030",
    "0x140647621",
    4,
    "6e225d6f"
  ],
  [
    "0x1415fae99",
    "0x140647625",
    1,
    "d6"
  ],
  [
    "0x1415faed5",
    "0x140647626",
    4,
    "6fca3bbe"
  ],
  [
    "0x141560b96",
    "0x14064762a",
    1,
    "fd"
  ],
  [
    "0x141560c17",
    "0x14064762b",
    4,
    "d0d2c9da"
  ],
  [
    "0x1414c3b52",
    "0x14064762f",
    1,
    "43"
  ],
  [
    "0x141505224",
    "0x140647630",
    4,
    "b96a6b68"
  ],
  [
    "0x141551dd9",
    "0x140647634",
    1,
    "7c"
  ],
  [
    "0x141551e22",
    "0x140647635",
    4,
    "8775b130"
  ],
  [
    "0x1414f9f03",
    "0x140647639",
    4,
    "94667393"
  ],
  [
    "0x1414c1582",
    "0x14064763d",
    1,
    "e3"
  ],
  [
    "0x1414c15ce",
    "0x14064763e",
    4,
    "60f7c93e"
  ],
  [
    "0x141534778",
    "0x140647642",
    1,
    "a3"
  ],
  [
    "0x1415347f2",
    "0x140647643",
    4,
    "dfd85687"
  ],
  [
    "0x1414d0eac",
    "0x140647647",
    4,
    "2bcdb601"
  ],
  [
    "0x1414d0f19",
    "0x14064764b",
    4,
    "0f053c98"
  ],
  [
    "0x1414d8e77",
    "0x14064764f",
    1,
    "06"
  ],
  [
    "0x1414d8edb",
    "0x140647650",
    4,
    "119ff8cc"
  ],
  [
    "0x1415fb8a8",
    "0x140647654",
    1,
    "ff"
  ],
  [
    "0x1415fb904",
    "0x140647655",
    4,
    "7081a4b6"
  ],
  [
    "0x1414d210b",
    "0x140647659",
    1,
    "9c"
  ],
  [
    "0x141606201",
    "0x14064765a",
    4,
    "e6996598"
  ],
  [
    "0x1414f63ab",
    "0x14064765e",
    4,
    "ec98ed0c"
  ],
  [
    "0x1414cb3ba",
    "0x140647662",
    1,
    "4b"
  ],
  [
    "0x1414cb406",
    "0x140647663",
    4,
    "8c76c9c1"
  ],
  [
    "0x1414c631c",
    "0x140647667",
    1,
    "d6"
  ],
  [
    "0x141508fef",
    "0x140647668",
    4,
    "740f648a"
  ],
  [
    "0x14155a747",
    "0x14064766c",
    8,
    "eaf9370d00ffffff"
  ],
  [
    "0x14155a7ab",
    "0x140647674",
    4,
    "bb3dd867"
  ],
  [
    "0x14157af0e",
    "0x140647678",
    4,
    "281e25db"
  ],
  [
    "0x14154d9d2",
    "0x14064767c",
    1,
    "bf"
  ],
  [
    "0x14154da30",
    "0x14064767d",
    4,
    "d5203f41"
  ],
  [
    "0x14156c804",
    "0x30010010",
    4,
    "c56d0000"
  ],
  [
    "0x14156c81d",
    "0x140647681",
    4,
    "89ab3084"
  ],
  [
    "0x141550267",
    "0x140647685",
    1,
    "88"
  ],
  [
    "0x1415502c0",
    "0x140647686",
    4,
    "865d613a"
  ],
  [
    "0x1414faa6c",
    "0x14064768a",
    4,
    "3127ba01"
  ],
  [
    "0x141543194",
    "0x14064768e",
    4,
    "15ff1550"
  ],
  [
    "0x141600578",
    "0x140647692",
    1,
    "d2"
  ],
  [
    "0x1414ed159",
    "0x140647693",
    4,
    "25af577b"
  ],
  [
    "0x141558d0c",
    "0x140647697",
    1,
    "01"
  ],
  [
    "0x141558d77",
    "0x140647698",
    4,
    "51097330"
  ],
  [
    "0x14157a32c",
    "0x14064769c",
    4,
    "96e54183"
  ],
  [
    "0x141607161",
    "0x1406476a0",
    1,
    "f9"
  ],
  [
    "0x1416071b2",
    "0x1406476a1",
    4,
    "374f2efe"
  ],
  [
    "0x1414e2ab3",
    "0x1406476a5",
    1,
    "9e"
  ],
  [
    "0x1414e2b0d",
    "0x1406476a6",
    4,
    "7a76944f"
  ],
  [
    "0x14151f011",
    "0x1406476aa",
    1,
    "78"
  ],
  [
    "0x14151f06e",
    "0x1406476ab",
    4,
    "abab9777"
  ],
  [
    "0x14154b60c",
    "0x1406476af",
    1,
    "0b"
  ],
  [
    "0x1415fe579",
    "0x1406476b0",
    4,
    "4f9a94df"
  ],
  [
    "0x141568df8",
    "0x1406476b4",
    4,
    "bb65c8f6"
  ],
  [
    "0x1414d5f62",
    "0x1406476b8",
    1,
    "d1"
  ],
  [
    "0x1414d5f99",
    "0x1406476b9",
    4,
    "981fc0fe"
  ],
  [
    "0x1415465d1",
    "0x1406476bd",
    4,
    "812b970c"
  ],
  [
    "0x1414b5f19",
    "0x1406476c1",
    1,
    "e2"
  ],
  [
    "0x1414b5f7c",
    "0x1406476c2",
    4,
    "cc5c3241"
  ],
  [
    "0x14155562a",
    "0x1406476c6",
    4,
    "2f3177f3"
  ],
  [
    "0x1414b4027",
    "0x1406476ca",
    1,
    "70"
  ],
  [
    "0x1414b4082",
    "0x1406476cb",
    4,
    "bb32cdfe"
  ],
  [
    "0x1414f7ce8",
    "0x1406476cf",
    1,
    "15"
  ],
  [
    "0x1415272df",
    "0x1406476d0",
    4,
    "902cd22c"
  ],
  [
    "0x141572a92",
    "0x1406476d4",
    4,
    "7fac6989"
  ],
  [
    "0x1414cdb86",
    "0x1406476d8",
    4,
    "dfc2e0aa"
  ],
  [
    "0x1414bd03b",
    "0x1406476dc",
    1,
    "3f"
  ],
  [
    "0x1414bd08c",
    "0x1406476dd",
    4,
    "33576838"
  ],
  [
    "0x14153c87c",
    "0x1406476e1",
    1,
    "0e"
  ],
  [
    "0x14155ba23",
    "0x1406476e2",
    4,
    "4fc0bc28"
  ],
  [
    "0x1414fd9f0",
    "0x1406476e6",
    4,
    "26d19b7c"
  ],
  [
    "0x141538314",
    "0x1406476ea",
    1,
    "0d"
  ],
  [
    "0x141538360",
    "0x1406476eb",
    4,
    "49083c81"
  ],
  [
    "0x14156d2c1",
    "0x1406476ef",
    4,
    "c9aabff6"
  ],
  [
    "0x1416089c8",
    "0x1406476f3",
    1,
    "21"
  ],
  [
    "0x141608a1d",
    "0x1406476f4",
    4,
    "be1fcb81"
  ],
  [
    "0x141557ace",
    "0x1406476f8",
    4,
    "e1d29876"
  ],
  [
    "0x14154dd8a",
    "0x1406476fc",
    4,
    "bd42d848"
  ],
  [
    "0x1414aea6b",
    "0x140647700",
    1,
    "69"
  ],
  [
    "0x1414aead3",
    "0x140647701",
    4,
    "d1359b67"
  ],
  [
    "0x1414fd5a8",
    "0x140647705",
    4,
    "7d55b2f6"
  ],
  [
    "0x14155c78c",
    "0x140647709",
    1,
    "31"
  ],
  [
    "0x14155c7de",
    "0x14064770a",
    4,
    "374dc9c1"
  ],
  [
    "0x14153dc4c",
    "0x14064770e",
    4,
    "3d6b4589"
  ],
  [
    "0x1415fae99",
    "0x140647712",
    1,
    "33"
  ],
  [
    "0x1415faed5",
    "0x140647713",
    4,
    "f78e387e"
  ],
  [
    "0x1414daf81",
    "0x140647717",
    1,
    "ee"
  ],
  [
    "0x1414d66cc",
    "0x140647718",
    4,
    "1c23032c"
  ],
  [
    "0x1415341f2",
    "0x14064771c",
    4,
    "349ca801"
  ],
  [
    "0x14153424d",
    "0x140647720",
    4,
    "ad63b955"
  ],
  [
    "0x1414b26ff",
    "0x140647724",
    1,
    "d5"
  ],
  [
    "0x1414b277d",
    "0x140647725",
    4,
    "f455a16c"
  ],
  [
    "0x1414b6490",
    "0x140647729",
    4,
    "1e455ffe"
  ],
  [
    "0x1414b64ec",
    "0x14064772d",
    4,
    "3a94bfdb"
  ],
  [
    "0x1415479d6",
    "0x140647731",
    1,
    "a7"
  ],
  [
    "0x141547a46",
    "0x140647732",
    4,
    "0a821703"
  ],
  [
    "0x141511fff",
    "0x140647736",
    4,
    "fdf6aa01"
  ],
  [
    "0x1414d20e4",
    "0x14064773a",
    4,
    "d921406d"
  ],
  [
    "0x141603fef",
    "0x14064773e",
    1,
    "3c"
  ],
  [
    "0x14160404d",
    "0x14064773f",
    4,
    "d23b3cb6"
  ],
  [
    "0x1415674cd",
    "0x140647743",
    8,
    "5352240d80faffff"
  ],
  [
    "0x141532360",
    "0x14064774b",
    4,
    "b5c1f8c9"
  ],
  [
    "0x1414e36bf",
    "0x14064774f",
    1,
    "ee"
  ],
  [
    "0x1414e372c",
    "0x140647750",
    4,
    "4dd17e8a"
  ],
  [
    "0x14160054d",
    "0x140647754",
    4,
    "99cf3c8b"
  ],
  [
    "0x1414c1582",
    "0x140647758",
    1,
    "fa"
  ],
  [
    "0x1414c15ce",
    "0x140647759",
    4,
    "8ea525c1"
  ],
  [
    "0x1414cb3ba",
    "0x14064775d",
    1,
    "c2"
  ],
  [
    "0x1414cb406",
    "0x14064775e",
    4,
    "ba662781"
  ],
  [
    "0x141569e28",
    "0x140647762",
    8,
    "9f66dbf290091a1c"
  ],
  [
    "0x1414c3a68",
    "0x14064776a",
    4,
    "ad6d7f9b"
  ],
  [
    "0x1414c474f",
    "0x14064776e",
    1,
    "83"
  ],
  [
    "0x1414c47a3",
    "0x14064776f",
    4,
    "415b4234"
  ],
  [
    "0x1414d69da",
    "0x140647773",
    1,
    "b8"
  ],
  [
    "0x1414d6a30",
    "0x140647774",
    4,
    "243a4034"
  ],
  [
    "0x1414fcb4b",
    "0x140647778",
    1,
    "61"
  ],
  [
    "0x1414fcba1",
    "0x140647779",
    4,
    "476a4534"
  ],
  [
    "0x141551c1a",
    "0x14064777d",
    1,
    "4e"
  ],
  [
    "0x141524f33",
    "0x14064777e",
    4,
    "319abecb"
  ],
  [
    "0x141510d10",
    "0x140647782",
    1,
    "20"
  ],
  [
    "0x141510d81",
    "0x140647783",
    4,
    "4b174434"
  ],
  [
    "0x1414b9a32",
    "0x140647787",
    1,
    "4a"
  ],
  [
    "0x1414b9a94",
    "0x140647788",
    4,
    "8beb4634"
  ],
  [
    "0x1414e96c6",
    "0x14064778c",
    1,
    "6e"
  ],
  [
    "0x1414e9730",
    "0x14064778d",
    4,
    "d3f54034"
  ],
  [
    "0x14154b516",
    "0x140647791",
    1,
    "8e"
  ],
  [
    "0x14154b58a",
    "0x140647792",
    4,
    "aaaabfcb"
  ],
  [
    "0x1415414df",
    "0x140647796",
    1,
    "87"
  ],
  [
    "0x14154153e",
    "0x140647797",
    4,
    "ffe44734"
  ],
  [
    "0x1414c631c",
    "0x14064779b",
    1,
    "1a"
  ],
  [
    "0x141508fef",
    "0x14064779c",
    4,
    "70374634"
  ],
  [
    "0x1414e36bf",
    "0x1406477a0",
    1,
    "11"
  ],
  [
    "0x1414e372c",
    "0x1406477a1",
    4,
    "6c27b8cb"
  ],
  [
    "0x1414c474f",
    "0x1406477a5",
    1,
    "d9"
  ],
  [
    "0x1414c47a3",
    "0x1406477a6",
    4,
    "db05b9cb"
  ],
  [
    "0x1414d69da",
    "0x1406477aa",
    1,
    "fa"
  ],
  [
    "0x1414d6a30",
    "0x1406477ab",
    4,
    "e664bbcb"
  ],
  [
    "0x1414fcb4b",
    "0x1406477af",
    1,
    "13"
  ],
  [
    "0x1414fcba1",
    "0x1406477b0",
    4,
    "5534becb"
  ],
  [
    "0x141551c1a",
    "0x1406477b4",
    1,
    "6c"
  ],
  [
    "0x141524f33",
    "0x1406477b5",
    4,
    "f3c44534"
  ],
  [
    "0x141510d10",
    "0x1406477b9",
    1,
    "9a"
  ],
  [
    "0x141510d81",
    "0x1406477ba",
    4,
    "7149bfcb"
  ],
  [
    "0x1414b9a32",
    "0x1406477be",
    1,
    "68"
  ],
  [
    "0x1414b9a94",
    "0x1406477bf",
    4,
    "a9b5bdcb"
  ],
  [
    "0x1414e96c6",
    "0x1406477c3",
    1,
    "ec"
  ],
  [
    "0x1414e9730",
    "0x1406477c4",
    4,
    "5df1bfcb"
  ],
  [
    "0x14150db13",
    "0x1406477c8",
    4,
    "3e959254"
  ],
  [
    "0x14154d9d2",
    "0x1406477cc",
    1,
    "6f"
  ],
  [
    "0x14154da30",
    "0x1406477cd",
    4,
    "5e931a7f"
  ],
  [
    "0x141607161",
    "0x1406477d1",
    1,
    "0b"
  ],
  [
    "0x1416071b2",
    "0x1406477d2",
    4,
    "6fdae83f"
  ],
  [
    "0x1414d5f62",
    "0x1406477d6",
    1,
    "8d"
  ],
  [
    "0x1414d5f99",
    "0x1406477d7",
    4,
    "98730080"
  ],
  [
    "0x1414b5f19",
    "0x1406477db",
    1,
    "be"
  ],
  [
    "0x1414b5f7c",
    "0x1406477dc",
    4,
    "230bfd3f"
  ],
  [
    "0x1414b4027",
    "0x1406477e0",
    1,
    "14"
  ],
  [
    "0x1414b4082",
    "0x1406477e1",
    4,
    "5602ff80"
  ],
  [
    "0x141538314",
    "0x1406477e5",
    1,
    "0c"
  ],
  [
    "0x141538360",
    "0x1406477e6",
    4,
    "b911f600"
  ],
  [
    "0x1416089c8",
    "0x1406477ea",
    1,
    "0e"
  ],
  [
    "0x141608a1d",
    "0x1406477eb",
    4,
    "851905c0"
  ],
  [
    "0x14155c78c",
    "0x1406477ef",
    1,
    "7c"
  ],
  [
    "0x14155c7de",
    "0x1406477f0",
    4,
    "45120f7f"
  ],
  [
    "0x1415fae99",
    "0x1406477f4",
    1,
    "58"
  ],
  [
    "0x1415faed5",
    "0x1406477f5",
    4,
    "7895ff7f"
  ],
  [
    "0x1414c1582",
    "0x1406477f9",
    1,
    "e7"
  ],
  [
    "0x1414c15ce",
    "0x1406477fa",
    4,
    "93cde880"
  ],
  [
    "0x1414cb3ba",
    "0x1406477fe",
    1,
    "f7"
  ],
  [
    "0x1414cb406",
    "0x1406477ff",
    4,
    "ea7dea00"
  ],
  [
    "0x14154d9d2",
    "0x140647803",
    1,
    "f5"
  ],
  [
    "0x14154da30",
    "0x140647804",
    4,
    "e4b7e280"
  ],
  [
    "0x141607161",
    "0x140647808",
    1,
    "11"
  ],
  [
    "0x1416071b2",
    "0x140647809",
    4,
    "b5fe10c0"
  ],
  [
    "0x1414d5f62",
    "0x14064780d",
    1,
    "af"
  ],
  [
    "0x1414d5f99",
    "0x14064780e",
    4,
    "5a57f87f"
  ],
  [
    "0x1414b5f19",
    "0x140647812",
    1,
    "cc"
  ],
  [
    "0x1414b5f7c",
    "0x140647813",
    4,
    "712f05c0"
  ],
  [
    "0x1414b4027",
    "0x140647817",
    1,
    "96"
  ],
  [
    "0x1414b4082",
    "0x140647818",
    4,
    "f426077f"
  ],
  [
    "0x141538314",
    "0x14064781c",
    1,
    "3e"
  ],
  [
    "0x141538360",
    "0x14064781d",
    4,
    "6b350eff"
  ],
  [
    "0x1416089c8",
    "0x140647821",
    1,
    "3c"
  ],
  [
    "0x141608a1d",
    "0x140647822",
    4,
    "b73dfd3f"
  ],
  [
    "0x14155c78c",
    "0x140647826",
    1,
    "e6"
  ],
  [
    "0x14155c7de",
    "0x140647827",
    4,
    "8db60800"
  ],
  [
    "0x1414dadc7",
    "0x14064782b",
    8,
    "be26f54c01000000"
  ],
  [
    "0x1414dae31",
    "0x140647833",
    4,
    "ffaa1d0e"
  ],
  [
    "0x14154b516",
    "0x140647837",
    1,
    "ae"
  ],
  [
    "0x14154b58a",
    "0x140647838",
    4,
    "24ec5b34"
  ],
  [
    "0x1414ef0ac",
    "0x14064783c",
    4,
    "0d4c4b12"
  ],
  [
    "0x1415fae99",
    "0x140647840",
    1,
    "fa"
  ],
  [
    "0x1415faed5",
    "0x140647841",
    4,
    "ba321480"
  ],
  [
    "0x1414c1582",
    "0x140647845",
    1,
    "bd"
  ],
  [
    "0x1414c15ce",
    "0x140647846",
    4,
    "f9b202ff"
  ],
  [
    "0x1415414df",
    "0x14064784a",
    1,
    "ed"
  ],
  [
    "0x14154153e",
    "0x14064784b",
    4,
    "bea5accb"
  ],
  [
    "0x1416083c7",
    "0x30010058",
    4,
    "5f3b2830"
  ],
  [
    "0x1416083e6",
    "0x14064784f",
    4,
    "0c1f343a"
  ],
  [
    "0x1414d635c",
    "0x140647853",
    1,
    "1b"
  ],
  [
    "0x1414d63bd",
    "0x140647854",
    4,
    "c0d1617d"
  ],
  [
    "0x1414c3996",
    "0x140647858",
    4,
    "2fd59abf"
  ],
  [
    "0x1414c39ea",
    "0x14064785c",
    4,
    "0b04bed8"
  ],
  [
    "0x141560b96",
    "0x140647860",
    1,
    "5e"
  ],
  [
    "0x141560c17",
    "0x140647861",
    4,
    "56d68e34"
  ],
  [
    "0x141514759",
    "0x140647865",
    4,
    "2b3f9053"
  ],
  [
    "0x1415147b3",
    "0x140647869",
    4,
    "38c690e4"
  ],
  [
    "0x1414c3b52",
    "0x14064786d",
    1,
    "d0"
  ],
  [
    "0x141505224",
    "0x14064786e",
    4,
    "3a7240d6"
  ],
  [
    "0x141551dd9",
    "0x140647872",
    1,
    "6f"
  ],
  [
    "0x141551e22",
    "0x140647873",
    4,
    "58999a3e"
  ],
  [
    "0x1414d1bae",
    "0x140647877",
    4,
    "082dc988"
  ],
  [
    "0x1414cb3ba",
    "0x14064787b",
    1,
    "bc"
  ],
  [
    "0x1414cb406",
    "0x14064787c",
    4,
    "5f72ef40"
  ],
  [
    "0x14157bc3e",
    "0x140647880",
    4,
    "415c02f7"
  ],
  [
    "0x14154d9d2",
    "0x140647884",
    1,
    "cc"
  ],
  [
    "0x14154da30",
    "0x140647885",
    4,
    "7e02e57f"
  ],
  [
    "0x1414f76e2",
    "0x140647889",
    4,
    "183869ac"
  ],
  [
    "0x1414f7733",
    "0x14064788d",
    4,
    "4ae4d53d"
  ],
  [
    "0x1415fb8a8",
    "0x140647891",
    1,
    "20"
  ],
  [
    "0x1415fb904",
    "0x140647892",
    4,
    "bf6371cf"
  ],
  [
    "0x1414d815c",
    "0x140647896",
    4,
    "1c1a8008"
  ],
  [
    "0x141607161",
    "0x14064789a",
    1,
    "24"
  ],
  [
    "0x1416071b2",
    "0x14064789b",
    4,
    "58a9f27f"
  ],
  [
    "0x141542327",
    "0x14064789f",
    4,
    "04a82af7"
  ],
  [
    "0x1414d5f62",
    "0x1406478a3",
    1,
    "6c"
  ],
  [
    "0x1414d5f99",
    "0x1406478a4",
    4,
    "74b2057f"
  ],
  [
    "0x141534778",
    "0x1406478a8",
    1,
    "23"
  ],
  [
    "0x1415347f2",
    "0x1406478a9",
    4,
    "e4f21cbd"
  ],
  [
    "0x1414d210b",
    "0x1406478ad",
    1,
    "79"
  ],
  [
    "0x141606201",
    "0x1406478ae",
    4,
    "c7b85586"
  ],
  [
    "0x141558d0c",
    "0x1406478b2",
    1,
    "c0"
  ],
  [
    "0x141558d77",
    "0x1406478b3",
    4,
    "0d528fd6"
  ],
  [
    "0x1414e2ab3",
    "0x1406478b7",
    1,
    "df"
  ],
  [
    "0x1414e2b0d",
    "0x1406478b8",
    4,
    "c7997739"
  ],
  [
    "0x1414c8531",
    "0x1406478bc",
    4,
    "59a42737"
  ],
  [
    "0x1414b5f19",
    "0x1406478c0",
    1,
    "61"
  ],
  [
    "0x1414b5f7c",
    "0x1406478c1",
    4,
    "3e6a0a3f"
  ],
  [
    "0x141539f9f",
    "0x1406478c5",
    4,
    "972e28d8"
  ],
  [
    "0x1414b4027",
    "0x1406478c9",
    1,
    "ed"
  ],
  [
    "0x1414b4082",
    "0x1406478ca",
    4,
    "f730f5c0"
  ],
  [
    "0x14154dc37",
    "0x1406478ce",
    4,
    "fbb81b36"
  ],
  [
    "0x141522507",
    "0x1406478d2",
    4,
    "85afff0c"
  ],
  [
    "0x1414b70f6",
    "0x1406478d6",
    4,
    "5c86613d"
  ],
  [
    "0x141538314",
    "0x1406478da",
    1,
    "db"
  ],
  [
    "0x141538360",
    "0x1406478db",
    4,
    "db580c40"
  ],
  [
    "0x1414d8e77",
    "0x1406478df",
    1,
    "a9"
  ],
  [
    "0x1414d8edb",
    "0x1406478e0",
    4,
    "fb031589"
  ],
  [
    "0x1414c631c",
    "0x1406478e4",
    1,
    "8f"
  ],
  [
    "0x141508fef",
    "0x1406478e5",
    4,
    "3d455034"
  ],
  [
    "0x1414e9c57",
    "0x1406478e9",
    8,
    "a3b303b3b17effff"
  ],
  [
    "0x1414e9ca2",
    "0x1406478f1",
    4,
    "08688426"
  ],
  [
    "0x1414c8719",
    "0x1406478f5",
    4,
    "dbdf6eaf"
  ],
  [
    "0x1416089c8",
    "0x1406478f9",
    1,
    "a6"
  ],
  [
    "0x141608a1d",
    "0x1406478fa",
    4,
    "faa1e0ff"
  ],
  [
    "0x14156805e",
    "0x1406478fe",
    4,
    "45d82436"
  ],
  [
    "0x14160096c",
    "0x140647902",
    4,
    "c5386703"
  ],
  [
    "0x1414b62de",
    "0x140647906",
    4,
    "d4313c30"
  ],
  [
    "0x14155c78c",
    "0x14064790a",
    1,
    "98"
  ],
  [
    "0x14155c7de",
    "0x14064790b",
    4,
    "9185feff"
  ],
  [
    "0x1414e36bf",
    "0x14064790f",
    1,
    "37"
  ],
  [
    "0x1414e372c",
    "0x140647910",
    4,
    "4a98a2cb"
  ],
  [
    "0x1414c474f",
    "0x140647914",
    1,
    "0f"
  ],
  [
    "0x1414c47a3",
    "0x140647915",
    4,
    "d8d6a0cb"
  ],
  [
    "0x1414e95c8",
    "0x140647919",
    4,
    "0e702f30"
  ],
  [
    "0x1415fae99",
    "0x14064791d",
    1,
    "fa"
  ],
  [
    "0x1415faed5",
    "0x14064791e",
    4,
    "83b3157f"
  ],
  [
    "0x1415fc086",
    "0x140647922",
    8,
    "ef2ae24cb17effff"
  ],
  [
    "0x1415fc0e5",
    "0x14064792a",
    4,
    "44390c9c"
  ],
  [
    "0x141550875",
    "0x14064792e",
    4,
    "401bf159"
  ],
  [
    "0x1414c1582",
    "0x140647932",
    1,
    "50"
  ],
  [
    "0x1414c15ce",
    "0x140647933",
    4,
    "b6af16bf"
  ],
  [
    "0x141513614",
    "0x140647937",
    4,
    "76b1a826"
  ],
  [
    "0x1414cb3ba",
    "0x14064793b",
    1,
    "16"
  ],
  [
    "0x1414cb406",
    "0x14064793c",
    4,
    "4bb3eb00"
  ],
  [
    "0x14154d9d2",
    "0x140647940",
    1,
    "7c"
  ],
  [
    "0x14154da30",
    "0x140647941",
    4,
    "26361c80"
  ],
  [
    "0x1414b8442",
    "0x140647945",
    4,
    "083697bf"
  ],
  [
    "0x1414b849a",
    "0x140647949",
    4,
    "2ce71c8d"
  ],
  [
    "0x141550267",
    "0x14064794d",
    1,
    "85"
  ],
  [
    "0x1415502c0",
    "0x14064794e",
    4,
    "4d654470"
  ],
  [
    "0x141602d3a",
    "0x140647952",
    2,
    "b115"
  ],
  [
    "0x141602d9b",
    "0x140647954",
    4,
    "4926b468"
  ],
  [
    "0x1414d69da",
    "0x140647958",
    1,
    "01"
  ],
  [
    "0x1414d6a30",
    "0x140647959",
    4,
    "3d465e34"
  ],
  [
    "0x1414fcb4b",
    "0x14064795d",
    1,
    "28"
  ],
  [
    "0x1414fcba1",
    "0x14064795e",
    4,
    "3e1a5b34"
  ],
  [
    "0x1415212cc",
    "0x140647962",
    4,
    "00cdcacf"
  ],
  [
    "0x141607161",
    "0x140647966",
    1,
    "ac"
  ],
  [
    "0x1416071b2",
    "0x140647967",
    4,
    "077309c0"
  ],
  [
    "0x14155d6a1",
    "0x14064796b",
    8,
    "f8c0f64c01040000"
  ],
  [
    "0x14155d6fc",
    "0x140647973",
    4,
    "f63cbf3d"
  ],
  [
    "0x1415026b0",
    "0x140647977",
    4,
    "a97e05a6"
  ],
  [
    "0x1414d5f62",
    "0x14064797b",
    1,
    "95"
  ],
  [
    "0x1414d5f99",
    "0x14064797c",
    4,
    "23370740"
  ],
  [
    "0x1414c4032",
    "0x140647980",
    4,
    "5875a9ac"
  ],
  [
    "0x1414b5f19",
    "0x140647984",
    1,
    "3e"
  ],
  [
    "0x1414b5f7c",
    "0x140647985",
    4,
    "3560fb40"
  ],
  [
    "0x14154da49",
    "0x140647989",
    8,
    "49ca07b3feffffff"
  ],
  [
    "0x14154da9e",
    "0x140647991",
    4,
    "f829ab33"
  ],
  [
    "0x1415098bd",
    "0x140647995",
    4,
    "f24794ea"
  ],
  [
    "0x1414b4027",
    "0x140647999",
    1,
    "79"
  ],
  [
    "0x1414b4082",
    "0x14064799a",
    4,
    "3baff880"
  ],
  [
    "0x141538314",
    "0x14064799e",
    1,
    "e9"
  ],
  [
    "0x141538360",
    "0x14064799f",
    4,
    "a53b0c00"
  ],
  [
    "0x1414e9c57",
    "0x1406479a3",
    8,
    "596bfe4c3149b8f9"
  ],
  [
    "0x1414e9ca2",
    "0x1406479ab",
    4,
    "613cb745"
  ],
  [
    "0x141551c1a",
    "0x1406479af",
    1,
    "74"
  ],
  [
    "0x141524f33",
    "0x1406479b0",
    4,
    "0b693474"
  ],
  [
    "0x141510d10",
    "0x1406479b4",
    1,
    "02"
  ],
  [
    "0x141510d81",
    "0x1406479b5",
    4,
    "82a83174"
  ],
  [
    "0x14156cec1",
    "0x1406479b9",
    4,
    "5b69ef10"
  ],
  [
    "0x1416089c8",
    "0x1406479bd",
    1,
    "46"
  ],
  [
    "0x141608a1d",
    "0x1406479be",
    4,
    "cc526740"
  ],
  [
    "0x1414d6bc9",
    "0x1406479c2",
    4,
    "6bd30bef"
  ],
  [
    "0x14155c78c",
    "0x1406479c6",
    1,
    "66"
  ],
  [
    "0x14155c7de",
    "0x1406479c7",
    4,
    "e0d086bf"
  ],
  [
    "0x1414dc99a",
    "0x1406479cb",
    4,
    "3f844c76"
  ],
  [
    "0x14157a12d",
    "0x1406479cf",
    4,
    "f6a92c4c"
  ],
  [
    "0x1414f57c5",
    "0x1406479d3",
    4,
    "202d5270"
  ],
  [
    "0x1415fae99",
    "0x1406479d7",
    1,
    "94"
  ],
  [
    "0x1415faed5",
    "0x1406479d8",
    4,
    "ede26e3f"
  ],
  [
    "0x1415fc086",
    "0x1406479dc",
    8,
    "957b990c9057b8f9"
  ],
  [
    "0x1415fc0e5",
    "0x1406479e4",
    4,
    "b862e368"
  ],
  [
    "0x1414b9a32",
    "0x1406479e8",
    1,
    "3d"
  ],
  [
    "0x1414b9a94",
    "0x1406479e9",
    4,
    "01a94034"
  ],
  [
    "0x141512226",
    "0x1406479ed",
    4,
    "13206daf"
  ],
  [
    "0x1414c1582",
    "0x1406479f1",
    1,
    "84"
  ],
  [
    "0x1414c15ce",
    "0x1406479f2",
    4,
    "82451f7f"
  ],
  [
    "0x14160d728",
    "0x1406479f6",
    4,
    "f154f7c9"
  ],
  [
    "0x1414b3d2e",
    "0x1406479fa",
    4,
    "e1a2edb2"
  ],
  [
    "0x1414afde3",
    "0x1406479fe",
    4,
    "fc8e2130"
  ],
  [
    "0x1414cb3ba",
    "0x140647a02",
    1,
    "78"
  ],
  [
    "0x1414cb406",
    "0x140647a03",
    4,
    "b091e33f"
  ],
  [
    "0x1414bf491",
    "0x140647a07",
    4,
    "18b93a06"
  ],
  [
    "0x14154d9d2",
    "0x140647a0b",
    1,
    "7a"
  ],
  [
    "0x14154da30",
    "0x140647a0c",
    4,
    "e78b1580"
  ],
  [
    "0x1414e96c6",
    "0x140647a10",
    1,
    "07"
  ],
  [
    "0x1414e9730",
    "0x140647a11",
    4,
    "16fab4cb"
  ],
  [
    "0x14155a2a5",
    "0x140647a15",
    4,
    "2323a27d"
  ],
  [
    "0x141607161",
    "0x140647a19",
    1,
    "30"
  ],
  [
    "0x1416071b2",
    "0x140647a1a",
    4,
    "b447e53f"
  ],
  [
    "0x1414d5f62",
    "0x140647a1e",
    1,
    "4e"
  ],
  [
    "0x1414d5f99",
    "0x140647a1f",
    4,
    "e544f340"
  ],
  [
    "0x14154b516",
    "0x140647a23",
    1,
    "c9"
  ],
  [
    "0x14154b58a",
    "0x140647a24",
    4,
    "ede2aecb"
  ],
  [
    "0x1415414df",
    "0x140647a28",
    1,
    "60"
  ],
  [
    "0x14154153e",
    "0x140647a29",
    4,
    "d8ac5634"
  ],
  [
    "0x1414c631c",
    "0x140647a2d",
    1,
    "c5"
  ],
  [
    "0x141508fef",
    "0x140647a2e",
    4,
    "2f7f5734"
  ],
  [
    "0x1414e36bf",
    "0x140647a32",
    1,
    "ce"
  ],
  [
    "0x1414e372c",
    "0x140647a33",
    4,
    "b36fa9cb"
  ],
  [
    "0x1414c474f",
    "0x140647a37",
    1,
    "96"
  ],
  [
    "0x1414c47a3",
    "0x140647a38",
    4,
    "744da8cb"
  ],
  [
    "0x1414d69da",
    "0x140647a3c",
    1,
    "4d"
  ],
  [
    "0x1414d6a30",
    "0x140647a3d",
    4,
    "512caacb"
  ],
  [
    "0x1414fcb4b",
    "0x140647a41",
    1,
    "8c"
  ],
  [
    "0x1414fcba1",
    "0x140647a42",
    4,
    "aa7cafcb"
  ],
  [
    "0x141551c1a",
    "0x140647a46",
    1,
    "63"
  ],
  [
    "0x141524f33",
    "0x140647a47",
    4,
    "1c8c5434"
  ],
  [
    "0x141510d10",
    "0x140647a4b",
    1,
    "ad"
  ],
  [
    "0x141510d81",
    "0x140647a4c",
    4,
    "0601aecb"
  ],
  [
    "0x1414b9a32",
    "0x140647a50",
    1,
    "37"
  ],
  [
    "0x1414b9a94",
    "0x140647a51",
    4,
    "16fdaccb"
  ],
  [
    "0x1414e96c6",
    "0x140647a55",
    1,
    "53"
  ],
  [
    "0x1414e9730",
    "0x140647a56",
    4,
    "eee3aacb"
  ],
  [
    "0x14154b516",
    "0x140647a5a",
    1,
    "63"
  ],
  [
    "0x14154b58a",
    "0x140647a5b",
    4,
    "27bc5534"
  ],
  [
    "0x1415414df",
    "0x140647a5f",
    1,
    "d2"
  ],
  [
    "0x14154153e",
    "0x140647a60",
    4,
    "6af2adcb"
  ],
  [
    "0x1414c631c",
    "0x140647a64",
    1,
    "07"
  ],
  [
    "0x141508fef",
    "0x140647a65",
    4,
    "4d21accb"
  ],
  [
    "0x1414e36bf",
    "0x140647a69",
    1,
    "4c"
  ],
  [
    "0x1414e372c",
    "0x140647a6a",
    4,
    "b1315234"
  ],
  [
    "0x1414c474f",
    "0x140647a6e",
    1,
    "e4"
  ],
  [
    "0x1414c47a3",
    "0x140647a6f",
    4,
    "a6135334"
  ],
  [
    "0x1414d69da",
    "0x140647a73",
    1,
    "8f"
  ],
  [
    "0x1414d6a30",
    "0x140647a74",
    4,
    "b3725134"
  ],
  [
    "0x1414fcb4b",
    "0x140647a78",
    1,
    "ae"
  ],
  [
    "0x1414fcba1",
    "0x140647a79",
    4,
    "08225434"
  ],
  [
    "0x141551c1a",
    "0x140647a7d",
    1,
    "c9"
  ],
  [
    "0x141524f33",
    "0x140647a7e",
    4,
    "d6d2afcb"
  ],
  [
    "0x141510d10",
    "0x140647a82",
    1,
    "97"
  ],
  [
    "0x141510d81",
    "0x140647a83",
    4,
    "ecdbaacb"
  ],
  [
    "0x14150db13",
    "0x140647b6d",
    4,
    "4edb9654"
  ],
  [
    "0x1414d5f62",
    "0x140647b71",
    1,
    "68"
  ],
  [
    "0x1414d5f99",
    "0x140647b72",
    4,
    "5d7f1880"
  ],
  [
    "0x1414b5f19",
    "0x140647b76",
    1,
    "cb"
  ],
  [
    "0x1414b5f7c",
    "0x140647b77",
    4,
    "7607e53f"
  ],
  [
    "0x1414b4027",
    "0x140647b7b",
    1,
    "61"
  ],
  [
    "0x1414b4082",
    "0x140647b7c",
    4,
    "230ee780"
  ],
  [
    "0x141538314",
    "0x140647b80",
    1,
    "19"
  ],
  [
    "0x141538360",
    "0x140647b81",
    4,
    "6c1dee00"
  ],
  [
    "0x1416089c8",
    "0x140647b85",
    1,
    "63"
  ],
  [
    "0x141608a1d",
    "0x140647b86",
    4,
    "08151dc0"
  ],
  [
    "0x14155c78c",
    "0x140647b8a",
    1,
    "49"
  ],
  [
    "0x14155c7de",
    "0x140647b8b",
    4,
    "501e177f"
  ],
  [
    "0x1415fae99",
    "0x140647b8f",
    1,
    "dd"
  ],
  [
    "0x1415faed5",
    "0x140647b90",
    4,
    "9d99e77f"
  ],
  [
    "0x1414c1582",
    "0x140647b94",
    1,
    "4a"
  ],
  [
    "0x1414c15ce",
    "0x140647b95",
    4,
    "3ec1f080"
  ],
  [
    "0x1414cb3ba",
    "0x140647b99",
    1,
    "6a"
  ],
  [
    "0x1414cb406",
    "0x140647b9a",
    4,
    "1771f200"
  ],
  [
    "0x14154d9d2",
    "0x140647b9e",
    1,
    "68"
  ],
  [
    "0x14154da30",
    "0x140647b9f",
    4,
    "79bbfa80"
  ],
  [
    "0x141607161",
    "0x140647ba3",
    1,
    "94"
  ],
  [
    "0x1416071b2",
    "0x140647ba4",
    4,
    "10f208c0"
  ],
  [
    "0x1414d5f62",
    "0x140647ba8",
    1,
    "02"
  ],
  [
    "0x1414d5f99",
    "0x140647ba9",
    4,
    "f75be07f"
  ],
  [
    "0x1414b5f19",
    "0x140647bad",
    1,
    "b1"
  ],
  [
    "0x1414b5f7c",
    "0x140647bae",
    4,
    "ec231dc0"
  ],
  [
    "0x1414b4027",
    "0x140647bb2",
    1,
    "4b"
  ],
  [
    "0x1414b4082",
    "0x140647bb3",
    4,
    "292a1f7f"
  ],
  [
    "0x141538314",
    "0x140647bb7",
    1,
    "d3"
  ],
  [
    "0x141538360",
    "0x140647bb8",
    4,
    "a63916ff"
  ],
  [
    "0x1416089c8",
    "0x140647bbc",
    1,
    "d9"
  ],
  [
    "0x141608a1d",
    "0x140647bbd",
    4,
    "5231e53f"
  ],
  [
    "0x14155c78c",
    "0x140647bc1",
    1,
    "83"
  ],
  [
    "0x14155c7de",
    "0x140647bc2",
    4,
    "ba3aef80"
  ],
  [
    "0x1415fae99",
    "0x140647bc6",
    1,
    "07"
  ],
  [
    "0x1415faed5",
    "0x140647bc7",
    4,
    "67bd1f80"
  ],
  [
    "0x1414c1582",
    "0x140647bcb",
    1,
    "40"
  ],
  [
    "0x1414c15ce",
    "0x140647bcc",
    4,
    "aef30a7f"
  ],
  [
    "0x14154da49",
    "0x140647bd0",
    8,
    "8589f74cf1d6fdf9"
  ],
  [
    "0x14154da9e",
    "0x140647bd8",
    4,
    "bee0d297"
  ],
  [
    "0x141510d10",
    "0x140647bdc",
    1,
    "70"
  ],
  [
    "0x141510d81",
    "0x140647bdd",
    4,
    "50b33d74"
  ],
  [
    "0x14156e989",
    "0x140647be1",
    4,
    "b886fd85"
  ],
  [
    "0x1414cb3ba",
    "0x140647be5",
    1,
    "a7"
  ],
  [
    "0x1414cb406",
    "0x140647be6",
    4,
    "da096ebf"
  ],
  [
    "0x14154d9d2",
    "0x140647bea",
    1,
    "35"
  ],
  [
    "0x14154da30",
    "0x140647beb",
    4,
    "f396993f"
  ],
  [
    "0x1414b9a32",
    "0x140647bef",
    1,
    "6c"
  ],
  [
    "0x1414b9a94",
    "0x140647bf0",
    4,
    "4d633474"
  ],
  [
    "0x1414e96c6",
    "0x140647bf4",
    1,
    "b0"
  ],
  [
    "0x1414e9730",
    "0x140647bf5",
    4,
    "0d7d3274"
  ],
  [
    "0x14154b516",
    "0x140647bf9",
    1,
    "70"
  ],
  [
    "0x14154b58a",
    "0x140647bfa",
    4,
    "5422cd8b"
  ],
  [
    "0x1415414df",
    "0x140647bfe",
    1,
    "01"
  ],
  [
    "0x14154153e",
    "0x140647bff",
    4,
    "f96c3574"
  ],
  [
    "0x1414c631c",
    "0x140647c03",
    1,
    "f4"
  ],
  [
    "0x141508fef",
    "0x140647c04",
    4,
    "3ebf3474"
  ],
  [
    "0x1414e36bf",
    "0x140647c08",
    1,
    "ff"
  ],
  [
    "0x1414e372c",
    "0x140647c09",
    4,
    "82afca8b"
  ],
  [
    "0x1414c474f",
    "0x140647c0d",
    1,
    "0f"
  ],
  [
    "0x1414c47a3",
    "0x140647c0e",
    4,
    "0d8dcb8b"
  ],
  [
    "0x1414d69da",
    "0x140647c12",
    1,
    "04"
  ],
  [
    "0x1414d6a30",
    "0x140647c13",
    4,
    "f8ecc98b"
  ],
  [
    "0x1414fcb4b",
    "0x140647c17",
    1,
    "ed"
  ],
  [
    "0x1414fcba1",
    "0x140647c18",
    4,
    "6bbccc8b"
  ],
  [
    "0x141551c1a",
    "0x140647c1c",
    1,
    "92"
  ],
  [
    "0x141524f33",
    "0x140647c1d",
    4,
    "8d4c3774"
  ],
  [
    "0x141510d10",
    "0x140647c21",
    1,
    "5c"
  ],
  [
    "0x141510d81",
    "0x140647c22",
    4,
    "b7c1cd8b"
  ],
  [
    "0x1414b9a32",
    "0x140647c26",
    1,
    "ae"
  ],
  [
    "0x1414b9a94",
    "0x140647c27",
    4,
    "6f3dcf8b"
  ],
  [
    "0x1414e96c6",
    "0x140647c2b",
    1,
    "0a"
  ],
  [
    "0x1414e9730",
    "0x140647c2c",
    4,
    "b723c98b"
  ],
  [
    "0x14154b516",
    "0x140647c30",
    1,
    "5a"
  ],
  [
    "0x14154b58a",
    "0x140647c31",
    4,
    "5e7c3674"
  ],
  [
    "0x1415414df",
    "0x140647c35",
    1,
    "bb"
  ],
  [
    "0x14154153e",
    "0x140647c36",
    4,
    "6332ce8b"
  ],
  [
    "0x1414c631c",
    "0x140647c3a",
    1,
    "2e"
  ],
  [
    "0x141508fef",
    "0x140647c3b",
    4,
    "64e1cf8b"
  ],
  [
    "0x1414e36bf",
    "0x140647c3f",
    1,
    "55"
  ],
  [
    "0x1414e372c",
    "0x140647c40",
    4,
    "48f13174"
  ],
  [
    "0x1414c474f",
    "0x140647c44",
    1,
    "95"
  ],
  [
    "0x1414c47a3",
    "0x140647c45",
    4,
    "f7d33074"
  ],
  [
    "0x1414d69da",
    "0x140647c49",
    1,
    "de"
  ],
  [
    "0x1414d6a30",
    "0x140647c4a",
    4,
    "e2b23274"
  ],
  [
    "0x1414fcb4b",
    "0x140647c4e",
    1,
    "8f"
  ],
  [
    "0x1414fcba1",
    "0x140647c4f",
    4,
    "59ccc98b"
  ],
  [
    "0x14158b7eb",
    "0x140602291",
    4,
    "8c7e2a5c"
  ],
  [
    "0x1415f44ba",
    "0x140602295",
    1,
    "8b"
  ],
  [
    "0x1415f4543",
    "0x140602296",
    4,
    "21134065"
  ],
  [
    "0x1415bd60e",
    "0x14060229a",
    1,
    "01"
  ],
  [
    "0x1415bd6a2",
    "0x14060229b",
    4,
    "91b9417d"
  ],
  [
    "0x1415cbe05",
    "0x14060229f",
    1,
    "8b"
  ],
  [
    "0x1415cbe99",
    "0x1406022a0",
    4,
    "6c7aba82"
  ],
  [
    "0x1415c2796",
    "0x1406022a4",
    1,
    "8d"
  ],
  [
    "0x141555929",
    "0x1406022a5",
    4,
    "1a0c416d"
  ],
  [
    "0x14159be9d",
    "0x1406022a9",
    1,
    "3f"
  ],
  [
    "0x14159bf3d",
    "0x1406022aa",
    4,
    "1afa4275"
  ],
  [
    "0x1415b6163",
    "0x1406022ae",
    1,
    "09"
  ],
  [
    "0x14158a26f",
    "0x1406022af",
    4,
    "de88be02"
  ],
  [
    "0x1414b10d0",
    "0x1406022b3",
    1,
    "45"
  ],
  [
    "0x1414b1179",
    "0x1406022b4",
    4,
    "08f4aee2"
  ],
  [
    "0x14157de57",
    "0x1406022b8",
    1,
    "1b"
  ],
  [
    "0x14158113d",
    "0x1406022b9",
    4,
    "64c05b65"
  ],
  [
    "0x14154d90a",
    "0x1406022bd",
    1,
    "fd"
  ],
  [
    "0x1415d24b4",
    "0x1406022be",
    4,
    "cd1e5855"
  ],
  [
    "0x1415a4c74",
    "0x1406022c2",
    1,
    "ba"
  ],
  [
    "0x1414e97d2",
    "0x1406022c3",
    4,
    "0099a292"
  ],
  [
    "0x141583e23",
    "0x1406022c7",
    1,
    "3f"
  ],
  [
    "0x14157d33d",
    "0x1406022c8",
    4,
    "2707a7ba"
  ],
  [
    "0x1415f44ba",
    "0x1406022cc",
    1,
    "31"
  ],
  [
    "0x1415f4543",
    "0x1406022cd",
    4,
    "9b255f65"
  ],
  [
    "0x1415bd60e",
    "0x1406022d1",
    1,
    "5b"
  ],
  [
    "0x1415bd6a2",
    "0x1406022d2",
    4,
    "4b8f5e7d"
  ],
  [
    "0x1415cbe05",
    "0x1406022d6",
    1,
    "a9"
  ],
  [
    "0x1415cbe99",
    "0x1406022d7",
    4,
    "ce4ca582"
  ],
  [
    "0x1415c2796",
    "0x1406022db",
    1,
    "8a"
  ],
  [
    "0x141555929",
    "0x1406022dc",
    4,
    "203a5e6d"
  ],
  [
    "0x14159be9d",
    "0x1406022e0",
    1,
    "80"
  ],
  [
    "0x14159bf3d",
    "0x1406022e1",
    4,
    "b8cc5d75"
  ],
  [
    "0x1415b6163",
    "0x1406022e5",
    1,
    "53"
  ],
  [
    "0x14158a26f",
    "0x1406022e6",
    4,
    "04bea102"
  ],
  [
    "0x1414b10d0",
    "0x1406022ea",
    1,
    "2a"
  ],
  [
    "0x1414b1179",
    "0x1406022eb",
    4,
    "6ac2b1e2"
  ],
  [
    "0x14157de57",
    "0x1406022ef",
    1,
    "3c"
  ],
  [
    "0x14158113d",
    "0x1406022f0",
    4,
    "39d7bd82"
  ],
  [
    "0x14158a2dc",
    "0x1406022f4",
    8,
    "e794afe9da050000"
  ],
  [
    "0x14158a341",
    "0x1406022fc",
    4,
    "e704e9ad"
  ],
  [
    "0x1415d095e",
    "0x140602300",
    1,
    "72"
  ],
  [
    "0x1415d09d1",
    "0x140602301",
    4,
    "3c7267b9"
  ],
  [
    "0x1414c54e5",
    "0x140602305",
    4,
    "522b3bb4"
  ],
  [
    "0x14154d90a",
    "0x140602309",
    1,
    "f9"
  ],
  [
    "0x1415d24b4",
    "0x14060230a",
    4,
    "49bfb8aa"
  ],
  [
    "0x1415a4c74",
    "0x14060230e",
    1,
    "fe"
  ],
  [
    "0x1414e97d2",
    "0x14060230f",
    4,
    "c438426d"
  ],
  [
    "0x141583e23",
    "0x140602313",
    1,
    "eb"
  ],
  [
    "0x14157d33d",
    "0x140602314",
    4,
    "5c32be8a"
  ],
  [
    "0x14156d1ad",
    "0x140602318",
    4,
    "a992740f"
  ],
  [
    "0x1415f44ba",
    "0x14060231c",
    1,
    "25"
  ],
  [
    "0x1415f4543",
    "0x14060231d",
    4,
    "0f624e65"
  ],
  [
    "0x1415bd60e",
    "0x140602321",
    1,
    "17"
  ],
  [
    "0x1415bd6a2",
    "0x140602322",
    4,
    "889db502"
  ],
  [
    "0x1414b1cbe",
    "0x140602326",
    4,
    "db76ed1a"
  ],
  [
    "0x1415cbe05",
    "0x14060232a",
    1,
    "30"
  ],
  [
    "0x1415cbe99",
    "0x14060232b",
    4,
    "da0b4a7d"
  ],
  [
    "0x1415c2796",
    "0x14060232f",
    1,
    "a6"
  ],
  [
    "0x141555929",
    "0x140602330",
    4,
    "8448b292"
  ],
  [
    "0x1415947f2",
    "0x140602334",
    4,
    "32deba0f"
  ],
  [
    "0x14159be9d",
    "0x140602338",
    1,
    "21"
  ],
  [
    "0x14159bf3d",
    "0x140602339",
    4,
    "944ab28a"
  ],
  [
    "0x1415b6163",
    "0x14060233d",
    1,
    "af"
  ],
  [
    "0x14158a26f",
    "0x14060233e",
    4,
    "f0354c75"
  ],
  [
    "0x1415d2f41",
    "0x140602342",
    4,
    "3b945929"
  ],
  [
    "0x1414b10d0",
    "0x140602346",
    1,
    "6f"
  ],
  [
    "0x1414b1179",
    "0x140602347",
    4,
    "a264bee2"
  ],
  [
    "0x14157de57",
    "0x14060234b",
    1,
    "99"
  ],
  [
    "0x14158113d",
    "0x14060234c",
    4,
    "59f3b5aa"
  ],
  [
    "0x1415d6bac",
    "0x140602350",
    1,
    "58"
  ],
  [
    "0x1415d6c3a",
    "0x140602351",
    4,
    "f5fb6e62"
  ],
  [
    "0x1415c48f8",
    "0x140602355",
    8,
    "0ba69b13da050000"
  ],
  [
    "0x1415853db",
    "0x14060235d",
    4,
    "e8fefd35"
  ],
  [
    "0x14158d025",
    "0x140602361",
    4,
    "0a2c5e6d"
  ],
  [
    "0x14154d90a",
    "0x140602365",
    1,
    "b1"
  ],
  [
    "0x1415d24b4",
    "0x140602366",
    4,
    "9901b69a"
  ],
  [
    "0x1415899ae",
    "0x14060236a",
    4,
    "2da03f58"
  ],
  [
    "0x141583166",
    "0x14060236e",
    4,
    "57966d10"
  ],
  [
    "0x14154b14f",
    "0x140602372",
    4,
    "9e7ed2aa"
  ],
  [
    "0x1415a4c74",
    "0x140602376",
    1,
    "15"
  ],
  [
    "0x1414e97d2",
    "0x140602377",
    4,
    "ba404f75"
  ],
  [
    "0x14158dc82",
    "0x14060237b",
    4,
    "932bffd1"
  ],
  [
    "0x14158e9a3",
    "0x14060237f",
    4,
    "dcdbf864"
  ],
  [
    "0x141583e23",
    "0x140602383",
    1,
    "5e"
  ],
  [
    "0x14157d33d",
    "0x140602384",
    4,
    "53bf4975"
  ],
  [
    "0x14159b30e",
    "0x140602388",
    8,
    "6c67c3a56d4a0000"
  ],
  [
    "0x14159b365",
    "0x140602390",
    4,
    "5f3a2613"
  ],
  [
    "0x1415b6a92",
    "0x140602394",
    1,
    "ce"
  ],
  [
    "0x1415b6b00",
    "0x140602395",
    4,
    "1ed2b412"
  ],
  [
    "0x141577e6c",
    "0x140602399",
    4,
    "9360abcc"
  ],
  [
    "0x1415f44ba",
    "0x14060239d",
    1,
    "93"
  ],
  [
    "0x1415f4543",
    "0x14060239e",
    4,
    "c9ba6a24"
  ],
  [
    "0x1415bd60e",
    "0x1406023a2",
    1,
    "bc"
  ],
  [
    "0x1415bd6a2",
    "0x1406023a3",
    4,
    "8eba94db"
  ],
  [
    "0x141587619",
    "0x1406023a7",
    1,
    "7f"
  ],
  [
    "0x141587691",
    "0x1406023a8",
    4,
    "90c9b42b"
  ],
  [
    "0x141604ba7",
    "0x1406023ac",
    1,
    "d1"
  ],
  [
    "0x141604c18",
    "0x1406023ad",
    4,
    "d1e34ce2"
  ],
  [
    "0x141586886",
    "0x1406023b1",
    1,
    "76"
  ],
  [
    "0x1415868fb",
    "0x1406023b2",
    4,
    "cc004a0c"
  ],
  [
    "0x1415e75df",
    "0x1406023b6",
    1,
    "37"
  ],
  [
    "0x1415e7652",
    "0x1406023b7",
    4,
    "a0f2b76d"
  ],
  [
    "0x1415be2d5",
    "0x1406023bb",
    1,
    "69"
  ],
  [
    "0x1415be344",
    "0x1406023bc",
    4,
    "4a9e45a2"
  ],
  [
    "0x1414e3f97",
    "0x1406023c0",
    1,
    "13"
  ],
  [
    "0x1414e3fef",
    "0x1406023c1",
    4,
    "483d4b03"
  ],
  [
    "0x1415c4251",
    "0x1406023c5",
    1,
    "c1"
  ],
  [
    "0x1415c42b7",
    "0x1406023c6",
    4,
    "81c0bab7"
  ],
  [
    "0x1414df8f0",
    "0x1406023ca",
    1,
    "66"
  ],
  [
    "0x1414df95d",
    "0x1406023cb",
    4,
    "e989b5ee"
  ],
  [
    "0x1415d095e",
    "0x1406023cf",
    1,
    "d0"
  ],
  [
    "0x1415d09d1",
    "0x1406023d0",
    4,
    "ff99b59c"
  ],
  [
    "0x1415d6bac",
    "0x1406023d4",
    1,
    "7e"
  ],
  [
    "0x1415d6c3a",
    "0x1406023d5",
    4,
    "79044800"
  ],
  [
    "0x1415b6a92",
    "0x1406023d9",
    1,
    "e8"
  ],
  [
    "0x1415b6b00",
    "0x1406023da",
    4,
    "80fab50a"
  ],
  [
    "0x141587619",
    "0x1406023de",
    1,
    "f7"
  ],
  [
    "0x141587691",
    "0x1406023df",
    4,
    "180eb22b"
  ],
  [
    "0x141604ba7",
    "0x1406023e3",
    1,
    "59"
  ],
  [
    "0x141604c18",
    "0x1406023e4",
    4,
    "59244ae2"
  ],
  [
    "0x141586886",
    "0x1406023e8",
    1,
    "a6"
  ],
  [
    "0x1415868fb",
    "0x1406023e9",
    4,
    "1cc74c0c"
  ],
  [
    "0x1415e75df",
    "0x1406023ed",
    1,
    "ef"
  ],
  [
    "0x1415e7652",
    "0x1406023ee",
    4,
    "7835b16d"
  ],
  [
    "0x1415be2d5",
    "0x1406023f2",
    1,
    "51"
  ],
  [
    "0x1415be344",
    "0x1406023f3",
    4,
    "f25943a2"
  ],
  [
    "0x1414e3f97",
    "0x1406023f7",
    1,
    "9b"
  ],
  [
    "0x1414e3fef",
    "0x1406023f8",
    4,
    "40fa4d03"
  ],
  [
    "0x1415c4251",
    "0x1406023fc",
    1,
    "61"
  ],
  [
    "0x1415c42b7",
    "0x1406023fd",
    4,
    "a107bcb7"
  ],
  [
    "0x1414df8f0",
    "0x140602401",
    1,
    "76"
  ],
  [
    "0x1414df95d",
    "
[Recorded excerpt: file exceeds 48,000 characters.]
````````````


File: `reverse/CyberCup-2077/cc2_probe_0x1406987c0_traps.json`

````````````text
{}
````````````


File: `reverse/CyberCup-2077/cc2_progress.md`

````````````text
# CyberCup resumed — 2026-10-31

Solving resumed by explicit user instruction. Prior progress-summary.md records the earlier pause.
Git remote contributions checked every 120 seconds; own checkpoints published every 300 seconds.

Current objective: recover hidden expected ciphertext backing values by fixing readiness or locating registration initialization.

## First resumed checks

Reproduced readiness failure with 45,185-instruction traces. Clearing versus setting CPUID leaf-1 hypervisor bit gives exactly the same instruction path. The dead marker is pushed by a virtual immediate handler at 0x1415b4c46; tracing bytecode/global setup next. Full native transform extraction reached stage 56; symbolic export still being generated. System Python 3.9 Unicorn crashes (SIGBUS); use ../../.venv/bin/python (3.14) for emulation.

## Readiness breakthrough

The emulator omitted the saved PEB OS-build fields, causing a fail path. Additionally check_clean.bin has zero at the initialized runtime pointer 0x14134d552, while unpack_initialized.bin has 0x30010000. Restoring the saved PEB plus that pointer reaches VirtualQuery. Modeling VirtualQuery for the unmapped sentinel range as MEM_FREE now registers real 0x3302 hidden-read traps. First backing address is 0x140f43d60. See cc2_init.py/log; registration run is in progress.

All 11 hidden read registrations recovered in cc2_init_0x1406987c0_traps.json. First backing QWORD is 0xf81277ed00eaa1dd, first expected ciphertext after comparison mask is 0x9b98bc82c49415c3. Existing 63-character concrete probe matches eighth character d, establishing prefix ctfcup{d. Running full symbolic checker including real trap reads and comparisons.

````````````


File: `reverse/CyberCup-2077/cc2_reads.py`

````````````text
"""Run the isolated input transformation, omitting UI and timing checks."""
from pathlib import Path
import argparse,struct,time,pickle,gzip
import unicorn
from unicorn.x86_const import *
from driver_analysis_hv import Hypervisor
P=argparse.ArgumentParser();P.add_argument('image');P.add_argument('flag',nargs='?',default='ctfcup{'+'A'*59+'}');P.add_argument('--trace',action='store_true');P.add_argument('--init',action='store_true');P.add_argument('--entry',type=lambda x:int(x,0),default=0x1406987c0);a=P.parse_args()
b=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);base=0x140000000
u.mem_map(base,(len(b)+4095)&~4095);u.mem_write(base,b)
u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x10000000);u.mem_map(0x7ff00000,0x100000)
def put(p,x):u.mem_write(p,struct.pack('<Q',x))
u.reg_write(UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff00030,0x7ff00000);put(0x7ff00008,0x11000000);put(0x7ff00010,0x10000000);put(0x7ff01010,base);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
sp=0x10fe0000;u.reg_write(UC_X86_REG_RSP,sp);u.reg_write(UC_X86_REG_RBP,sp+0x100);u.reg_write(UC_X86_REG_RDI,0x20000000);u.mem_write(0x20000000,a.flag.encode());u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RSI,0)
snap=pickle.load(gzip.open('unpack_initialized_state.pkl.gz'))
for addr,blob in snap['mem']:
 if addr==0x30000000:u.mem_write(addr,blob)
apis=snap['apis'] if a.init else {}
u.mem_map(0x70000000,0x100000);u.mem_write(0x70000000,b'\xc3'*0x100000)
hv=Hypervisor(pid=1234,trace=lambda *x:print('HV',x) if x[0]=='trap' else None);last=[]
tsc=100000000
def hook(u,pc,size,data):
 global tsc
 raw=bytes(u.mem_read(pc,min(size,3)))
 if raw[:2]==b'\x0f\x31' or raw[:3]==b'\x0f\x01\xf9':
  tsc+=100;u.reg_write(UC_X86_REG_EAX,tsc);u.reg_write(UC_X86_REG_EDX,0);u.reg_write(UC_X86_REG_RIP,pc+size);print('RDTSC',hex(pc),tsc);return
 if pc in apis:
  name=apis[pc];print('API',name,'RCX',hex(u.reg_read(UC_X86_REG_RCX)),'RDX',hex(u.reg_read(UC_X86_REG_RDX)))
  if name=='GetCurrentProcess':v=0xffffffffffffffff
  elif name in ['GetCurrentProcessId','GetCurrentThreadId']:v=1234
  elif name=='IsDebuggerPresent':v=0
  elif name=='CheckRemoteDebuggerPresent':u.mem_write(u.reg_read(UC_X86_REG_RDX),b'\0'*4);v=1
  elif name=='NtQueryInformationProcess':
   cl=u.reg_read(UC_X86_REG_EDX);buf=u.reg_read(UC_X86_REG_R8);sz=u.reg_read(UC_X86_REG_R9);print('QUERY',cl,hex(buf),sz);u.mem_write(buf,(1 if cl==31 else 0).to_bytes(sz,'little'));v=0
  elif name=='VirtualProtect':
   put(u.reg_read(UC_X86_REG_R9),0x40);v=1
  elif name=='GetSystemTimeAsFileTime':put(u.reg_read(UC_X86_REG_RCX),13245678900123456);v=1
  elif name=='QueryPerformanceCounter':put(u.reg_read(UC_X86_REG_RCX),123456789);v=1
  elif name=='GetTickCount':v=123456
  else:raise RuntimeError(('API',name))
  rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RAX,v);u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret);return
 if pc==0x141541b37:print('FINALRET',hex(u.reg_read(UC_X86_REG_RSP)),bytes(u.mem_read(u.reg_read(UC_X86_REG_RSP),64)).hex())
 if hv.handle(u,pc,size):return
 if pc==0x140698edb:
  print('RESULT',hex(u.reg_read(UC_X86_REG_EAX)));u.emu_stop();return
 if pc==0x140699420: # MSVC security-cookie verification outside the transform.
  rsp=u.reg_read(UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ra);return
 if len(last)>20:last.pop(0)
 last.append(pc)
 if a.trace and 0x140698a19<=pc<0x140698edb:print('MAIN',hex(pc))
u.hook_add(unicorn.UC_HOOK_CODE,hook)
def intr(u,n,data):
 if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(UC_X86_REG_RIP))))
u.hook_add(unicorn.UC_HOOK_INTR,intr)
def invalid(u,access,p,n,v,data):
 print('UNMAPPED',access,hex(p),n,hex(u.reg_read(UC_X86_REG_RIP)))
 for n in ['RAX','RCX','RDX','RBX','RSI','RDI','RBP','RSP','R8','R9','R10','R11','R12','R13','R14','R15']:print(n,hex(u.reg_read(globals()['UC_X86_REG_'+n])))
 return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
def cpuid(u,d):
 leaf=u.reg_read(UC_X86_REG_EAX);sub=u.reg_read(UC_X86_REG_ECX);vals=[0,0,0,0]
 if leaf==0x4ffffffd:
  x=sub^0x9c3017a5;x^=x>>16;x=x*0x7feb352d&0xffffffff;x^=x>>15;x=x*0x846ca68b&0xffffffff;x^=x>>16
  vals=[leaf,x^0x43453032^0x73d45bc1,0x41434631,0]
 elif leaf==0x4fffffff:
  vals=[leaf,0x706d6953,0x7653656c,0x2020206d]
  if sub==1:vals=[leaf,0,0,0x20000]
  elif sub==2:vals=[leaf,0,0,0]
  elif sub==3:vals=[leaf,1,1,0]
  elif sub==4:vals=[leaf,0x43453032,0x4241434b,0x414c4953]
 elif leaf==0:vals=[13,0x756e6547,0x6c65746e,0x49656e69]
 elif leaf==1:vals=[0x306a9,0x00010800,0xfffafbff,0xbfebfbff]
 elif leaf==0x80000000:vals=[0x80000008,0,0,0]
 elif leaf==0x80000001:vals=[0,0,0x121,0x2c100800]
 elif leaf==0x80000008:vals=[0x3028,0,0,0]
 elif leaf in [0x80000002,0x80000003,0x80000004]:vals=list(struct.unpack('<4I',b'Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz          '.ljust(48,b' ')[(leaf-0x80000002)*16:(leaf-0x80000001)*16]))
 print('CPUID',hex(leaf),hex(sub),flush=True)
 for reg,val in zip([UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX],vals):u.reg_write(reg,val)
 return True
u.hook_add(unicorn.UC_HOOK_INSN,cpuid,None,1,0,UC_X86_INS_CPUID)
reads=[]
def read(u,access,addr,size,value,data):
 if (base<=addr<base+0x124b000) or 0x30000000<=addr<0x40000000 or 0x7ff00000<=addr<0x80000000:
  reads.append([hex(u.reg_read(UC_X86_REG_RIP)),hex(addr),size,bytes(u.mem_read(addr,size)).hex()])
u.hook_add(unicorn.UC_HOOK_MEM_READ,read)
t=time.time()
try:
 if a.init:
  put(sp-8,0x140698a19);u.reg_write(UC_X86_REG_RSP,sp-8)
 u.emu_start(a.entry if a.init else 0x140698a19,0,count=10000000)
except Exception as e:print('ERROR',e)
print('TIME',time.time()-t,'RIP',hex(u.reg_read(UC_X86_REG_RIP)),'STATE',bytes(u.mem_read(sp+0x50,80)).hex());print('LAST',list(map(hex,last)))

import json
Path('cc2_probe_'+hex(a.entry)+'_traps.json').write_text(json.dumps(hv.traps))
print('TRAPS',hv.traps)

import json
Path('cc2_datareads.json').write_text(json.dumps(reads,indent=2))

````````````


File: `reverse/CyberCup-2077/cc2_solve_first.py`

````````````text
from pathlib import Path
import z3 as z,time
cs=z.parse_smt2_file('cc2_block0.smt2')
s=z.Then('simplify','propagate-values','solve-eqs','bit-blast','sat').solver();s.set(timeout=60000);s.add(cs)
s.add(z.BitVec('state_00',32)==0xc49415c3,z.BitVec('state_04',32)==0x9b98bc82)
for i in range(2):
 w=z.BitVec('input_word_%02d'%i,32)
 for j in range(4):
  x=z.Extract(j*8+7,j*8,w);s.add(z.UGE(x,32),z.ULE(x,126))
t=time.time();r=s.check();print(r,time.time()-t,flush=True)
if r==z.sat:
 m=s.model();print(b''.join(m.eval(z.BitVec('input_word_%02d'%i,32)).as_long().to_bytes(4,'little') for i in range(2)),flush=True)

````````````


File: `reverse/CyberCup-2077/cc2_symbolic.py`

````````````text
"""Symbolic shadow of native checker; table arithmetic is replaced by Z3 operations."""
from pathlib import Path
import argparse,struct,time,json,sys
import unicorn,unicorn.x86_const as ux
from capstone import *
from capstone.x86 import *
import z3 as z
from driver_analysis_hv import Hypervisor
B=0x140000000
mask=lambda n:(1<<n)-1

def norm(v,n):
 if isinstance(v,int):return v&mask(n)
 if v.size()>n:v=z.Extract(n-1,0,v)
 elif v.size()<n:v=z.ZeroExt(n-v.size(),v)
 v=z.simplify(v,mul2concat=True,bv_extract_prop=True,bv_sort_ac=True,sort_sums=True,local_ctx=True)
 return v.as_long() if z.is_bv_value(v) else v

def bv(v,n):return z.BitVecVal(v&mask(n),n) if isinstance(v,int) else norm(v,n)
def join(vals):
 if len(vals)==1:return vals[0]
 if all(isinstance(x,int) for x in vals):return sum(x<<(8*i) for i,x in enumerate(vals))
 return norm(z.Concat(*[bv(x,8) for x in vals[::-1]]),len(vals)*8)

class Shadow:
 def __init__(self,u):
  self.u=u;self.reg={};self.mem={};self.cache={};self.flags=False;self.flagstack={};self.n=0;self.unknown=0;self.tables=[];self.defs=[];self.bindings=[]
  self.md=Cs(CS_ARCH_X86,CS_MODE_64);self.md.detail=True
  for d in json.loads(Path('lut_catalog.json').read_text()):self.tables.append((int(d['rows'],16),int(d['data'],16),d['operation'][0]))
 def desc(self,r):
  s=self.md.reg_name(r)
  if s in ('rip','eip'):return 'rip',64 if s=='rip' else 32,0
  if s.startswith('r') and s[1:].rstrip('dwb').isdigit():
   e=s[-1];return s.rstrip('dwb'),{'d':32,'w':16,'b':8}.get(e,64),0
  names={'rax':['rax','eax','ax','al','ah'],'rbx':['rbx','ebx','bx','bl','bh'],'rcx':['rcx','ecx','cx','cl','ch'],'rdx':['rdx','edx','dx','dl','dh'],'rsp':['rsp','esp','sp','spl'],'rbp':['rbp','ebp','bp','bpl'],'rsi':['rsi','esi','si','sil'],'rdi':['rdi','edi','di','dil']}
  for q,xs in names.items():
   if s in xs:
    i=xs.index(s);return q,[64,32,16,8,8][i],8 if i==4 else 0
  return s,64,0
 def concrete_reg(self,r):return self.u.reg_read(getattr(ux,'UC_X86_REG_'+self.md.reg_name(r).upper()))
 def getreg(self,r):
  k,n,off=self.desc(r);v=self.reg.get(k)
  if v is None:return self.concrete_reg(r)
  return norm(z.LShR(v,off) if off else v,n)
 def setreg(self,r,v):
  k,n,off=self.desc(r);v=norm(v,n)
  if n>=32:new=norm(v,64)
  else:
   old=self.reg.get(k)
   if old is None:old=self.u.reg_read(getattr(ux,'UC_X86_REG_'+k.upper()))
   if isinstance(old,int) and isinstance(v,int):new=(old&~(mask(n)<<off))|(v<<off)
   else:new=norm((bv(old,64)&bv(~(mask(n)<<off),64))|(bv(v,64)<<off),64)
  if isinstance(new,int):self.reg.pop(k,None)
  else:self.reg[k]=new
 def addr(self,o,i):
  m=o.mem;c=m.disp;v=m.disp
  for reg,scale in [(m.base,1),(m.index,m.scale)]:
   if reg:
    cv=i.address+i.size if reg==X86_REG_RIP else self.concrete_reg(reg)
    sv=cv if reg==X86_REG_RIP else self.getreg(reg)
    c+=cv*scale;v=v+sv*scale
  return c&mask(64),norm(v,64)
 def fresh(self,v,n,c,size):
  v=norm(v,n)
  if isinstance(v,int):return v
  x=z.BitVec("lut_%05d"%len(self.defs),n);self.defs.append(x==v);self.bindings.append((x,z.BitVecVal(int.from_bytes(self.u.mem_read(c,size),"little"),n)));return x
 def readmem(self,c,a,size):
  if not isinstance(a,int):
   for rows,data,op in self.tables:
    if rows<=c<rows+2048:
     assert size==8
     return norm(bv(data,64)+(z.LShR(bv(a,64)-rows,3)<<8),64)
    if data<=c<data+65536:
     assert size==1
     off=bv(a,64)-data;x=z.Extract(15,8,off);y=z.Extract(7,0,off)
     if op=='xor':v=x^y
     elif op=='and':v=x&y
     elif op=='or':v=x|y
     elif op.startswith('funnel_left_'):
      n=int(op.rsplit('_',1)[1]);v=(x<<n)|z.LShR(y,8-n)
     return self.fresh(v,8,c,size)
   rows=0x140fd8600;data=0x1410d8600
   if rows<=c<data:
    assert size==8
    return norm(bv(data,64)+(z.LShR(bv(a,64)-rows,3)<<2),64)
   if data<=c<0x141158600:
    assert size==4
    return self.fresh(z.LShR(bv(a,64)-data,2),32,c,size)
   if 0x141158610<=c<0x141158710:
    return self.fresh(z.If(bv(a,64)==0x141158610,z.BitVecVal(1,8),z.BitVecVal(0,8)),8,c,size)
   raise ValueError(('SYMBOLIC ADDRESS',hex(c),a,size))
  data=bytes(self.u.mem_read(c,size));vals=[self.mem.get(c+j,data[j]) for j in range(size)]
  return join(vals)
 def get(self,o,i):
  if o.type==X86_OP_IMM:return o.imm&mask(o.size*8)
  if o.type==X86_OP_REG:return self.getreg(o.reg)
  if o.type==X86_OP_MEM:
   c,a=self.addr(o,i);return self.readmem(c,a,o.size)
  raise ValueError(o.type)
 def put(self,o,v,i):
  if o.type==X86_OP_REG:self.setreg(o.reg,v);return
  c,a=self.addr(o,i)
  if not isinstance(a,int):raise ValueError(('SYMBOLIC WRITE',hex(c),a))
  v=norm(v,o.size*8)
  for j in range(o.size):
   if isinstance(v,int):self.mem.pop(c+j,None)
   else:
    x=norm(z.Extract(j*8+7,j*8,v),8)
    if isinstance(x,int):self.mem.pop(c+j,None)
    else:self.mem[c+j]=x
 def unk(self,n):
  self.unknown+=1;return z.BitVec(f'UNKNOWN_{self.unknown}',n)
 def step(self,pc,size):
  i=self.cache.get(pc)
  if i is None:
   i=next(self.md.disasm(bytes(self.u.mem_read(pc,size)),pc));self.cache[pc]=i
  m=i.mnemonic;o=i.operands;self.n+=1
  if m in ('nop','jmp','ret','call','int3','vmmcall','cpuid'):return
  if m=='pushfq':self.flagstack[self.u.reg_read(ux.UC_X86_REG_RSP)-8]=self.flags;return
  if m=='popfq':self.flags=self.flagstack.get(self.u.reg_read(ux.UC_X86_REG_RSP),False);return
  if m=='push':
   v=self.get(o[0],i);addr=self.u.reg_read(ux.UC_X86_REG_RSP)-8
   for j in range(8):
    if isinstance(v,int):self.mem.pop(addr+j,None)
    else:self.mem[addr+j]=norm(z.Extract(j*8+7,j*8,bv(v,64)),8)
   return
  if m=='pop':
   addr=self.u.reg_read(ux.UC_X86_REG_RSP);self.put(o[0],self.readmem(addr,addr,8),i);return
  if m in ('clc','stc','cmc'):self.flags=False;return
  if m in ('mov','movabs','movzx','movsx','movsxd'):
   v=self.get(o[1],i)
   if m in ('movsx','movsxd'):
    n=o[1].size*8;t=o[0].size*8
    if isinstance(v,int):v=v-(1<<n) if v>>(n-1) else v
    else:v=z.SignExt(t-n,v)
   self.put(o[0],v,i);return
  if m=='lea':self.put(o[0],self.addr(o[1],i)[1],i);return
  if m=='xchg':
   a=self.get(o[0],i);b=self.get(o[1],i);self.put(o[0],b,i);self.put(o[1],a,i);return
  if m in ('xor','and','or','add','sub','neg','not','inc','dec','shl','sal','shr','sar','rol','ror','cmp','test'):
   a=self.get(o[0],i);n=o[0].size*8;b=self.get(o[1],i) if len(o)>1 else None
   sym=not isinstance(a,int) or (b is not None and not isinstance(b,int))
   if m in ('cmp','test'):self.flags=sym;return
   if sym:
    a=bv(a,n)
    if b is not None:b=bv(b,n)
   if m=='xor':v=a^b
   elif m=='and':v=a&b
   elif m=='or':v=a|b
   elif m=='add':v=a+b
   elif m=='sub':v=a-b
   elif m=='neg':v=-a
   elif m=='not':v=-a-1 if sym else ~a
   elif m=='inc':v=a+1
   elif m=='dec':v=a-1
   else:
    b=b&(63 if n==64 else 31)
    if m in ('shl','sal'):v=a<<b
    elif m=='shr':v=z.LShR(a,b) if sym else a>>b
    elif m=='sar':v=a>>b if sym else (a-(1<<n) if a>>(n-1) else a)>>b
    elif m in ('rol','ror'):
     if sym:v=z.RotateLeft(a,b) if m=='rol' else z.RotateRight(a,b)
     else:
      b%=n;v=(a<<b)|(a>>(n-b)) if m=='rol' else (a>>b)|(a<<(n-b))
   self.put(o[0],v,i)
   if m!='not':self.flags=sym
   return
  if m=='bswap':
   a=self.get(o[0],i);n=o[0].size
   if isinstance(a,int):v=int.from_bytes(a.to_bytes(n,'little'),'big')
   else:v=z.Concat(*[z.Extract(x*8+7,x*8,a) for x in range(n)])
   self.put(o[0],v,i);return
  reads,writes=i.regs_access();tainted=self.flags or any(not isinstance(self.getreg(r),int) for r in reads if self.md.reg_name(r) not in ('rflags','eflags'))
  for r in writes:
   s=self.md.reg_name(r)
   if s in ('rflags','eflags'):self.flags=tainted
   elif s.startswith(('xmm','ymm','zmm')):pass
   else:
    if tainted:self.setreg(r,self.unk(self.desc(r)[1]))
    else:self.reg.pop(self.desc(r)[0],None)

def main():
 p=argparse.ArgumentParser();p.add_argument('image');p.add_argument('--stop-stage',type=int,default=1000);p.add_argument('--validate',action='store_true');p.add_argument('--solve',action='store_true');p.add_argument('--word-input',action='store_true');p.add_argument('--no-workspace',action='store_true');p.add_argument('--traps');p.add_argument('--transforms-only',action='store_true');p.add_argument('--output',default='check_state.smt2');a=p.parse_args()
 data=Path(a.image).read_bytes();u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64);u.mem_map(B,(len(data)+4095)&~4095);u.mem_write(B,data)
 u.mem_map(0x10000000,0x1000000);u.mem_map(0x20000000,0x1000000);u.mem_map(0x30000000,0x20000);u.mem_map(0x7ff00000,0x100000)
 def put(p,x):u.mem_write(p,struct.pack('<Q',x))
 u.reg_write(ux.UC_X86_REG_GS_BASE,0x7ff00000);put(0x7ff00060,0x7ff01000);put(0x7ff00040,1234);put(0x7ff01010,B);put(0x7ff01018,0x7ff02000);put(0x7ff01030,0x30000000)
 sp=0x10fe0000;u.reg_write(ux.UC_X86_REG_RSP,sp);u.reg_write(ux.UC_X86_REG_RBP,sp+0x100);u.reg_write(ux.UC_X86_REG_RDI,0x20000000)
 concrete=b'ctfcup{'+b'A'*59+b'}';u.mem_write(0x20000000,concrete);u.reg_write(ux.UC_X86_REG_RBX,0);u.reg_write(ux.UC_X86_REG_RSI,0)
 hv=Hypervisor(pid=1234);s=Shadow(u);words=[z.BitVec('input_word_%02d'%x,32) for x in range(17)];chars=[z.Extract((x%4)*8+7,(x%4)*8,words[x//4]) for x in range(67)] if a.word_input else [z.BitVec('flag_%02d'%x,8) for x in range(67)]
 for j,x in enumerate(chars):s.mem[0x20000000+j]=x
 if a.traps:
  ts=json.loads(Path(a.traps).read_text())
  hv.traps={int(k,0) if isinstance(k,str) else k:tuple(int(x,0) if isinstance(x,str) else x for x in v) for k,v in ts.items()}
 stages=0;done=False;prevpc=0;t=time.time();last=[]
 def hook(u,pc,size,d):
  nonlocal stages,done,prevpc
  if len(last)>20:last.pop(0)
  last.append(pc)
  if size==1 and bytes(u.mem_read(pc,1))==b'\x90':
   chunk=bytes(u.mem_read(pc,256));n=0
   while n<len(chunk) and chunk[n]==0x90:n+=1
   u.reg_write(ux.UC_X86_REG_RIP,pc+n);return
  if pc in hv.traps and hv.traps[pc][0]==3 and u.reg_read(ux.UC_X86_REG_R10)==hv.traps[pc][2]:
   u.reg_write(ux.UC_X86_REG_R10,hv.traps[pc][1]);s.reg.pop('r10',None)
  if hv.handle(u,pc,size):return
  if pc==0x140698edb:
   print('RESULT',u.reg_read(ux.UC_X86_REG_EAX),'symbolic',s.getreg(X86_REG_EAX),flush=True);done=True;u.emu_stop();return
  if pc==0x140699420:
   rsp=u.reg_read(ux.UC_X86_REG_RSP);ra=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(ux.UC_X86_REG_RSP,rsp+8);u.reg_write(ux.UC_X86_REG_RIP,ra);return
  if 0x140698a19<=pc<0x140698edb and bytes(u.mem_read(pc,1))==b'\xe8':
   stages+=1;print('STAGE',stages,'PC',hex(pc),'TIME',time.time()-t,'SYMBYTES',len(s.mem),'UNKNOWN',s.unknown,flush=True)
   if stages>a.stop_stage:u.emu_stop();return
   transform_stages=set(range(1,6))|set(range(8,12))|set(range(14,18))|set(range(20,24))|set(range(26,31))|set(range(33,37))|set(range(39,43))|set(range(45,49))|set(range(51,56))
   if a.transforms_only and stages not in transform_stages:
    if stages>55:u.emu_stop();return
    u.reg_write(ux.UC_X86_REG_RIP,pc+size);return
  s.step(pc,size)
 u.hook_add(unicorn.UC_HOOK_CODE,hook)
 def intr(u,n,d):
  if not hv.handle_exception(u,n):raise RuntimeError(('intr',n,hex(u.reg_read(ux.UC_X86_REG_RIP))))
 u.hook_add(unicorn.UC_HOOK_INTR,intr)
 try:u.emu_start(0x140698a19,0,count=10000000)
 except Exception as e:print('ERROR',repr(e),'LAST',list(map(hex,last)),flush=True);raise
 print('FINISHED',time.time()-t,'INSTRUCTIONS',s.n,flush=True)

 out={}
 for off in range(0x2080):
  v=s.mem.get(sp+0xa0+off)
  if v is not None:out[off]=v
 solver=z.Solver();solver.add(s.defs)
 for x in chars[7:-1]:solver.add(z.Or(z.And(x>=48,x<=57),z.And(x>=65,x<=90),z.And(x>=97,x<=122),x==95))
 for j,v in enumerate(b'ctfcup{'):solver.add(chars[j]==v)
 solver.add(chars[-1]==ord('}'))
 if done:
  result=s.getreg(X86_REG_EAX);solver.add(bv(result,32)==1)
  Path('cc2_constraints.smt2').write_text(solver.to_smt2())
  if a.solve:
   print('SOLVING',flush=True);r=solver.check();print(r,flush=True)
   if r==z.sat:print('FLAG',bytes(solver.model().eval(x).as_long() for x in chars).decode(),flush=True)
 if not a.no_workspace:
  summary=z.Solver();summary.add(s.defs)
  for off,v in out.items():summary.add(z.BitVec('workspace_%04x'%off,8)==v)
  Path('cc2_workspace.smt2').write_text(summary.to_smt2())
 state_solver=z.Solver();state_solver.add(s.defs)
 for off in range(0,72,4):state_solver.add(z.BitVec('state_%02d'%off,32)==s.readmem(sp+0x50+off,sp+0x50+off,4))
 Path(a.output).write_text(state_solver.to_smt2())
 if a.validate:
  subs=[(x,z.BitVecVal(int.from_bytes((concrete+b'\0')[j*4:j*4+4],'little'),32)) for j,x in enumerate(words)] if a.word_input else [(x,z.BitVecVal(concrete[j],8)) for j,x in enumerate(chars)];subs+=s.bindings;bad=[]
  for addr,v in s.mem.items():
   ev=z.simplify(z.substitute(bv(v,8),*subs));actual=u.mem_read(addr,1)[0]
   if not z.is_bv_value(ev) or ev.as_long()!=actual:bad.append((hex(addr),str(ev),actual))
  print('VALIDATION_BAD',len(bad),bad[:20],flush=True)
if __name__=='__main__':main()

````````````
