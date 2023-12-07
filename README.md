# Meraki Eval

This is a repo to build the evaluation tool for evaluating different models.

Currently this supports LLM models.

## How to run this?

(Please setup a virtualenv with Python 3.11.7)

```bash
# Setup requirements after activating the virtualenv
pip install -r requirements.txt
```

```bash
python main.py \
    --golden-data <location of the golden data of prompt response pair in .csv> \
    --model-response <location of the model prompt respone in .csv>
```

The two arguments can be updated in `./configs/data.py` as well

## Data format

Golden data needs to be in a `.csv` format with at least these three columns

- prompt_id
- prompt
- response

Model response needs to be in a `.csv` format with at least these two columns

- prompt_id
- response
