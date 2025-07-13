from rest_framework import serializers
from .models import QualityLog, Defect

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = ['defect_description', 'error_code', 'error_value', 'cvqs_id']

class QualityLogSerializer(serializers.ModelSerializer):
    defects = DefectSerializer(many=True, read_only=True)

    class Meta:
        model = QualityLog
        fields = ['id', 'body_no', 'device_id', 'total_result', 'date_time', 'assembly_no', 'vin_no', 'vehicle_code', 'frame_type', 'frame_no', 'vehicle_id', 'work_group', 'file_path', 'defects']
