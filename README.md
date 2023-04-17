[![codecov](https://codecov.io/gh/OmniSpective/OmniBridge/branch/main/graph/badge.svg)](https://codecov.io/gh/OmniSpective/OmniBridge)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/OmniSpective/OmniBridge/tests.yml)
![PyPI - License](https://img.shields.io/pypi/l/omnibridge)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/OmniSpective/OmniBridge)
![PyPI - Downloads](https://img.shields.io/pypi/dd/omnibridge?style=plastic)

# OmniBridge

OmniBridge wrap and connects different AI models. It helps access different AI models in a centralized place.


# Install
Clone the repository
```
git clone https://github.com/OmniSpective/OmniBridge.git
```

```
cd OmniBridge/
```
Inside the repository, install pipenv dependencies and launch the environment
```
pipenv install
```
```
pipenv shell
```

Now you can start using OmniBridge! 

# Usage

Add your key
```
python main.py create key --name open_ai --value <value>
```

Add your model
```
python main.py create model chatgpt --name gpt3.5 --key open_ai
```

You can now run chatGPT from your cli!
```
python main.py run model --name gpt3.5 --prompt "tell me a joke"
```

You can also use the model you created to build flows (aka Auto-GPT), passing the output of one model to several others!
```
python main.py create flow --name chef --model gpt3.5 -i "what ingridients do I need for the dishes?" 
"what wine would you suggest to pair with the dishes" "how much time does it take to prepare?"
```
This command set up four instances of your model, the first instance will handle your prompt as you would expect 
regularly, however, instead of returning the output, it will pass it to the other three, adding a specific instruction
for each!

Understand it best with an example -
(Notice it may take a short while to generate a response.)
```
python main.py run flow --name chef --prompt "suggest two dishes for a romantic date"
```

This should return
```
1. Filet Mignon with Roasted Vegetables: <description>
2. Lobster Risotto: <description>
******************************************************************

Ingridients:
< a list of ingridients>
******************************************************************

1. Filet Mignon with Roasted Vegetables: A red wine like a Cabernet Sauvignon or a Merlot...
2. Lobster Risotto: A white wine like a Chardonnay or a Sauvignon Blanc...
******************************************************************

Typical cooking times for a filet mignon can range from 8 to 12 minutes, and for lobster risotto, 
it can take around 30-40 minutes.
```
<br/><br/>
We are working on more cool stuff! 

# Community 
Come share your ideas, usage, and suggestions! <br/>
Join our <a href=https://discord.gg/RjPHfAKd7D>discord server</a>  and share your feedback and ideas with us! 
<a href="https://discord.gg/RjPHfAKd7D"><img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a69f118df70ad7828d4_icon_clyde_blurple_RGB.svg" alt="Discord Icon" width="40" height="20"></a>


# Contribute:

Join us in shaping the future of A.I!<br/>
For information on how to contribute, see [here](.github/CONTRIBUTING.md).



