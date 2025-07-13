import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CsrfService } from './csrf.service';

@Injectable()
export class CsrfInterceptor implements HttpInterceptor {
  constructor(private csrfService: CsrfService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Add CSRF token to all requests including login
    const csrfToken = this.csrfService.getCsrfToken();
    if (csrfToken) {
      const cloned = req.clone({
        headers: req.headers.set('X-CSRFToken', csrfToken),
        withCredentials: true,
      });
      return next.handle(cloned);
    } else {
      return next.handle(req);
    }
  }
}
