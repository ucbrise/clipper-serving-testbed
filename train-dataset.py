#!/usr/bin/env python

import sys
import os
from clipper_admin import ClipperConnection, KubernetesContainerManager
from clipper_admin.deployers import python as python_deployer

if len(sys.argv) != 4:
    print("Usage: python train-dataset.py dataset_file_path clipper-cluster-IP redis-cluster-IP")
    print("For example, python train-dataset.py dataset/tr.csv 35.185.255.223 35.197.66.133")
    sys.exit(1)

redis_ip = 'https://' + sys.argv[3]
clipper_ip = 'https://' + sys.argv[2]
dataset = sys.argv[1]

# train model on dataset
os.system('cp -f ' + dataset + ' kaggle/tr.csv')
os.system('cd kaggle')
os.system('python run.py')

# after training, deploy to clipper and build custom docker image
os.system('cd ..')
os.system('mv kaggle/model lib/')
os.system('docker build -t libffm dockerfiles/LIBFFMDockerfile')
clipper_conn = ClipperConnection(KubernetesContainerManager(clipper_ip, redis_ip))
clipper_conn.connect()

# model python closure to deploy to clipper
def libffm(xs):
    # create csv according to Criteo dataset format
    os.system('echo "Id,Label,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12,I13,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26" > te.csv')
    i = 0
    for x in xs:
        os.system('echo ' + str(i) + ',0,' + ",".join(x) + ' >> te.csv')
        i += 1
    # process and predict - inspired by kaggle/run.py
    os.system('/container/parallelizer-a.py -s 1 /container/pre-a.py te.csv te.gbdt.dense te.gbdt.sparse')
    os.system('/container/gbdt -t 30 -s 1 te.gbdt.dense te.gbdt.sparse te.gbdt.dense te.gbdt.sparse te.gbdt.out te.gbdt.out')
    os.system('rm -f te.gbdt.dense te.gbdt.sparse')
    os.system('/container/parallelizer-b.py -s 1 /container/pre-b.py te.csv te.gbdt.out te.ffm')
    os.system('rm te.gbdt.out')
    os.system('/container/ffm-predict te.ffm /container/model te.out')
    os.system('/container/calibrate.py te.out te.out.cal')
    os.system('/container/make_submission.py te.out.cal submission.csv')
    # turn into predictions
    with open('te.csv') as fh:
        lines = fh.readlines()[1:] # ignore first line
    preds = [line.strip().split(',')[1] for line in lines]
    return preds

# finally deploy new version of model to clipper (set version as timestamp)
python_deployer.deploy_python_closure(
    clipper_conn,
    name="ffm",
    base_image="libffm",
    version=int(time.time()),
    input_type="strings",
    registry='ryanhoque',
    func=libffm)
clipper_conn.link_model_to_app(
    app_name="testbed", model_name="ffm")
