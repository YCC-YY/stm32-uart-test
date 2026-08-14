import json
from pathlib import Path


class _TestReporter:
    def __init__(self):
        self.case_list = []

    def add_record(self, case_name: str, pass_flag: bool, resp: str):
        self.case_list.append({
            "case": case_name,
            "pass": pass_flag,
            "response": resp
        })

    def save_json(self, path="report.json"):
        out = {
            "total": len(self.case_list),
            "pass": sum(1 for item in self.case_list if item["pass"]),
            "data": self.case_list
        }
        Path(path).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


# 全局单例，测试用例直接导入
rep = _TestReporter()
