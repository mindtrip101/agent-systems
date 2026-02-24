import argparse
from app.policy import approve

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request-id", required=True)
    ap.add_argument("--approver", default="human")
    args = ap.parse_args()

    ok = approve(args.request_id, args.approver)
    if ok:
        print("Approved.")
    else:
        print("Request id not found.")

if __name__ == "__main__":
    main()
