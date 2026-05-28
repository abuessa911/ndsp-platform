from __future__ import annotations

import logging
import time

from app.services.elite_trial_service import close_expired_accounts, summary
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def main() -> None:
    logging.info("elite trial expiry worker started")
    while True:
        try:
            result = close_expired_accounts()
            s = summary()
            logging.info(
                "elite_trial checked closed=%s ordinary_used=%s analyst_used=%s waitlist=%s",
                result.get("closed_count"),
                s.get("ordinary_used"),
                s.get("analyst_used"),
                s.get("waitlist_count")
            )
        except Exception as e:
            logging.error("elite_trial_expiry_error=%s", str(e))
        time.sleep(3600)

if __name__ == "__main__":
    main()
