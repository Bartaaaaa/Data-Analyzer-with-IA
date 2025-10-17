import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth/authService';
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './register.html',
  styleUrls: ['../auth.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Register {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private authService = inject(AuthService);
  loading = signal(false);
  error = signal<string | null>(null);
  checkPassword = signal<string | null>(null);

  form = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required],
  });

  submit() {
    if (this.form.invalid || this.loading()) return;

    this.loading.set(true);

    const { username, password } = this.form.getRawValue();
    this.authService
      .register({
        username: username!,
        password: password!,
      })
      .subscribe({
        next: () => {
          this.loading.set(false);
          this.router.navigateByUrl('/login');
        },
        error: (err) => {
          console.error(err);
        },
      });
  }

  goLogin() {
    this.router.navigateByUrl('/login');
  }
}
