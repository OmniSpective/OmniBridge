# Contributing an API Based Wrapper

An API based wrapper is a wrapper to an AI model that is accessible via API.

In this guide, you will learn how you can contribute a new API based wrapper, including tests and wiring it to the CLI application.

## Creating the Wrapper

* Go to `omnibridge/wrappers/wrapper_instances` and create a new file for your wrapper
* Create a new class that inherits from `RestAPIWrapper`
* Implement all of the abstract methods

Implementing the methods should be straightforward, but if you have any questions, be sure to ask it in our [discord server](https://discord.gg/RjPHfAKd7D) or open an issue.

## Wiring the Wrapper
In the previous step you implemented the wrapper, now in order for it to be accessible via the CLI, you'll have to make a few more simple additions.

First of all, ask yourself if you need additional input from the user in order to make requests in your wrapper.
If you need more input from the user, go to `omnibridge/cli/create/create_parser.py` and add more arguments in the `add_create_model_sub_parser` function.


* Go to `omnibridge/cli/create/create_command_handler.py` and add a new function that will handle the addition of the model. there are a few examples in the file such as `add_chatgpt`, `add_dalle`, and `add_huggingface` which you can take inspiration from.

* In the same file `omnibridge/cli/create/create_command_handler.py`, modify the `MODEL_TYPE_TO_CREATION_FUNCTION` mapping to include your newly added model and it's corresponding function.

* Lastly, go to `omnibridge/wrappers/wrapper_instances/type_name_to_wrapper.py` and add your Wrapper into the mapping `type_names`.


# Writing Tests

* Go to `tests/unit/wrappers` and create a new test file for your wrapper.
* Write a few tests while mocking the API calls themselves using a library called `responses` - you have usage examples in `tests/unit/wrappers/test_gpt_wrapper.py`

---

If you are having any issue be sure to let us know in the [discord server](https://discord.gg/RjPHfAKd7D) or open an issue.
