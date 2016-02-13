"""
Usage:
  upload.py <file_to_transfer> <bucket_name> <s3_keyname>

"""
from boto.s3.connection import S3Connection
import time
import os
from optparse import OptionParser


def upload(bucket_name, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID, transfer_file, s3_keyname):
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID)
	mybucket = conn.get_bucket(bucket_name)
	k = mybucket.new_key(s3_keyname)
	size = os.stat(transfer_file).st_size
	size = float(size)/1024/1024
	print 'Uploading file %s...' % transfer_file
	start = time.time()
	k.set_contents_from_filename(transfer_file)
	k.set_acl('private')
	print 'File size: %.2f MB. Time to upload: %.2f seconds' % (size, (time.time() - start)) 

def main(transfer_file, bucket_name, s3_keyname):
	AWS_ACCESS_KEY_ID = '************'; # Put your access key here
    AWS_ACCESS_SECRET_ID = '************'; # Put your secret key here
	upload(bucket_name, AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_ID, transfer_file, s3_keyname)

if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    main(*args)		