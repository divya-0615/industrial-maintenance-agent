from hindsight_client import Hindsight
from dotenv import load_dotenv
import os

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

try:
    result = client.recall(
        bank_id="industrial-maintenance-agent",
        query="What caused Machine M1 to overheat, and how was it fixed?"
    )

    print("\n--- PERSISTENT MEMORY TEST ---")

    for memory in result.results:
        print("-", memory.text)

finally:
    client.close()