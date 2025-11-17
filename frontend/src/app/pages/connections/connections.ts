import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { SpotifyService } from '../../services/spotifyService';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './connections.html',
  styleUrls: ['./connections.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Connections {
  private spotifyService = inject(SpotifyService);

  isSpotifyConnected = signal(false);

  ngOnInit() {
    this.checkSpotifyConnection();
  }

  async checkSpotifyConnection() {
    this.spotifyService.checkToken().subscribe({
      next: (response) => {
        this.isSpotifyConnected.set(response.isConnected);
      },
    });
  }

  spotifyLogin() {
    this.spotifyService.login();
  }
}
