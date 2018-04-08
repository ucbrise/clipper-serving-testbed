# clipper-serving-testbed

Scripts for setting up a long-running Clipper cluster for stress testing and other purposes. Currently trains a model on Criteo's 2014 display advertising dataset and deploys it to Clipper. The specific model is [LIBFFM](https://github.com/guestwalk/libffm), the first place winner of the Kaggle competition with this dataset. The testbed is currently running on a GCP instance on Kubernetes with Redis configured to run externally in fault-tolerant mode. 

[Design Doc](https://docs.google.com/document/d/13HZvSnTj6trosyv4SenoHLj9fcoGPdzgGBOff14arTw/edit?usp=sharing)
