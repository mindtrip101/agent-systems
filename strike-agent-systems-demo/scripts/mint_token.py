import argparse, jwt, time
from pathlib import Path
from app.config import settings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sub", required=True)
    ap.add_argument("--scopes", nargs="*", default=[])
    ap.add_argument("--out", default=".token")
    args = ap.parse_args()

    now = int(time.time())
    payload = {
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "sub": args.sub,
        "iat": now,
        "exp": now + 3600,
        "scopes": args.scopes,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    Path(args.out).write_text(token, encoding="utf-8")
    print(f"Wrote token to {args.out} (expires in 1h)")

if __name__ == "__main__":
    main()
