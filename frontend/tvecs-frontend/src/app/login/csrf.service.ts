import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class CsrfService {
  getCookie(name: string): string | null {
    const nameEQ = name + '=';
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  getCsrfToken(): string | null {
    return this.getCookie('csrftoken');
  }
}
