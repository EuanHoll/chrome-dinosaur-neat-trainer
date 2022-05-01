# Chrome Dinosaur Neat Trainer

## Description

This is my first go at using python-neat to learn about genetic algorithms.
This was created following the examples from [Code Bucket's NEAT Tutorials](https://www.youtube.com/playlist?list=PL30AETbxgR-d03tf_HIr8-OA1gmClI3mE) though the code has been edited heavily to make it easier to understand and use.
Some extra features have also been added.

## Installation

You can use either `poetry` or `pip` for the install. \
For `poetry` simply use `poetry install` in the directory. \
For `pip` use `pip install -r requirements.txt` in the directory.

## Running

To run the training: `python ./src/main.py -m train` \
To run the previous winner sole: `python ./src/main.py -m run`

## Usage

```
usage: main.py [-h] [-wp WINNER_PATH] [-ip INPUT_PATH] [-up USE_PREVIOUS] [-m MODE] [-g GENERATIONS]

Run a Neat Algorithm to Play / Train on the Chrome Dinosaur Game

optional arguments:
  -h, --help            show this help message and exit
  -wp WINNER_PATH, --winner_path WINNER_PATH
                        Path to save the winner file to.
  -ip INPUT_PATH, --input_path INPUT_PATH
                        Path to the input nueral network.
  -up USE_PREVIOUS, --use_previous USE_PREVIOUS
                        Use previous winner in the first generation of training.
  -m MODE, --mode MODE  Whether the program is set to 'train' or 'run' mode.
  -g GENERATIONS, --generations GENERATIONS
                        Number of generations the networks will train for. Must be greater than 0.
```

## Outputs

The program will always output the "winner" or best of a batch. This will be writen to the `winner_path`. The high_score of the last generation will also be written to `rsrc/high_score.txt`.
