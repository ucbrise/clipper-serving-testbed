#!/bin/bash

gcloud container clusters get-credentials redis-cluster
kubectl cluster-info
