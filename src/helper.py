import random
import numpy as np
import pandas as pd
import gradio as gr

from .utils import get_ip, log2file
from .logger import logger

enable_btn = gr.Button.update(interactive=True, visible=True)
disable_btn = gr.Button.update(interactive=False, visible=True)

def get_model_output(id, model:pd.DataFrame):
    return model.query('prompt_id == @id').response.iloc[0]


def get_sample_prompt(id, golden:pd.DataFrame):
    p = golden.query('prompt_id == @id').prompt.iloc[0]
    r = golden.query('prompt_id == @id').response.iloc[0]
    return p, r


def sample_prompt(golden, model, num_btns: gr.Variable, request: gr.Request):
    logger.info(get_ip(request))

    sample_prompt_id = random.choice(golden.prompt_id.unique())
    logger.info(f'Prompt chosen is {sample_prompt_id}')

    sample_prompt, saved_output = get_sample_prompt(id=sample_prompt_id, golden=golden)
    model_output = get_model_output(id=sample_prompt_id, model=model)

    # Randomly flip the model output to either left or right panel
    if np.random.uniform() < 0.5:
        return (
            sample_prompt_id,
            sample_prompt,
            saved_output,
            model_output,
            sample_prompt_id,
            False,
        ) + (enable_btn,) * num_btns

    return (
        sample_prompt_id,
        sample_prompt,
        model_output,
        saved_output,
        sample_prompt_id,
        True,
    ) + (enable_btn,) * num_btns


def on_left_better_click(sample_prompt_id, is_model_left):
    if is_model_left:
        logger.info(f'For {sample_prompt_id} model response is selected')
        log2file(
            sample_prompt_id=sample_prompt_id,
            result='model'
        )
    else:
        logger.info(f'For {sample_prompt_id} saved response is selected')
        log2file(
            sample_prompt_id=sample_prompt_id,
            result='saved'
        )

    return (disable_btn,) * 4


def on_right_better_click(sample_prompt_id, is_model_left):
    if is_model_left:
        logger.info(f'For {sample_prompt_id} saved response is selected')
        log2file(
            sample_prompt_id=sample_prompt_id,
            result='saved'
        )
    else:
        logger.info(f'For {sample_prompt_id} model respomse is selected')
        log2file(
            sample_prompt_id=sample_prompt_id,
            result='model'
        )

    return (disable_btn,) * 4


def on_tie_click(sample_prompt_id, is_model_left):
    logger.info('Both responses are equally good!')
    log2file(
        sample_prompt_id=sample_prompt_id,
        result='tie'
    )

    return (disable_btn,) * 4


def on_both_bad_click(sample_prompt_id, is_model_left):
    logger.info('Both responses are equally bad!')
    log2file(
        sample_prompt_id=sample_prompt_id,
        result='both_bad'
    )

    return (disable_btn,) * 4
