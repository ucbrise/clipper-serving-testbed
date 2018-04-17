#!/usr/bin/env python
import time
import sys
import os
from clipper_admin import ClipperConnection, KubernetesContainerManager
from clipper_admin.deployers import python as python_deployer
import six
from cloudpickle import CloudPickler

if len(sys.argv) != 4:
    print("Usage: python train-dataset.py dataset_file_path clipper-cluster-IP redis-cluster-IP")
    print("For example, python train-dataset.py dataset/tr.csv 35.197.66.133 10.59.247.82")
    sys.exit(1)

redis_ip = 'https://' + sys.argv[3]
clipper_ip = 'https://' + sys.argv[2]
dataset = sys.argv[1]

# train model on dataset
print('TRAINING...')
#os.system('cp -f ' + dataset + ' kaggle/tr.csv')
#os.system('cd kaggle')
#os.system('cd kaggle && python run.py')

# after training, move model to appropriate location
#os.system('mv kaggle/model docker/lib/')

# declare prediction function
def libffm(xs):
    # create csv according to Criteo dataset format
    import os
    os.system('chmod a+x /model/*.py')
    os.chdir('/model')
    os.system('echo "Id,Label,I1,I2,I3,I4,I5,I6,I7,I8,I9,I10,I11,I12,I13,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26" > te.csv')
    i = 0
    for x in xs:
        os.system('echo ' + str(i) + ',0,' + x + ' >> te.csv')
        i += 1
    # process and predict - inspired by kaggle/run.py
    os.system('/model/parallelizer-a.py -s 1 /model/pre-a.py te.csv te.gbdt.dense te.gbdt.sparse')
    os.system('/model/gbdt -t 30 -s 1 te.gbdt.dense te.gbdt.sparse te.gbdt.dense te.gbdt.sparse te.gbdt.out te.gbdt.out')
    os.system('rm -f te.gbdt.dense te.gbdt.sparse')
    os.system('/model/parallelizer-b.py -s 1 /model/pre-b.py te.csv te.gbdt.out te.ffm')
    os.system('rm te.gbdt.out')
    os.system('/model/ffm-predict te.ffm /model/model te.out')
    os.system('/model/calibrate.py te.out te.out.cal')
    os.system('/model/make_submission.py te.out.cal submission.csv')
    # turn into predictions
    with open('submission.csv') as fh:
        lines = fh.readlines()[1:] # ignore first line
    preds = [line.strip().split(',')[1] for line in lines]
    return preds

# pickle function and write to appropriate location
s = six.StringIO()
c = CloudPickler(s, 2)
c.dump(libffm)
serialized_prediction_function = s.getvalue()
filepath = 'docker/lib/func.pkl'
with open(filepath, 'w') as fh:
    fh.write(serialized_prediction_function)

# refresh creds
os.system('gcloud container clusters get-credentials redis-cluster')
os.system('kubectl cluster-info')

clipper_conn = ClipperConnection(KubernetesContainerManager(clipper_ip, useInternalIP=True))
clipper_conn.connect()

# Build model and deploy to clipper
version = int(time.time())
clipper_conn.build_and_deploy_model('ffm', version, 'strings', 'docker/lib', 'clipper/python-closure-container:develop', container_registry='ryanhoque')
# Uncomment the following if first time
#clipper_conn.link_model_to_app(app_name="testbed", model_name="ffm") 

# finally deploy new version of model to clipper (set version as timestamp)
print('Successfully deployed model ffm version ' + str(version) + ' to Clipper.')
