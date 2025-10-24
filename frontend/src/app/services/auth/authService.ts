import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { TokenStorage } from './tokenStorageService';
import { catchError, map, Observable, tap, throwError } from 'rxjs';
import { API_BASE_URL } from '../../config/apiBaseUrlToken';
import { API_ROUTES } from '../../utils/apiRoutes';

interface RegisterRequest {
  username: string;
  password: string;
}
interface LoginRequest {
  username: string;
  password: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private store = inject(TokenStorage);
  private apiBase = inject(API_BASE_URL);

  isAuthenticated = signal(!!this.store.token);

  login(login: LoginRequest) {
    return this.http
      .post<{ access: string }>(`${this.apiBase}${API_ROUTES.auth.login}`, login, {
        responseType: 'json',
      })
      .pipe(
        tap((response) => this.setToken(response.access)),
        catchError((err) => {
          this.isAuthenticated.set(false);
          return throwError(() => err);
        })
      );
  }

  setToken(token: string) {
    this.store.setToken(token);
    this.isAuthenticated.set(true);
  }

  register(request: RegisterRequest) {
    return this.http
      .post(`${this.apiBase}${API_ROUTES.auth.register}`, request, {
        observe: 'response',
        responseType: 'json',
      })
      .pipe(
        map((res) => {
          if (res.status === 200 || res.status === 201) {
            return { ok: true, message: res.body?.toString() || '' };
          }
          throw new Error('Unexpected status: ' + res.status);
        }),
        catchError((err) => throwError(() => err))
      );
  }

  logout() {
    this.store.clear();
    this.isAuthenticated.set(false);
    localStorage.clear();
    this.router.navigateByUrl('/login');
  }

  checkAuth(token: string): Observable<boolean> {
    return this.http
      .post<boolean>(
        `${this.apiBase}${API_ROUTES.auth.checkAuth}`,
        {},
        {
          params: { token },
          observe: 'response',
        }
      )
      .pipe(map((response) => !!response.body));
  }

  private normalizeToken(raw: string): string {
    return raw
      .trim()
      .replace(/^Bearer\s+/i, '')
      .replace(/^"(.*)"$/, '$1');
  }
}
