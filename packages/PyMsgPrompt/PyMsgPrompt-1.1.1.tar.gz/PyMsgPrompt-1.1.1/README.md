# PyMsgPrompt

PyMsgPrompt is a python module to embed prompt functionality in your code.

## Version

The current version of this module is `1.1.1` and this is the first BETA release after last Alpha version `0.0.5`, however, you can run the below command to check the version of the module.

```bash
python -m pymsgprompt.version
```

## Platform Supports

This is a cross platform module and supported both in python 2 and 3.

## Installation

To install this module you can use clone with git or just simply run pip install command.

### Using git

```bash
git clone https://github.com/antaripchatterjee/PyMsgPrompt.git
cd PyMsgPrompt
python setup.py install
```

### Using pip

```bash
pip install pymsgprompt
```

## Uninstallation

Uninstallation can be done by running pip uninstall command.

```bash
pip uninstall pymsgpropmt
```

## Usage

To test this module, you can run the below simple code.

```python
from pymsgprompt.prompt import ask, log
import time
if __name__ == '__main__':
    answer = ask('Do you want to close?', choices=['yes', 'no', 'yesss'], default='no', timestamp=True, regexp=True, ignore_case=False)
    # with open('test.txt', 'w') as test:
    #     print (log('Answer is %s'%answer, logtype='error', timestamp=True, file=test))
    if answer.startswith('n'):
        log('Answer is %s'%answer, logtype='error', timestamp=False, reset=True)
    else:
        log('Answer is %s'%answer, logtype='info', timestamp=False, reset=True)
    for i in range(1000, 0, -1):
        log('The message is %d'%i, timestamp=True, end=None)
        time.sleep(0.01)
```

Below is the output,

```output
[QUES] 2020-Oct-13 23:52:03: Do you want to close? (yesss/ no/ yes)[no]
no
Answer is no
[INFO] 2020-Oct-13 23:52:16: The message is 1
```

## API Reference

A good documentation, specially for the developers, will be provided later.

## Development Areas

I am already working on some other functionalities, which will be provided in the future releases.

## License

This module is licensed under [MIT License](https://github.com/antaripchatterjee/PyMsgPrompt/blob/master/LICENSE).

## Contribution

Pull requests are always awesome, but please make sure of raising request, before making any changes.