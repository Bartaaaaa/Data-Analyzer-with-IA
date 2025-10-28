import { inject, Injectable, signal } from '@angular/core';
import { catchError, map, Observable, tap, throwError } from 'rxjs';
import { API_BASE_URL } from '../config/apiBaseUrlToken';
import { API_ROUTES } from '../utils/apiRoutes';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { UserResponse } from '../models/user/UserResponse';

@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);
  private apiBase = inject(API_BASE_URL);
  token = localStorage.getItem('token');

  getMyData(): Observable<UserResponse> {
    return this.http.get<UserResponse>(`${this.apiBase}${API_ROUTES.user.getMe}`);
  }
}
