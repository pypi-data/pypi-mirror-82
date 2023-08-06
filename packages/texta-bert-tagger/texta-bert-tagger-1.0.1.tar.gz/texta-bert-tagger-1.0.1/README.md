# TEXTA Bert Tagger Python package


## Installation


##### From Git
`pip install git+https://git.texta.ee/texta/texta-bert-tagger-python.git`

### Testing

`python -m pytest -v tests`

### Documentation

Documentation is available [here](https://git.texta.ee/texta/texta-bert-tagger-python/-/wikis/Documentation).

## Usage

### Fine-tune BERT model

```
>>> from texta_bert_tagger.tagger import BertTagger
>>> bert_tagger = BertTagger()

>>> data_sample = {"good": ["Täna on ilus ilm.", "Kuidas käsi käib?"], "bad": ["Arno on loll.", "ei"]}

# Train model

>>> bert_tagger.train(data_sample, n_epochs=1)


# Predict

>>>  bert_tagger.tag_text("Ei hooli.")
'bad'
```
