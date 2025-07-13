from django.db import models

class QualityLog(models.Model):
    body_no = models.IntegerField()
    device_id = models.CharField(max_length=50)
    total_result = models.CharField(max_length=10)
    date_time = models.DateTimeField()
    assembly_no = models.CharField(max_length=50, null=True, blank=True)
    vin_no = models.CharField(max_length=50, null=True, blank=True)
    vehicle_code = models.CharField(max_length=50, null=True, blank=True)
    frame_type = models.CharField(max_length=50, null=True, blank=True)
    frame_no = models.CharField(max_length=50, null=True, blank=True)
    vehicle_id = models.CharField(max_length=10, null=True, blank=True)
    work_group = models.CharField(max_length=255, null=True, blank=True)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return str(self.body_no)

class Defect(models.Model):
    quality_log = models.ForeignKey(QualityLog, on_delete=models.CASCADE, related_name='defects')
    defect_description = models.CharField(max_length=255)
    error_code = models.CharField(max_length=100, null=True, blank=True)
    error_value = models.CharField(max_length=50, null=True, blank=True)
    cvqs_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.defect_description
