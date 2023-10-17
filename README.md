# jaybirds
Codebase for the EN.605.601 (Foundations of Software Engineering) group project. This repo contains an implementation of the board game "Clue" that can be played by multiple people in the browser. Implementation details TBD.

# Setup

1. Create conda environment [SKIP if already done]

```bash
conda create -n "jaybirds" python=3.10
```

2. Activate conda environment

```bash
conda activate jaybirds
```

2. Pip install required python packages [SKIP if already done]

```bash
pip install -r requirements.txt
```

> If you run into SSL errors, run `pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt`

3. Run main file

```bash
python code/clue.py
```

4. Open the hosted http address on a browser

For example:

```
 * Running on http://127.0.0.1:5000
```

5. It will prompt you for your username and password. Get valid pairs in `jaybirds/code/credentials.json`.

6. Enter your name and game ID. 

7. Hit `Join Game` or `Create Game`.

8. Select your player out of the six options.