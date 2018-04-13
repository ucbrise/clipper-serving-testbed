from clipper_admin import ClipperConnection, KubernetesContainerManager
from clipper_admin.deployers import python as python_deployer
import requests, json, numpy as np
import time

clipper_conn = ClipperConnection(
    KubernetesContainerManager("https://35.197.66.133", useInternalIP=True))

clipper_conn.connect()
addr = clipper_conn.get_query_addr()
headers = {"Content-type": "application/json"}

# sample from 5 arbitrary valid feature vectors

possible_data = [
"27,17,45,28,2,28,27,29,28,1,1,,23,68fd1e64,960c983b,9fbfbfd5,38c11726,25c83c98,7e0ccccf,fe06fd10,062b5529,a73ee510,ca53fc84,67360210,895d8bbb,4f8e2224,f862f261,b4cc2435,4c0041e5,e5ba7672,b4abdd09,21ddcdc9,5840adea,36a7ab86,,32c7478e,85e4d73f,010f6491,ee63dd9b",
"1,1,19,7,1,3,1,7,7,1,1,,2,09ca0b81,8947f767,a87e61f7,c4ba2a67,25c83c98,7e0ccccf,ce6020cc,062b5529,a73ee510,b04d3cfe,70dcd184,899eb56b,aca22cf9,b28479f6,a473257f,88f592e4,d4bb7bd8,bd17c3da,1d04f4a4,a458ea53,82bdc0bb,,32c7478e,5bdcd9c4,010f6491,cca57dcc",
"8,11,38,9,316,25,8,11,10,1,1,,9,05db9164,09e68b86,aa8c1539,85dd697c,25c83c98,7e0ccccf,bc252bd0,5b392875,a73ee510,ef5c0d3c,0bd0c3b3,d8c29807,c0e6befc,8ceecbc8,d2f03b75,c64d548f,e5ba7672,63cdbb21,cf99e5de,5840adea,5f957280,,55dd3565,1793a828,e8b83407,b7d9c3bc",
",4,13,20,17700,,0,20,1,,0,,20,68fd1e64,08d6d899,9143c832,f56b7dd5,0942e0a7,7e0ccccf,e88f1cec,0b153874,a73ee510,3b08e48b,8f410860,ae1bb660,b8eec0b1,b28479f6,bffbd637,bad5ee18,776ce399,bbf70d82,,,0429f84b,,be7c41b4,c0d61a5c,,",
"16,18,5203,8,0,0,4,49,10,0,1,,0,05db9164,9f7e1d07,0253bbf5,d6420627,4cf72387,,0db090eb,0b153874,a73ee510,3b08e48b,10e6a64f,31adfaee,38b5339a,07d13a8f,3e25e5f5,1621c7f4,e5ba7672,6a58e423,21ddcdc9,5840adea,bcc7a461,,32c7478e,3214afd4,ea9a246c,e7ecb821"
]

fh = open('predictions.log', 'w')
while(True):
    # poisson process with rate 0.1
    interarrival_time = np.random.exponential(scale=10)
    time.sleep(interarrival_time)
    num_requests = int(np.random.random() * 10) + 1 # uniform between 1 and 10
    input = list()
    for _ in range(num_requests):
        input.append(possible_data[int(np.random.random() * 5)])
    # query clipper
    res = requests.post(
        "http://%s/testbed/predict" % addr,
        headers=headers,
        data=json.dumps({"input_batch": input})).json()
    print(res)
    fh.write(json.dumps(res))

fh.close()

