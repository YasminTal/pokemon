import boto3
import os


# ---------- SETTINGS ----------
KEY_PAIR_NAME = 'vockey'
PEM_FILE = f'C:/Users/talts/Yasmin/bash/python/pokemon/Deploy/{KEY_PAIR_NAME}.pem'
INSTANCE_TYPE = 't2.micro'
REGION = 'us-west-2'  # Change if you're using a different region
# Latest Amazon Linux 2 AMI for u
AMI_ID = 'ami-0892d3c7ee96c0bf7'
USER_DATA_FILE = 'C:/Users/talts/Yasmin/bash/python/pokemon/Deploy/user-data.sh'
# -------------------------------

#  Read user-data script
with open(USER_DATA_FILE, 'r') as file:
    user_data_script = file.read()


# 1. Create EC2 client and resource
ec2_client = boto3.client('ec2', region_name=REGION)
ec2_resource = boto3.resource('ec2', region_name=REGION)

# # 2. Create Key Pair (if it doesn't exist)
try:
    key_pair = ec2_client.create_key_pair(KeyName=KEY_PAIR_NAME)
    with open(PEM_FILE, 'w') as file:
        file.write(key_pair['KeyMaterial'])
    os.chmod(PEM_FILE, 0o400)
    print(f"✅ Key pair created and saved to {PEM_FILE}")
except ec2_client.exceptions.ClientError as e:
    if "InvalidKeyPair.Duplicate" in str(e):
        print(f"ℹ️ Key pair '{KEY_PAIR_NAME}' already exists. Skipping creation.")
    else:
        raise e


# Get default VPC and default SG
default_vpc = ec2_client.describe_vpcs(Filters=[
    {'Name': 'isDefault', 'Values': ['true']}
])['Vpcs'][0]['VpcId']

default_sg = ec2_client.describe_security_groups(
    Filters=[
        {'Name': 'vpc-id', 'Values': [default_vpc]},
        {'Name': 'group-name', 'Values': ['default']}
    ]
)['SecurityGroups'][0]

default_sg_id = default_sg['GroupId']

# Make sure port 22 is open to all IPs
has_ssh_rule = any(
    rule.get('FromPort') == 22 and rule.get('ToPort') == 22 and
    any(ip.get('CidrIp') == '0.0.0.0/0' for ip in rule.get('IpRanges', []))
    for rule in default_sg.get('IpPermissions', [])
)

if not has_ssh_rule:
    ec2_client.authorize_security_group_ingress(
        GroupId=default_sg_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
    )
    print("✅ Opened port 22 (SSH) to all IPs in default security group")
else:
    print("ℹ️ Port 22 already open to 0.0.0.0/0 in default SG")

# 3. Launch EC2 Instance
print("🚀 Launching EC2 instance...")
instances = ec2_resource.create_instances(
    ImageId=AMI_ID,
    InstanceType=INSTANCE_TYPE,
    KeyName=KEY_PAIR_NAME,
    MinCount=1,
    MaxCount=1,
    UserData=user_data_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'pokemon-ec2'}]
        }
    ]
)

instance = instances[0]
print(f"⏳ Waiting for instance {instance.id} to be running...")
instance.wait_until_running()
instance.reload()

# 4. Output ssh info
print(f"✅ Instance {instance.id} is running.")
print(f"🌐 Public IP: {instance.public_ip_address}")
print(f"💡 Connect with:\nssh -i {PEM_FILE} ec2-user@{instance.public_ip_address}")