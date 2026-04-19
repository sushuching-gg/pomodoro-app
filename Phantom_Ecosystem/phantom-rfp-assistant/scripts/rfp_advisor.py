import os
import argparse
import sys
import docx
from datetime import datetime

class RFPAdvisor:
    def __init__(self, database_root):
        self.db_root = database_root
        self.template_patterns = [
            r"1_115\u65b0\u5e74\u5ea6\u898f\u5243\\1_115\u90e8\u5167\u62db\u6a19\u6587\u4ef6\\\u9644\u4ef65_\u9700\u6c42\u898f\u7bc4\u66f80130(final)v1.docx",
            r"3_\u8cc7\u6599\u5b58\u6a94\\2025\\\u81fa\u5317\u79df\u501f2.0\u57f7\u884c\\\u4e09\u66f8\u53ca\u53c3\u8003\u8cc7\u6599\\\u9644\u4ef65-\u9700\u6c42\u898f\u7bc4\u66f81105CCdocx.docx"
        ]

    def find_templates(self, keyword):
        print(f"[\u6316\u6398] \u6b63\u5728 PO \u8cc7\u6599\u5eab\u641c\u5c0b\u300c{keyword}\u300d\u76f8\u95dc\u7684\u62db\u6a19\u9700\u6c42\u66f8\u7bc4\u4f8b...")
        # Since these are absolute paths relative to root:
        found_any = False
        for p in self.template_patterns:
            full_p = os.path.join(self.db_root, p.replace('\\\\', '\\'))
            if os.path.exists(full_p):
                print(f"  -> \u5efa\u8b70\u53c3\u8003\uff1a{full_p}")
                found_any = True
        if not found_any:
            print("  ! \u7121\u6cd5\u627e\u5230\u9019\u4e9b\u6A94\u6848\uFF0C\u8ACB\u78BA\u8a8D D \u69FD\u9023\u63A5\u3002")

    def provide_guidance(self, rfp_path=None):
        print("\n=== \u62db\u6a19\u9700\u6c42\u66f8\u64b0\u5beb\u9867\u554f (Mid-term) ===")
        print("[\u960e\u8b80] \u76ee\u524d\u5b9a\u4f4d\uff1a\u8a08\u756B\u4e2d\u671f - Q1 \u671f\u521d\u8F14\u5C0E")
        print("[\u76ee\u6a19] \u5354\u52a9\u7e23\u5e02\u7522\u51fa\u5408\u898F\u4e14\u9ad8\u54c1\u8cea\u7684\u62db\u6a19\u6587\u4ef6\n")
        
        if rfp_path and os.path.exists(rfp_path):
            print(f"[\u5206\u6790] \u6b63\u5728\u6aa2\u8996\u7e23\u5e02\u8349\u6848\uff1a{os.path.basename(rfp_path)}")
            print("  - \u601d\u8003\uff1a\u662f\u5426\u5df2\u5305\u542b 114 \u5e74\u5ea6\u6838\u5fc3 KPI\uff1f")
            print("  - \u63d0\u9192\uff1a\u8acb\u52a0\u5165\u300c\u8cc7\u901a\u5b89\u5168\u5f31\u9ede\u6383\u63cf\u300d\u5fc5\u5099\u683c\u5f0f\u3002")
        else:
            print("[\u6316\u6398] \u6b63\u5728\u70BA\u60A8\u51C6\u5099\u6307\u5F15\u6587\u4EF6...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', help='\u641c\u5c0b\u7bc4\u4f8b\u95dc\u9375\u5b57')
    parser.add_argument('--input', help='\u7e23\u5e02\u62db\u6a19\u8349\u6848\u8def\u5f91')
    args = parser.parse_args()
    
    advisor = RFPAdvisor(r"D:\1_working")
    if args.search:
        advisor.find_templates(args.search)
    advisor.provide_guidance(args.input)
