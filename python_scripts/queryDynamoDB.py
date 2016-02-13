import csv
import boto.dynamodb
from boto.dynamodb.condition import BEGINS_WITH
from boto.s3.connection import S3Connection
from heapq import nlargest
from operator import itemgetter

AWS_ACCESS_KEY_ID = '************'; # Put your access key here
AWS_ACCESS_SECRET_ID = '************'; # Put your secret key here
REGION = '*******'; # Put your dynamodb region here e.g. us-west-2

conn = boto.dynamodb.connect_to_region(REGION,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_ACCESS_SECRET_ID)

table = conn.get_table('popgrowth')

statelist = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


with open('visualize.csv', 'wb') as f:
	writer = csv.writer(f, delimiter=',')
	writer.writerow(['STATE', '%POPGROWTH'])

x = {}

for state in statelist:
	print state
	total2010 = 0
	total2011 = 0

	statedata = table.query(hash_key=state)
	for res in statedata:
		total2010 = total2010 + res['popestimate2010']
		total2011 = total2011 + res['popestimate2011']
		
	
	popgrowth = ((float(total2011)-float(total2010))/float(total2010))*100
	popgrowth = "%.2f" % popgrowth
	print "Population growth percent: ",popgrowth
		
	x.update({state:popgrowth})
		
	with open('visualize.csv', 'a') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow([state, popgrowth])
		

with open('top10.csv', 'wb') as f:
	writer = csv.writer(f, delimiter=',')
	writer.writerow(['STATE', '%POPGROWTH'])
	
for name, score in nlargest(10, x.iteritems(), key=itemgetter(1)):
	with open('top10.csv', 'a') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow([name, score])

# Uploading processed files to S3

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID)
mybucket = conn.get_bucket('mycensusdata')
k = mybucket.new_key('visualize.csv')
print 'Uploading file visualize.csv to S3...'
k.set_contents_from_filename('visualize.csv')
k.set_acl('public-read')
print 'Uploaded successfully!'


k = mybucket.new_key('top10.csv')
print 'Uploading file top10.csv to S3...'
k.set_contents_from_filename('top10.csv')
k.set_acl('public-read')
print 'Uploaded successfully!'