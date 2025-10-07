# -*- coding: utf-8 -*-
import random
import pandas as pd
from faker import Faker


# --- 1. Data Generation ---
def generate_data(num_records: int) -> pd.DataFrame:
    """Generates a Pandas DataFrame with fake log data."""
    
    print(f"Generating {num_records:,} fake log records...")

    fake = Faker()

    # Pre-generate a list of URLs to make grouping more meaningful
    urls = [f'/{fake.uri_path()}' for _ in range(1000)]

    data = {
        'event_time': [fake.date_time_this_year() for _ in range(num_records)],
        'url': [random.choice(urls) for _ in range(num_records)],
        'country': [fake.country_code() for _ in range(num_records)],
        'response_time_ms': [random.randint(20, 5000) for _ in range(num_records)]
    }

    return pd.DataFrame(data)