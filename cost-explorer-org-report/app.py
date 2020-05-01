import boto3
import datetime
import os
import re
import time
from operator import itemgetter

# set up connections with the cost explorer api and s3 api
c = boto3.client('ce')
s = boto3.client('s3')
n = boto3.client('ses')


def lambda_handler(event, context):
    # get the timestamps for today as the end date for the report and the

    days2report = int(os.environ['days'])

    endd = datetime.datetime.now()                       # today
    tomod = endd + datetime.timedelta(days=1)            # tomorrow
    yestd = endd - datetime.timedelta(days=1)            # yesterday
    startd = endd - datetime.timedelta(days=days2report)

    # run a query against the cost api to retrieve the cost and usage reports. since the query is done exclusive of the last day, we run it for tomorrow
    z = c.get_cost_and_usage(TimePeriod={'Start': startd.strftime("%Y-%m-%d"), 'End': tomod.strftime("%Y-%m-%d")}, GroupBy=[
                             {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], Granularity='DAILY', Metrics=['AmortizedCost'])

    # iterate of the dates returned
    fname = '/tmp/cost-report-' + endd.strftime('%Y-%m-%d') + '.csv'
    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))

    # create the headers for the csv file in a list
    csvf = ['date,acc,svc,amortizedCost']

    for x in z['ResultsByTime']:
        # per record entry, retrieve the date, itemname and daily total cost
        for y in x['Groups']:
            dat = x['TimePeriod']['Start']
            acc = y['Keys'][0]
            svc = y['Keys'][1]
            cost = y['Metrics']['AmortizedCost']['Amount']
            citem = dat+','+acc+','+svc+','+str(cost)
            csvf.append(citem.strip())

        # open a file on the '/tmp' disk and write the report
        tmp = open(fname, 'w')
        for item in csvf:
            tmp.write(item+'\n')
        tmp.close()

    print('saving output to: ' + os.environ['bucket'] + '/' + fname[5:])
    s.put_object(Bucket=os.environ['bucket'], Body=open(
        fname, 'rb'), Key=fname[5:], ContentType='text/plain')
