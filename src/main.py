import argparse
import pandas as pd
import gradio as gr
from functools import partial

from configs.data import FilesConfig
from .helper import (
    sample_prompt,
    on_both_bad_click,
    on_left_better_click,
    on_right_better_click,
    on_tie_click
)

def build_panels(
    golden_data: pd.DataFrame,
    model_reponse: pd.DataFrame,
):

    with gr.Blocks() as demo:
        btn = gr.Button("Sample a new prompt")

        with gr.Row():
            with gr.Column(scale=1):
                prompt_id = gr.Textbox(label='Prompt ID')
            with gr.Column(scale=8):
                prompt = gr.Textbox(label="Prompt")

        with gr.Row():
            with gr.Column(scale=1):
                o1 = gr.Textbox(label='Output 1')
            with gr.Column(scale=1):
                o2 = gr.Textbox(label='Output 2')

        with gr.Row():
            left_better = gr.Button('👈 Output 1 is better', interactive=False)
            tie = gr.Button('🤝 Tie', interactive=False)
            both_bad = gr.Button('👎 Both are bad', interactive=False)
            right_better = gr.Button('👉 Output 2 is better', interactive=False)

        # State for each of the voting button
        btns_list = [
            left_better,
            right_better,
            both_bad,
            tie,
        ]

        # Variables to maintain states
        is_model_left = gr.Variable(False)
        sample_prompt_id = gr.Variable(0)
        num_btns = gr.Variable(len(btns_list))
        golden = gr.Variable(golden_data)
        model = gr.Variable(model_reponse)

        btn.click(
            fn=sample_prompt,
            inputs=[golden, model, num_btns],
            outputs=[prompt_id, prompt, o1, o2, sample_prompt_id, is_model_left] + btns_list
        )

        left_better.click(
            on_left_better_click,
            inputs=[prompt_id, is_model_left],
            outputs=btns_list
        )

        right_better.click(
            on_right_better_click,
            inputs=[prompt_id, is_model_left],
            outputs=btns_list
        )

        tie.click(
            on_tie_click,
            inputs=[prompt_id, is_model_left],
            outputs=btns_list
        )

        both_bad.click(
            on_both_bad_click,
            inputs=[prompt_id, is_model_left],
            outputs=btns_list
        )

    return demo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--golden_data',
        help='Location of the golden data',
        required=False,
        type=str
    )

    parser.add_argument(
        '--model_response',
        help='Location of the model responses',
        required=False,
        type=str
    )

    args = parser.parse_args()
    golden_data = args.golden_data if args.golden_data is not None else FilesConfig.GOLDEN_DATA
    model_response = args.model_response if args.model_response is not None else FilesConfig.MODEL_RESPONSE


    assert golden_data is not None and golden_data != '', f'Golden data location not provided nor found in configs'
    assert model_response is not None and model_response != '', f'Model response location not provided nor found in configs'

    webui = build_panels(
        pd.read_csv(golden_data),
        pd.read_csv(model_response)
    )
    webui.launch()
