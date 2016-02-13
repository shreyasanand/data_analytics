import boto.dynamodb

AWS_ACCESS_KEY_ID = '************'; # Put your access key here
AWS_ACCESS_SECRET_ID = '************'; # Put your secret key here
REGION = '*******'; # Put your dynamodb region here e.g. us-west-2

conn = boto.dynamodb.connect_to_region(REGION,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_ACCESS_SECRET_ID)

print "Defining schema..."
popgrowth_table_schema = conn.create_schema(
	hash_key_name='state',
	hash_key_proto_value=str,
	range_key_name='county',
	range_key_proto_value=str
)

print "Creating table..."
table = conn.create_table(
	name='popgrowth',
	schema=popgrowth_table_schema,
	read_units=10,
	write_units=5
)
	
conn.list_tables()
print "Created table successfully..!"