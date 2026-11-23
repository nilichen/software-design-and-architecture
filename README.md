# Software Design and Architecture — example code

Example code for the video series **Software Design and Architecture** (YouTube · CatDataING): unofficial study notes on software design, retold with a made-up car-rental app.

Each folder is one small app, shown as one diff: a commit with the app as it starts (it works, but has the problems the video talks about), then a commit applying the video's fixes. The folder's README links that diff (open it with *Split* for side by side) and lists what changed and why.

| Folder | Video |
|---|---|
| [`clean-code/inheritance-vs-composition/`](clean-code/inheritance-vs-composition/) | Clean Code \| Inheritance vs Composition |
| [`clean-code/cohesion-and-coupling/`](clean-code/cohesion-and-coupling/) | Clean Code \| Cohesion, Coupling and Where the Data Lives |
| [`clean-code/abstractions-and-factories/`](clean-code/abstractions-and-factories/) | Clean Code \| Abstractions, Factories, DRY, KISS, YAGNI |
| [`clean-code/script-to-project/`](clean-code/script-to-project/) | Clean Code \| From Script to Project |
| [`clean-code/reviewing-ai-code/`](clean-code/reviewing-ai-code/) | Clean Code \| Reviewing AI-Written Code |

Python 3.12+, standard library only. Run an app from its folder (its README gives the command, usually `python3 main.py`); run the tests with `uvx pytest`.

Licence: MIT.
