# Refresh kube creds & connect to clipper.
from clipper_admin import ClipperConnection, KubernetesContainerManager
import os
os.system('gcloud container clusters get-credentials redis-cluster')
os.system('kubectl cluster-info')
clipper_conn = ClipperConnection(
    KubernetesContainerManager("https://35.197.66.133", useInternalIP=True))
clipper_conn.connect()
