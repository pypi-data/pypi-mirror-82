class AzureVM(object):

    """Accessible nested properties about a Microsoft Azure VM

    Returns:
        AzureVM: Returns a AzureVM object and properties about a Azure VM
    """
    __AZ_METRICS = None

    @property
    def details(self):
        """Access details about a Microsoft Azure VM

        Returns:
            AzureVMDetails: Returns a AzureVMDetails object containing properties details about a Azure VM
        """
        from .azurevmdetails import AzureVMDetails
        return AzureVMDetails()

    @property
    def metrics(self):
        """Metrics related to a random Azure VM

        Returns:
            AzureVMMetrics: Returns an object containing properties to access metrics related to an Azure VM
        """
        from .azurevmmetrics import AzureVMMetrics
        return AzureVMMetrics()
