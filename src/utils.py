import json
import gradio as gr
from configs.data import FilesConfig

def get_ip(request: gr.Request):
    if "cf-connecting-ip" in request.headers:
        ip = request.headers["cf-connecting-ip"]
    else:
        ip = request.client.host
    return ip

def log2file(sample_prompt_id: int, result: str):
    with open(FilesConfig.RESULTS_FILE, 'a') as fp:
        data = {
            'prompt_id': sample_prompt_id,
            'result': result
        }

        fp.write(json.dumps(data))
        fp.write('\n')
