from django.core.management.base import BaseCommand
from logs.models import QualityLog, Defect
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Add sample QualityLog and Defect entries for testing'

    def handle(self, *args, **kwargs):
        # Clear existing logs and defects
        Defect.objects.all().delete()
        QualityLog.objects.all().delete()

        # Create sample logs
        for i in range(1, 6):
            log = QualityLog.objects.create(
                body_no=i,
                device_id=f'Device-{i}',
                total_result=random.choice(['Pass', 'Fail']),
                date_time=timezone.now(),
                assembly_no=f'Assembly-{i}',
                vin_no=f'VIN{i:05d}',
                vehicle_code=f'Code-{i}',
                frame_type=f'Type-{i}',
                frame_no=f'Frame-{i}',
                vehicle_id=f'VID{i}',
                work_group=f'Group-{i}',
                file_path=f'/path/to/file{i}.jpg'
            )
            # Add defects to some logs
            for j in range(random.randint(0, 3)):
                Defect.objects.create(
                    quality_log=log,
                    defect_description=f'Defect description {j+1} for log {i}',
                    error_code=f'ERR{j+1}',
                    error_value=str(random.randint(1, 100)),
                    cvqs_id=f'CVQS-{i}-{j+1}'
                )
        self.stdout.write(self.style.SUCCESS('Sample logs and defects added successfully.'))
