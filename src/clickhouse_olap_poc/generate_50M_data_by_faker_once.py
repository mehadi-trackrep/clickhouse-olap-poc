# -*- coding: utf-8 -*-
import os
import random
import pandas as pd
from faker import Faker


# --- Configuration ---
TOTAL_RECORDS = 50_000_000  # 50M
CHUNK_SIZE = 1_000_000     # Generate 1M records at a time
OUTPUT_FILE = 'data/fake_logs.csv'


def generate_chunk(fake, urls, size: int) -> pd.DataFrame:
    """Generate a single chunk of fake log data."""
    return pd.DataFrame({
        'event_time': [fake.date_time_this_year() for _ in range(size)],
        'url': [random.choice(urls) for _ in range(size)],
        'country': [fake.country_code() for _ in range(size)],
        'response_time_ms': [random.randint(20, 5000) for _ in range(size)]
    })


def generate_data_in_chunks(total_records: int, chunk_size: int, output_file: str):
    fake = Faker()
    urls = [f'/{fake.uri_path()}' for _ in range(1000)]

    total_chunks = (total_records + chunk_size - 1) // chunk_size
    print(f"==> Starting generation of {total_records:,} records "
          f"({total_chunks} chunks of {chunk_size:,})...\n")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if os.path.exists(output_file):
        os.remove(output_file)

    records_generated = 0

    for chunk_num in range(1, total_chunks + 1):
        current_chunk_size = min(chunk_size, total_records - records_generated)
        df_chunk = generate_chunk(fake, urls, current_chunk_size)

        df_chunk.to_csv(
            output_file,
            mode='a',
            index=False,
            header=(chunk_num == 1)
        )

        records_generated += current_chunk_size

        """ Progress reporting """
        percent = (records_generated / total_records) * 100
        print(f"#Chunk {chunk_num}:\t& progress: [ ({chunk_num} / {total_chunks})  = {percent:.1f}% ]")

    print("Data generation completed.")


if __name__ == "__main__":
    generate_data_in_chunks(TOTAL_RECORDS, CHUNK_SIZE, OUTPUT_FILE)
    print(f"All data saved to '{OUTPUT_FILE}'.")