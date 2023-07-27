import boto3

def get_rds_instances():
    # Replace 'your_aws_region' with the AWS region where your RDS instances are located
    client = boto3.client('rds', region_name='your_aws_region')

    instances_list = []
    multi_az_count = 0
    mariadb_count = 0
    mysql_count = 0
    postgres_count = 0
    mariadb_multi_az = 0
    mysql_multi_az = 0
    postgres_multi_az = 0
    instance_classes = {}

    try:
        response = client.describe_db_instances()
        db_instances = response['DBInstances']

        for instance in db_instances:
            instance_class = instance['DBInstanceClass']
            engine = instance['Engine']
            multi_az = instance['MultiAZ']

            instances_list.append({
                'instance_id': instance['DBInstanceIdentifier'],
                'instance_class': instance_class,
                'database_type': engine,
                'multi_az': multi_az
            })

            instance_classes.setdefault(engine, {}).setdefault(multi_az, set()).add(instance_class)

            if multi_az:
                multi_az_count += 1

            if engine == 'mariadb':
                mariadb_count += 1
                if multi_az:
                    mariadb_multi_az += 1
            elif engine == 'mysql':
                mysql_count += 1
                if multi_az:
                    mysql_multi_az += 1
            elif engine == 'postgres':
                postgres_count += 1
                if multi_az:
                    postgres_multi_az += 1

    except Exception as e:
        print("Error retrieving RDS instances:", e)

    return instances_list, multi_az_count, mariadb_count, mariadb_multi_az, mysql_count, mysql_multi_az, postgres_count, postgres_multi_az, instance_classes

def print_instance_classes(engine, classes):
    print(f"{engine.capitalize()}:")
    for multi_az, class_list in classes.items():
        print(f"  {'Multi-AZ' if multi_az else 'Single-AZ'}:")
        for instance_class in class_list:
            print(f"    {instance_class}: {sum(1 for instance in rds_instances if instance['instance_class'] == instance_class and instance['database_type'] == engine and instance['multi_az'] == multi_az)}")

if __name__ == "__main__":
    rds_instances, multi_az_count, mariadb_count, mariadb_multi_az, mysql_count, mysql_multi_az, postgres_count, postgres_multi_az, instance_classes = get_rds_instances()
    total_instances = len(rds_instances)

    print(f"Total RDS Instances: {total_instances}")
    print(f"Total Multi-AZ Instances: {multi_az_count}")
    print(f"Total MariaDB Instances: {mariadb_count}")
    print(f"Total MySQL Instances: {mysql_count}")
    print(f"Total PostgreSQL Instances: {postgres_count}")
    print("---------------")

    print(f"MariaDB Multi-AZ Instances: {mariadb_multi_az}")
    print(f"MySQL Multi-AZ Instances: {mysql_multi_az}")
    print(f"PostgreSQL Multi-AZ Instances: {postgres_multi_az}")
    print("---------------")

    print("Instance Classes:")
    for engine, classes in instance_classes.items():
        print_instance_classes(engine, classes)
