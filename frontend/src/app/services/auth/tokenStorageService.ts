import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class TokenStorage {
  private accessKey = 'access_token';
  private refreshKey = 'refresh_token';

  get token(): string | null {
    return localStorage.getItem(this.accessKey);
  }
  setAccessToken(token: string) {
    localStorage.setItem(this.accessKey, token);
  }
  setRefreshToken(token: string) {
    localStorage.setItem(this.refreshKey, token);
  }
  clear() {
    localStorage.removeItem(this.accessKey);
  }
}
