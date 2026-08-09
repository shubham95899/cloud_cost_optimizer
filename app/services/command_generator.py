def generate_action(resource, category):
    provider = resource.provider.lower()
    rid = resource.resource_id
    region = resource.region

    if provider == "aws" and category == "orphaned_storage":
        cli = f"aws ec2 delete-volume --volume-id {rid}" + (f" --region {region}" if region else "")
        api = "boto3.client('ec2').delete_volume(VolumeId=resource_id)"
        return cli, api

    if provider == "aws" and category in {"idle_compute", "stopped_compute"}:
        cli = f"aws ec2 terminate-instances --instance-ids {rid}" + (f" --region {region}" if region else "")
        api = "boto3.client('ec2').terminate_instances(InstanceIds=[resource_id])"
        return cli, api

    if provider == "azure" and category == "orphaned_storage":
        cli = f"az disk delete --ids {rid} --yes"
        api = "azure.mgmt.compute.ComputeManagementClient(...).disks.begin_delete(resource_group_name, disk_name)"
        return cli, api

    if provider == "azure" and category in {"idle_compute", "stopped_compute"}:
        cli = f"az vm delete --ids {rid} --yes"
        api = "azure.mgmt.compute.ComputeManagementClient(...).virtual_machines.begin_delete(resource_group_name, vm_name)"
        return cli, api

    return None, None
