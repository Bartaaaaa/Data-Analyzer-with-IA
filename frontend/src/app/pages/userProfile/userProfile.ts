import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SpotifyService } from '../../services/spotifyService';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/userService';
import { UserResponse } from '../../models/user/UserResponse';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './userProfile.html',
  styleUrls: ['./userProfile.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserProfile {
  private spotifyService = inject(SpotifyService);
  private userService = inject(UserService);
  user = signal<UserResponse | null>(null);
  private router = inject(Router);

  loading = signal(false);
  error = signal<string | null>(null);

  isSpotifyConnected = false;
  spotifyToken = signal<string | null>(null);
  ngOnInit() {
    this.checkSpotifyConnection();
    this.userService.getMyData().subscribe({
      next: (response) => {
        this.user.set(response);
      },
    });
  }

  async checkSpotifyConnection() {
    if (this.spotifyService.checkToken()) {
      this.isSpotifyConnected = true;
    } else {
      this.isSpotifyConnected = false;
    }
  }
  spotifyLogin() {
    this.spotifyService.login();
  }

  logout() {
    localStorage.clear();
    this.router.navigateByUrl('/login');
  }
}
