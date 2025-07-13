import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-logs',
  standalone: false,
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.css']
})
export class LogsComponent implements OnInit {
  logs: any[] = [];
  errorMessage: string = '';

  expandedLogId: number | null = null; // Track expanded row

  // Filter input properties
  filterBodyNo: string = '';
  filterStartDateTime: string = '';
  filterEndDateTime: string = '';
  filterTotalResult: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchLogs();
  }

  fetchLogs() {
    // Build query params based on filter inputs
    const params: any = {};
    if (this.filterBodyNo) {
      params['body_no'] = this.filterBodyNo;
    }
    if (this.filterStartDateTime) {
      params['start_date_time'] = this.filterStartDateTime;
    }
    if (this.filterEndDateTime) {
      params['end_date_time'] = this.filterEndDateTime;
    }
    if (this.filterTotalResult) {
      params['total_result'] = this.filterTotalResult;
    }

    this.http.get<any[]>('http://localhost:8000/api/logs/', { params: params, withCredentials: true })
      .subscribe({
        next: (data) => {
          this.logs = data;
          this.expandedLogId = null; // Collapse any expanded row on new data load
        },
        error: (error) => {
          this.errorMessage = 'Failed to load logs. Please login first.';
        }
      });
  }

  clearFilters(): void {
    this.filterBodyNo = '';
    this.filterStartDateTime = '';
    this.filterEndDateTime = '';
    this.filterTotalResult = '';
    this.fetchLogs();
  }

  downloadFile(filePath: string) {
    const url = `http://localhost:8000/api/download-file/?file_path=${encodeURIComponent(filePath)}`;
    this.http.get(url, { responseType: 'blob', withCredentials: true }).subscribe({
      next: (blob) => {
        const a = document.createElement('a');
        const objectUrl = URL.createObjectURL(blob);
        a.href = objectUrl;
        a.download = filePath.split('/').pop() || 'file.csv';
        a.click();
        URL.revokeObjectURL(objectUrl);
      },
      error: (error) => {
        this.errorMessage = 'Failed to download file.';
      }
    });
  }

  toggleRow(logId: number) {
    if (this.expandedLogId === logId) {
      this.expandedLogId = null;
    } else {
      this.expandedLogId = logId;
    }
  }
}
