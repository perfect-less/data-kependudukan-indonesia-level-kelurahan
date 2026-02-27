from typing import List
import pandas as pd

import requests
import urllib
import json
import os

BATCH_SIZE = 1000
OUTPUT_DIRECTORY = 'data'
JSON_SAVE_FILE_NAME = 'data_kependudukan_kelurahan.json'
CSV_SAVE_FILE_NAME = 'data_kependudukan_kelurahan.csv'
PARQUET_SAVE_FILE_NAME = 'data_kependudukan_kelurahan.parquet'


class APICaller:
    def __init__(
            self,
            batch_size: int = 50,
            hostname: str = 'gis.dukcapil.kemendagri.go.id',
            url_path: str = 'arcgis/rest/services/AGR_VISUAL_KEL_FIX/MapServer/0/query'
            ):
        self.batch_size = batch_size
        self.hostname = hostname
        self.url_path = url_path
        self.rename_mapping = self.get_rename_mapping()

    def build_query_dict(self, offset: int = 0, count: int = None) -> dict:
        count = self.batch_size if not count else count
        return {
                "f": "json",
                "resultOffset": str(offset),
                "resultRecordCount": str(count),
                "where": "1=1",
                "orderByFields": "",
                "outFields": "*",
                "returnGeometry": "false",
                "spatialRel": "esriSpatialRelIntersects"
                }

    def build_url(self, params_dict: dict):
        return f"https://{self.hostname}/{self.url_path}?{urllib.parse.urlencode(params_dict)}"

    def _retrieve_data(self, offset: int = 0, count: int = 50) -> dict:
        params_dict = self.build_query_dict(offset, count)
        url = self.build_url(params_dict)
        response = requests.request("GET", url)
        if response.status_code != 200:
            raise Exception(f"Error when querying to '{url}'")

        resp_dict = json.loads(response.text)
        return resp_dict

    def get_rename_mapping(self):
        resp_dict = self._retrieve_data(0, 1)

        rename_mapping = {}
        for field in resp_dict['fields']:
            field_name = field['name']
            repl_name = field_name.replace('(', '__').replace(')', '__')
            if field_name != repl_name:
                rename_mapping[field_name] = repl_name
                field_name = repl_name
        return rename_mapping

    def retrieve_batch_data(self, batch_number: int = 0) -> List[dict]:
        offset = batch_number * self.batch_size

        resp_dict = self._retrieve_data(offset=offset, count=self.batch_size)
        unpacked_dicts = []
        for feature in resp_dict['features']:
            unpacked_dicts.append(feature['attributes'])

        return unpacked_dicts


if __name__ == "__main__":
    print("Begin program")

    batch_size = BATCH_SIZE
    json_save_file_path = os.path.join(OUTPUT_DIRECTORY, JSON_SAVE_FILE_NAME)
    csv_save_file_path = os.path.join(OUTPUT_DIRECTORY, CSV_SAVE_FILE_NAME)
    parquet_save_file_path = os.path.join(OUTPUT_DIRECTORY, PARQUET_SAVE_FILE_NAME)

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    caller = APICaller(
            batch_size=batch_size
            )

    data = []

    batch_number = 0
    ingested_rows = 0
    print("begin ingestion process..")
    while True:

        retrieved_data = caller.retrieve_batch_data(batch_number)
        if len(retrieved_data) <= 0:
            print(f"  ingested: {ingested_rows}", end='\r')
            break
        data.extend(retrieved_data)

        batch_number += 1
        ingested_rows += batch_size
        print(f"  ingested: {ingested_rows}", end='\r')

    print(f"\nSaving JSON object to -> '{json_save_file_path}'")
    json_str = json.dumps(data)
    with open(json_save_file_path, 'w') as file:
        file.write(json_str)
    file.close()
    del json_str

    print("Converting data to DataFrame")
    df = pd.DataFrame(data) \
        .rename(columns=caller.rename_mapping) \
        .sort_values(by=['nama_prop', 'nama_kab', 'nama_kec', 'nama_kel'])
    del data

    print(f"Saving CSV data to -> '{csv_save_file_path}'")
    df.to_csv(csv_save_file_path, sep=';')

    print(f"Saving Parquet data to -> '{parquet_save_file_path}'")
    df.to_parquet(parquet_save_file_path)

    print("Done, exitting...")
