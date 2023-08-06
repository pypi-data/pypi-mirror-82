# Plurk Dice

## Install

```bash
pip install plurk-dice
```

## Usage

```python
>>> from plurk_dice import Dice

# Roll a dice directly

>>> Dice(20).roll()
{'result': 7, 'url': 'https://s.plurk.com/ff94b39b3f0927042f8479fac0fd92d1.png'}

>>> Dice("bzz").roll(base64=True)
{'result': 'B', 'url': 'https://s.plurk.com/e3481a0219283c49455d8af6012980ea.png', 'base64': 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAARxJREFUeNqs1bFLAmEYx/H3Ui6c2sR0jByV3EWE2gMRkyJpcDOXBsF2JynrDwhqUf8MHaWWtKWtocBwDhzCvhePcYOHd+/bC5/hOR5+vHfv3XOWrb6V5krgEEOMlxc3lP6KoYEbpP8jMIU48riTWjswigpCUmdwiz3dwCpyrnqOJLJhjbB91Fz1APeY4CNo4A5aciCf6Mjzm/51OK+NT1voYYERDlb1+Q0L4VrC+tj16vUTZuESX7iSnSqTwDpmaMJe178u7AxvOJedKpPAE7ygEuDgPANLeEI5SJhX4BEeUQwatirQuc1nnZ0tOV/KJiIooI42urojKCyz7BinuMCDwUj7HV/veJUPvK8MlyW/AGdQbsvEmJsE/ggwAMem4bIle0IVAAAAAElFTkSuQmCC'}

# Roll dices parse from text

>>> Dice.parse("(dice20)(dice8)")
[{'result': 2, 'url': 'https://s.plurk.com/27866de1cbed77d98cd8a886205c9dcb.png'}, {'result': 6, 'url': 'https://s.plurk.com/17c9123ed084f917ede14447afdfabdf.png'}]
>>> Dice.parse("(dice20)(dice8)", base64=True)
...
```

## Run tests

```bash
python -m unittest
```
