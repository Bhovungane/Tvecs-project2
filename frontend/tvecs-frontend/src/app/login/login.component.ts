import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    this.errorMessage = '';
    this.http.post<any>('http://localhost:8000/api/login/', { username: this.username, password: this.password }, { withCredentials: true })
      .subscribe({
        next: (response) => {
          console.log('Login response:', response);
          if (response.message === 'Login successful') {
            this.router.navigate(['/logs']);
          } else {
            if (response.message === 'User is not staff') {
              this.errorMessage = 'Access denied: You must be a staff member to log in.';
            } else {
              this.errorMessage = response.message;
            }
          }
        },
        error: (error) => {
          console.log('Login error:', error);
          if (error.status === 401) {
            this.errorMessage = 'Invalid credentials';
          } else if (error.status === 403) {
            this.errorMessage = 'Access denied: You must be a staff member to log in.';
          } else {
            this.errorMessage = 'Login failed. Please try again.';
          }
        }
      });
  }
}
