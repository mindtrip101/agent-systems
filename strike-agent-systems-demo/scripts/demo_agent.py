"""A tiny 'agent' client to show the loop:
- list tools
- call safe tool
- attempt risky tool -> gets approval request id
- simulate approval then re-run with _request_id
"""
import argparse, httpx, subprocess, sys, json

def sh(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return p.stdout.strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:8000")
    ap.add_argument("--token-file", default=".token")
    args = ap.parse_args()

    token = open(args.token_file, "r", encoding="utf-8").read().strip()
    headers = {"Authorization": f"Bearer {token}"}

    with httpx.Client(timeout=10.0) as c:
        tools = c.get(f"{args.base}/tools", headers=headers).json()
        print("TOOLS:", json.dumps(tools, indent=2))

        r = c.post(f"{args.base}/invoke", headers=headers, json={"tool":"health.ping","args":{"message":"hello"}}).json()
        print("PING:", json.dumps(r, indent=2))

        r2 = c.post(f"{args.base}/invoke", headers=headers, json={"tool":"finance.transfer","args":{"amount_usd":50,"to":"acct_123"}}).json()
        print("TRANSFER:", json.dumps(r2, indent=2))

        if r2.get("requires_approval"):
            rid = r2["request_id"]
            print("Approving request:", rid)
            sh(f"python scripts/approve.py --request-id {rid} --approver demo")
            r3 = c.post(f"{args.base}/invoke", headers=headers, json={"tool":"finance.transfer","args":{"amount_usd":50,"to":"acct_123","_request_id":rid}}).json()
            print("TRANSFER (after approval):", json.dumps(r3, indent=2))

if __name__ == "__main__":
    main()
