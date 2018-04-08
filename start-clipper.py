#!/usr/bin/env python
# Start long-lived Clipper cluster
import sys
from clipper_admin import ClipperConnection, KubernetesContainerManager
from clipper_admin.deployers import python as python_deployer

if len(sys.argv) != 3:
    print('Usage: python start-clipper.py clipper-cluster-IP redis-cluster-IP')
    print("For example, python start-clipper.py 35.185.255.223 35.197.66.133")
    sys.exit(1)

clipper_ip = 'https://' + sys.argv[1]
redis_ip = 'https://' + sys.argv[2]

clipper_conn = ClipperConnection(
    KubernetesContainerManager(clipper_ip, redis_ip))
try:
    clipper_conn.stop_all()
    clipper_conn.stop_all_model_containers()
    clipper_conn.start_clipper()
    clipper_conn.register_application(
        name="testbed",
        input_type="strings",
        default_output="-1.0",
        slo_micros=100000)
    clipper_conn.get_all_apps()
except Exception as e:
    print(e)
