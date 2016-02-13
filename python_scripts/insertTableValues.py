"""
Usage:
  insertTableValues.py <file_to_download> <bucket_name> <s3_keyname>

"""
from boto.s3.connection import S3Connection
import time
import os
from optparse import OptionParser
import csv
import boto.dynamodb


def getFromS3(bucket_name, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID, transfer_file, s3_keyname):
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID)
	mybucket = conn.get_bucket(bucket_name)
	k = mybucket.get_key(s3_keyname)
	print 'Retrieving file %s...' % s3_keyname
	start = time.time()
	k.get_contents_to_filename(transfer_file)
	size = os.stat(transfer_file).st_size
	size = float(size)/1024/1024
	print 'File size: %.2f MB. Time to retrieve: %.2f seconds' % (size, (time.time() - start))
	insertToDynamoDB(transfer_file, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID)

def insertToDynamoDB(transfer_file, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID):
	conn = boto.dynamodb.connect_to_region('us-west-2',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_ACCESS_SECRET_ID)
	table = conn.get_table('popgrowth')
    
	print "Inserting items from csv file..."
	with open(transfer_file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader)
		for row in reader:
			statename=row[5]
			countyname=row[6]
			popest2010=int(row[9])
			popest2011=int(row[10])
			print statename
			item_data = {
				'popestimate2010':popest2010,
				'popestimate2011':popest2011,
			}
			item = table.new_item(
				hash_key =statename,
				range_key =countyname,
				attrs=item_data
			)
			item.put()
		
	print "Inserted items to DynamoDB successfully...!!!"
	
	
def main(transfer_file, bucket_name, s3_keyname):
	AWS_ACCESS_KEY_ID = '***************' # Put your access key here
	AWS_ACCESS_SECRET_ID = '**************' # Put your secret key here
	getFromS3(bucket_name, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID, transfer_file, s3_keyname)

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    main(*args)		