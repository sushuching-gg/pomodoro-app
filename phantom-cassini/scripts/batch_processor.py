import os
import sys
import json
import logging
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FutureTimeoutError

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "..", "..", "skills", "phantom-web-officer", "scripts"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

try:
    from plan_parser import parse_plan
except ImportError:
    logger.error("Could not import plan_parser. Exiting.")
    sys.exit(1)

def process_file(file_path):
    try:
        if os.path.basename(file_path).startswith("~$"):
            return None
        result = parse_plan(file_path)
        if "error" in result:
            return {"status": "error", "file": file_path, "message": result['error']}
        if 'tables' in result:
            result['table_count'] = len(result['tables'])
            del result['tables']
        return {"status": "success", "file": file_path, "data": result}
    except Exception as e:
        return {"status": "error", "file": file_path, "message": str(e)}

def batch_process(root_dir, output_file="batch_scan_report.json", max_workers=None, per_file_timeout=60):
    """
    [P6] max_workers is configurable (default: cpu_count, capped at 16).
         per_file_timeout prevents a single file from blocking the whole batch.
    """
    logger.info("Scanning directory: %s", root_dir)

    docx_files = glob.glob(os.path.join(root_dir, "**", "*.docx"), recursive=True)
    logger.info("Found %d DOCX files.", len(docx_files))

    results = {
        "summary":      {"total": 0, "success": 0, "error": 0, "timeout": 0},
        "success_data": [],
        "errors":       [],
    }

    # [P6] Dynamic worker count
    if max_workers is None:
        max_workers = min(os.cpu_count() or 4, 16)
    logger.info("Using %d worker threads.", max_workers)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in docx_files}

        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            results['summary']['total'] += 1
            try:
                # [P6] per_file_timeout prevents one bad file from stalling the pool
                res = future.result(timeout=per_file_timeout)
                if res:
                    if res['status'] == 'success':
                        results['success_data'].append(res['data'])
                        results['summary']['success'] += 1
                        logger.info("[OK]   %s", os.path.basename(file_path))
                    else:
                        results['errors'].append(res)
                        results['summary']['error'] += 1
                        logger.warning("[FAIL] %s: %s", os.path.basename(file_path), res['message'])
            except FutureTimeoutError:
                results['errors'].append({"status": "timeout", "file": file_path, "message": "Exceeded {}s".format(per_file_timeout)})
                results['summary']['timeout'] += 1
                logger.error("[TIMEOUT] %s", os.path.basename(file_path))
            except Exception as exc:
                results['errors'].append({"status": "error", "file": file_path, "message": str(exc)})
                results['summary']['error'] += 1
                logger.error("[FAIL] %s: %s", os.path.basename(file_path), exc)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info("Batch processing complete. Total=%d  OK=%d  Fail=%d  Timeout=%d",
                results['summary']['total'], results['summary']['success'],
                results['summary']['error'], results['summary']['timeout'])
    logger.info("Report saved to: %s", output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phantom Cassini Batch Processor")
    parser.add_argument("root_dir", help="Root directory to scan for DOCX files")
    parser.add_argument("--output", default="batch_scan_report.json", help="Output JSON path")
    # [P6] Allow worker count and timeout to be set from CLI
    parser.add_argument("--workers", type=int, default=None,
                        help="Number of parallel workers (default: cpu_count)")
    parser.add_argument("--timeout", type=int, default=60,
                        help="Per-file timeout in seconds (default: 60)")
    args = parser.parse_args()

    if not os.path.exists(args.root_dir):
        logger.error("Directory not found: %s", args.root_dir)
        sys.exit(1)

    batch_process(args.root_dir,
                  output_file=args.output,
                  max_workers=args.workers,
                  per_file_timeout=args.timeout)
