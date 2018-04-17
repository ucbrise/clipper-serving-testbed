# clipper-serving-testbed

Scripts for setting up a long-running Clipper cluster for stress testing and other purposes. Currently trains a model on Criteo's 2014 display advertising dataset and deploys it to Clipper. The specific model is [LIBFFM](https://github.com/guestwalk/libffm), the first place winner of the Kaggle competition with this dataset. The testbed is currently running on a GCP instance on Kubernetes with Redis configured to run externally in fault-tolerant mode.

If you want to set this up on a new computer, run the following:
```
$ python start-clipper.py clipper-server-IP redis-service-IP # starts a Clipper instance
$ python train-dataset.py path-to-dataset clipper-server-IP redis-service-IP # run periodically to train model and deploy it to Clipper
$ ./start-client.sh # start client to query Clipper at a Poisson rate
```

[Design Doc](https://docs.google.com/document/d/13HZvSnTj6trosyv4SenoHLj9fcoGPdzgGBOff14arTw/edit?usp=sharing)
