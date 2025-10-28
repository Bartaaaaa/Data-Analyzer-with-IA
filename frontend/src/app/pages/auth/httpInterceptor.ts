import { HttpInterceptorFn } from '@angular/common/http';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access_token');
  const cloned = token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }) : req;

  return next(cloned);
};
