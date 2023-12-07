from dataclasses import dataclass

@dataclass
class FilesConfig:
    GOLDEN_DATA: str = 'data/golden_data.csv'
    MODEL_RESPONSE: str = 'data/model_response.csv'
    RESULTS_FILE: str = 'data/results.jsonl'
